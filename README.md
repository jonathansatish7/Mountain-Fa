# Mountain-Finding

## Probelm Formulation
* The problem here is to write the algorithm to detect the ridge line(mountain detection) using the input image given to us. 

* Here, we used simple(Naive-Bayes) approach, HMM (took reference of seam carving in image processing), human feedback where user gives particular pixel index 
which will definitely be on ridge line. 

* the key idea we have used is to use concept of seam carving in find the transition probability values and how probable the next pixel selected is on mountain ridge line. 
(The code for this transition probability is referenced from my Applied Algorithm course work where we learned the concept of seam carving) 

We have used dynamic programming to find the maximum probable pixel index and found the total pixel values for different possible paths.
After finding all possible paths, we selected the path which has maximum and is continuous path. We then backtracked this path to get the index values of this path. 
These index values are passed to drawedge function(given to us) to get the output image.

## Our Algorithm Description
* In simple method, we have transposed the pixel matrix, and found the maximum pixel value in each column. We store these index values in a list and is given as input to draw edge function
to get the output image. 

* In Viterbi menthod, we used concept of seam carving to find the transition probabilities and dynamic programming to backtrack the best path found. 
Here, we have transposed the edge strength matrix and passed to viterbi function as input. After finding the sum of pixel values for all possible paths, we took the path which has the maximum value.
An then, we used dynamic programming to backtrack the index values of that path and stored in a list. We passed this list as input to draw_edge function to get the output image.

*In human feedback method, we considered the neighbourhood values (nearest pixel values) based on the row,col values given by user. 
If the col value given is not starting or end column, we divided the problem into parts (left to col and roight to col). Then we find neighbours for both the parts and stored the best probable index value in output list.  
Here, we thought of another way where we can make the pixel value at the given index to maximum and then apply same function(viterbi) used in part-2 of this problem. 
If we do that, we are getting fluctuated output and we feel considering neighbours gives us better output. 

## Assumptions, Difficulties.
* We have transposed the edge_strength matrix and also converted numpy array to 2D list for part-3 of this question.
* We have faced dificulties while finding the transition probabilities and also while workimg with numpy arrys. 
* Used the grey scale matrix of an image while parsing input to function
* We used human feedback indexes(ROW,COL) as below to get the output images we attached:
Mountain-1 -> (74,77),
Mountain-2 -> (56,152),
Mountain-3 -> (43,160),
Mountain-4 -> (55,141),
Mountain-5 -> (59,93),
Mountain-6 -> (72,95),
Mountain-7 -> (20,83),
Mountain-8 -> (64,125),
Mountain-9 -> (70,169).
