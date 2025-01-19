import tkinter as tk
from tkinter import ttk
import tkintermapview
import gpxpy
import math
import sqlite3

################################## DB FUNCTIONS ##################################

# Create SQLite database
def init_db():
    conn = sqlite3.connect('dander.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            name TEXT PRIMARY KEY,
            distance REAL
        )
    ''')  # Create table with a primary key
    conn.commit()
    conn.close()

# Store distance data
def store_distance(name, distance):
    with sqlite3.connect('dander.db') as conn:
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO users (name, distance) VALUES (?, ?)''', (name, distance))
        conn.commit()

# Retrieve distance data
def get_distance(name):
    with sqlite3.connect('dander.db') as conn:
        c = conn.cursor()
        c.execute('''SELECT distance FROM users WHERE name=?''', (name,))
        result = c.fetchone()
        return result[0] if result else 0

################################## FUNCTIONS ##################################

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

        print(f'new user1: {new_user1_distance}')
        print(f'new user1: {new_user2_distance}')

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

################################## MAIN LOOP ##################################

# Initiating SQLite database at start of program

# Initialize the database
init_db()

#########  GUI CREATION #########

# Create main app window
root = tk.Tk()
root.title("DANDER")
root.geometry("1200x800") # Set window size

# Sidebar for inputs and stats
sidebar = ttk.Frame(root, padding='10', width=200)
sidebar.grid(row=0, column=0, sticky="NS") # stick to the top and bottom

# Main area for map display
map_area = ttk.Frame(root, padding="10", relief="ridge", width=600, height=600)
map_area.grid(row=0, column=1, sticky="NSEW") # Expand to fill space

# Make map area expand with the window
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

# User 1 stats
ttk.Label(sidebar, text="Rebecca's Stats:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, pady=10, sticky="W")
ttk.Label(sidebar, text="Total Distance:").grid(row=1, column=0, sticky="W")
user1_distance = ttk.Label(sidebar, text="0 km")
user1_distance.grid(row=1, column=1, sticky="E")

# User 2 stats
ttk.Label(sidebar, text="Raymond's Stats:", font=("Helvetica", 12, "bold")).grid(row=2, column=0, pady=10, sticky="W")
ttk.Label(sidebar, text="Total Distance:").grid(row=3, column=0, sticky="W")
user2_distance = ttk.Label(sidebar, text="0 km")
user2_distance.grid(row=3, column=1, sticky="E")

# Input for daily distances
ttk.Label(sidebar, text="Add Daily Distance").grid(row=4, column=0, pady=20, sticky="W")

ttk.Label(sidebar, text="Rebecca:").grid(row=5, column=0, sticky="W")
user1_input = ttk.Entry(sidebar, width=10)
user1_input.grid(row=5, column=1, sticky="E")

ttk.Label(sidebar, text="Raymond:").grid(row=6, column=0, sticky="W")
user2_input = ttk.Entry(sidebar, width=10)
user2_input.grid(row=6, column=1, sticky="E")

# Generate Map
map_view = tkintermapview.TkinterMapView(map_area, width=600, height=600, corner_radius=0)

# Starting coordinates of the Appalachian Trail
map_view.set_position(34.626652, -84.193899, marker=True, text="Start")

# Create path
trail_coords = load_gpx("appalachian_trail_path.gpx")

# Plot the trail as a polyline on the map
map_view.set_path(trail_coords, color='red')

# Set zoom level
map_view.set_zoom(11)

map_view.pack(expand=True, fill="both")

# On startup, load the saved distances for both users
user1_distance_value = get_distance('Rebecca')
user2_distance_value = get_distance('Raymond')
print(user1_distance_value)
print(user2_distance_value)

user1_distance.config(text=f"{user1_distance_value} km")
user2_distance.config(text=f"{user2_distance_value} km")

# Update the map with the user's progress based on stored distances
if user1_distance_value > 0:
    update_map_path(user1_distance_value)  # For Rebecca

if user2_distance_value > 0:
    update_map_path(user2_distance_value)  # For Raymond

ttk.Button(sidebar, text="Update Distances", command=update_distances).grid(row=7, column=0, columnspan=2, pady=10)
ttk.Button(sidebar, text="Reset", command=reset_distances).grid(row=9, column=0, columnspan=2, pady=10)


# Run the app
root.mainloop()