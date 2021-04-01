import pickle
#Methods
#dump()  - serializes to an open file
#dumps() - serialize to a string
#load()  - deserializes from an open-like object
#loads() - deserializes from a string 

def serialize(data):
    #return serialized data
    return pickle.dumps(data)

def deserialize(dump):
    #return deserialized data
    return pickle.loads(dump)