from comparation import euclidaen_distance
import extractor as extr

class KNN(object):
    def __init__(self, k, vec):
        self.k         = k      #number of neighbours
        self.vec       = vec    #source vector
        self.neighbors = list() #list of nearest neighbors

    """
    Method adds descriptor vector with its distance to neighbors list
    calls method append
    Params: 
        i: int - index of input vector in database
        sec_vec: list - descriptor vector
    """
    def add(self, i, sec_vec):
        distance = euclidaen_distance(self.vec, sec_vec)
        self.append(i, distance)

    """
    Method appends descriptor with its distance from 
    source vector to neighbors
    Neighbors are sorted by distance
    Parameters:
        i: int - index of descriptor vector
        p: list - vector with descriptor
    """
    def append(self, i, p):
        if (len(self.neighbors)<self.k):
            self.neighbors.append((i, p))
            self.neighbors.sort(key=lambda e: e[1])

        elif (p < self.neighbors[self.k-1][1]):
            self.neighbors[self.k-1] = (i, p)
            self.neighbors.sort(key=lambda e: e[1])

    def get_neighbors(self):
        return self.neighbors

"""
This class differs from above one by used comparisement
This one use function to retrieve similar descriptors
more there are, better result, probabbly more similar pictures
"""
class KNN_similarity(object):
    def __init__(self, k, vec):
        self.k         = k      #number of neighbours
        self.vec       = vec    #source vector
        self.neighbors = list() #list of nearest neighbors

    """
    Method adds descriptor vector with its distance to neighbors list
    calls method append
    Params: 
        i: int - index of input vector in database
        sec_vec: list - descriptor vector
    """
    def add(self, i, sec_vec):
        similarity = extr.extract_similar_descriptors (self.vec, sec_vec)
        self.append(i, similarity)

    """
    Method appends descriptor with its distance from 
    source vector to neighbors
    Neighbors are sorted by distance
    Parameters:
        i: int - index of descriptor vector
        p: list - vector with descriptor
    """
    def append(self, i, p):
        if (len(self.neighbors)<self.k):
            self.neighbors.append((i, p))
            self.neighbors.sort(key=lambda e: e[1])

        elif (p > self.neighbors[self.k-1][1]):
            self.neighbors[self.k-1] = (i, p)
            self.neighbors.sort(key=lambda e: e[1], reverse=True)
    """
    Retrieve similar pictures, their indexes
    """
    def get_neighbors(self):
        real_neighbors = list()
        for n in self.neighbors:
            real_neighbors.append(n[0])
        return real_neighbors
