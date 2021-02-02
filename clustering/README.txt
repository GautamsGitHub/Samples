The python program clusterer generates a list of centroids such that the total distance from any point to its nearest centroid is minimised.

The data is from the 2018 word cup and was kindly provided by statsbomb.com.

The csv file contains pairs of times for the length of pass a player receives and gives. It was generated using JavaScript to get JSON files from Statsbomb's github then sieve the desired information on passes from them. Statsbomb's online data has been restructured so the JavaScript programs are undergoing repairs.

Using these centroids, we can see which players make which types of plays. For example, Olivier Giroud abnormally frequently receives long passes then makes a short one; this is seen in my analysis but is backed up by what we see while watching football suggesting my program works. This program could be useful to a team for example if they were looking to replace an injured key player.

The clustering algorithm uses k-means (I chose k to be 5 based on a combination of intuition and a graph of all of the points but this can be easily changed in the Python) clustering.

Five centroids contains the expected output (reformatted). The algorithm takes a long time.