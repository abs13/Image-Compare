# Testing strategy:
    The following test scenarios were executed
## File handling and I/O:
- Input file empty
- Permission denied on output file creation
- Input file not readable
  
## Image comparison
- Specified image file(s) not found
- Same files compared [Same](./tests/results/same_out.csv)
- Same files but different extensions compared [diff extensions](./tests/results/same_out.csv)
- Same file in color & monochrome [color & monochrome](./tests/results/color_bw_out.csv)
- File compared with same file rotated 90 degrees [flipped](./tests/results/rotated_out.csv)
- File compared with a 20 points increase in highlights [blown h/l](./tests/results/highlights_results.csv)
- Files compared with 20 points decrease in shodows [crushed shadows](./tests/results/shadows_results.csv)
- File compared with a cropped version of file [cropped](./tests/results/cropped_results.csv)
  