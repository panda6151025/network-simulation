import numpy as np

def generate_random_movement(num_ues, grid_size, time_steps):
    movements = []
    positions = np.random.randint(0, grid_size[0], (num_ues, 2))

    for t in range(time_steps):
        for i in range(num_ues):
            direction = np.random.choice(['up', 'down', 'left', 'right'])
            if direction == 'up':
                positions[i][1] = min(positions[i][1] + 1, grid_size[1] - 1)
            elif direction == 'down':
                positions[i][1] = max(positions[i][1] - 1, 0)
            elif direction == 'left':
                positions[i][0] = max(positions[i][0] - 1, 0)
            elif direction == 'right':
                positions[i][0] = min(positions[i][0] + 1, grid_size[0] - 1)
        movements.append(positions.copy())

    return movements
