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
2. Enable agent and environment resuse by adding a reset and initialization logic
3. Organize `contrib` module for specialized agents and environments
4. Differentiate continuous observers (pygame) from one-shot observers (d3, matplotlib, pandas)
