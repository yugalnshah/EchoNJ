import numpy as np
import pandas as pd
from flask import Flask, request
from flask_socketio import SocketIO, emit
from datetime import datetime

# Load dataset
file_path = '/Users/yugal/Downloads/officialHackRUFINAL.csv'
data = pd.read_csv(file_path)

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Helper function to normalize time
def normalize_time(time_str):
    hours, minutes, seconds = map(int, time_str.split(":"))
    if hours >= 24:
        hours = hours % 24
    return "{:02}:{:02}:{:02}".format(hours, minutes, seconds)

# Define functions for getting next train time, route-based stops, etc., as in your original code

# Check if travel is possible on the same route
def can_travel_between_stops(start_stop, destination_stop):
    start_stop = start_stop.strip().upper()
    destination_stop = destination_stop.strip().upper()
    data['normalized_stop_name'] = data['stop_name'].str.upper().str.strip()
    routes_from_start = data[data['normalized_stop_name'] == start_stop]['route_long_name'].unique()
    for route in routes_from_start:
        if destination_stop in data[(data['route_long_name'] == route)]['normalized_stop_name'].values:
            return f"Yes, you can travel from {start_stop} to {destination_stop} on the {route} line."
    return f"No, it is not possible to travel directly from {start_stop} to {destination_stop} on any single line."

# New Function: Check if travel to destination is possible with a transfer
def can_transfer_to_destination(start_stop, destination_stop):
    start_stop = start_stop.strip().upper()
    destination_stop = destination_stop.strip().upper()
    data['normalized_stop_name'] = data['stop_name'].str.upper().str.strip()
    
    # Routes that serve the starting stop
    routes_from_start = data[data['normalized_stop_name'] == start_stop]['route_long_name'].unique()
    # Routes that serve the destination stop
    routes_to_destination = data[data['normalized_stop_name'] == destination_stop]['route_long_name'].unique()
    
    # Find possible transfer stops
    for route_start in routes_from_start:
        stops_on_start_route = data[data['route_long_name'] == route_start]['normalized_stop_name'].unique()
        
        # For each stop on the start route, check if there's a connecting route to the destination
        for transfer_stop in stops_on_start_route:
            connecting_routes = data[data['normalized_stop_name'] == transfer_stop]['route_long_name'].unique()
            for route in connecting_routes:
                if route in routes_to_destination and transfer_stop != start_stop:
                    return f"Yes, you can transfer from {start_stop} to {destination_stop} at {transfer_stop} on the {route} line."
    
    return f"No, there is no transfer route from {start_stop} to {destination_stop}."

def get_next_train_time(stop_name, current_time):
    relevant_trains = data[(data['stop_name'].str.upper().str.strip() == stop_name.upper().strip()) & (data['arrival_time'] > current_time)]
    if not relevant_trains.empty:
        next_arrival = relevant_trains.iloc[0]['arrival_time']
        return f"The next train to {stop_name} is scheduled to arrive at {next_arrival}."
    else:
        return f"No more trains are scheduled to arrive at {stop_name} today."

# Route-Based Function
def list_stops_on_route(route_name):
    route_stops = data[data['route_long_name'].str.upper().str.strip() == route_name.upper().strip()]['stop_name'].unique()
    if route_stops.size > 0:
        return f"The stops on the {route_name} are: " + ", ".join(route_stops) + "."
    else:
        return f"No stops found for the route named {route_name}."
    
# Travel Time Calculation Function
def travel_time_between_stops(start_stop, destination_stop):
    start_stop = start_stop.strip().upper()
    destination_stop = destination_stop.strip().upper()
    data['normalized_stop_name'] = data['stop_name'].str.upper().str.strip()
    start_data = data[data['normalized_stop_name'] == start_stop]
    destination_data = data[data['normalized_stop_name'] == destination_stop]
    if start_data.empty or destination_data.empty:
        print("Available stops in the dataset for matching:")
        print(data['normalized_stop_name'].unique())
        return f"One or both of the stops named {start_stop} and {destination_stop} are not found in the data."
    start_time_str = normalize_time(start_data.iloc[0]['arrival_time'])
    destination_time_str = normalize_time(destination_data.iloc[0]['arrival_time'])
    fmt = '%H:%M:%S'
    start_time = datetime.strptime(start_time_str, fmt)
    destination_time = datetime.strptime(destination_time_str, fmt)
    time_difference = destination_time - start_time
    return f"The travel time from {start_stop} to {destination_stop} is approximately {time_difference}."

# Main question-processing function with added logic
def answer_question(question):
    if "next train" in question:
        stop_name = question.split(" at ")[-1].strip()
        return get_next_train_time(stop_name, "05:00:00")
    
    elif "stops on the" in question:
        route_name = question.split(" the ")[-1].strip()
        return list_stops_on_route(route_name)
    
    elif "how far has the train traveled" in question:
        stop_name = question.split("reaches ")[-1].strip()
        return distance_traveled_to_stop(stop_name)
    
    elif "how long does it take from" in question:
        stops = question.split(" from ")[-1].split(" to ")
        if len(stops) < 2:
            return "Please provide both the start and destination stops."
        start_stop = stops[0].strip()
        destination_stop = stops[1].strip()
        return travel_time_between_stops(start_stop, destination_stop)
    
    elif "can i go from" in question.lower():
        stops = question.split(" from ")[-1].split(" to ")
        if len(stops) < 2:
            return "Please provide both the start and destination stops."
        start_stop = stops[0].strip()
        destination_stop = stops[1].strip()
        return can_travel_between_stops(start_stop, destination_stop)
    
    elif "can i transfer from" in question.lower():
        stops = question.split(" from ")[-1].split(" to ")
        if len(stops) < 2:
            return "Please provide both the start and destination stops."
        start_stop = stops[0].strip()
        destination_stop = stops[1].strip()
        return can_transfer_to_destination(start_stop, destination_stop)
    
    elif "thanks for helping" in question.lower():
        return "You're welcome, have a nice day!"
    
    else:
        return "I'm sorry, I can help with train schedules, stop counts, and route information. Could you rephrase your question?"



# SocketIO event to handle incoming questions from the client
@socketio.on('question')
def handle_question(data):
    question = data.get('question')
    print("Received question:", question)
    
    # Process the question and get the answer
    answer = answer_question(question)
    print("Answer:", answer)
    
    # Send the answer back to the client (client-side handles TTS)
    emit('answer', {'answer': answer})

# Flask route for testing the server
@app.route('/')
def index():
    return "Flask-SocketIO server is running."

# Run the server
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
