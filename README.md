CSE-5911-Lit-Network
====================

##Summary
This project is used to compile multiple protein networks into a single reduced network, extrapolating links between a set of target proteins. 

1. Files in data/unprocessed\_sources are processed and placed into data/processed\_sources in a common format. This is performed by scripts in litnetworks/cleaners, where one script exists for each file to be processed. This script contains the logic to convert to the common format 
2. Files in data/processed\_sources are then combined into data/compiled\_processed\_sources.tab by litnetwork/compile\_processed.py
3. litnetwork/reduce\_network.py then analyzes data/compiled\_processed\_sources.tab and data/target\_hugo.txt to filter out proteins not connected to one of the target proteins of interest. The maximum distance from a target protein is configurable in litnetwork/config.py.
4. The final step is compiling the reduced network into adjacency matrices showing the distance between source and target nodes, and the computed score of their edges(data/compiled\_network\_lengths\_adj.tab and data/compiled\_network\_score\_adj.tab). This is performed by litnetwork/write\_matrices.py



##Setup
* Install [networkx](http://networkx.github.io/)
* Add the repo's directory to your $PYTHONPATH or $PATH
* Make sure gen\_all is executable
* Run ./gen\_all or python gen\_all
