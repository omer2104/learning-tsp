import time
import argparse
import pprint as pp
import os
from tqdm import tqdm
import numpy as np
from concorde.tsp import TSPSolver  # https://github.com/jvkersch/pyconcorde


def normalize_coordinates(coords):
    """Normalize coordinates using max normalization to preserve relative distances"""
    coords = np.array(coords)
    
    # Find the maximum absolute value across all coordinates
    max_abs_val = np.max(np.abs(coords))
    
    # Avoid division by zero
    if max_abs_val == 0:
        return coords
    
    # Scale all coordinates by the maximum absolute value
    normalized_coords = coords / max_abs_val
    return normalized_coords


def read_tsp_file(filename):
    """Read TSP instances from file with format: coords output tour"""
    instances = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Split the line into parts
            parts = line.split()
            
            # Find the "output" keyword
            try:
                output_idx = parts.index("output")
            except ValueError:
                print(f"Warning: Skipping line without 'output' keyword: {line[:100]}...")
                continue
            
            # Extract coordinates (everything before "output")
            coord_str = parts[:output_idx]
            if len(coord_str) % 2 != 0:
                print(f"Warning: Skipping line with odd number of coordinates: {line[:100]}...")
                continue
            
            # Convert coordinates to numpy array
            coords = []
            for i in range(0, len(coord_str), 2):
                try:
                    x, y = float(coord_str[i]), float(coord_str[i+1])
                    coords.append([x, y])
                except ValueError:
                    print(f"Warning: Skipping line with invalid coordinates: {line[:100]}...")
                    continue
            
            if len(coords) == 0:
                continue
                
            instances.append(np.array(coords))
    
    return instances


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True, 
                       help="Input file containing TSP instances")
    parser.add_argument("--output_file", type=str, default=None,
                       help="Output file for solved instances (default: input_file_solved.txt)")
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--normalize", type=str, default="True", choices=["True", "False"],
                       help="Normalize coordinates to [0, 1] range (default: True)")
    opts = parser.parse_args()
    
    np.random.seed(opts.seed)
    
    if opts.output_file is None:
        base_name = os.path.splitext(opts.input_file)[0]
        opts.output_file = f"{base_name}_solved.txt"
    
    # Pretty print the run args
    pp.pprint(vars(opts))
    
    # Read instances from file
    print(f"Reading TSP instances from {opts.input_file}...")
    instances = read_tsp_file(opts.input_file)
    print(f"Found {len(instances)} instances")
    
    if len(instances) == 0:
        print("No valid instances found. Exiting.")
        exit(1)
    
    with open(opts.output_file, "w") as f:
        start_time = time.time()
        
        for i, nodes_coord in enumerate(tqdm(instances, desc="Solving TSP instances")):
            num_nodes = len(nodes_coord)
            print(f"Solving instance {i + 1} / {len(instances)} with {num_nodes} nodes")
            
            # Normalize coordinates if requested (for solver only)
            normalized_coords = nodes_coord
            if opts.normalize.lower() == "true":
                normalized_coords = normalize_coordinates(nodes_coord)
                print(f"Normalized coordinates for solver (preserving relative distances)")
            
            try:
                solver = TSPSolver.from_data(normalized_coords[:, 0], normalized_coords[:, 1], norm="GEO")  

                solution = solver.solve(verbose=False)
                
                # Only write instances with valid solutions
                if (np.sort(solution.tour) == np.arange(num_nodes)).all():
                    f.write(" ".join(str(x) + " " + str(y) for x, y in nodes_coord))
                    f.write(" " + "output" + " ")
                    f.write(" ".join(str(node_idx + 1) for node_idx in solution.tour))
                    f.write(" " + str(solution.tour[0] + 1) + " ")
                    f.write("\n")
                else:
                    print(f"Warning: Invalid solution for instance {i + 1}")
                    
            except Exception as e:
                print(f"Error solving instance {i + 1}: {e}")
                continue
        
        end_time = time.time() - start_time
        
    print(f"Completed solving {len(instances)} TSP instances.")
    print(f"Results saved to: {opts.output_file}")
    print(f"Total time: {end_time/60:.1f}m")
    print(f"Average time: {end_time/len(instances):.1f}s")
