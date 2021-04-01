import cv2
from   knn_algorithm import KNN
import numpy as np
"""
Function prepare single picture for keypoint search
it just change color to gray and resize to 300x300
for faster computation
we can also use madianblur and gaussionblur, but result are 
not that great, keypoints are not unique for picture
Parameters:
    img_name: str - image name

Result: 
    Image: resized with changed color
"""
def prepare_img(img_name):
    image = cv2.imread(img_name)
    image = image.astype('uint8')
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)#cv2.COLOR_BGR2GRAY)   
    #image = cv2.medianBlur(image, 5)
    #image = cv2.GaussianBlur(image, (5,5), 0)
    image = cv2.resize(image, (300, 300))

    return image

"""
This function finds and returns descriptors of picture
Parameters:
    image_path: path where image is stored
    vector_size:    number of descriptors to loads from picture
                    too much and too little can cause bad results
Returns:
    dst: vector of descriptors
"""
# Feature extractor
def extract_img_features(image_path, feature_name, vector_size=64):

    #getting image 
    image = prepare_img(image_path)
    
    try:
        #We can use Surf, Sift, Akaze, Kaze, Orb..
        #if we use orb, it returns binary vector, this application is not made for it
        #with binary data we would need different compare function, but it will work just fine with current one
        #alg = cv2.xfeatures2d.SIFT_create(300)
        if (feature_name == "kaze"):
            alg = cv2.KAZE_create()
        if (feature_name == "skaze"):
            alg = cv2.AKAZE_create()
        if (feature_name == "orb"):
            alg = cv2.ORB_create()
        if (feature_name == "brisk"):
            alg = cv2.BRISK_create()
        else:
            alg = cv2.BRISK_create()
        #Get image keypoints
        kps = alg.detect(image)
        
        #Sort keypoints and get just those, that are more importatnt than others
        #bigger response better
        kps.sort(key=lambda x: x.response, reverse=True)
        kps = kps[:vector_size]

        #store picture with keypoints
        #img = cv2.drawKeypoints(image, kps, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #cv2.imwrite("/home/omraidav/"+(image_path.split('/')[-1].lower()), img)

        #get keypoints and descriptors
        kps, dsc = alg.compute(image, kps)

        #extract_similar_descriptors(dsc, dsc)

        #compute without selecting keypoints
        ##ks, dsc = alg.detectAndCompute(image, None)

        """
        #old version
        #flattend array to make feature vector
        dsc = dsc.flatten()
        #To compare descriptors we need them to be the same size
        #We have vector_size keypoints, their length is 64 per one
        needed_size = (vector_size * 64)
        #This is true just if there were enough keypoins before
        #if that's not the case, we have to fill empty space with 0
        if dsc.size < needed_size:
            dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
        """
        
    except cv2.error as e:
        #if error occours, print it and return none
        print("Error: ", e)
        return None
    
    return np.asarray(dsc)

"""
Function comare two sets of descriptors set and returns just best 
of them, best matches
Parameters:
    first_set: first set of pictures
    second_set: second set of pictures
    k: number of nearest neighbours to return
"""
def knn_match_descriptors(first_set, second_set, k=2):
    matches = list()
    #matches = list()
    for i in first_set:
        knn_match = KNN(k, i)
        for j in second_set:
            knn_match.add(0, j)
        matches.append(knn_match.get_neighbors())
    return matches

"""
Function returns the most similar pictures from sets with similarity greater than sim_range
Parameters
    first_set: first set of pictures
    second_set: second set of pictures
    sim_range: similarity range
Return:
    number of similar descriptors
"""
def extract_similar_descriptors(first_set, second_set, sim_range = -1):
    #get best matches
    matches = knn_match_descriptors(first_set, second_set, 2)

    good = list()
    if (len(matches)>1):
        for f, s in matches:
            if f[1] < 0.75*s[1]:
                good.append(f[0])

                good_len = len(good)

                if sim_range != -1:
                    percent = (good_len*100)/len(second_set)
                    #uncomment to show similarity percent
                    #print(percent, "\% similarity")
                    if percent >= sim_range*100:
                        return True
    
    if sim_range == -1:
        return len(good)



"""
old version with serialization of descriptors, that was stored in database
def batch_extractor(images_path, tableName): # pickled_db_path="features.pck"
    print("here")
    db = database.MyBase("simijo.db")
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    idDB = 0
    result = {}
    for f in files:
        print("Extracting features from image %s" % f)
        name = f.split('/')[-1].lower()
        #load this to database!!!
        db.insert(tableName+"Data", idDB, srz.serialize(extract_img_features(f)))
        db.insert(tableName+"Names", name, idDB)
        idDB+=1
        #result[name] = extract_features(f)
    print(type(result))
    for key in result:
        print(key)
        print(result[key])
    db.commit()
    
    print(db.receive("SELECT * FROM ds1Names"))
    
    #return result
    # saving all our feature vectors in pickled file
    #with open(pickled_db_path, 'wb') as fp:
    #   pickle.dump(result, fp)

def extract_features(firstSet, secondSet):

    #batch_extractor(firstSet, "ds1")
    #batch_extractor(secondSet,"ds2")

    thread1 = threading.Thread(target=batch_extractor, args=(firstSet, "ds1",))
    thread2 = threading.Thread(target=batch_extractor, args=(secondSet, "ds2",))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

# Feature extractor
def extract_raw(img1, img2):

    image1 = prepare_img(img1)
    image2 = prepare_img(img2)

    try:        
        alg = cv2.xfeatures2d.SURF_create(400)

        k1 = alg.detect(image1)
        k2 = alg.detect(image2)
        
        k1.sort(key=lambda x: -x.response)
        k1= k1[:36]

        k2.sort(key=lambda x: -x.response)
        k2 = k2[:36]

        #kps = alg.detect(image)
        k1, d1 = alg.compute(image1, k1)
        k2, d2 = alg.compute(image2, k2)

        bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

        matches = bf.match(d1, d2)
        matches = sorted(matches, key=lambda x:x.distance)
        #print ("for img ", img1, " ", img2, " is ", len(matches))
        #img3 = cv2.drawMatches(image1, k1, image2, k2, matches, image2, flags=2)
        #cv2.imwrite("/home/omraidav/"+(img1.split('/')[-1].lower())+(img2.split('/')[-1].lower()), img3)

    except cv2.error as e:
        print("Error: ", e)
"""
