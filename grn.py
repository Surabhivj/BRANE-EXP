# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:47:37 2021

@author: jagtaps
"""
import networkx as nx
import pandas as pd
from sklearn.preprocessing import normalize
import ast

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def parse_arguments():
    
    parser = ArgumentParser(description="walks",formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--emb', type=str, default='tf_coexp.emb', nargs='+', help="embedding file.")
    parser.add_argument('--output', type=str, default= 'tf_coexp.grn', help='The path of grn file.')
    parser.add_argument('--node_map', type=str, default='yeast_node_map.txt', help='The file to map node to gene names.')
    parser.add_argument('--tf_list', type=str, default='tf_list', help='The path of TF list file.')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    
    emb = args.emb
    netfile = args.output
    node_map = args.node_map
    tf_list = args.tf_list
    
    file = open(node_map, "r")
    contents = file.read()
    dictionary = ast.literal_eval(contents)
    tf_list = pd.read_csv(tf_list, delimiter = "\t", header = None)
    tf = tf_list[0].values
    tf_id = [ dictionary.get(item,item) for item in tf ]


    def net_recons_graph(emb):
        Mat = emb.values @ emb.values.transpose()
        MatNorm  = (normalize(Mat))
        MatNormDF = pd.DataFrame(MatNorm, index=list(emb.index), columns=list(emb.index))
        MatNormDF.sort_index()
        MatNormDF_melt = MatNormDF.stack().reset_index()
        emb_tf = MatNormDF_melt[MatNormDF_melt['level_0'].isin(tf_id)]  
        return emb_tf
    
    grn = net_recons_graph(emb)
    nx.write_edgelist(grn,'tf_coexp.grn')










