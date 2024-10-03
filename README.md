# De Bruijn Graph Construction from FASTA File

This repository contains a Python script that reads sequences from a gzipped FASTA file and constructs a De Bruijn graph. De Bruijn graphs are commonly used in bioinformatics for genome assembly and sequence analysis. The script also includes functionality to visualize a subgraph of the De Bruijn graph to aid in understanding the structure of the data.

## Table of Contents

- [De Bruijn Graph Construction from FASTA File](#de-bruijn-graph-construction-from-fasta-file)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Usage](#usage)
  - [Script Overview](#script-overview)
  - [Functions](#functions)
  - [Visualization](#visualization)
  - [Saving and Loading the Graph](#saving-and-loading-the-graph)
  - [Notes](#notes)
  - [License](#license)

## Prerequisites

- **Python 3.6** or higher
- **Required Python Packages:**
  - `networkx` (version 3.0 or higher)
  - `matplotlib`

You can install the required packages using `pip`:

```bash
pip install networkx matplotlib
```

## Usage
To run the script, use the following command:

```bash
python fasta.py <input_fasta_file>
```

Replace <input_fasta_file> with the path to your gzipped FASTA file.

## Script Overview
The script performs the following steps:

1. Reads sequences from a gzipped FASTA file.
2. Constructs a De Bruijn graph from the sequences.
3. Provides functionality to visualize a subgraph of the De Bruijn graph.

## Functions

`read_fasta(file_path)
`

Reads sequences from a gzipped FASTA file.

`construct_de_bruijn_graph(sequences, k)
`

Constructs a De Bruijn graph from the given sequences with k-mers of length k.

`visualize_subgraph(graph, node, radius)
`

Visualizes a subgraph of the De Bruijn graph centered around a given node within a specified radius.

## Visualization
To visualize a subgraph of the De Bruijn graph, use the visualize_subgraph function. This function requires matplotlib to display the graph.

Example:

```python
import networkx as nx
import matplotlib.pyplot as plt
from fasta import read_fasta, construct_de_bruijn_graph, visualize_subgraph

sequences = read_fasta('example.fasta.gz')
graph = construct_de_bruijn_graph(sequences, k=21)
visualize_subgraph(graph, node='ATG', radius=2)
plt.show()
```

## Saving and Loading the Graph
You can save the constructed De Bruijn graph to a file and load it later using networkx functions.

Example:
```python
nx.write_gpickle(graph, 'de_bruijn_graph.gpickle')
loaded_graph = nx.read_gpickle('de_bruijn_graph.gpickle')
```

## Notes
Ensure that the input FASTA file is gzipped.
The script assumes that the sequences are DNA sequences.

## License
This project is licensed under the MIT License.
