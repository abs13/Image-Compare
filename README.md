# Image-Compare

Image compare is a python script that reads an input csv file and can compare two images provided on each row. 
The utility uses [imagehash](https://pypi.org/project/ImageHash/) module for core image comparison.
The algorithm used was [p-hash](https://www.phash.org/docs/howto.html) or perceptual hash.
A perceptual hash of two images is calculated followed by finding the [hamming distance](https://en.wikipedia.org/wiki/Hamming_distance) between these hashes.

## Walkthrough 
- On running the script, the program/utility captures the arguments passed to the script
  - -h (optional) displays the usage
  - -v (optional) displays the function
  - -o (optional) capture the output filename with path.
  - -i (required) captures the input csv filename with path
  - -i represent the input file absolute path and is mandator
      - if no input is provides, the code throws an error and displays usage
      - if no output file is provides, default output filename, same as *input-file*_results.csv is assigned
- The main() function then calls backuponRerun()
- The backuponRerun() function, examines the input file and if a file with *input-file*_results.csv exists, renames it to *input-file*_results_*YYYY_DD_MM_H_M_S*.csv
- The backuponRerun() then passed control back to main()
- The function main() then calls processCompare()
-  processCompare() takes three inputs.
      -  Input file
      -  Output file
      -  Verbosity (how descriptive the output for thrown exceptions should be)
- processcompare() calls a function getOSType() to display what Operating system the program is being executed on
- It checks if output file can be appended to. If not, an appropriate exception is raised. 
- If no exceptions are thrown while opening output file for insertion of records, the code checks if the input file exists and is not empty
    - If input file exists and is empty, exception is raised that the input file is empty and execution halted
    - If the input file does not exist, exception is thrown that the file does not exist and execution halted
    - If the input file exists and is not empty, the input file is read line by line in a loop.
    - For each iteration, the two images are passed to a function getimagehash()
    - getimagehash() will calculate a perceptual hash of each image and then calculate the [*hamming distance*](https://en.wikipedia.org/wiki/Hamming_distance)
    - The call to hamming distance is wrapped inside timeit() to calculate the execution cost of each image set
    - The hamming distacne is executed with a run_number of 100 to get the average execution cost.
    - This calculated hamming distance and the execution cost are then passed back to processcompare()
- processcompare() then appends the list [*imagefile1*,*imagefile2*,*hamming* distance, *avg cost of execution*] to the output file
- The process is repeated for each line in the csv file
- Once processing of the input file is complete, the output file is closed and control returned to command prompt.
  
## Testing scenarios and test data
Details about testing scenarios can be found [here](./Test%20Strategy.md)
##### The 'tests' folder
The tests folder contains:
-  Test images
-  Test csv files
-  results for each scenario

## How-To Guide:
Available at [How To Guide](./Howto.md)

## Developer Documentation
Available at [documentation](https://htmlpreview.github.io/?https://github.com/abs13/Image-Compare/blob/master/html/image_compare.html)

## Contributing

## License
