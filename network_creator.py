import random
from collections import Counter

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from tabulate import tabulate

from centality_compare import centrality_compare
from gensim_testing import testing_gensim
from wevi_parser import wevi_parser


use_new_version = 1
show_graph = 0
number_of_walks = 20
length_of_walks = 10
window_size = 2
num_of_iteration = 2000
number_of_graphs = 1
number_of_nodes = 20
csv_path = "C:\Users\Dvir\Desktop\NNftw\words2.csv"


def graph_maker():
    list1 = [1 if num < 5 else 5 for num in range(10)]
    # graph = nx.configuration_model(list1, seed=123)
    # graph = nx.gnp_random_graph(10, 0.24,seed=15) # awesome graph
    # graph = nx.gnp_random_graph(11, 0.24,seed=1341) # awesome graph2
    # graph = nx.gnp_random_graph(10, 0.24,seed=1341) # spider graph2
    # graph = nx.gnp_random_graph(20, 0.12,seed=1234)
    # graph = nx.gnp_random_graph(50, 0.2,seed=1234)
    # graph = nx.gnp_random_graph(number_of_nodes, 0.24)
    graph = nx.barabasi_albert_graph(number_of_nodes, 1, seed=465)

    print "done creating network"
    return graph


def get_neighbor(row_index, adj_mat):
    # Select an adjacent node to node 'row_index'
    adjacent_nodes = np.argwhere(adj_mat[row_index] != 0).flatten()
    if len(adjacent_nodes) == 0:
        return -1
    return random.choice(adjacent_nodes)


def make_random_walks(adj_mat, num_of_walks, len_of_walks):
    # Generate a sentence for each random walk
    random_walks_sentences = []

    num_of_adjacency_matrix_rows = adj_mat.shape[0]
    # Iterate over the rows of the adjacency matrix
    # Variable i represents the starting node of the random walk
    for i in range(num_of_adjacency_matrix_rows):
        for j in range(num_of_walks):
            current_node = i

            # Starting node - always node i
            current_walk = list(["Node" + str(i)])

            # travel to other nodes and append them to the random walk
            for k in range(len_of_walks):
                current_node = get_neighbor(current_node, adj_mat)
                if current_node != -1:
                    current_walk.append("Node" + str(current_node))
                else:
                    break

            # append to the result matrix
            current_sentence = ' '.join(current_walk)
            random_walks_sentences.append(current_sentence)
    result = pd.DataFrame({"String": random_walks_sentences})

    # Value counts
    listses = [x.split(" ") for x in random_walks_sentences]
    biglist = [item for sublist in listses for item in sublist]
    count2 = dict(Counter(biglist))

    final_list = [count2["Node"+str(i)] for i in range(len(count2))]

    return result, final_list, listses



def save_to_csv(random_walks, csv_path):
    random_walks.to_csv(csv_path, index=False)


def calculate_num_of_iteration(number_of_walks, length_of_walks, num_of_vectors):
    return number_of_walks * (length_of_walks + 1) * num_of_vectors

def make_graph_and_calculate_centrality():

    # make graph
    graph = graph_maker()

    # draw the graph if you want to
    nx.draw_networkx(graph)
    if show_graph:
        plt.show()

    # get the adjacency matrix
    adj_matrix = nx.adjacency_matrix(graph)

    # turn it from sparse to regular
    sparse_df = pd.SparseDataFrame(
        [pd.SparseSeries(adj_matrix[x].toarray().ravel()) for x in np.arange(adj_matrix.shape[0])])
    df = sparse_df.to_dense()

    # change the name of the rows
    df.index = ['Node' + str(x) for x in df]
    adj_matrix = df

    # make the random walks
    random_walks, value_counts, separated_string = make_random_walks(adj_matrix, number_of_walks, length_of_walks)
    print "done with random walks"
    # Calculate the number of iteration needed
    num_of_iteration = calculate_num_of_iteration(number_of_walks, length_of_walks, len(df.index))

    # after_parse =  wevi_parser(random_walks, window_size)
    # print "num of iter is {}".format(num_of_iteration)
    # centrality_vector = wevi_automate(after_parse, num_of_iteration)
    # centrality_compare(graph, centrality_vector)

    if use_new_version:
        input1 = str(testing_gensim(separated_string))[1:-1]
    else:
        print "The input to wevi:"
        print wevi_parser(random_walks, window_size)
        print "Please paste here the results from wevi"
        input1 = raw_input()

    compare_dict = centrality_compare(graph, input1, value_counts)
    return compare_dict


def main():
    sum_of_pearson = Counter()
    for i in range(number_of_graphs):
        print "Iteration number - {}".format(i)
        # run the algorithem
        compare_dict = make_graph_and_calculate_centrality()

        sum_of_pearson += Counter({key: value[0] for key, value in compare_dict.items()})

    avg_of_measures = {key: value/number_of_graphs for key,value in sum_of_pearson.items()}
    print tabulate([[x] + [y] for x, y in avg_of_measures.items()], headers=['Name', 'Pearson', 'Spearman', 'linregress', 'Pearson p-value', 'Spearman p-value', 'linregress p-value'])


if __name__ == "__main__":
    main()
