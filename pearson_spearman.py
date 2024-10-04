import argparse
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from biom import load_table
from datetime import datetime

def load_biom_tables(biom_files):
    """
    Loads OTU tables from multiple BIOM files and combines them into a single DataFrame.

    Parameters:
    biom_files (list of str): Paths to the BIOM files.

    Returns:
    pandas.DataFrame: Combined DataFrame with OTUs as rows and samples as columns.
    """
    dataframes = []
    for biom_file in biom_files:
        table = load_table(biom_file)
        df = table.to_dataframe(dense=True)
        dataframes.append(df)
    # Combine the DataFrames
    combined_df = pd.concat(dataframes, axis=1, sort=False).fillna(0)
    return combined_df

def compute_correlations(df, method='pearson'):
    """
    Computes pairwise correlations between OTUs.

    Parameters:
    df (pandas.DataFrame): DataFrame with OTUs as rows and samples as columns.
    method (str): Correlation method ('pearson' or 'spearman').

    Returns:
    pandas.DataFrame: Correlation matrix.
    """
    if method not in ['pearson', 'spearman']:
        raise ValueError("method should be 'pearson' or 'spearman'")
    correlation_matrix = df.T.corr(method=method)
    
    # Generate timestamp and save to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"correlation_matrix_{method}_{timestamp}.csv"
    correlation_matrix.to_csv(output_file)
    
    return correlation_matrix

def build_cooccurrence_network(correlation_matrix, threshold):
    """
    Builds a co-occurrence network based on the correlation matrix.

    Parameters:
    correlation_matrix (pandas.DataFrame): Correlation matrix.
    threshold (float): Threshold for including an edge in the network.

    Returns:
    networkx.Graph: Co-occurrence network.
    """
    G = nx.Graph()
    # Add nodes
    for otu in correlation_matrix.index:
        G.add_node(otu)
    # Add edges
    for i, otu1 in enumerate(correlation_matrix.index):
        for j, otu2 in enumerate(correlation_matrix.columns):
            if i < j:
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) >= threshold:
                    G.add_edge(otu1, otu2, weight=corr_value)
    return G

def visualize_network(G, title, num_nodes=None):
    """
    Visualizes the co-occurrence network.

    Parameters:
    G (networkx.Graph): Co-occurrence network.
    title (str): Title for the plot.
    num_nodes (int): Number of nodes to visualize (optional).
    """
    if num_nodes and G.number_of_nodes() > num_nodes:
        subgraph_nodes = list(G.nodes())[:num_nodes]
        G = G.subgraph(subgraph_nodes)

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.15, iterations=20)
    # Edge colors based on weight
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    nx.draw_networkx_nodes(G, pos, node_size=50)
    nx.draw_networkx_edges(G, pos, edge_color=weights, edge_cmap=plt.cm.viridis, width=1)
    plt.title(title)
    plt.axis('off')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Build and visualize a co-occurrence network from multiple BIOM files.')
    parser.add_argument('biom_files', nargs='+', help='Paths to the BIOM files.')
    parser.add_argument('--method', type=str, choices=['pearson', 'spearman', 'both'], default='both', help='Correlation method to use.')
    parser.add_argument('--threshold', type=float, default=0.5, help='Correlation threshold for including edges.')
    parser.add_argument('--num_nodes', type=int, default=None, help='Number of nodes to visualize.')
    args = parser.parse_args()

    df = load_biom_tables(args.biom_files)
    print(f"Loaded data with {df.shape[0]} OTUs and {df.shape[1]} samples.")

    methods = []
    if args.method == 'both':
        methods = ['pearson', 'spearman']
    else:
        methods = [args.method]

    for method in methods:
        print(f"\nComputing {method} correlations...")
        correlation_matrix = compute_correlations(df, method=method)
        G = build_cooccurrence_network(correlation_matrix, args.threshold)
        print(f"Co-occurrence network using {method} correlation with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges created.")
        # Visualize the network
        visualize_network(G, title=f'Co-occurrence Network ({method.capitalize()} Correlation)', num_nodes=args.num_nodes)

if __name__ == "__main__":
    main()
