import tkinter as tk
from tkinter import ttk
import tkintermapview
import gpxpy
import math
import sqlite3

from d_sqlite import init_db, store_distance, get_distance
from d_funcs import update_distances, haversine, load_gpx, update_map_path, reset_distances

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

user1_distance.config(text=f"{user1_distance_value} km")
user2_distance.config(text=f"{user2_distance_value} km")

# Update the map with the user's progress based on stored distances
if user1_distance_value > 0:
    update_map_path(user1_distance_value, trail_coords, map_view)  # For Rebecca

if user2_distance_value > 0:
    update_map_path(user2_distance_value, trail_coords, map_view)  # For Raymond

ttk.Button(sidebar, text="Update Distances", 
           command=lambda: update_distances(user1_input, user2_input, user1_distance, user2_distance)
           ).grid(row=7, column=0, columnspan=2, pady=10)
ttk.Button(sidebar, text="Reset", 
           command=lambda: reset_distances(user1_distance, user2_distance, map_view)
           ).grid(row=9, column=0, columnspan=2, pady=10)

# Run the app
root.mainloop()