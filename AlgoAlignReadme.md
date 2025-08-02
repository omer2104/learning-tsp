In here we will document all that has been done on this repo as part of the research.

## Setup
Installation and running locally: TODO

## Generating datasets

Using the file `data/tsp/generate_tsp.py`, I was able to create random datasets of tsp and solve them with the concorde solver.

This is the package of the solver: https://github.com/jvkersch/pyconcorde

It can be installed with this line:
```
pip install 'pyconcorde @ git+https://github.com/jvkersch/pyconcorde'
```

Easily running on Mac, on Windows can't run natively. Lucklily I also have a Mac and it doesn't take long for the algorithm to run.

After each dataset generation, the Concorder solver will write a lot of unneccessary file to the root folder the script runs on.
You can clear those out with:
```
just clean-tsp-files
```

### Re-Solving an existing dataset
I created a new script to take an existing example 
Launch json example:
```
{
    "name": "solve_current_dataset.py",
    "type": "debugpy",
    "request": "launch",
    "program": "data/tsp/solve_current_dataset.py",
    "console": "integratedTerminal",
    "args": [
        "--input_file",
        "tsp10-200_with_side_100.txt",
        "--output_file",
        "tsp10-200_with_side_100_solved.txt",
    ]
}
```
This will take the nodes from the dataset, and solve them again with the Concorde Solver, by applying a max normalization so that the coordinates will be between 0 and 1. The normalization happens by default, and can be turned off with the parameter `--normalize False`.
