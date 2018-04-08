import json
import numpy
import cv2
import math
import argparse
import sys
import features
import random
from collections import deque

path_index = "./index/"
Number_of_images = 5

def readIndex():
    json_data = open(path_index + "histogram.index").read()
    return json.loads(json_data)

def CreateImage(path, number_of_tiles):
    i = cv2.imread(path)
    (h, w, _) = i.shape
    i = cv2.resize(i, (int(w / number_of_tiles * number_of_tiles), int(h / number_of_tiles * number_of_tiles)))
    return i

def startpatching(path, number_of_tiles):
    image = cv2.imread(path_index + path)
    image = cv2.resize(image, (number_of_tiles, number_of_tiles))
    return image

def calcDistance(fts1, fts2, vectors):
    distance = 0
    for vec in vectors:
        distance += math.pow(fts1[vec] - fts2[vec], 2)
    return math.sqrt(distance)

def importImage_index(fts, index, vectors):
    minDistance = sys.maxsize
    bestImages = deque([])
    for item in index:
        distance = calcDistance(fts, item, vectors)
        if distance < minDistance:
            minDistance = distance
            bestImages.append(item["file"])
            if len(bestImages) > Number_of_images:
                bestImages.popleft();

    return random.choice(bestImages)

def CalcLine(i, w, index, inputImage, number_of_tiles, channels):
    for j in range(0, w // number_of_tiles):
        roi = inputImage[i * number_of_tiles:(i + 1) * number_of_tiles, j * number_of_tiles:(j + 1) * number_of_tiles]
        fts = features.extractFeature(roi)
        patcher = startpatching(importImage_index(fts, index, channels), number_of_tiles)
        inputImage[i * number_of_tiles:(i + 1) * number_of_tiles, j * number_of_tiles:(j + 1) * number_of_tiles] = patcher
        cv2.imshow("Progress", inputImage)
        cv2.waitKey(1)

def main():
    
    if len(sys.argv) < 5:
        print ("Not enough arguments or is invalid!")
        print ("Call with " + sys.argv[0] + " input.jpg [tile-size] [rgb|hsv] output.jpg")
        sys.exit(1)
        

    Image_path = str(sys.argv[1])
    number_of_tiles = int(sys.argv[2])
    channels = list(str(sys.argv[3]))
    index = readIndex()
    inputImage = CreateImage(Image_path, number_of_tiles)
        
    (h, w, _) = inputImage.shape
     
    inputImage = cv2.resize(inputImage, (int(w / number_of_tiles * number_of_tiles), int(h / number_of_tiles * number_of_tiles)))
    print (inputImage.shape)
    
	
    for i in range(0, h // number_of_tiles):
        CalcLine(i, w, index, inputImage, number_of_tiles, channels)
        
    print ("Done Processing")
     
    
    cv2.imwrite(str(sys.argv[4]), inputImage)
     
     
if __name__ == "__main__":
	main()