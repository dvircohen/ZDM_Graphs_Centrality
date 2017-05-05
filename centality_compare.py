from collections import OrderedDict

import networkx as nx
from scipy.stats.stats import pearsonr, spearmanr
from tabulate import tabulate


def graph_maker():
    list1 = [1 if num < 5 else 5 for num in range(10)]
    graph = nx.configuration_model(list1, seed=123)
    return graph


def centrality_compare(graph=None, nodes_string=None):
    measurements_dict = OrderedDict()
    compare_dict = OrderedDict()

    # The data from wevi
    if nodes_string is None:
        nodes_list = [0.07553153757502284, 0.008804137964580436, 0.009528332679916485, 0.09411131873310066,
                      0.056807282025497695, 0.09709045935848355, 0.058825181534953086, 0.2655416154784191,
                      0.18734994882402486, 0.14641018582600146]
    else:
        nodes_list = [float(x) for x in nodes_string.split(",")]
    # Put the wevi data in a dictionary
    node_dict = {num: val for num, val in enumerate(nodes_list)}

    # Make the graph and make it simple graph instead of multi graph
    if graph is None:
        graph = graph_maker()
    graph = nx.Graph(graph)

    # Add all the measurements to the measurements dict
    measurements_dict["wevi"] = node_dict.values()
    measurements_dict["closeness centrality"] = nx.closeness_centrality(graph).values()
    measurements_dict["eigenvector centrality"] = nx.eigenvector_centrality(graph).values()
    measurements_dict["degree centrality"] = nx.degree_centrality(graph).values()
    measurements_dict["betweenness centrality"] = nx.betweenness_centrality(graph).values()
    measurements_dict["katz centrality"] = nx.katz_centrality(graph).values()
    measurements_dict["load centrality"] = nx.load_centrality(graph).values()

    # Loop over all the cenrality measurements
    for centrality_name, centrality_value in measurements_dict.items():
        # Calculate correlations
        pearson = pearsonr(centrality_value, nodes_list)
        spearman = spearmanr(centrality_value, nodes_list)

        # add it the the compare dict
        compare_dict[centrality_name] = [pearson[0], spearman[0], pearson[1]]

    # Print the results nicely
    print tabulate([[x, y[0], y[1], y[2]] for x, y in compare_dict.items()],
                   headers=['Name', 'Pearson', 'Spearman', 'p-value'])


if __name__ == "__main__":
    centrality_compare()