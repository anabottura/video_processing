from process_utils import *

# Edit file directory and filename to point to video to be cut

filedir = "/Users/anacarolinabotturabarros/University of Glasgow/kohl-lab - PG MSc Project 20-21/Data for Sophie/coho0003_favpc1_AB/precond/"
filename = "deval_precond2017-10-14T09_30_46.avi"

f_rate = 10.0

# specify the number of boxes in each axis in the grid
box_y = 2
box_x = 2

# Adjust after running test_cut to properly get only boxes videos
ystart = 250
yend = 972
xstart = 285
xend = 1245

# Run to cut off non video bits
# test_cut(filedir, filename, [xstart,xend], [ystart,yend])

# This finds the dimensions of each box depending on variables above
boxes = boxes_locations([box_x, box_y], [xstart, xend], [ystart, yend])
print(boxes)

# Use this to split the video into videos of individual boxes
split_box_videos(filedir, filename, boxes)

# # I think this is to trim video if needed??
# print(trim_video(filedir, filename))
