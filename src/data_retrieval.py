import database_handler as daha
import numpy as np
import os
#format of final data is [[name_of_pic, [similar_pictures]],...]

"""
Function cleans old data from project directory
"""
def clean_old_data():
    try:
        os.remove("simijo.db")
        files = [os.path.join("static/data/firstSet", p) for p in sorted(os.listdir("static/data/firstSet"))]
        for f in files:
            os.remove(f)
        
        files = [os.path.join("static/data/secondSet", p) for p in sorted(os.listdir("static/data/secondSet"))]
        for f in files:
            os.remove(f)
    except:
        print("none")
    

"""
Function it returns list of first and second dataset
"""
def data_retrieval():
    first_set = retrieve_dataset_data("ds1")
    second_set = retrieve_dataset_data("ds2")

    return first_set, second_set

"""
This function retrieve data from given table from database
Parameters:
    dataset_name: name of dataset
"""
def retrieve_dataset_data(dataset_name):
    result_list = list()
    table_name = dataset_name + "Names"
    dataset_len = daha.get_data_length(table_name)

    for i in range(0, dataset_len):
        sublist = list()
        parent_name = daha.get_name(table_name, i)
        sublist.append(parent_name)
        
        neighbors = daha.get_similar(i, dataset_name, "ds1" if dataset_name=="ds2" else "ds2", "ds1Ds2Similarity")

        self_neighbors = daha.get_similar(i, dataset_name, dataset_name, dataset_name+"Similarity")

        neighbors.extend(self_neighbors)

        sublist.append(neighbors)

        result_list.append(sublist)
    
        
    return result_list