import database as database
import serializator as srz
from   extractor import extract_img_features as extr_img_feat

"""
Function store image from user to special folder
Parameters:
    image: image to save
    table_name: this indicates which dataset is this picture from
Return:
    new path for picture
"""
def store_image_to_static(image, table_name):
    new_path = ""
    if table_name == "ds1":
        new_path = "static/data/firstSet/"+image.filename
    else:
        new_path = "static/data/secondSet/"+image.filename
    
    image.save(new_path)
    return new_path

"""
Function checks if given file is img
"""
def validateImgFile(imgName):

    if imgName.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        return True
    return False
"""
Function save all names and data of pictures to database
vector of descriptors are serialized before sending into database
Parameters:
    images: path to images
    table_name: indicates what dataset this is
"""
def store_names(images, table_name, key_num, fea_ex):
    db = database.MyBase()
    
    idDB = 0
    #print(images)
    for f in images:
        if validateImgFile(f.filename) == True:
            name = store_image_to_static(f, table_name)
            #load this to database!!!
            db.insert(table_name+"Names", idDB, name)
            #store image descriptors
            db.insert(table_name+"Data", idDB, srz.serialize(extr_img_feat(name, fea_ex, key_num)))
            #increase
            idDB+=1
    db.commit()

"""
Function stores ids to database
this means id from first dataset and second one, pictures with these ids are similar
"""
def store_ids(id1, id2, table_name):
    db = database.MyBase()
    db.insert(table_name, id1, id2)
    db.commit()

"""
Function retrieve descriptor of picture from database
"""
def get_descriptor(table_name, id):
    db = database.MyBase()
    
    pic_descr = db.receive("select data from "+str(table_name)+"Data where fileId="+str(id)+";")[0][0]
    pic_descr = srz.deserialize(pic_descr)

    return pic_descr

"""
Function returns rows length of given table from database
"""
def get_data_length(table_name):
    db = database.MyBase()
    data_len = int(db.receive("select count(*) from "+table_name+";")[0][0])
    return data_len

"""
Function returns name of file from database
"""
def get_name(table_name, id):
    db = database.MyBase()
    
    pic_name = db.receive("select fileName from "+str(table_name)+" where fileId="+str(id)+";")[0][0]

    return pic_name

"""
Function returns similar pictures from database
"""
def get_similar(parent_id, first_table, second_table, table_name):
    first_name = first_table
    second_name = second_table
    if first_name==second_name:
        if first_name == "ds1":
            second_name = "ds2"
        if first_name == "ds2":
            first_name = "ds1"
    
    first_table += "Names"
    second_table += "Names"

    db = database.MyBase()

   #get names of similar picures
    neighbors = db.receive(""+
    "select tab2.fileName from "+second_table+" as tab2 "+
    "inner join "+table_name+" as mid "+
    "on tab2.fileId==mid."+second_name+" "+
    "inner join "+first_table+" as tab1 on tab1.fileId==mid."+first_name+" "+
    "where tab1.fileId == "+str(parent_id))

    return neighbors
