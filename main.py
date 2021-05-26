from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import subprocess
import os
import networkx as nx
import pandas as pd
import baised_walk
import ast
import argparse

def parse_args():
    

    parser = argparse.ArgumentParser(description="compute walks.")

    parser.add_argument('--nets', type=str, default=['tf_target.edgelist','coexp.edgelist'],
    nargs='+', help="Input networks.")

    parser.add_argument('--output', nargs='?', default='../emb/?',
    help='Embeddings path')
    parser.add_argument('--walk-length', type=int, default=20,
                        help='Length of walk per source. Default is 80.')

    parser.add_argument('--num-walks', type=int, default=10,
                        help='Number of walks per source. Default is 10.')

    parser.add_argument('--i_value', type=float, default=1.0,
                        help='Multitative factor. Default is 1.0')

    parser.add_argument('--weighted', dest='weighted', action='store_true',
                        help='Boolean specifying (un)weighted. Default is unweighted.')
    parser.add_argument('--unweighted', dest='unweighted', action='store_false')
    parser.set_defaults(weighted=False)

    parser.add_argument('--directed', dest='directed', action='store_true',
                        help='Graph is (un)directed. Default is undirected.')
    parser.add_argument('--undirected', dest='undirected', action='store_false')
    parser.set_defaults(directed=False)

    parser.add_argument('--BFS', dest='BFS', action='store_true',
                        help='Do random walks based on DFS(BFS). Default is DFS.')
    parser.add_argument('--DFS', dest='DFS', action='store_false')
    parser.set_defaults(BFS=False)
    parser.add_argument('--method', type=str, required=True, choices=['bern'],
                        help='The community detection method.')
    parser.add_argument('--window_size', type=int, required=False, default=5,
                        help='The window size.')
    parser.add_argument('--neg_sample', type=int, required=False, default=5,
                        help='The number of negative samples.')
    parser.add_argument('--dim', type=int, required=False, default=128,
                        help='The dimension size.')
    parser.add_argument('--starting_alpha', type=float, required=False, default=0.025,
                        help='Initial learning rate.')
    parser.add_argument('--min_alpha', type=float, required=False, default=0.0001,
                        help='Minimum learning rate.')
    parser.add_argument('--decay_rate', type=float, required=False, default=1,
                        help='The decay rate.')
    parser.add_argument('--num_iters', type=int, required=False, default=1,
                        help='The number of iterations.')
    parser.add_argument('--sigma', type=float, required=False, default=1,
                        help='The sigma value for norm model.')

    return parser.parse_args()

def process(args):

    cwd = os.getcwd()
    efge_path = os.path.join(cwd, "efge")

    if not os.path.isfile(efge_path):
        print("Please run \"make all\" command to compile the files.")
    else:

        subprocess.run( args=[efge_path,
                              "--corpus", args.corpus,
                              "--output", args.output,
                              "--method", args.method,
                              "--window_size", str(args.window_size),
                              "--neg_sample", str(args.neg_sample),
                              "--dim", str(args.dim),
                              "--starting_alpha", str(args.starting_alpha),
                              "--min_alpha", str(args.min_alpha),
                              "--decay_rate", str(args.decay_rate),
                              "--num_iters", str(args.num_iters),
                              "--sigma", str(args.sigma)
                              ],
                       )



def read_graphs():
    
    args = parse_arguments()
    
    net_list = args.nets
    
    alpha_within = args.alpha_within
    alpha_across = args.alpha_across
    
    net1 = net_list[0]
    net2 = net_list[1]
    
    print("-----------------------Graphs read successfuly---------------------------------")

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

    return(multinet)
    
    
def compute_walks(multinet):  
    
    print("--------------------------------Simulating walks---------------------------------")

    
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
    
    return(walklist)


if __name__ == "__main__":
    args = parse_args()
    print ("Walk length"), args.walk_length
    print ("i_value"), args.i_value
    print("Number of walks: "), args.num-walks
    multinet = read_graphs()
    walklist = compute_walks(multinet)
    args.corpus = walklist
    process(args)


