import sys
import re
import time
word = 'ACGT'

def main():
    input = sys.stdin.readline

    S = '1'
    start_time = time.time()

    while S != '0':
        
        line = input()
        print("Line read: ", line[0:-1])
        data = line.split()

        S = data[0]
        if S == '0':
            break
        L = data[1]
        # For input substring S of L
        # test 3 types of matches
        # Print output like: case1 case 2 case3 every loop
        case1 = 0
        case2 = 0
        case3 = 0

        # case 1 - matching substrings
        case1 = len(re.findall('(?=('+ S +'))', L))
        print("Case1: ", str(case1))

        # case 2 - matches when one letter is deleted
        S_old = []  # unique strings
        S_all = []
        for i in range(len(S)):
            # remove one letter at a time
            S_new = S[:i] + S[i+1:]
            # Check if the string is not unique
            if S_new in S_old:
                pass
            else:
                S_old.append(S_new)
                case2 += len(re.findall('(?=('+ S_new +'))', L))
            S_all.append(S_new) # TA BORT #---------------------------------------------

        print("Case2: ", str(case2))
        print("Unique substrings case2: ", " ".join(S_old))
        print("All substrings case2: ", " ".join(S_all))

        # case 3 - matches when one letter is added
        S_old = []
        S_all = []
        # Loop through the whole string S
        for i in range(len(S)+1): 
            # for every loop, add the four letters ACGT to S in a loop, 
            # check that the new S is unique, count case3 occurences
            for addLetter in word: 
                S_new = S[:i] + addLetter + S[i:]
                # Check if the string is not unique
                if S_new in S_old:
                    pass
                else:
                    S_old.append(S_new)
                    case3 += len(re.findall('(?=('+ S_new +'))', L))
                S_all.append(S_new) # TA BORT #---------------------------------------------

            print("Case3: ", str(case3))
        print("Unique substrings case3: ", " ".join(S_old))
        print("All substrings case3: ", " ".join(S_all))

        print(" ".join((str(case1), str(case2), str(case3))))
    print("--- %s seconds ---" % (time.time() - start_time))

    return 0

if __name__ == '__main__':
    main()