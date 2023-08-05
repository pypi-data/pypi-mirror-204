relativePath = "./src/data/"


def readData(fileName: str, array):
    touch(relativePath + fileName)
    file = open(relativePath + fileName, "r")
    lines = file.readlines()
    file.close()

    readArray = [
        [n for n in l.split(",")] for l in lines
    ]

    rows = range(min(len(readArray), len(array)))

    for rowNum in rows:
        for colNum in rows:
            readVal = readArray[rowNum][colNum]
            if (readVal == "None" or readVal == "None\n"):
                readVal = None
            else:
                readVal = float(readVal)
            array[rowNum][colNum] = readVal


def touch(fileName: str):
    file = open(fileName, "a+")
    file.close()


def writeData(fileName: str, array):
    file = open(relativePath + fileName, "w")
    for row in array:
        file.write(",".join([str(x) for x in row])+"\n")
    file.close()
