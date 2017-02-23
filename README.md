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
2. Differentiate continuous observers (pygame) from one-shot observers (d3, matplotlib, pandas)
3. Let agents access parameters of the environment
4. Provide a hook for users to update environment parameters at each step