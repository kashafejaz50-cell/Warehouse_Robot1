#!/usr/bin/env python3
"""Main entry point for warehouse robot delivery system."""

import argparse
import sys
from pathlib import Path

# ----------------------------
# Force Python to see the project root
# This ensures 'src' and 'experiments' are always importable
# ----------------------------
project_root = Path(__file__).parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# ----------------------------
# Imports
# ----------------------------
from src.utils import set_seed, load_config
from src.state import RobotState
from src.search import UniformCostSearch
from src.problem import WarehouseProblem

# Import experiments functions (matches your actual file)
from experiments.run_experiments import get_grid_from_csv, parse_grid

# ----------------------------
# Main function
# ----------------------------
def main():
    parser = argparse.ArgumentParser(description="Warehouse Robot Delivery")
    parser.add_argument(
        "--grid",
        type=str,
        default="simple_5x5",
        help="Grid name (simple_5x5, medium_8x8, hard_10x10)"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--no-mlflow", action="store_true", help="Disable MLflow")
    
    args = parser.parse_args()
    
    # Load config
    config = load_config()
    
    # Set seed
    set_seed(args.seed)
    
    # Load grid
    grid = get_grid_from_csv(args.grid)
    if not grid:
        print(f"Grid {args.grid} not found")
        return
    
    # Find positions in grid
    package_positions = []
    delivery_pos = None
    start_pos = None
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'P':
                package_positions.append((i, j))
            elif grid[i][j] == 'D':
                delivery_pos = (i, j)
            elif grid[i][j] == 'S':
                start_pos = (i, j)
    
    if start_pos is None or delivery_pos is None:
        print("Error: Grid missing start 'S' or delivery 'D' position")
        return
    
    # Create problem and initial state
    problem = WarehouseProblem(grid, package_positions, delivery_pos)
    initial_state = RobotState(start_pos, frozenset())
    
    # Solve with Uniform Cost Search
    ucs = UniformCostSearch(problem)
    path, cost, nodes, time_taken = ucs.solve(initial_state)
    
    # Print results
    if path:
        print(f"\n✓ Solution found!")
        print(f" Cost: {cost}")
        print(f" Path: {path}")
        print(f" Nodes expanded: {nodes}")
        print(f" Time: {time_taken:.3f}s")
    else:
        print("\n✗ No solution found")

# ----------------------------
# Entry point
# ----------------------------
if __name__ == "__main__":
    main()
    