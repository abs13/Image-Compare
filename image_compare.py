import sys
import os
from os import path
import functools
import csv
import traceback
from pprint import pprint
import errno
import pathlib

def getOSType():
    '''
        function to check the platform that the utility is running on and prints it on system out
            parameters:
                
            returns:
                a (str) : The type of OS in upper case ( Linux, Mac OS, Windows)
    '''
    import platform 
    my_platform = platform.system().upper() #
    if my_platform == 'WINDOWS':
        print ("Running on Windows")
    elif my_platform == 'LINUX' :
        print("Running on Linux")
    elif my_platform == 'DARWIN':
        print("Running on Mac OS")
    return(my_platform)

def backuponRerun(outcsvfile,verbosity):
    '''
        Function to create backup of previosuly generated files before creating new file.

        Checks for write permissions for new file.

        If no filename is passed. Create a default name
        
            parameters:
                a (str): Path to output csv file.
                b (str): Verbosity TRUE or FALSE
            returns:
                : Nothing
    '''
    import datetime #import datetime. This will be used to create a backup of the output file in case older output dile exists.
    #import pathlib  #Import pathlib to handle paths and create backups of folders
    suffx_var = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") # Calculate the suffix to append to old output file. Format is YYYY_MM_DD_H_M_S
    #open output file and insert the header into it
    if path.exists(outcsvfile):
        print('deault output file specified or re-run detected. Creating a backup')
        vfilebase = pathlib.Path(outcsvfile).stem # capture the filename without extension. 
        print('re-naming ' + outcsvfile)
        try:
            os.rename(outcsvfile,vfilebase + "_"+suffx_var + '.csv') #regenerate the filename as <file_name>_<Date Suffic>.csv
            #check if can rename a file in the specified directory
        except PermissionError as permissionerr: # If permission denied, capture that and displat to user. Exit futher execution
            
            if verbosity is True:
                print(permissionerr)
                
                print ("******************Premission Denied to rename old file")
                print()
                print ("******************Check permissions and retry")
                exc_type, exc_value, exc_tb = sys.exc_info()
                pprint(traceback.format_exception(exc_type,exc_value,exc_tb))
                exit(2)
            else:
                print(permissionerr)
                print('run utility with --verbose for detailed error' )
        except IOError as ioerr: #If any other IO error  (e.g. DISK Full), Capture that , stop further execution and display the exception to user.
            if verbosity is True:
                print()
                exc_type, exc_value, exc_tb = sys.exc_info()
                pprint(traceback.format_exception(exc_type,exc_value,exc_tb))
        
            else:
                print(ioerr)
                print('run utility with --verbose for detailed error' )
        

def getimagehash(image1path,image2path):
    '''
        Function to compare images. 

        uses phash as the hashing method

            parameters:
                a (str) : path to image 1
                b (str) : path to image 2
      
            returns: 
                a (int): diff of the two image hashes
    '''
    from PIL import Image
    import imagehash 
    #print(imagehash.__doc__)   
    myimghash1 = imagehash.phash(Image.open(image1path,))
    
    myimghash2 = imagehash.phash(Image.open(image2path))
    myhashdiff = myimghash1 - myimghash2
   # print(myhashdiff)
    return (myhashdiff) #return the Hammer difference between the phash of two input images
#def cleanupEmpty():
#    print('dummy')

def main(): #Function to generate the menu for the utility
    '''
        Generate help menu and manage command line arguments. Calls output file initialization and compare process functions

            -h (optional) displays the usage 

            -v (optional) displays the function

            -o (optional) capture the output filenname with path.

            -i (required) captures the input csv filename with path

                paramater: 
                    : Nothing
                returns: 
                    : Nothing
    '''
    import argparse
    #sys.tracebacklimit = 0
    parser = argparse.ArgumentParser(prog='image_compare',description="Use this to compare images") #initate the parser
    parser.version = "1.0" # Set version as 1.0. this can be displayed using the -v optional paramater
    parser.add_argument('-i',action="store",dest='input_file',help="Input csv containig paths of images to compare", required=True) #define a required param, to capture the input csv file
    parser.add_argument('-o',action="store", dest="output_file",type=str,default='dflt_val') #define an option parameter for output file
    parser.add_argument('--verbose',action="store_true") #define a version param

    parser.add_argument('-v',action="version",) #define a version param
    my_arguments=parser.parse_args()
    csvtoread = my_arguments.input_file
    outcsvfile = my_arguments.output_file
    if outcsvfile == 'dflt_val':
        outcsvfile = (pathlib.Path(csvtoread).stem + "_results.csv")
        
    verbosity = my_arguments.verbose 
   
    backuponRerun(outcsvfile,verbosity) #call the fuction to initialize the output file. the called function only adds a header here
    processCompare(csvtoread,outcsvfile,verbosity) #Call the function to compare the file sets based on the paths provided in input csv file
