# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:14:02 2021

@author: jagtaps
"""
import networkx as nx
import pandas as pd
import baised_walk
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter




def parse_arguments():
    
    parser = ArgumentParser(description="walks",
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('--nets', type=str, default=['tf_target.edgelist','coexp.edgelist'], nargs='+', help="Input networks.")

    parser.add_argument('--output', type=str, required=True, help='The path of walk file.')

    parser.add_argument('--walk_length', type=int, required=False, default=5,
                        help='The length of walk.')
    parser.add_argument('--number_of _walks', type=int, required=False, default=20,
                        help='Number of walks per node.')
    parser.add_argument('--alpha_within', type=float, required=False, default=1,
                        help='decay parameter to walk within layer.')
    parser.add_argument('--alpha_across', type=float, required=False, default=1,
                        help='decay parameter for walking across layer.')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    
    net_list = args.nets
    
    alpha_within = args.alpha_within
    alpha_across = args.alpha_across
    
    net1 = net_list[0]
    net2 = net_list[1]
    
    net1 = nx.read_weighted_edgelist(net1)
    net2 =  nx.read_weighted_edgelist(net2)
    
    net1_nodes_new = [str(x) + 'A' for x in list(net1.nodes)]
    net_nodes_map = dict(zip(list(net1.nodes), net1_nodes_new))
    net1_net_G = nx.relabel_nodes(net1, net_nodes_map)
    
    net2_nodes_new = [str(x) + 'B' for x in list(net2.nodes)]
    net2_nodes_map = dict(zip(list(net2.nodes), net2_nodes_new))
    net2_net_G = nx.relabel_nodes(net2, net2_nodes_map)
    
    df12 = pd.DataFrame({'net1': sorted(list(net1_net_G.nodes)), 'net2': sorted(list(net2_net_G.nodes)),'weight': [alpha_across]*len(net1_net_G.nodes)})
    net_accross_nx = nx.from_pandas_edgelist(df12,'net1','net2','weight')
    
    multinet = nx.compose_all([net2_net_G,net1_net_G,net_accross_nx])
    
    multinet_G = baised_walk.Graph(multinet, False ,5, 0.5, True)
    multinet_G_walks = multinet_G.simulate_walks(20)

    walklist = []
    for walk in multinet_G_walks:
        walkstr = list(map(str, walk))
        res = [sub[ : -1] for sub in walkstr]
        rss = list(map(lambda x: '0' if x == '' else x, res))
        walklist.append(rss) 
    
    file = args.output
    
    with open(file, 'w') as fh:
        for l in walklist:
            fh.write("{}\n".format(' '.join([str(a) for a in l])))

