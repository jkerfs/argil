# argil

A simple library designed primarily for crowd and robot simulations in Python.

## Project Goals:

1. straightforward interface and API
2. flexible visualization and data collection
3. contrib modules for crowd, geometry, robot algorithm primitives


## Current Observers

- d3 (https://d3js.org/)
- matplotlib (http://matplotlib.org/)
- pygame (http://www.pygame.org/lofi.html)
- pandas (http://pandas.pydata.org/)

## Roadmap

1. Document modeling api and individual observers
2. Organize `contrib` module for specialized agents and environments
3. Differentiate continuous observers (pygame) from one-shot observers (d3, matplotlib, pandas)
4. Implement multiple runs and combinations of parameters
5. Let agents access parameters of the environment
6. Provide a hook for users to update environment parameters at each step