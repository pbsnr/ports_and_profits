from collections import deque

def create_boat(name, coordinates, route, boat_grid, grid):

    if boat_grid[coordinates[0]][coordinates[1]] == 0 and grid[coordinates[0]][coordinates[1]] != 1:
        boat = {'name': name, 'coordinates': coordinates, 'route': route, 'trace': []}
        boat_grid[coordinates[0]][coordinates[1]] = 1  # Mark the boat's position on the grid
        return boat, boat_grid
    
    return None

def generate_boat_grid(grid, ports):
    boat_grid = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    boats_list = []  # List to store boat positions

    boat, boat_grid = create_boat('bateau', ports[0]['coordinates'], ["Myriakon", "Thaleptra"], boat_grid, grid)
    boats_list.append(boat)  # Add the boat's position to the list
    
    return boat_grid, boats_list


def move_boat(boat_grid, grid, boat):

    x1, y1 = boat['trace'][0]
    boat['trace'].pop(0)  # Remove the first element from the trace

    # Check if the new position is within bounds and not an island
    if x1 < 0 or x1 >= len(grid) or y1 < 0 or y1 >= len(grid[0]):
        return boat_grid, grid, boat

    x, y = boat['coordinates']  # Get the current position of the boat

    if grid[x1][y1] != 1 and boat_grid[x1][y1] == 0:
        boat_grid[x][y] = 0  # Remove the boat from the old position
        boat_grid[x1][y1] = 1  # Place the boat at the new position
        boat['coordinates'] = (x1, y1)

    return boat_grid, grid, boat

def shortest_path_with_trace(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    queue = deque([(start, [start])])
    visited = set()
    visited.add(start)

    while queue:
        (r, c), path = queue.popleft()

        if (r, c) == end:
            return path

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if (0 <= nr < rows and 0 <= nc < cols and
                grid[nr][nc] != 1 and (nr, nc) not in visited):
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))

    return None  # No path found

def plan_route_and_move(boat, ports, grid, boat_grid):
    next_port = next((p for p in ports if p["name"] == boat['route'][1]), None)

    if boat['coordinates'] == next_port['coordinates']:
        first = boat['route'].pop(0)
        boat['route'].append(first)

    if boat['trace'] == []:
        boat['trace'] = shortest_path_with_trace(grid, boat['coordinates'], next_port['coordinates'])

    boat_grid, grid, boat = move_boat(boat_grid, grid, boat)

    return boat_grid, grid, boat