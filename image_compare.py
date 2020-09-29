import sys
import os.path
from os import path
import functools
import csv
import traceback
from pprint import pprint
#check if csv file exists
#if csv exists then read csv file
#for each line check if the respective image 1 and image 2 files exist
#calcuate hash of both images in each line
#if hash matches then set evaluate to 0
#if hash does not match then use pythin image lib to comapre the images to evaluate the differences and capture the output for \
# both time delta in images

def getOSType():
    import platform
    my_platform = platform.system().upper()
    if my_platform == 'WINDOWS':
        print ("Running on Windows")
    elif my_platform == 'LINUX' :
        print("Running on Linux")
    elif my_platform == 'DARWIN':
        print("Running on Mac OS")
def getimagehash(image1path,image2path):
    from PIL import Image
    import imagehash
    
    myimghash1 = imagehash.dhash(Image.open(image1path,))
    myimghash2 = imagehash.dhash(Image.open(image2path))
    myhashdiff = myimghash1 - myimghash2
    return (myhashdiff)

#define file to write into 
def initializeOutfile(outcsvfile):
    import datetime
    import pathlib
    suffx_var = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    #open output file and insert the header into it
    if path.exists(outcsvfile):
        vfilebase = pathlib.Path(outcsvfile).stem
        os.rename(outcsvfile,vfilebase + "_"+suffx_var + '.csv')
    try:
        outputfile = open(outcsvfile , 'w')
      
    except PermissionError as permissionerr:
        print(permissionerr)
        print()
        print ("******************Premission Denied to create file in the specified output location******************")
        print ("******************Check permissions and retry******************")
        print()
        exc_type, exc_value, exc_tb = sys.exc_info()
        pprint(traceback.format_exception(exc_type,exc_value,exc_tb))
        exit(2)
    except IOError as ioerr:
        print(ioerr)
        print()
        
        exc_type, exc_value, exc_tb = sys.exc_info()
        pprint(traceback.format_exception(exc_type,exc_value,exc_tb))
        exit(2)
        

    else:
        writehandle = csv.writer(outputfile)
        writehandle.writerow(['Image1','Image2', 'Similar','Elapsed'])
        outputfile.close()  

#define files to read

#check if the csv with image paths exists
def checkArgs():
    import argparse
    
    
    parser = argparse.ArgumentParser(prog='image_compare',description="Use this to compare images")
    parser.version = "1.0"
    parser.add_argument('-i',action="store",dest='input_file',help="Input csv containig paths of images to compare", required=True)
    parser.add_argument('-o',action="store", dest="output_file",type=str,default='output.csv')
    parser.add_argument('-v',action="version",)
    my_arguments=parser.parse_args()
    csvtoread = my_arguments.input_file
    outcsvfile = my_arguments.output_file
    
    #if outcsvfile == None:
    #        outcsvfile = 'output.csv'
   
    initializeOutfile(outcsvfile)
    processCompare(csvtoread,outcsvfile)

def permissionErr():
    #print()
    print()
    print ("******************Check permissions and retry******************")
    print()
    exc_type, exc_value, exc_tb = sys.exc_info()
    pprint(traceback.format_exception(exc_type,exc_value,exc_tb))
def processCompare(csvtoread,outcsvfile):
    # Read the input file by line and run a loop for each line capturing paths of image1 and image2
    import timeit
    if path.exists(csvtoread):
        try:
            my_input_cvs=open(csvtoread, 'r')
            
        except PermissionError as permissionerr:
            permissionErr(permissionerr)
            
        else:
            with my_input_cvs:    
                csvcontent = csv.reader(my_input_cvs)
                next(csvcontent, None)  # skip the headers
                itr_var = 1
                for line in csvcontent:
                    itr_var = itr_var + 1 
                    img1 = line[1]
                    img2 = line[2]
                    #check if the paths defined for image1 and image2 exist on the filesystem
                    if path.exists(img1) and path.exists(img2):
                        #call the imagehash calculater function to calculate the hashdiff of image1 and image2
                        myhashdiff = getimagehash(img1, img2)
                        #calculate time taken to calculate each hash by above function
                        execCost = timeit.timeit(stmt=functools.partial(getimagehash, img1, img2), number=1)
                        try:
                            outputfile = open(outcsvfile , 'a')
                        except IOError as ioerr:
                            print(ioerr)
                            print()
                            exc_type, exc_value, exc_tb = sys.exc_info()
                            pprint(traceback.format_exception(exc_type,exc_value,exc_tb))
                            exit(2)
    
                        else:    
                            writehandle = csv.writer(outputfile)
                            writehandle.writerow([img1,img2,myhashdiff,execCost])
                            outputfile.close()
                    elif path.exists(img1) == False and path.exists(img2):
                        print (img1 + " not a valid path on row " + str(itr_var) )
                        print ("Skipping row " + str(itr_var))
                    elif path.exists(img1) and path.exists(img2) == False:
                        print (img2 + " not a valid path on row " + str(itr_var))
                        print ("Skipping row " + str(itr_var))

                    elif path.exists(img1) ==False and path.exists(img2) == False:
                        print (img2 + "and" + img2 + " not a valid path on row " + str(itr_var))
                        print ("Skipping row " + str(itr_var))
    else:
        print("Input CVS file " + csvtoread + 'does not exist.' )
        print("Please check path specified and try again")
                    



if __name__ == '__main__':
    checkArgs()
                 

