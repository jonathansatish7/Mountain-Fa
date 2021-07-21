#!/usr/local/bin/python3
#
# Authors: bkmaturi-josatiru-sgaraga
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, April 2021
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
import numpy

# calculate "Edge strength map" of an image
#
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image


# main program
#
gt_row = -1
gt_col = -1
if len(sys.argv) == 2:
    input_filename = sys.argv[1]
elif len(sys.argv) == 4:
    (input_filename, gt_row, gt_col) = sys.argv[1:]
else:
    raise Exception("Program requires either 1 or 3 parameters")

# load in image 
input_image = Image.open(input_filename)

# compute edge strength mask
edge_strength = edge_strength(input_image)
#edge_strength1 = edge_strength.T
imageio.imwrite('edges.jpg', uint8(255 * edge_strength / (amax(edge_strength))))
b_w_edge = uint8(255 * edge_strength / (amax(edge_strength)))
# You'll need to add code here to figure out the results! For now,
# just create a horizontal centered line.
def simple(edge_matrix):
    return [argmax(i) for i in edge_matrix]


def viterbi_path(edge_matrix):
    R = len(edge_matrix)
    C = len(edge_matrix[0])
    
    tran_prob_matrix = [edge_matrix[0]]
    final_index = [0] * R
    for i in range(1, R):
        tmp = []
        for j in range(C):
            if j == 0:
                tmp.append(edge_matrix[i][j] + max(tran_prob_matrix[i - 1][j], tran_prob_matrix[i - 1][j + 1]))
            elif j == C - 1:
                tmp.append(edge_matrix[i][j] + max(tran_prob_matrix[i - 1][j], tran_prob_matrix[i - 1][j - 1]))
            else:
                tmp.append(edge_matrix[i][j] + max(tran_prob_matrix[i - 1][j - 1], tran_prob_matrix[i - 1][j], tran_prob_matrix[i - 1][j + 1]))
        tran_prob_matrix.append(tmp)

    
    final_index[R - 1] = numpy.argmax(tran_prob_matrix[R - 1])
    for i in range(R - 2, -1, -1):
        j = final_index[i + 1]
        if j == 0:
            final_index[i] = numpy.argmax(tran_prob_matrix[i][j:j + 2]) + j
        elif j == C - 1:
            final_index[i] = numpy.argmax(tran_prob_matrix[i][j - 1:j + 1]) + j - 1
        else:
            final_index[i] = numpy.argmax(tran_prob_matrix[i][j - 1:j + 2]) + j - 1
    return final_index



def user_input(edge_matrix,row,col):
    rows = len(edge_matrix)
    cols = len(edge_matrix[0])
    out = [0]*cols
    out[col] = row
    if col == 0:
        for i in range(0,cols-1):            
            b = [edge_matrix[row-1][i+1],edge_matrix[row][i+1],edge_matrix[row+1][i-1],]
            out[i+1] = b.index(max(b))+row-1
            row = out[i+1]
    elif col == cols-1:
        for i in range(cols-1,-1,-1):
            b = [edge_matrix[row-1][i-1],edge_matrix[row][i-1],edge_matrix[row+1][i-1],]
            out[i-1] = b.index(max(b))+row-1
            row = out[i-1]
    else:
        for i in range(col,cols-1): 
            b1 = [edge_matrix[row-1][i+1],edge_matrix[row][i+1],edge_matrix[row+1][i-1],]
            out[i+1] = b1.index(max(b1))+row-1
            row = out[i+1]
        for i in range(col,-1,-1):
            b2 = [edge_matrix[row-1][i-1],edge_matrix[row][i-1],edge_matrix[row+1][i-1],]
            out[i-1] = b2.index(max(b2))+row-1
            row = out[i-1]
    return out
simple_ind = simple(edge_strength.T)
input_image = draw_edge(input_image, simple_ind, (255, 0, 0), 5)
vit_ind = viterbi_path(edge_strength.T)
# for i in range(len(edge_strength.T)):
#     if viterbi_1[i] != argmax(edge_strength.T[i]):
#         viterbi_1[i] = argmax(edge_strength.T[i])
#ridge = [ edge_strength.shape[0]/2] * edge_strength.shape[1]
input_image = draw_edge(input_image, vit_ind, (0, 0, 255), 5)
list_edge_s = [list(i) for i in b_w_edge]
human_ind = user_input(list_edge_s,int(gt_row),int(gt_col))

# output answer
imageio.imwrite("output.jpg", draw_edge(input_image, human_ind, (0, 255, 0), 5))
