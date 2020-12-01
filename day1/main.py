def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    numbers = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return numbers

def findNumberInList(lst, total, numvariables, numbers):
    for i in range(len(lst)):
        current = lst[i]

        y = total - int(current)

        targetlst = lst.copy()
        targetlst.pop(i)
        if (numvariables == 1):
            if str(y) in targetlst:
                numbers.append(int(current))
                numbers.append(y)
                return True
        else:
            if (findNumberInList(targetlst, y, numvariables - 1, numbers)):
                numbers.append(int(current))
                return True

    return False

def getResult(file, total, numvariables):
    numbers = []
    if (findNumberInList(readFile(file), total, numvariables, numbers)):
        total = 1
        for number in numbers:
            total = total * number

        print("Found!")
        print(numbers)
        print(total)
    else:
        print("Not found")


getResult("day1/test.txt", 2020, 1)
getResult("day1/input.txt", 2020, 1)
getResult("day1/input2.txt", 2020, 2)
