from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_socketio import SocketIO, emit
from island_generator import prepare_game
from boats import generate_boat_grid, plan_route_and_move, create_boat
import time
import threading

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session handling
socketio = SocketIO(app)  # Initialize Flask-SocketIO

# Global variables for shared data
grid = []
ports = []
boat_grid = []
boats_list = []

@app.route("/")
def home():
    return render_template("index.html")  # Serve the form for map generation

@app.route("/generate", methods=["POST"])
def generate():
    global grid, ports, boat_grid, boats_list

    # Get map parameters from the form
    width = int(request.form.get("width", 100))
    height = int(request.form.get("height", 30))
    num_islands = int(request.form.get("num_islands", 4))
    island_size = float(request.form.get("island_size", 0.3))
    num_ports = int(request.form.get("num_ports", 2))  # New parameter for ports

    grid, ports = prepare_game(width, height, num_islands, island_size, num_ports)

    boat_grid, boats_list = generate_boat_grid(grid, ports)

    # boat, boat_grid = create_boat('bateau2', ports[3]['coordinates'], ["Zarimun", "Carthessa"], boat_grid, grid)
    # boats_list.append(boat)  # Add the boat's position to the list

    return redirect(url_for("map_page"))  # Redirect to the map display page

@app.route("/map")
def map_page():
    global grid, ports, boat_grid
    return render_template("map.html", grid=grid, ports=ports, boat_grid=boat_grid)

# WebSocket event to send updated map data
@socketio.on("request_update")
def send_updated_map():
    global grid, ports, boat_grid
    emit("update_map", {"grid": grid, "ports": ports, "boat_grid": boat_grid})

# Background task to update the map data
def background_update_loop():
    global grid, ports, boat_grid, boats_list

    while True:

        time.sleep(0.1)

        for boat in boats_list:
             boat_grid, grid, boat = plan_route_and_move(boat, ports, grid, boat_grid)

        # Emit the updated map to all connected clients
        socketio.emit("update_map", {"grid": grid, "ports": ports, "boat_grid": boat_grid})


# Start the background thread
thread = threading.Thread(target=background_update_loop)
thread.daemon = True  # Ensure the thread exits when the main program exits
thread.start()

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5001)