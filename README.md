# Co-occurrence Network Construction from Multiple BIOM Files

This repository contains a Python script that reads OTU (Operational Taxonomic Unit) tables from multiple BIOM files and constructs co-occurrence networks using both Pearson and Spearman correlations. The script is designed to handle multiple samples and generates networks based on the abundance patterns of OTUs across these samples. Visualization functionality is included to help understand the structure of the networks.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Functions](#functions)
- [Visualization](#visualization)
- [Saving and Loading the Network](#saving-and-loading-the-network)
- [License](#license)

## Prerequisites

- Python 3.6 or higher
- Required Python Packages:
  - `networkx`
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `biom-format`

You can install the required packages using pip:

```bash
pip install networkx pandas numpy matplotlib biom-format
```

## Usage

- Prepare Your BIOM Files:
   1. Collect all your BIOM files (one per sample) and place them in a directory.
   2. Ensure that the OTU IDs are consistent across all files.
- Run the Script:
```bash
python cooccurrence_network.py sample1.biom sample2.biom sample3.biom --method both --threshold 0.6 --num_nodes 100
```
- Parameters:
  - `sample1.biom` `sample2.biom` `sample3.biom`: Paths to your BIOM files. You can list as many as needed.
  - `--method`: Correlation method to use. Options are `'pearson'`, `'spearman'`, or `'both'`. Default is `'both'`.
  - `--threshold`: Correlation threshold for including edges in the network. Edges with absolute correlation values above this threshold will be included.
  - `--num_nodes`: Number of nodes to visualize (optional). Helps manage visualization of large networks.


- Script Output:
  - The script will load the BIOM files, combine them into a single DataFrame, and compute the correlation matrices.
  - It will build co-occurrence networks based on the specified correlation method(s).
  - The script will print the number of OTUs, samples, nodes, and edges.
  - Visualization windows will display the co-occurrence networks.

## Functions
### `load_biom_tables(biom_files)`

Loads OTU tables from multiple BIOM files and combines them into a single DataFrame.
- Parameters:
  - `biom_files` (list of str): Paths to the BIOM files.
- Returns:
  - `pandas.DataFrame`: Combined DataFrame with OTUs as rows and samples as columns.

### `compute_correlations(df, method='pearson')`

Computes pairwise correlations between OTUs.
- Parameters:
  -  `df (pandas.DataFrame)`: DataFrame with OTUs as rows and samples as columns.
  -  `method` (str): Correlation method ('pearson' or 'spearman').
-  Returns:
   -  `pandas.DataFrame`: Correlation matrix.

### `build_cooccurrence_network(correlation_matrix, threshold)`

Builds a co-occurrence network based on the correlation matrix.
- Parameters:
  - `correlation_matrix (pandas.DataFrame)`: Correlation matrix.
  - `threshold` (float): Threshold for including an edge in the network.
- Returns:
  - `networkx.Graph`: Co-occurrence network.

### `visualize_network(G, title, num_nodes=None)`

Visualizes the co-occurrence network.
- Parameters:
  - `G (networkx.Graph)`: Co-occurrence network.
  - `title` (str): Title for the plot.
  - `num_nodes` (int): Number of nodes to visualize (optional).

## Visualization

Due to the potentially large size of the networks, the `visualize_network()` function allows you to limit the number of nodes displayed.
- Adjusting the Number of Nodes:
```bash
--num_nodes 200  # Visualizes 200 nodes
```
- Edge Coloring:
  - Edges are colored based on their correlation values.
  - Positive and negative correlations can be visually distinguished if desired.
- Saving the Visualization:
  - If you prefer to save the visualization to a file instead of displaying it, you can modify the `visualize_network()` function:
```python
    plt.savefig('cooccurrence_network.png', dpi=300)
```
## Saving and Loading the Network

You can save the constructed networks for later analysis.
- Saving the Network:
```python
nx.write_gpickle(G, f'cooccurrence_network_{method}.gpickle')
```
- Loading the Network:
```python
    import networkx as nx

    G = nx.read_gpickle('cooccurrence_network_pearson.gpickle')
```
## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Contact Information:

For questions or support, please contact brandon@chitownbio.org.