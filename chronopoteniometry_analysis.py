# Author: Jennifer John
# Date: August 10, 2016
# Description: Given data obtained via charge/discharge graphs, this program
# combines the second cycles from each file into one file. It also creates
# a new file with the areal capacitances from each original file.

files=[]
print("""
Welcome to Jennifer's chronopotentiometry data analysis program!

This program takes in a set of data files obtained via chronopotentiometry (charge/discharge) tests. It combines the files into a single file with only the second charge/discharge cycles called "final CD file." It also creates a file with the areal capacitances of the files, called "areal capacitances".

Please note that for the program to work correctly, the program file must be saved in the same folder as the data files. Also, the program currently only workes on graphs with 4 segments.

If you have any questions, suggestions, or find any bugs, please email the developer at jenniferneda@gmail.com.""")

response=input("\n****************************************************\nEnter the name of a file. If you have finished, enter 'Done'. ")
while response.upper() != 'DONE':
    if ".txt" not in response:
        response+=('.txt')
    file = open(response, "r")
    lines = file.readlines()
    file.close()
    files.append(lines)
    response=input("Enter the name of a file. If you have finished, enter 'Done'. ")

print("Great! Please wait a moment while the program runs.")
xCoords=[]
for i in range(1, len(files[0])):
    xCoords.append(str(0.02*i))
IVals=[]
tInitVals=[]
uVals=[]
tFinVals=[]
cVals=[]

def isDecreasing(lineCount, lines):
    if len(lines)>100:
        p=12
    else:
        p=5
    for i in range(0, p):
        a=float(lines[lineCount+i].split()[1])
        b=float(lines[lineCount+i+1].split()[1])
        if b>=a:
            return False
    return True

def isIncreasing(lineCount, lines):
    if len(lines)>100:
        p=15
    else:
        p=5
    for i in range(0, p):
        if lineCount+i<len(lines)-1:
            a=float(lines[lineCount+i].split()[1])
            b=float(lines[lineCount+i+1].split()[1])
            if b<a:
                return False
    return True

def getSecondCycle(lines): # returns the new lines with only the 2nd cycle
    # first find I
    currLine=0
    nums=['1','2','3','4','5','6','7','8','9','0']
    while "Cathodic Current" not in lines[currLine]:
        currLine+=1
    index=0
    while lines[currLine][index] not in nums:
        index+=1
    I=float(lines[currLine][index:].rstrip())*10**3
    IVals.append(I)
    lineCount=int((len(lines)-21)/3)+21 # start searching 1/3 of the way through. 21 is subtracted to account for the info lines

    while isDecreasing(lineCount, lines)==False: # keep searching until 3 consequetive pts with decreasing y vals are found
        lineCount+=1
    newLines = [] # new list to contain the pts from the last cycle
    done=False
    xCoord=0.02
    for i in range(lineCount, len(lines)): # loop over all pts in the last cycle
        xCoord+=0.02
        xCoord=round(xCoord, 2)
        yCoord=float(lines[i].split()[1])
        if i!=len(lines)-1:
            nextYCoord=float(lines[i+1].split()[1]) # point immediately after the current one
        if done==False and abs(yCoord)-abs(nextYCoord)>0.008:
            if isIncreasing(i, lines):
                done=True
                tInitVals.append(float(xCoord)) # add the current x coordinate to the list of t_I values
                uVals.append(nextYCoord) # add the next y coordinate to the list of u values
        newLines.append(str(yCoord)) # add the current y coordinate to the list of last cycle pts
    tFinVals.append(round(xCoord-0.02, 2)) # add the t_F value
    cVals.append((-1)*IVals[len(IVals)-1]*(tFinVals[len(tFinVals)-1]-tInitVals[len(tInitVals)-1])/uVals[len(uVals)-1])                
    return newLines

finalFile=open('final CD file.txt', 'w')
combinedLines=[]
for i in range(0, len(files)):
    files[i]=getSecondCycle(files[i])

for i in range(0, len(files[0])):
    currLine=xCoords[i]+', '
    for file in files:
        if i<len(file):
            currLine+=file[i].rstrip()
            currLine+=', '
    currLine=currLine[:-2]
    currLine+='\n'
    combinedLines.append(currLine)
for line in combinedLines:
    finalFile.write(line)
finalFile.close()

capacitances=open('areal capacitances.txt','w')
for i in cVals:
    capacitances.write(str(i))
    capacitances.write('\n')
capacitances.close()
input("The program has finished. Press the 'enter' key to exit.")
