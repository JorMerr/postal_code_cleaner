import re
import pandas as pd

file = input("Enter your relative filepath : ")
columnName = input("Enter the exact name of the column which contains postal codes : ")

df = pd.read_csv(file)

first_letter = 'abceghjklmnprstvxy'
valid_letters = 'abceghjklmnprstvwxyz'
valid_nums = '0123456789'
# alphPlace = [0,2,4]
# numPlace = [1,3,5]

df[columnName] = df[columnName].str.lower().str.replace(' ','')

cleanedCode = []
invalidCode = []
for currentIndex in df.index:                   # loop through rows of the data and assign postal codes to list
    code = df.loc[currentIndex, columnName]     # assign current postal code to variable
    if (len(code) != 6):                        # check if length of postal code matches A1A1A1 format
        cleanedCode.insert(currentIndex, "")
        invalidCode.append("Invalid length")
    elif (not code[5] in valid_nums):           #check last character is a number
        if (code[5] == "o"):                    # common error letter "o" replaced with "0"
            code = ("").join([c.replace('o','0') for c in code])
            cleanedCode.insert(currentIndex, code)
            invalidCode.append("Sixth character must be number")
    elif (not code[4] in valid_letters):        # check if fifth character is a valid letter
        cleanedCode.insert(currentIndex, "")
        invalidCode.append("Fifth character must be a valid letter")
    elif (not code[3] in valid_nums):           # similar to above, check fourth character is a valid number
        if (code[3] == "o"):
            code = "".join([c.replace('o','0') for c in code])
            cleanedCode.insert(currentIndex, code)
            invalidCode.append("Fourth character must be number")
    elif (not code[2] in valid_letters):        # check if third character is a valid letter
        cleanedCode.insert(currentIndex, "")
        invalidCode.append("Third character must be a valid letter")
    elif (not code[1] in valid_nums):           # check if second character is a valid number
        if (code[1] == "o"):
            code = "".join([c.replace('o','0') for c in code])
            cleanedCode.insert(currentIndex, code)
            invalidCode.append("Second character must be number")
    elif (not code[0] in valid_letters):         # check if first character is a valid letter
        cleanedCode.insert(currentIndex, "")
        invalidCode.append("First character must be a valid letter") 
    elif (not code[0] in first_letter):
        cleanedCode.insert(currentIndex, "")
        invalidCode.append("First cannot be 'w' or 'z'") 
    else:        
        cleanedCode.append(code)
        invalidCode.append("")


df['cleanedCode'] = cleanedCode
df['invalidCode'] = invalidCode

cleanedCode2 = []
invalidCode2 = []
columnName = "cleanedCode"
for currentIndex in df.index: #loop through rows of the data and assign postal codes to list
    code = df.loc[currentIndex, columnName] # assign current postal code to variable
    if (len(code) != 6): # check if length of postal code matches A1A1A1 format
        cleanedCode2.insert(currentIndex, "")
        invalidCode2.append("Invalid length")
    elif (not code[5] in valid_nums): #check last character is a number
        if (code[5] == "o"): #common error letter "o" replaced with "0"
            code = ("").join([c.replace('o','0') for c in code])
            cleanedCode2.insert(currentIndex, code)
            invalidCode2.append("Sixth character must be number")
    elif (not code[4] in valid_letters): # check if fifth character is a valid letter
        cleanedCode2.insert(currentIndex, "")
        invalidCode2.append("Fifth character must be a valid letter")
    elif (not code[3] in valid_nums): # similar to above, check fourth character is a valid number
        if (code[3] == "o"):
            code = "".join([c.replace('o','0') for c in code])
            cleanedCode2.insert(currentIndex, code)
            invalidCode2.append("Fourth character must be number")
    elif (not code[2] in valid_letters): # check if third character is a valid letter
        cleanedCode2.insert(currentIndex, "")
        invalidCode2.append("Third character must be a valid letter")
    elif (not code[1] in valid_nums):       # check if second character is a valid number
        if (code[1] == "o"):
            code = "".join([c.replace('o','0') for c in code])
            cleanedCode2.insert(currentIndex, code)
            invalidCode2.append("Second character must be number")
    elif (not code[0] in valid_letters):         # check if first character is a valid letter
        cleanedCode2.insert(currentIndex, "")
        invalidCode2.append("First character must be a valid letter") 
    elif (not code[0] in first_letter):
        cleanedCode2.insert(currentIndex, "")
        invalidCode2.append("First character cannot be 'w' or 'z'") 
    else:        
        cleanedCode2.append(code)
        invalidCode2.append("")


df['cleanedCode2'] = cleanedCode2
df['invalidCode2'] = invalidCode2

newCodes = []
for c in cleanedCode2:
    c = f"{c[:3]} {c[3:]}"
    newCodes.append(c)
df['cleanPostalCodes'] = newCodes
df['cleanPostalCodes'] = df['cleanPostalCodes'].str.upper()
df = df.drop(['cleanedCode','invalidCode','cleanedCode2'], axis=1)
df = df[['postalCodes','cleanPostalCodes','invalidCode2']]
df.rename(columns = {'invalidCode2': 'invalidMessage'}, inplace = True)

# Write to new output file to preserve raw data format
df.to_csv('cleanedPostalCodes.csv')