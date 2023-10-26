import sys
import time
import math as math

converge_limit = 1e-7

def main():
    input = sys.stdin.readline
    start_time = time.time()
    temp1 = input() 
    temp2 = temp1.split()
    nrVertices = int(temp2[0]) # second element of first line says how many more lines there are
    nrEdges = int(temp2[1])
    print("nrVertices: ", nrVertices)
    print("nrEdges: ", nrEdges)
    adj_list = {}
        
    for _ in range(nrEdges):
        line = input()
        print("Line read: ", line[:-1])
        data = line.split()

        # There's a path from n to m
        n = int(data[0]) 
        m = int(data[1]) 
        # Add path to m in n's adj list
        if n not in adj_list:
            adj_list[n] = []
        adj_list[n].append(m)
        # Add path to n in m's adj list
        if m not in adj_list:
            adj_list[m] = []
        adj_list[m].append(n)
    
    print("\nAdjacency list")
    print(adj_list)
    print("Exit node = ", nrVertices-1)

    # Init the hitting matrix - how long time expected between two vertices - will converge
    H = [[float('inf' if i != j else 0) for j in range(nrVertices)] for i in range(nrVertices)]

    # Init the transition probability matrix - what probability of going from on vertex to another - constant
    P = [[float(0) for j in range(nrVertices)] for i in range(nrVertices)]

    print("\nH init: ")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in H]))
    print("\nP init")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in P]))

    # loop through each vertex
    for v in range(nrVertices):
        for neighbor in adj_list[v]: # adj_list[v] are the neighbors of v
            H[v][neighbor] = 1 # 1 minute to reach neighbor clearing
            P[v][neighbor] = 1/len(adj_list[v]) # probability to go from vertex v to neighbor is 1/deg(v) where deg(v) = amount of neighbors of v (for uniform random walk)
    
    ## REMOVE
    # for c in range(nrVertices):
    #     if c != nrVertices-1:
    #         P[nrVertices-1][c] = 0
    #     else:
    #         P[nrVertices-1][c] = 1
    ## END REMOVE

    print("\nH init2: ")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in H]))
    print("\nP init2")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in P]))

    
    is_H_converged = False
    n = 0
    while not is_H_converged:
        H_prev = [row[:] for row in H]

        # For each vertex
        for i in range(nrVertices):
            # Compare it to all other vertices
            for j in range(nrVertices):
                # Except for itself
                if i != j:
                    sumPH = 0
                    for k in adj_list[i]: # k are the neighbors of i
                        # if k != j: #?????
                        PH = (P[i][k] * H_prev[k][j])
                        if math.isinf(PH):
                            PH = 0
                            print("Set inf to 0")
                        sumPH = sumPH + PH
                        # sumPH = sumPH + H_prev[k][j]/len(adj_list[i])
                    H[i][j] = 1 + sumPH

        print("\nH3: ")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in H]))

        #H_diff = H-H_prev
        #print("H_diff")
        #print(H_diff)
        n += 1
        if n >= 200:
            nr = H[0][nrVertices-1]
            if math.isinf(nr):
                print("Postponing converge")
                if n >= 210:
                    is_H_converged = True
                    print("Inf answer, didn't converge")
            else:
                is_H_converged = True # REMOVE____change to some criteria
        
        # max_change = max(abs(H[i][j]-H_prev[i][j]) for i in range(nrVertices) for j in range(nrVertices))
        max_change = abs(H[0][nrVertices-1]-H_prev[0][nrVertices-1])
        if max_change < converge_limit:
            is_H_converged = True
            print("\nConverged at iteration ", n)

    print("\nTime to go from 0 to ", (nrVertices-1))
    print(H[0][nrVertices-1])

if __name__ == '__main__':
    main()