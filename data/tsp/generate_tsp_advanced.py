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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--min_nodes", type=int, default=20)
    parser.add_argument("--max_nodes", type=int, default=50)
    parser.add_argument("--samples_per_node_size", type=int, default=1280)
    parser.add_argument("--num_nodes_increment", type=int, default=10)
    parser.add_argument("--square_side", type=float, default=1.0)
    parser.add_argument("--normalize", type=str, default="False", choices=["True", "False"],
                       help="Normalize coordinates using max normalization (default: False)")
    parser.add_argument("--filename", type=str, default=None)
    parser.add_argument("--seed", type=int, default=1234)
    opts = parser.parse_args()
    
    np.random.seed(opts.seed)
    
    if opts.filename is None:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        opts.filename = f"tsp{opts.min_nodes}-{opts.max_nodes}_square_side_{int(opts.square_side)}_concorde_{timestamp}.txt"
    
    # Pretty print the run args
    pp.pprint(vars(opts))
    
    with open(opts.filename, "w") as f:
        start_time = time.time()
        total_samples = 0
        total_failures = 0
        
        # Generate samples for each node size from min_nodes to max_nodes
        current_nodes = opts.min_nodes
        node_size_idx = 0
        
        while current_nodes <= opts.max_nodes:
            print(f"Generating {opts.samples_per_node_size} samples for {current_nodes} nodes")
            
            for sample_index in tqdm(range(opts.samples_per_node_size), desc=f"Node size {current_nodes}"):
                # Generate coordinates based on square_side parameter
                if opts.square_side > 1.0:
                    nodes_coord = np.random.uniform(0, opts.square_side, size=[current_nodes, 2])
                else:
                    nodes_coord = np.random.random([current_nodes, 2])
                
                original_nodes_coord = nodes_coord.copy()
                # Normalize coordinates if requested
                if opts.normalize.lower() == "true":
                    nodes_coord = normalize_coordinates(nodes_coord)
                
                solver = TSPSolver.from_data(nodes_coord[:, 0], nodes_coord[:, 1], norm="GEO")  
                solution = solver.solve(verbose=False)
                
                # Only write instances with valid solutions
                if (np.sort(solution.tour) == np.arange(current_nodes)).all():
                    f.write(" ".join(str(x) + " " + str(y) for x, y in original_nodes_coord))
                    f.write(" " + "output" + " ")
                    f.write(" ".join(str(node_idx + 1) for node_idx in solution.tour))
                    f.write(" " + str(solution.tour[0] + 1) + " ")
                    f.write("\n")
                    total_samples += 1
                else:
                    print(f"Warning: Invalid solution for {current_nodes} nodes, sample {sample_index + 1}")
                    total_failures += 1
            
            # Move to next node size
            node_size_idx += 1
            current_nodes = opts.min_nodes + (opts.num_nodes_increment * node_size_idx)
            
            # Check if we've exceeded max_nodes
            if current_nodes > opts.max_nodes:
                break
        
        end_time = time.time() - start_time
        
    print(f"Completed generation of {total_samples} samples across node sizes {opts.min_nodes}-{opts.max_nodes}.")
    print(f"Results saved to: {opts.filename}")
    print(f"Total samples: {total_samples}")
    print(f"Total failures: {total_failures}")
    print(f"Total time: {end_time/60:.1f}m")
    if total_samples > 0:
        print(f"Average time: {end_time/total_samples:.1f}s")