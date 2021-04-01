import numpy as np
import database_handler as daha
import extractor as extr
import knn_algorithm as knnal

"""
Fast function for euclidean distance
Parameters:
    A: first vector
    B: second vector
Returns:
    euclidean distance
"""
#euclidean_distance(A, B) = Sqrt(Sum[n, i=1]((A[i]-B[i])**2))
def euclidaen_distance(A, B):
    Z = A - B
    out = np.sqrt(np.einsum('i,i->', Z, Z))
    return out

"""
Function compare pictures from datasets with givan function type
Parameters:
    func_type: function type
    func_data: function data
"""
def compare_controller(func_type, func_data):
    if func_type == "knn":        
        compare_knn(func_data)
        compare_self_knn("ds1", func_data)
        compare_self_knn("ds2", func_data)
    
    elif func_type == "range":
        compare_distance(func_data)
        compare_self_distance("ds1", func_data)
        compare_self_distance("ds2", func_data)

"""
Function compares pictures from first set with pictures from second set
and stores those with similarity greater than func_data
Params:
    func_data: similarity of pictures has to be greater than 0-1
"""
def compare_distance(func_data):
    first_len = daha.get_data_length("ds1Names")
    second_len = daha.get_data_length("ds2Names")
    for i in range(0, first_len):
        #first_name = daha.get_name("ds1Names", i)
        
        first_descr = daha.get_descriptor("ds1", i)
        #first_descr = extr.extract_img_features(first_name)

        for j in range(0, second_len):
            #second_name = daha.get_name("ds2Names", j)
            
            second_descr = daha.get_descriptor("ds2", j)
            #second_descr = extr.extract_img_features(second_name)

            res = extr.extract_similar_descriptors(first_descr, second_descr, float(func_data))

            #dist = cosim.cosine_similarity(first_descr, second_descr)

            if res == True:#dist > float(func_data):
                daha.store_ids(i, j, "ds1Ds2Similarity")

"""
Function copares two sets of pictures with using knn with k = func_data
Parameters:
    func_data: number of nearest neighbors to use in knn algorithm
"""
def compare_knn(func_data):
    first_len = daha.get_data_length("ds1Names")
    second_len = daha.get_data_length("ds2Names")
    for i in range(0, first_len):
        #first_name = daha.get_name("ds1Names", i)
        
        first_descr = daha.get_descriptor("ds1", i)

        knn = knnal.KNN_similarity(int(func_data), first_descr)

        for j in range(0, second_len):
            #second_name = daha.get_name("ds2Names", j)

            second_descr = daha.get_descriptor("ds2", j)

            knn.add(j, second_descr)
    
        neighbors = knn.get_neighbors()
        for n in neighbors:
            daha.store_ids(i, n, "ds1Ds2Similarity")

"""
Compares pictures in its dataset
"""
def compare_self_distance(set_name, func_data):
    table_name = set_name + "Names"

    len = daha.get_data_length(table_name)
    
    for i in range(0, len):
        #first_name = daha.get_name(table_name, i)
        
        first_descr = daha.get_descriptor(set_name, i)

        for j in range(0, len):
            if j == i:
                continue
            #second_name = daha.get_name(table_name, j)
            
            second_descr = daha.get_descriptor(set_name, j)

            res = extr.extract_similar_descriptors(first_descr, second_descr, float(func_data))

            if res==True:
                daha.store_ids(i, j, set_name+"Similarity")

"""
Function compares pictures from current dataset
"""
def compare_self_knn(set_name, func_data):
    table_name = set_name + "Names"

    len = daha.get_data_length(table_name)
    
    for i in range(0, len):
        #first_name = daha.get_name(table_name, i)
        
        first_descr = daha.get_descriptor(set_name, i)

        knn = knnal.KNN_similarity(int(func_data), first_descr)

        for j in range(0, len):
            if i == j:
                continue
            #second_name = daha.get_name(table_name, j)
            
            second_descr = daha.get_descriptor(set_name, j)

            knn.add(j, second_descr)

        neighbors = knn.get_neighbors()
        
        for n in neighbors:
            daha.store_ids(i, n, set_name+"Similarity")

"""
#old version
def compare_datasets(mode):
    first_len = daha.get_data_length("ds1Names")
    second_len = daha.get_data_length("ds2Names")
    print("first len ", first_len)
    print("second len", second_len)
    for i in range(0, first_len):
        first_name = daha.get_name("ds1Names", i)
        
        first_descr = extr.extract_img_features(first_name)
        knn = knnal.KNN(6, first_descr)

        for j in range(0, second_len):
            second_name = daha.get_name("ds2Names", j)
            
            second_descr = extr.extract_img_features(second_name)

            dist = cosim.cosine_similarity(first_descr, second_descr)
            
            print("\n\nfirst name ", first_name)
            print("second name ", second_name)
            print("cosine descriptor " + str(dist))
            print("\n\n\n")

            if dist <= 0.5:
                daha.store_ids(i, j, "ds1Ds2Similarity")
            
            dist = knn.add(j, second_descr)
    
        neighbors = knn.get_neighbors
        for n in neighbors:
            daha.store_ids(i, n, "ds1Ds2Similarity")
  

def compare_descriptors(first_descr, second_descr):
    if (len(first_descr)!=len(second_descr)):
        return None
    return euclidaen_distance(first_descr, second_descr)
"""