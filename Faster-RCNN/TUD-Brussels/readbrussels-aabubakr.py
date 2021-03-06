import os
import re


noann_regex = re.compile('"(.+)"[;.]')
name_regex = re.compile('"(.+)":')
tud_regex = re.compile('(\d+),\s+(\d+),\s+(\d+),\s+(\d+)')

def readidl(images_folder, idlfilename):
    """
    Returns a list of tuples. The first element of a tuple is the full path of the image. The second element of the tuple is 0, if there are no people in the image. If there are people in the image, then the second element of the tuple is a list of tuples. Each tuple is of length 4 (Xmin, Ymin, Xmax, Ymax). So, number of elements in the list would be equal to the number of people annotated in the image.
    """
    fid = open(idlfilename, 'r')
    output = []
    for line in fid:
        line = line.strip()
        if re.match(noann_regex, line):
            name = list(map(str, re.findall(noann_regex, line)))[0]
            #fname = os.path.join(images_folder, name)
            output.append((name, 0))
        else:
            #name = list(map(str, re.findall(name_regex, line)))[0]
            name = list(map(str, re.findall(name_regex, line)))[0]
            #fname = os.path.join(images_folder, name)
            annotations = re.findall(tud_regex, line)
            annotations = list(map(lambda x: tuple(map(int, list(x))), annotations))
            #annotations = list(map(lambda x: tuple(map(int, list(x))), annotations))
            output.append((name, annotations))
    return output

def get_data(images_folder, idlfile):
    return readidl(images_folder, idlfile)


if __name__ == "__main__":
    # The following is for positive images in training set
    motionpairs_pos = get_data("/data/stars/user/aabubakr/pd_datasets/datasets/TUD-Brussels/TUD-MotionPairs/positive", "/data/stars/user/aabubakr/pd_datasets/datasets/TUD-Brussels/TUD-MotionPairs/positive/train-pos.idl")
    #print(motionpairs_pos)

    # The following is for negative images in training set
    motionpairs_neg = get_data("/data/stars/user/aabubakr/pd_datasets/datasets/TUD-Brussels/TUD-MotionPairs/negative", "/data/stars/user/aabubakr/pd_datasets/datasets/TUD-Brussels/TUD-MotionPairs/negative/train-neg.idl")
 
    # The following is for additional negative images in training set
    motionpairs_additional = get_data("/data/stars/user/aabubakr/pd_datasets/datasets/TUD-Brussels/TUD-MotionPairs/additional-negative-bootstrap", "/data/stars/user/aabubakr/pd_datasets/datasets/TUD-Brussels/TUD-MotionPairs/additional-negative-bootstrap/train-neg-additional.idl")

    # The following is for the testing set
    tudbrussels = get_data("/data/stars/user/aabubakr/pd_datasets/datasets/TUD-Brussels/TUD-Brussels", "/data/stars/user/aabubakr/pd_datasets/datasets/TUD-Brussels/TUD-Brussels/annotation.idl")
    
    # save to file
    #f = open("/data/stars/user/aabubakr/pd_datasets/datasets/TUD-Brussels/TUD-MotionPairs/positive/train-pos-anno.idl", 'w')
    
    for row in motionpairs_pos:
        #f = open("/data/stars/user/aabubakr/pd_datasets/datasets/TUD-Brussels/TUD-MotionPairs/positive/train-pos-anno.idl", 'w')
        #f.write(str(row)+ '\n')
        #print(row)
        file_name = row[0]

        print(file_name)
        annot_folder = "/data/stars/user/aabubakr/pd_datasets/datasets/TUD-Brussels/TUD-MotionPairs/positive/annotations"
        if not os.path.exists(annot_folder):
               os.makedirs(annot_folder)

        fname = os.path.join(annot_folder, os.path.basename(file_name) + str(".txt") )
        f = open(fname, 'w')
        annot = row[1] # list of tuples
        if annot !=0:
            for annotelems in annot: # annotelems is tuple of (Xmin, Ymin, Xmax, Ymax)
                Xmin = annotelems[0]
                Ymin = annotelems[1]
                Xmax = annotelems[2]
                Ymax = annotelems[3]
                f.write(str(Xmin) + " " + str(Ymin) + " " + str(Xmax) + " " + str(Ymax) + '\n' )
            f.close()


    for row in motionpairs_neg:
        
        file_name = row[0]

        print(file_name)
        annot_folder = "/data/stars/user/aabubakr/pd_datasets/datasets/TUD-Brussels/TUD-MotionPairs/negative/annotations"
        if not os.path.exists(annot_folder):
               os.makedirs(annot_folder)

        fname = os.path.join(annot_folder, os.path.basename(file_name) + str(".txt") )
        f = open(fname, 'w')
        annot = row[1] # list of tuples
        if annot !=0:
            for annotelems in annot: # annotelems is tuple of (Xmin, Ymin, Xmax, Ymax)
                Xmin = annotelems[0]
                Ymin = annotelems[1]
                Xmax = annotelems[2]
                Ymax = annotelems[3]
                f.write(str(Xmin) + " " + str(Ymin) + " " + str(Xmax) + " " + str(Ymax) + '\n' )
            f.close()

    
    for row in motionpairs_additional:

        file_name = row[0]

        print(file_name)
        annot_folder = "/data/stars/user/aabubakr/pd_datasets/datasets/TUD-Brussels/TUD-MotionPairs/additional-negative-bootstrap/annotations"
        if not os.path.exists(annot_folder):
               os.makedirs(annot_folder)

        fname = os.path.join(annot_folder, os.path.basename(file_name) + str(".txt") )
        f = open(fname, 'w')
        annot = row[1] # list of tuples
        if annot !=0:
            for annotelems in annot: # annotelems is tuple of (Xmin, Ymin, Xmax, Ymax)
                Xmin = annotelems[0]
                Ymin = annotelems[1]
                Xmax = annotelems[2]
                Ymax = annotelems[3]
                f.write(str(Xmin) + " " + str(Ymin) + " " + str(Xmax) + " " + str(Ymax) + '\n' )
            f.close()


    for row in tudbrussels:

        file_name = row[0]

        print(file_name)
        annot_folder = "/data/stars/user/aabubakr/pd_datasets/datasets/TUD-Brussels/TUD-Brussels/annotations"
        if not os.path.exists(annot_folder):
               os.makedirs(annot_folder)

        fname = os.path.join(annot_folder, os.path.basename(file_name) + str(".txt") )
        f = open(fname, 'w')
        annot = row[1] # list of tuples
        if annot !=0:
            for annotelems in annot: # annotelems is tuple of (Xmin, Ymin, Xmax, Ymax)
                Xmin = annotelems[0]
                Ymin = annotelems[1]
                Xmax = annotelems[2]
                Ymax = annotelems[3]
                f.write(str(Xmin) + " " + str(Ymin) + " " + str(Xmax) + " " + str(Ymax) + '\n' )
            f.close()


