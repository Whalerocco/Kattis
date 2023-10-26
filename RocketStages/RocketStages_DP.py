import sys
import time 

g = 9.8
maxWeight = 10000

def calcVelocity(m_dry,L,T,C):
    if m_dry > 0:
        # m_dry is total mass of rest of rocket + current stage (without fuel weight of current stage)
        m_tot = m_dry + L
        F_start = (T/(m_tot)) - g
        F_end = (T/(m_dry)) - g
        a_mean = 0.5*(F_start+F_end)
        t_comb = L/C
        dV = a_mean*t_comb
    return dV 

def main():
    start_time = time.time()
    input = sys.stdin.readline
    nrStages = int(input()) # first line says how many more lines there are
    print("number of stages is: ", str(nrStages))

    # stages = np.zeros((nrStages+1, 4)) # First stage stores a stage with all 0s
    stages = [[0 for _ in range(4)] for _ in range(nrStages+1)] # First stage stores a stage with all 0s
    print("nrStages prior: ", nrStages)
    
    nrStageIncl = 0 # nr stages included

    # Place read data into stages matrix
    for i in range(1, nrStages+1):
        line = input()
        if i == nrStages:
            print("Line read: ", line)
        else:
            print("Line read: ", line[:-1])
        data = line.split()

        S = int(data[0]) # mass of the stage [m]
        L = int(data[1]) # mass of the fuel [m]
        T = int(data[2]) # thrust by stage [Nm]
        C = int(data[3]) # fuel consumption [kg/s]

        V = calcVelocity(S,L,T,C)
        if V < 0:
            nrStages -= 1
            # print("Excluded stage nr %d bc of negative dV: " % i)
        else:
            nrStageIncl += 1
            stages[nrStageIncl][0] = S
            stages[nrStageIncl][1] = L
            stages[nrStageIncl][2] = T
            stages[nrStageIncl][3] = C
            
        # print(stages[i])
    
    print("nrStages after: ", nrStages)

    # dynamic programming table storing max speeds
    # of rocket built from n parts
    maxVelocities = [[0 for _ in range(maxWeight+1)] for _ in range(nrStages+1)]
    utilizedWeights = [[0 for _ in range(maxWeight+1)] for _ in range(nrStages+1)]
    
    nrSkipped = 0

    # Check each stage and possible mass
    for i in range(1, nrStages+1): # The first row #0 represents the velocoties if no stages are chosen, all zeroes
        S = stages[i][0]
        L = stages[i][1]
        T = stages[i][2]
        C = stages[i][3]
        wt = int(S+L) # (fueled) weight of current rocket stage
        # The current stage won't affect any velocity values below its weight - copy those ones from the row above
        maxVelocities[i][0:wt] = maxVelocities[i-1][0:wt]
        utilizedWeights[i][0:wt] = utilizedWeights[i-1][0:wt]

        # mass and speed for option # 2 in the for loop below (The current stage alone)
        m2 = wt
        V2 = calcVelocity(S, L, T, C)
        m3_prior = 0    # Used to compare if the mass has changed, if it hasn't then we probably don't need to calculate the vel again for option 3
        V3_prior = 0
        V_max_row = 0   # Max speed of the current row
        m_row = 0       # Corresponding mass

        for currentMaxWt in range(wt, maxWeight+1): # decide which rocket stage is best to use for each weight
            
            maxVel = 0      # Max velocity possible considering stages 1->i and currentMaxWt as the maxWeight limit
            wt_maxVel = 0   # Corresponding weight to the max velocity
        
            # Three options that might give largest velocity, choose one of them

            # 1. Max speed of prior stages (row above)
            m1 = utilizedWeights[i-1][currentMaxWt]
            V1 = maxVelocities[i-1][currentMaxWt]

            # 2. The current stage alone  (calculated outside the for loop)
            # m2
            # V2

            # 3. The current stage + the prior stage(s) that fit in currentMaxWt 
                # for this option, the mass of the stages need to be stored for all stages (i) and currentMaxWt combos
            V3 = 0 # Init to 0, use 0 if it doesn't pass the if below
            m3 = int(utilizedWeights[i-1][currentMaxWt-wt] + wt)
            # print("m3: ", m3)
            
            if m3 != m3_prior: # New combination of stages - need to calc the new vel
                dV3 = calcVelocity(m3-L, L, T, C)
                if dV3 > 0:
                    V3 = dV3 + maxVelocities[i-1][currentMaxWt-wt]
                else: 
                    V3 = 0

                V3_prior = V3 # update V3_prior to equal the newly calculated value
                m3_prior = m3
            else: 
                nrSkipped += 1
                V3 = V3_prior # use the last velocity since the mass has not changed

            # Now choose the largest velocity and corresponding weight

            if V1 >= V2 and V1 >= V3:
                maxVel = V1
                wt_maxVel = m1
            elif V2 >= V1 and V2 >= V3:
                maxVel = V2
                wt_maxVel = m2
            else:
                maxVel = V3
                wt_maxVel = m3

            # New speed is the largest one calculated for this set of stages
            if maxVel > V_max_row:
                maxVelocities[i][currentMaxWt] = maxVel
                utilizedWeights[i][currentMaxWt] = wt_maxVel
                V_max_row = maxVel
                m_row = wt_maxVel
            # There is a higher speed previously calculated for this set of stages
            else:
                maxVelocities[i][currentMaxWt] = V_max_row
                utilizedWeights[i][currentMaxWt] = m_row
            

    print("Skipped nr of V3 calcs: ", nrSkipped)
    print("\n--- %s seconds ---" % (time.time() - start_time))
    print("\nMax Velocities")
    print('\n'.join([str(int(max(row))) for row in maxVelocities]))
    # print('\n'.join(['\t'.join([str(int(cell)) for cell in row]) for row in maxVelocities]))
    print("\n Corresponding Weights")
    print('\n'.join([str(int(row[-1])) for row in utilizedWeights]))
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in utilizedWeights]))

    # Find which items were picked
    # HOW TO INDEX SAME ITEM AS MAX VELOCITY? Or is it solved since maxVel_row is spread along the row?
    stagesPicked = []
    wtLeft = utilizedWeights[-1][-1]
    for i in reversed(range(nrStages+1)):
            wt = int(stages[i][0] + stages[i][1])

            print("Weight: %d, weight space left: %d" % (wt, wtLeft))

            if utilizedWeights[i][wtLeft] == 0:
                break
            elif utilizedWeights[i][wtLeft] != utilizedWeights[i-1][wtLeft]: # this item was picked 
                stagesPicked.append((i))
                wtLeft = wtLeft - wt
                continue
            else:
                continue

    stagesPicked = stagesPicked[::-1]
    print("Picked stages (if weight is same for several stages it doesn't work (if not all are chosen)): \n", stagesPicked)

    V = max(map(max, maxVelocities)) # Max of subset where all stages were considered
    
    print("Final velocity [m/s] ", int(V))
    print(round(V))

if __name__ == '__main__':
    main()
