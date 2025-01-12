import tkinter as tk
from tkinter import ttk
from tkhtmlview import HTMLLabel
import tkintermapview
import folium
import webview

# Create main app window
root = tk.Tk()
root.title("Dander")
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

# Submit button
def update_distances():
    try:
        user1_new = float(user1_input.get())
        user2_new = float(user2_input.get())
        current_user1 = float(user1_distance.cget("text").split()[0])
        current_user2 = float(user2_distance.cget("text").split()[0])

        user1_distance.config(text=f"{current_user1 + user1_new} km")
        user2_distance.config(text=f"{current_user2 + user2_new} km")

        # Clear input fields
        user1_input.delete(0, tk.END)
        user2_input.delete(0, tk.END)
    except ValueError:
        print("Invalid input! Please enter numbers.")

ttk.Button(sidebar, text="Update Distances", command=update_distances).grid(row=7, column=0, columnspan=2, pady=10)

# Starting coordinates of the Appalachian Trail
start_coords = [34.6268, -83.1955]

# Create map
m = folium.Map(location=start_coords, zoom_start=6)

# Add marker at start of trail
folium.Marker(location=start_coords, popup="Start of Trail").add_to(m)

# Add line for the train, below is an example only
trail_coords = [
    [34.6268, -83.1955],
    [35.0, 82.7],
    [36.0, 81.5]
]
folium.PolyLine(trail_coords, color="red", weight=2.5, opacity=1).add_to(m)

# Save map to HTML file
m.save("appalachian_trail.html")

# Map Placeholder
map_view = tkintermapview.TkinterMapView(map_area, width=600, height=600, corner_radius=0)
map_view.pack()

# Run the app
root.mainloop()