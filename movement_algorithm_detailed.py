# Detailed Explanation of Car.move() Method Logic
# This explains the exact algorithm used in the move() method

"""
STEP-BY-STEP BREAKDOWN OF Car.move(time) METHOD:

1. DISTANCE CALCULATION:
   distance_to_dest = ||destination_coordinates - current_position||
   
2. MOVEMENT DECISION:
   IF distance_to_dest < speed * time:
       # Car will reach destination within this time step
       GOTO: DESTINATION_REACHED_LOGIC
   ELSE:
       # Car continues on current path
       GOTO: NORMAL_MOVEMENT_LOGIC

3. DESTINATION_REACHED_LOGIC:
   a) Calculate timing:
      - time_to_reach = distance_to_dest / speed
      - residual_time = time - time_to_reach
   
   b) Update source/destination:
      - previous_source = current_source
      - current_source = current_destination
      - new_destination = get_next_destination(...)
   
   c) Calculate new speed vector:
      - direction = new_dest_coords - new_source_coords
      - speed_vector = normalize(direction) * speed
   
   d) Update position:
      - current_position = new_source_coords + speed_vector * residual_time

4. NORMAL_MOVEMENT_LOGIC:
   current_position = current_position + speed_vector * time

5. get_next_destination() LOGIC:
   a) Find all neighbors of current node
   b) Remove previous_source to prevent immediate reversal
   c) If only one option: choose it
   d) If multiple options: use probability based on direction alignment
      - Calculate cosine similarity between current direction and each option
      - Assign 50% probability to most aligned direction
      - Distribute remaining 50% equally among other options

VISUAL REPRESENTATION:

Time t=0:    [Source]---------->current_pos----------[Destination]
             Node A                                   Node B

Time t=1:    [Source]---------------->current_pos----[Destination]
             Node A                                   Node B

Time t=2:    [Source]----------------------->current_pos[Destination]
             Node A                                   Node B (reached!)

Time t=3:    [Old Dest/New Source]-------->current_pos----[New Destination]
             Node B                                        Node C

DATA FLOW EXAMPLE:

Initial state:
- source = 142
- destination = 157  
- current_position = [40.7589, -73.9851]
- speed_vector = [0.0003, 0.0009]
- speed = 0.001

After move(1):
- If destination not reached:
  current_position = [40.7589, -73.9851] + [0.0003, 0.0009] * 1
                   = [40.7592, -73.9842]

- If destination reached (distance < 0.001):
  1. Calculate residual_time
  2. source = 157, destination = get_next_destination(157, 142, ...)
  3. Update speed_vector for new direction
  4. current_position = pos_list[157] + new_speed_vector * residual_time

COORDINATE SYSTEM:
- Coordinates are in latitude/longitude format
- Speed is converted from mph to coordinate units per time step
- Original: 13.59 mph
- Converted: 13.59 * 0.00145/100 = 0.000197 coord_units/timestep

REALISTIC MOVEMENT BEHAVIOR:
- Cars prefer to continue straight (50% probability for most aligned direction)
- Cars avoid immediate U-turns (previous_source is excluded)
- Movement is continuous (not just node-hopping)
- Speed is constant but direction changes at intersections
"""

def explain_probability_calculation():
    """
    Explains how direction-based probability works
    """
    import numpy as np
    
    print("=== Direction-Based Probability Calculation ===\n")
    
    # Example scenario: car at intersection with 3 options
    current_speed_vector = np.array([1, 0])  # Moving east
    
    # Three possible directions from intersection
    option1 = np.array([1, 0])    # Continue straight (east)
    option2 = np.array([0, 1])    # Turn left (north)  
    option3 = np.array([0, -1])   # Turn right (south)
    
    directions = [option1, option2, option3]
    direction_names = ["Straight", "Left", "Right"]
    
    print("Current direction: East [1, 0]")
    print("Available options:")
    
    # Calculate cosine similarities
    similarities = []
    for i, direction in enumerate(directions):
        cos_sim = np.dot(direction, current_speed_vector) / (
            np.linalg.norm(direction) * np.linalg.norm(current_speed_vector)
        )
        similarities.append(cos_sim)
        print(f"  {direction_names[i]}: {direction} -> cosine similarity: {cos_sim:.3f}")
    
    similarities = np.array(similarities)
    max_similarity = np.max(similarities)
    
    # Calculate probabilities
    probabilities = np.ones_like(similarities) * (0.5 / (len(similarities) - 1))
    probabilities[similarities == max_similarity] = 0.5
    
    print(f"\nProbability distribution:")
    for i, (name, prob) in enumerate(zip(direction_names, probabilities)):
        print(f"  {name}: {prob:.3f} ({prob*100:.1f}%)")
    
    print(f"\nExplanation:")
    print(f"- Most aligned direction gets 50% probability")
    print(f"- Remaining 50% is split equally among other options")
    print(f"- This creates realistic turning behavior")

if __name__ == "__main__":
    explain_probability_calculation()
