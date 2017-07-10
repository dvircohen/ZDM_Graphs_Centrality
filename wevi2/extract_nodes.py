import pandas as pd
from os import listdir
from os.path import isfile, join
import glob
import os


def get_nodes_list(adj_matrix):
    """
    This function recieves a DataFrame and returns all the columns names which are not empty.
    :return:
    A list of column names.
    """
    counter = 0
    node_list = []
    all_names_list = list(adj_matrix.columns.values)
    for col in adj_matrix.values: #Going through all the columns one by one
        for num in col: # Going through all the values in each column.
            if num != 0:
                node_list.append(all_names_list[counter])
                break
        counter += 1
    return node_list

def read_csv():
    """
    This function iterates through all the .csv files in a path and sends
    them through the get_node_list dunc, and then prints the result in a tuple
    :return:
    None
    """
    f = open('Log.txt', 'w')
    path = "C:\Users\Dvir\Desktop\NNftw\Metabolits" #Path to scan
    allfiles = glob.glob(os.path.join(path, "*.csv")) #Only scanning the .csv files
    for file_ in allfiles:
        df = pd.read_csv(file_, index_col=None, header=0)
        df = df.set_index('Unnamed: 0') #fixing a slight movement in the columns.
        names = get_nodes_list(df)
        if len(names) != 0: #Printing only the column names and files that are not empty.
            tup = (os.path.basename(file_), names)
            f.write(os.path.basename(file_) + ",")
            f.write(names)
            print tup
    f.close()

read_csv()