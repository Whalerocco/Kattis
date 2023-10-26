import sys
import math as math

converge_limit = 1e-9

def main():
    input = sys.stdin.readline
    temp1 = input() 
    temp2 = temp1.split()
    nrVertices = int(temp2[0]) # second element of first line says how many more lines there are
    nrEdges = int(temp2[1])
    adj_list = {}
        
    for _ in range(nrEdges):
        line = input()
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
    
    # Init the hitting matrix - how long time expected between two vertices - will converge
    H = [[float('inf' if i != j else 0) for j in range(nrVertices)] for i in range(nrVertices)]

    # Init the transition probability matrix - what probability of going from on vertex to another - constant
    P = [[float(0) for j in range(nrVertices)] for i in range(nrVertices)]

    # loop through each vertex
    for v in range(nrVertices):
        for neighbor in adj_list[v]: # adj_list[v] are the neighbors of v
            H[v][neighbor] = 1 # 1 minute to reach neighbor clearing
            P[v][neighbor] = 1/len(adj_list[v]) # probability to go from vertex v to neighbor is 1/deg(v) where deg(v) = amount of neighbors of v (for uniform random walk)
    
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
                        PH = (P[i][k] * H_prev[k][j])
                        if math.isinf(PH):
                            PH = 9999
                        sumPH = sumPH + PH
                    H[i][j] = 1 + sumPH

        n += 1
        if n >= 1000000:
            nr = H[0][nrVertices-1]
            if math.isinf(nr):
                if n >= 1000010:
                    is_H_converged = True
            else:
                is_H_converged = True 
        
        max_change = abs(H[0][nrVertices-1]-H_prev[0][nrVertices-1])
        if max_change < converge_limit:
            is_H_converged = True

    print(H[0][nrVertices-1])

if __name__ == '__main__':
    main()