from sys import stdin, stdout
import sys
import time
import math as math
g = 9.81
dL = 0.0001
rad2deg = (360/(2*math.pi))

def calcLanding(j, p, H, L):
    l = 0 # landing point
    h = 0 # landing height

    v_x = math.sqrt(2*g*j)
    # print("Approach speed is: %s" % str(v_x))
    v_x2 = v_x**2
    L2 = L**2
    # Calc impact of flight path with three ramp curves, then after check which one is valid
    # solve for l, then input l in the flight path to get the height of the impact

    # Flight Path f(l) == slope h(l)

    # f(l) = -(g*(l**2))/(2*(v_x**2)) + H + p

    # case 1 - 0 <= l <= L/2
    a_1 = ((H+p)/H-1)
    # print("a_1 ", str(a_1))
    n_1 = ((g/(2*H*(v_x2)))-(2/(L2)))
    # print("n_1 ", str(n_1))

    if n_1 >= 0:
        l_1 = math.sqrt(a_1/n_1)
    else:
        l_1 = -111
    # print("L1 = ", str(l_1))

    # case 2 - L/2 <= l <= L
    # pq formula, choose largest x
    n_2 = (4*H*(v_x2))+(g*(L2)) # var to make it shorter
    # print("n_2 ", str(n_2))
    p_2 = -((8*H*(v_x2)*L)/(n_2))
    # print("p_2 ", str(p_2))
    a_2 = (4*H*(v_x2)*(L2))
    # print("a_2 ", str(a_2))
    q_2 = a_2/(n_2) * (1-(H+p)/(2*H))
    # print("q_2 ", str(q_2))
    # print("((p_2/2)**2)-q_2 = ", str(((p_2/2)**2)-q_2))
    p2q = pow(p_2/2, 2)-q_2
    if p2q < 0:
        # print("Negative sqrt value")
        l_2 = -222
    else:
        l_2 = -p_2/2 + math.sqrt(p2q) # only + here because it will be the largest x that's the one
        # print("L2 = ", str(l_2))

    # case 3 - L <= l
    l_3 = math.sqrt(2*(v_x2)*(H+p)/g)
    # print("L3 = ", str(l_3))

    if (0 <= l_1) and (l_1 < L/2):
        l = l_1 
        slopeAngle = calcSlopeAngle(1, l, H, L)
    elif (L/2 <= l_2) and (l_2 < L):
        l = l_2
        slopeAngle = calcSlopeAngle(2, l, H, L)
    elif L <= l_3:
        l = l_3
        slopeAngle = calcSlopeAngle(3, l, H, L)
    else:
        l = -1
        # print("Ajdå")

    h_landing = H + p - g/2*((l/v_x)**2) # landing height

    v_l, fallAngle = calcLandingSpeedAndAngle(v_x, H, p, h_landing)
    # print("Fall angle: ", str(fallAngle))
    relativeAngle = (fallAngle - slopeAngle)
    # print("Relative angle: ", str(relativeAngle))

    return l, v_l, relativeAngle

def calcSlopeAngle(case, l, H, L):
    if case == 1:
        dh = calc_h_case1(l, H, L) - calc_h_case1(l+dL, H, L)
    elif case == 2:
        dh = calc_h_case2(l, H, L) - calc_h_case2(l+dL, H, L)
    elif case == 3:
        dh = 0

    slopeAngle = rad2deg*math.atan(dh/dL)
    # print("Angle of the slope: ", str(slopeAngle))
    return slopeAngle

#calc height for case 1: 0 <= l < L/2
def calc_h_case1(l,H,L):
    return H*(1-2*(pow(l/L, 2)))

#calc height for case 1: L/2 <= l < L
def calc_h_case2(l,H,L):
    return 2*H*pow((l/L-1), 2)


def calcLandingSpeedAndAngle(v_x, H, p, h_landing):
    # Speed
    h_fall = H+p-h_landing
    v_y = math.sqrt(2*g*h_fall)
    v_landing = math.sqrt(pow(v_x, 2) + pow(v_y, 2))

    # Angle
    fallAngle = rad2deg*math.atan(v_y/v_x)
    
    return v_landing, fallAngle

## MAIN ##
def main():
    input = sys.stdin.readline
    start_time = time.time()
    nrLines = int(input()) # first line says how many more lines there are
    # print("number of lines is: ", str(nrLines))
    for _ in range(nrLines):
        line = input()
        # print("Line read: ", line)
        data = line.split()

        j = int(data[0])
        p = int(data[1])
        H = int(data[2])
        L = int(data[3])

        # ----- Input -----
        # print("Input (lines, j, p, H, L): ", " ".join((str(nrLines), str(j), str(p), str(H), str(L))))
        
        # ----- Output -----
        l, v_l, relativeAngle = calcLanding(j, p, H, L)
        # print("Correct landing l, v_l, relativeAngle: ")
        print(" ".join((str(l), str(v_l), str(relativeAngle))))
    
    # print("--- %s seconds ---" % (time.time() - start_time))
    return 0
    
if __name__ == '__main__':
    main()