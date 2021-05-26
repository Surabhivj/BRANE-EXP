# BRANE-EXP
Multiomics Data Integration with Exponential Family Embeddings

**Data**:
**Download the network files from https://bit.ly/37ZO37e**

#### Compilation

**1.** To compile type the following command:
```
make all
```

**2.** To learn representation type the following command:
```
python main.py --nets tftarget_net.edgelist coexpression.edgelist --output tf_coexp.emb
```

**4.** To infer GRN from embeddings type the following command:
```
python grn.py --emb tf_coexp.emb --node_map yeast_node_map.txt --tf_list tf_list.txt--output tf_coexp.grn
```

**5.** To see the detailed parameter settings, you can use
```
./efge --help
```

#### References
A. Celikkanat and F. D. Malliaros, [Exponential Family Graph Embeddings](https://arxiv.org/pdf/1911.09007.pdf)

Duong Nguyen and Fragkiskos D. Malliaros, [BiasedWalk: Biased Sampling for Representation Learning on Graphs](https://arxiv.org/pdf/1809.02482.pdf)

#### Publication

Multiomics Data Integration for Gene Regulatory Network Inference with Exponential Family Embeddings
Surabhi Jagtap, Abdulkadir Çelikkanat, Aurélie Pirayre, Frederique Bidard, Laurent Duval, and Fragkiskos D. Malliaros.
European Signal Processing Conference (EUSIPCO),2021
