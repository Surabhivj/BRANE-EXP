# BRANE-EXP
Multiomics Data Integration with Exponential Family Embeddings

![braneexp](https://user-images.githubusercontent.com/47250394/211617786-f465033b-e87d-4b71-ac7f-8b6fdc744f83.png)


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



#### Publication

>| Multiomics Data Integration for Gene Regulatory Network Inference with Exponential Family Embeddings Surabhi Jagtap, Abdulkadir Çelikkanat, Aurélie Pirayre, Frederique Bidard, Laurent Duval, and Fragkiskos D. Malliaros. European Signal Processing Conference (EUSIPCO),2021 | 
>
>@inproceedings{jagtap2021multiomics,
  title={Multiomics Data Integration for Gene Regulatory Network Inference with Exponential Family Embeddings},
  author={Jagtap, Surabhi and Celikkanat, Abdulkadir and Pirayre, Aur{\'e}lie and Bidard, Frederique and Duval, Laurent and Malliaros, Fragkiskos},
  booktitle={29th European Signal Processing Conference (EUSIPCO)},
  year={2021}
}
>| --- |



