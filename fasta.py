import gzip
import networkx as nx
import argparse
import matplotlib.pyplot as plt
import pickle  # Added for graph serialization

def build_de_bruijn_graph(fasta_gz_file, k):
    """
    Builds a De Bruijn graph from sequences in a gzipped FASTA file.

    Parameters:
    fasta_gz_file (str): Path to the gzipped FASTA file.
    k (int): Length of k-mers to use for the graph.

    Returns:
    networkx.DiGraph: A directed graph representing the De Bruijn graph.
    """
    G = nx.DiGraph()
    with gzip.open(fasta_gz_file, 'rt') as f:
        seq = ''
        for line in f:
            if line.startswith('>'):
                # Process the previous sequence
                if seq != '':
                    add_sequence_to_graph(seq, G, k)
                    seq = ''
            else:
                seq += line.strip()
        # Add the last sequence
        if seq != '':
            add_sequence_to_graph(seq, G, k)
    return G

def add_sequence_to_graph(seq, G, k):
    """
    Adds k-mers from a sequence to the De Bruijn graph.

    Parameters:
    seq (str): The DNA sequence.
    G (networkx.DiGraph): The De Bruijn graph.
    k (int): Length of k-mers to use for the graph.
    """
    for i in range(len(seq) - k + 1):
        kmer = seq[i:i+k]
        prefix = kmer[:-1]
        suffix = kmer[1:]
        G.add_edge(prefix, suffix)

def visualize_graph(G, num_nodes=100):
    """
    Visualizes a subgraph of the De Bruijn graph.

    Parameters:
    G (networkx.DiGraph): The De Bruijn graph.
    num_nodes (int): Number of nodes to include in the visualization.
    """
    # If the graph is too big, sample a subgraph
    if G.number_of_nodes() > num_nodes:
        subgraph_nodes = list(G.nodes())[:num_nodes]
        subgraph = G.subgraph(subgraph_nodes)
    else:
        subgraph = G

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(subgraph, k=0.15, iterations=20)
    nx.draw(subgraph, pos, node_size=50, arrowsize=10, with_labels=False)
    plt.title('De Bruijn Graph Visualization')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Build and visualize a De Bruijn graph from a gzipped FASTA file.')
    parser.add_argument('fasta_gz_file', type=str, help='Path to the gzipped FASTA file.')
    parser.add_argument('k', type=int, help='Length of k-mers to use for the graph.')
    parser.add_argument('--num_nodes', type=int, default=100, help='Number of nodes to include in the visualization.')
    args = parser.parse_args()

    G = build_de_bruijn_graph(args.fasta_gz_file, args.k)
    # Save the graph using pickle
    with open('de_bruijn_graph.gpickle', 'wb') as f:
        pickle.dump(G, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"De Bruijn graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges created.")
    # Visualize the graph
    visualize_graph(G, num_nodes=args.num_nodes)

if __name__ == "__main__":
    main()