def processCompare(csvtoread,outcsvfile,verbosity):
    ''' 
        Takes two inputs, the input and output csv files. Loops over all lines in input csv and processes hash diffs.

        Calls the hash calculation function after making sure all I/O operations( permission and DISK space etc) are possible

            parameters:
                a (str) :  path to input csv
                b (str) :  path to output csv
            returns:
                    : nothing
    '''
    import timeit
    my_platform = getOSType() # get the OS type

    try:
        outputfile = open(outcsvfile , 'a') # check if output file can be opened for inserting new records ( in append mode )
        headernames = ['Image1','Image2','Similar','Elapsed']
        writehandle = csv.DictWriter(outputfile,fieldnames=headernames)
        writehandle.writeheader()
    
    except PermissionError as permissionerr:
        
        if verbosity is True :
            print(permissionerr)
            exc_type, exc_value, exc_tb = sys.exc_info()
            pprint(traceback.format_exception(exc_type,exc_value,exc_tb))
        else:
            print ('******************Check permissions and retry******************')
            print()
            print(permissionerr)
    except IOError as ioerr: #capture any IO excpetions e.g. DISK FULL
        if verbosity is True :
            print(ioerr) 
            print()
            exc_type, exc_value, exc_tb = sys.exc_info()
            pprint(traceback.format_exception(exc_type,exc_value,exc_tb))
        else:
            print('I/O Erro')
            print('run utility with --verbose')
        exit(2)
    else:
        
        
        if path.isfile(csvtoread) and path.getsize(csvtoread) > 0 : #check if the input file provided by users exists and is a file
            try:
                my_input_cvs=open(csvtoread, 'r')
            
            except PermissionError as permissionerr: #capture any permission errors in case user does not have permissions to read the file
                if verbosity is True :
                    print(permissionerr)
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    pprint(traceback.format_exception(exc_type,exc_value,exc_tb))
                else:
                    print(permissionerr)
                    print ("******************Check permissions and retry******************")
                    print()
                
            
            else:
             
                with my_input_cvs: #If no errors raised, continue processing the file
                    csvcontent = csv.reader(my_input_cvs) # read each line from file
                    next(csvcontent, None)  # skip the headers in the input csv file
                    itr_var = 1 #initialize a counter. this will be used to display the row number in case processing failes for any of the rows i csv file
                    for line in csvcontent: 
                        if not line : #if the line is empty, do nothing and moved to next
                            continue
                        else: #else continue processing
                            itr_var = itr_var + 1  
                            img1 = line[0] #get the path for first image file (marked for comparison in the input cvs)
                            
                            img2 = line[1] #get path for the second image file ( marked for comparison in the input cvs)
                            
                        
                        #check if the paths defined for image1 and image2 exist on the filesystem
                            if path.isfile(img1) and path.isfile(img2):
                                #call the imagehash calculater function to calculate the hashdiff of image1 and image2
                                myhashdiff = getimagehash(img1, img2)
                                #calculate time taken to calculate each hash by above function
                                execCost = timeit.timeit(stmt=functools.partial(getimagehash, img1, img2), number=100)
                                writehandle.writerow({'Image1': img1,'Image2': img2,'Similar': myhashdiff,'Elapsed': execCost})
                               
                            elif path.isfile(img1) == False and path.isfile(img2): # check for both images if the path defined exists.
                                print (img1 + " not a valid path on row " + str(itr_var) ) 
                                print ("Skipping row " + str(itr_var))

                            elif path.isfile(img1) and path.isfile(img2) == False:
                                print (img2 + " not a valid path on row " + str(itr_var))
                                print ("Skipping row " + str(itr_var))

                            elif path.isfile(img1) ==False and path.isfile(img2) == False:
                                print (img1 + " and " + img2 + " not a valid path on row " + str(itr_var))
                                print ("Skipping row " + str(itr_var))
            finally:
                outputfile.close()
                #cleanupEmpty()
        elif path.isfile(csvtoread) and path.getsize(csvtoread) == 0:
            raise Exception('Input csv empty. Exiting....')
            exit()
        
        elif path.isfile(csvtoread) is False:
            raise FileNotFoundError (errno.ENOENT, os.strerror(errno.ENOENT), csvtoread)
            print("Input CVS file " + csvtoread + ' does not exist.' ) # If input csv path does not exist, inform the user.
            print("Please check path specified and try again")
            exit(2)
if __name__ == '__main__':
    
    main() #Call the main function
                 

