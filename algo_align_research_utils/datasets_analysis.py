import math
from tqdm import tqdm
import pandas as pd


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


def dataset_control_parameter_analysis(filename: str, square_size: float, offset: int = 0, limit: int = None) -> pd.DataFrame:
    num_nodes_col = []
    tour_length_col = []

    total_lines = len(open(filename, "r").readlines())

    print(f"Total lines: {total_lines}")

    if limit is None:
        limit = total_lines

    lines = open(filename, "r").readlines()[offset:(offset + limit)]
    for line in tqdm(lines):
        line = line.split(" ")
        num_nodes = int(line.index('output') // 2)
        cities_points = [Point(float(line[idx]), float(line[idx + 1])) for idx in range(0, 2 * num_nodes, 2)]
        tour_nodes = [int(node) - 1 for node in line[line.index('output') + 1:-1]]

        tour_length = sum(
            cities_points[tour_nodes[i]].distance(cities_points[tour_nodes[i + 1]])
            for i in range(len(tour_nodes) - 1)
        )
        
        num_nodes_col.append(num_nodes)
        tour_length_col.append(tour_length)

    base_df = pd.DataFrame({
        "num_nodes": num_nodes_col,
        "tour_length": tour_length_col,
    })

    control_parameter = base_df.apply(
        lambda row: row['tour_length'] / math.sqrt(row["num_nodes"] * square_size),
        axis=1
    )

    df_with_control_parameter = pd.concat([
        base_df,
        pd.Series(control_parameter, name='control_parameter'),
    ], axis=1)

    return df_with_control_parameter