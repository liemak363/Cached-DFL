# Car Movement Algorithm Explanation
# This file demonstrates how the Car.move() method works with example data

import numpy as np

def demonstrate_car_movement():
    """
    Demonstrates the Car movement algorithm with example data
    """
    
    # Example road network data
    pos_list = [
        (40.7589, -73.9851),  # Node 0: Times Square
        (40.7614, -73.9776),  # Node 1: Bryant Park  
        (40.7505, -73.9934),  # Node 2: Penn Station
        (40.7411, -73.9897),  # Node 3: Union Square
    ]
    
    # Adjacency matrix (simplified 4-node network)
    adj_matrix = np.array([
        [0, 1, 1, 0],  # Node 0 connects to 1,2
        [1, 0, 0, 1],  # Node 1 connects to 0,3
        [1, 0, 0, 1],  # Node 2 connects to 0,3
        [0, 1, 1, 0]   # Node 3 connects to 1,2
    ])
    
    print("=== Car Movement Algorithm Demonstration ===\n")
    
    # Initial car state
    source = 0      # Starting at Times Square
    destination = 1 # Going to Bryant Park
    speed = 0.001   # Speed in coordinate units per time step
    
    # Calculate initial speed vector
    source_pos = np.array([pos_list[source][0], pos_list[source][1]])
    dest_pos = np.array([pos_list[destination][0], pos_list[destination][1]])
    speed_vector = dest_pos - source_pos
    
    # Normalize to maintain constant speed
    norm = np.linalg.norm(speed_vector)
    if norm > 0:
        speed_vector = speed_vector / norm * speed
    
    current_position = source_pos.copy()
    
    print(f"Initial State:")
    print(f"  Source: Node {source} at {source_pos}")
    print(f"  Destination: Node {destination} at {dest_pos}")
    print(f"  Speed: {speed}")
    print(f"  Speed Vector: {speed_vector}")
    print(f"  Current Position: {current_position}")
    print()
    
    # Simulate movement over several time steps
    for time_step in range(5):
        print(f"Time Step {time_step + 1}:")
        
        # Distance to destination
        distance_to_dest = np.linalg.norm(dest_pos - current_position)
        print(f"  Distance to destination: {distance_to_dest:.6f}")
        
        time = 1  # Time step duration
        
        # Check if car reaches destination in this time step
        if distance_to_dest < speed * time:
            print(f"  Car reaches destination!")
            
            # Calculate time to reach destination
            time_to_dest = distance_to_dest / speed
            residual_time = time - time_to_dest
            
            print(f"  Time to reach dest: {time_to_dest:.3f}")
            print(f"  Residual time: {residual_time:.3f}")
            
            # Update source and destination
            previous_source = source
            source = destination
            
            # Find next destination (simplified - just pick first available)
            neighbors = np.where(adj_matrix[source] == 1)[0]
            # Remove previous source to prevent immediate reversal
            if len(neighbors) > 1:
                neighbors = neighbors[neighbors != previous_source]
            
            destination = neighbors[0]  # Simplified selection
            
            # Update speed vector for new direction
            source_pos = np.array([pos_list[source][0], pos_list[source][1]])
            dest_pos = np.array([pos_list[destination][0], pos_list[destination][1]])
            speed_vector = dest_pos - source_pos
            norm = np.linalg.norm(speed_vector)
            if norm > 0:
                speed_vector = speed_vector / norm * speed
            
            # Update position: at new source + movement for residual time
            current_position = source_pos + speed_vector * residual_time
            
            print(f"  New source: Node {source}")
            print(f"  New destination: Node {destination}")
            print(f"  New speed vector: {speed_vector}")
            
        else:
            # Normal movement along current path
            current_position = current_position + speed_vector * time
            print(f"  Moving along current path...")
        
        print(f"  New position: {current_position}")
        print()

def demonstrate_data_structures():
    """
    Shows the actual data structure formats used in the Car class
    """
    print("=== Car Class Data Structures ===\n")
    
    # Example pos_list (from real New York data)
    print("1. pos_list (node coordinates):")
    pos_list_example = [
        (40.7589, -73.9851),  # Node 0
        (40.7614, -73.9776),  # Node 1
        (40.7505, -73.9934),  # Node 2
        # ... hundreds more nodes
    ]
    print(f"   Type: {type(pos_list_example)}")
    print(f"   Length: {len(pos_list_example)} nodes")
    print(f"   Example: pos_list[0] = {pos_list_example[0]}")
    print()
    
    # Example adjacency matrix
    print("2. adj_matrix (connectivity):")
    adj_matrix_example = np.array([
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ])
    print(f"   Type: {type(adj_matrix_example)}")
    print(f"   Shape: {adj_matrix_example.shape}")
    print(f"   Example connections for node 0: {np.where(adj_matrix_example[0] == 1)[0]}")
    print()
    
    # Example speed vector
    print("3. speed_vector (direction and magnitude):")
    speed_vector_example = np.array([0.0002, -0.0003])
    print(f"   Type: {type(speed_vector_example)}")
    print(f"   Shape: {speed_vector_example.shape}")
    print(f"   Magnitude: {np.linalg.norm(speed_vector_example):.6f}")
    print(f"   Direction: {speed_vector_example}")
    print()
    
    # Example current position
    print("4. current_position (exact coordinates):")
    current_pos_example = np.array([40.7595, -73.9820])
    print(f"   Type: {type(current_pos_example)}")
    print(f"   Shape: {current_pos_example.shape}")
    print(f"   Coordinates: [lat={current_pos_example[0]}, lon={current_pos_example[1]}]")
    print()

if __name__ == "__main__":
    demonstrate_data_structures()
    print("\n" + "="*50 + "\n")
    demonstrate_car_movement()
