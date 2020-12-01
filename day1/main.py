def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    numbers = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return numbers

def findNumberInList(lst, total):
    for i in range(len(lst)):
        current = lst[i]
        target = total - int(current)
        targetlst = lst.copy()
        targetlst.pop(i)
        if str(target) in targetlst:
            result = int(current) * target
            print("Found: " + str(result))
            return result


findNumberInList(readFile("day1/test.txt"), 2020)
findNumberInList(readFile("day1/input.txt"), 2020)
