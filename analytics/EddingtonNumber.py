import pandas as pd
import math

def main():
    count ={}
    for i in range(1, 1000):
        count[i] = 0

    df = pd.read_csv("activities.csv", encoding="utf16")
    for index, row in df.iterrows():
        distance = row[2]
        miles = int(math.floor(distance * 0.00062137))
        for i in range(1, miles+1):
            count[i] = count[i] + 1

    en = 1
    for i in range(1, 126):
        if count[i] >= i:
            en = i
        else:
            break

    print("Current Eddington Number:{}\n".format(en))
    for i in range(0,30):
        new = i +en
        print("Required rides to reach Eddington Number:{} is {} additional rides".format(new, new - count[new]))


if __name__ == "__main__":

    main()