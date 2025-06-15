# Function Relationship and Data Flow in road_sim.py

"""
FUNCTION CALL HIERARCHY AND DATA FLOW:

1. generate_roadNet_pair_area_list() [MAIN FUNCTION]
   ├── Creates road network from CSV data
   ├── Builds adjacency matrix
   ├── Creates Car objects
   └── Simulation loop:
       ├── car.move(1) for each car
       └── caculate_pair() to find meetings

2. Car.__init__() [CONSTRUCTOR]
   ├── Stores network data (pos_list, adj_matrix)
   ├── Calls get_cordinate_by_node() to get coordinates
   ├── Calculates initial speed_vector
   └── Sets initial current_position

3. Car.move(time) [MOVEMENT METHOD]
   ├── Calculates distance to destination
   ├── If destination reached:
   │   ├── Calls get_next_destination()
   │   └── Updates position with residual time
   └── Else: moves along current path

4. get_next_destination() [PATHFINDING]
   ├── Finds neighbors from adjacency matrix
   ├── Removes previous source (no U-turns)
   ├── If multiple options:
   │   ├── Calls get_road_choice_probability()
   │   └── Uses np.random.choice() with probabilities
   └── Returns next destination node

5. get_road_choice_probability() [REALISTIC BEHAVIOR]
   ├── Calculates direction vectors to each option
   ├── Calls cosine_similarity() for each direction
   ├── Assigns 50% to most aligned direction
   └── Distributes remaining 50% equally

6. cosine_similarity() [DIRECTION ALIGNMENT]
   ├── Calculates dot product
   ├── Calculates vector norms
   └── Returns similarity score (-1 to +1)

7. get_cordinate_by_node() [COORDINATE LOOKUP]
   └── Returns [x, y] coordinates for given node ID

8. filter_edges_by_group() [AREA RESTRICTIONS]
   └── Creates area-restricted adjacency matrix

DATA STRUCTURE TRANSFORMATIONS:

CSV Data → NetworkX Graph → Adjacency Matrix → Car Objects → Position Tracking

Raw Road Data:
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ StartLat    │ StartLong   │ EndLat      │ EndLong     │
├─────────────┼─────────────┼─────────────┼─────────────┤
│ 40.7589     │ -73.9851    │ 40.7614     │ -73.9776    │
│ 40.7614     │ -73.9776    │ 40.7505     │ -73.9934    │
└─────────────┴─────────────┴─────────────┴─────────────┘

pos_list (Node Coordinates):
┌─────────┬─────────────────────────┐
│ Node ID │ Coordinates (lat, lon)  │
├─────────┼─────────────────────────┤
│ 0       │ (40.7589, -73.9851)    │
│ 1       │ (40.7614, -73.9776)    │
│ 2       │ (40.7505, -73.9934)    │
└─────────┴─────────────────────────┘

adj_matrix (Connectivity):
     0  1  2  3
  ┌─────────────┐
0 │ 0  1  1  0  │  ← Node 0 connects to nodes 1,2
1 │ 1  0  0  1  │  ← Node 1 connects to nodes 0,3
2 │ 1  0  0  1  │  ← Node 2 connects to nodes 0,3
3 │ 0  1  1  0  │  ← Node 3 connects to nodes 1,2
  └─────────────┘

Car Instance Data:
┌─────────────────┬──────────────────┬─────────────┐
│ Attribute       │ Type             │ Example     │
├─────────────────┼──────────────────┼─────────────┤
│ source          │ int              │ 142         │
│ destination     │ int              │ 157         │
│ current_position│ numpy.array(2,)  │ [40.7, -73.9]│
│ speed_vector    │ numpy.array(2,)  │ [0.0003, 0.0009]│
│ speed           │ float            │ 0.000197    │
│ car_type        │ int              │ 0           │
└─────────────────┴──────────────────┴─────────────┘

MEMORY LAYOUT VISUALIZATION:

Car Object Memory:
┌─────────────────────────────────────────────┐
│ Car Instance #1                             │
├─────────────────────────────────────────────┤
│ source: 142 (4 bytes)                       │
│ destination: 157 (4 bytes)                  │
│ current_position: [40.7589, -73.9851]      │
│                   (16 bytes - 2 doubles)    │
│ speed_vector: [0.0003, 0.0009]             │
│               (16 bytes - 2 doubles)        │
│ speed: 0.000197 (8 bytes)                  │
│ car_type: 0 (4 bytes)                      │
│ pos_list: → (reference to shared list)     │
│ adj_matrix: → (reference to shared array)  │
└─────────────────────────────────────────────┘

ALGORITHMIC COMPLEXITY:

Car.move() Method:
- Time Complexity: O(k) where k = number of neighbors (usually 2-4)
- Space Complexity: O(1)

get_next_destination():
- Time Complexity: O(k) for neighbor lookup + O(k) for probability calc
- Space Complexity: O(k) for storing neighbor list

get_road_choice_probability():
- Time Complexity: O(k²) due to cosine similarity calculations
- Space Complexity: O(k) for direction vectors

Overall Simulation:
- Time Complexity: O(num_cars × num_timesteps × avg_neighbors)
- Space Complexity: O(num_nodes² + num_cars)

COORDINATE SYSTEM DETAILS:

Speed Conversion:
Real-world: 13.59 mph
→ Multiply by 0.00145/100 (conversion factor)
→ Simulation: 0.000197 coordinate_units/timestep

Distance Calculation:
Euclidean distance in lat/lon coordinates:
distance = √[(lat₂-lat₁)² + (lon₂-lon₁)²]

Note: This is approximate for small distances.
For accuracy, should use haversine formula for spherical Earth.

EDGE CASES HANDLED:

1. Zero-length speed vector:
   - Set to zero vector instead of normalizing
   - Prevents division by zero

2. No neighbors available:
   - Return to previous source (U-turn)
   - Prevents car from getting stuck

3. Single neighbor:
   - Choose it directly without probability calculation
   - Optimizes common case

4. Area restrictions:
   - Use adj_matrix_area instead of full adj_matrix
   - Keeps cars within assigned geographical areas
"""
