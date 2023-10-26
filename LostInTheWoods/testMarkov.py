from numpy import *

hit_idx = (0, 3)

# Define a graph by edge list
edges = [[0,1],[1,3],[3,0],[0,2]]

# Create adj. matrix
A = zeros((4,4))
# print(zip(*edges))
# A[zip(*edges)] = 1

for i in range(len(edges)):
        # There's a path from n to m
        n = int(edges[i][0]) 
        m = int(edges[i][1]) 

        # Add path to m in n's adj list
        A[n][m] = 1
        A[m][n] = 1

# Undirected condition
A += A.T

# Make the final state an absorbing condition
A[hit_idx[1],:] = 0
A[hit_idx[1],hit_idx[1]] = 1

# Make a proper Markov matrix by row normalizing
A = (A.T/A.sum(axis=1)).T
print("A")
print(A)
B = A.copy()

Z = []
for n in range(100):
    Z.append( B[hit_idx] )
    B = dot(B,A)
print("B")
print(B)

from pylab import *
plot(Z)
xlabel("steps")
ylabel("hit probability")
show()    