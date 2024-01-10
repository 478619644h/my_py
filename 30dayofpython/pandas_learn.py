
import pandas as pd
import numpy as np

nums = [1,2,3,4,5]
s = pd.Series(nums)

#creating pandas series with custom index
s1 = pd.Series(nums,index=nums)

fruits = ['Orange','Banana','Mango']
fruits = pd.Series(fruits,index=[1,2,3])

linspace = pd.Series(np.linspace(1,100))

data = [
    {"Name": "Asabeneh", "Country":"Finland","City":"Helsinki"},
    {"Name": "David", "Country":"UK","City":"London"},
    {"Name": "John", "Country":"Sweden","City":"Stockholm"}]
df = pd.DataFrame(data)

def bmi():
    weights = df['Weight']
    heights = df['Height']
    bmi = []
    for w,h in zip(weights,heights):
        bmi.append(w/(h*h))
    return bmi

if __name__ == '__main__':
    #print(fruits)
   # print(linspace)
    df['Weight'] = [74,75,76]
    heights = [173, 175, 169]
    df['Height'] = heights
    df['Height'] = df['Height'] * 0.01
    df['BMI'] = bmi()
    df['NMI'] = round(df['BMI'],2)
    print(df)

    print(df.Weight.dtype)