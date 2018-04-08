import glob
import json
import cv2
import ntpath
import os

import features

IMAGE_PATH = "./images"
path_index = "./index/"
LENGTH = 200

def Convert(path):
    image = cv2.imread(path)
    height, width, depth = image.shape
    image_ratio = float(height)/float(width)
    print (height, width, image_ratio)
    if height > width:
        image = cv2.resize(image, (LENGTH, int(LENGTH*image_ratio))) 
        h = int(LENGTH*image_ratio); 
        margin = int(float(h-LENGTH)/float(2)) 
        image = image[margin:(LENGTH + margin), 0:LENGTH]
    else:
        image = cv2.resize(image, (int(LENGTH/image_ratio), LENGTH))
     
        w = int(LENGTH/image_ratio); 
        margin = int(float(w-LENGTH)/float(2)) 
        image = image[0:LENGTH, margin:(LENGTH+margin)] 
    
    cv2.imwrite(path_index + ntpath.basename(path), image)
    return image

def List_Of_Files():
    included_extenstions = ['jpg','bmp','png','gif' ] ;
    return [fn for fn in os.listdir(IMAGE_PATH) if any([fn.endswith(ext) for ext in included_extenstions])];

def main():
    index = []
    if not os.path.exists(path_index):
        os.makedirs(path_index)
    files = glob.glob(IMAGE_PATH + "/" + "*.jpg")
    
    access = {}
    
    for file in files:
        print ("File Processing: " + file)
        image = Convert(file)
        access = features.extractFeature(image)
        access["file"] = ntpath.basename(file)
        index.append(access)

    with open(path_index + "histogram.index", 'w') as outfile:
        json.dump(index, outfile, indent=4)
        
    print ("Written to: " + path_index + "histogram.index")

if __name__ == "__main__":
    main()