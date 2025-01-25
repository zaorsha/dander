import tkinter as tk
from tkinter import ttk
import tkintermapview
import gpxpy
import math

# Submit button
def update_distances():
    try:
        user1_new_distance = float(user1_input.get() or 0)
        user2_new_distance = float(user2_input.get() or 0)

        # Get current distance
        current_user1_distance = get_distance("Rebecca")
        current_user2_distance = get_distance("Raymond")

        # Update user distances
        new_user1_distance = current_user1_distance + user1_new_distance
        new_user2_distance = current_user2_distance + user2_new_distance

        # Store the updated distances in the database
        store_distance("Rebecca", new_user1_distance)
        store_distance("Raymond", new_user2_distance)

        # Update the labels with new distances
        user1_distance.config(text=f"{new_user1_distance} km")
        user2_distance.config(text=f"{new_user2_distance} km")

        # Clear input fields
        user1_input.delete(0, tk.END)
        user2_input.delete(0, tk.END)

        # Update the map with the new progress
        update_map_path(new_user1_distance)  # For Rebecca
        update_map_path(new_user2_distance)  # For Raymond

    except ValueError:
        print("Invalid input! Please enter numbers.")

# Function to calculate the distance between two points using Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    # Radius of Earth in kilometers
    R = 6371.0

    # Convert degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Difference in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance

def load_gpx(file_path):
    with open(file_path, 'r') as f:
        gpx = gpxpy.parse(f)

    # Create a list of coordinates from the GPX file
    trail_coords = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                trail_coords.append([point.latitude, point.longitude])

    return trail_coords

# Function to update the path with green for the user's progress
def update_map_path(total_distance_walked):
    traveled_coords = []
    distance_traveled = 0

    for i in range(1, len(trail_coords)):
        lat1, lon1 = trail_coords[i - 1]
        lat2, lon2 = trail_coords[i]

        # Calculate the distance between two consecutive points
        segment_distance = haversine(lat1, lon1, lat2, lon2)
        distance_traveled += segment_distance

        if distance_traveled >= total_distance_walked:
            # Add points to the traveled path (green)
            traveled_coords.append([lat1, lon1])
            break
        else:
            # Add the whole segment to the traveled path (green)
            traveled_coords.append([lat1, lon1])
            traveled_coords.append([lat2, lon2])

    # Plot the traveled path (in green)
    map_view.set_path(traveled_coords, color="green")

# Reset all distances in the database to 0
def reset_distances():
    with sqlite3.connect('dander.db') as conn:
        c = conn.cursor()
        c.execute('UPDATE users SET distance = 0')  # Reset all distances to 0
        conn.commit()
    
    # Update the displayed values in the GUI
    user1_distance.config(text="0 km")
    user2_distance.config(text="0 km")

    # Reset the map to remove the green path
    map_view.delete_all_path()
    map_view.set_path(trail_coords, color='red')  # Replot the original red trail