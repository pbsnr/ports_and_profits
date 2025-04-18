import random

ports_names = [
    "Velinthos", "Myriakon", "Thaleptra", "Zarimun", "Carthessa",
    "Elythrae", "Nemorion", "Aurelka", "Darnethra", "Phoros",
    "Tyrragonia", "Karnethys", "Vallumea", "Serapion", "Delkara",
    "Asprades", "Mithralor", "Orontheum", "Halzura", "Tarkossa",
    "Edracium", "Belyphon", "Nazkara", "Virethon", "Ozythria",
    "Thessamor", "Kalibrix", "Zenothra", "Quorali", "Ambracyn",
    "Pelarion", "Scarnathos", "Yllirak", "Hathorim", "Zenthurion",
    "Loricaea", "Durmathra", "Oxenath", "Kymelios", "Tragonis",
    "Ularikon", "Xanthyra", "Volithar", "Naraspes", "Helionda",
    "Crassava", "Obrython", "Tarnakos", "Zephurion", "Galmyra"
]

# Check if a cell is adjacent to an existing island
def check_island(grid, x, y):
    if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
        return False
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 1:
                return True
    return False

# Generate a specified number of islands on the map
def generate_islands(grid, nb_islands):
    nb_islands_to_build = nb_islands
    max_attempts = len(grid) * len(grid[0]) * 10  # Limit the number of attempts
    attempts = 0

    while nb_islands_to_build > 0 and attempts < max_attempts:
        x = random.randint(1, len(grid) - 2)
        y = random.randint(1, len(grid[0]) - 2)
        if not check_island(grid, x, y):
            grid[x][y] = 1
            nb_islands_to_build -= 1
        attempts += 1

    if nb_islands_to_build > 0:
        print(f"Warning: Could not place all {nb_islands} islands. {nb_islands_to_build} islands remain.")

# Grow an island by expanding it randomly
def grow_island(grid, island_size):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 1:
                # Randomly grow the island by changing adjacent cells to 1
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 1 <= nx < len(grid) - 1 and 1 <= ny < len(grid[0]) - 1 and grid[nx][ny] == 0:
                            if random.random() < island_size:
                                grid[nx][ny] = 1

def fill_ocean(grid):
    rows, cols = len(grid), len(grid[0])
    stack = [(0, 0)]  # Start from top-left corner
    visited = set()

    while stack:
        x, y = stack.pop()
        if (x, y) in visited or x < 0 or y < 0 or x >= rows or y >= cols or grid[x][y] != 0:
            continue
            
        visited.add((x, y))
        grid[x][y] = -1  # Mark as ocean
        
        # Add adjacent cells to stack
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            stack.append((nx, ny))

def generate_map(x, y, nb_islands, island_size):
    grid = [[0 for _ in range(x)] for _ in range(y)]
    generate_islands(grid, nb_islands)
    grow_island(grid, island_size)
    fill_ocean(grid)
    return grid

def add_ports(grid, nb_ports):
    ports_added = 0
    max_attempts = len(grid) * len(grid[0]) * 10  # Limit the number of attempts
    attempts = 0
    ports = []

    while ports_added < nb_ports and attempts < max_attempts:
        x = random.randint(0, len(grid) - 1)
        y = random.randint(0, len(grid[0]) - 1)

        if grid[x][y] == -1:
            # Check if at least one adjacent cell is open sea
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 1:
                    grid[x][y] = 2  # Mark port with a different value
                    ports_added += 1
                    ports.append({'name': ports_names[ports_added], 'coordinates': (x, y)})
                    break
        attempts += 1

    if ports_added < nb_ports:
        print(f"Warning: Could not place all {nb_ports} ports. {nb_ports - ports_added} ports remain.")

    return grid, ports

def prepare_game(width, height, num_islands, island_size, num_ports):
    # Generate the map
    grid = generate_map(width, height, num_islands, island_size)

    # Add ports to the map
    grid, ports = add_ports(grid, num_ports)

    return grid, ports