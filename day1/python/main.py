import time


def readfile(filepath):
    """
    This function reads the file associated with filename and returns a list of numbers

    :param filepath: The path of the file containing the list of numbers
    :return: returns list of numbers
    """
    fileObj = open(filepath, "r")
    numbers = list(map(int, fileObj.read().splitlines()))
    fileObj.close()
    return numbers


def resolve_equation(lst, total, numvariables, numbers_summing_total):
    """
    This function resolves the equation getting the set of numbers summing total.
    The length of the set is determined by numvariables:
    Example: numvariables = 2 means total = x + y; total - x = y
    Example: numvariables = 3 means total = x + y + z; total - x = y + z; (total - x) - y = z

    :param lst: list of numbers
    :param total: amount to get adding numvariables
    :param numvariables: num of variables in the equation
    :param numbers_summing_total: list of numbers that added each others result equals to total:
    :return: returns true/false whether the equation was solved or not
    """
    for i in range(len(lst)):
        x = lst[i]
        y = total - x

        list_without_x = lst.copy()
        list_without_x.pop(i)
        if numvariables == 2:
            if y in list_without_x:
                numbers_summing_total.append(x)
                numbers_summing_total.append(y)
                return True
        else:
            if resolve_equation(list_without_x, y, numvariables - 1, numbers_summing_total):
                numbers_summing_total.append(x)
                return True

    return False


def multiply(numbers_solving_equation):
    """
    This function multiplies the numbers reolving the equation

    :param numbers_solving_equation: set of numbers resolving the equation (x,y,z...)
    :return: result of the product
    """
    total = 1
    for number in numbers_solving_equation:
        total = total * number

    return total


def main(file, total, numvariables, sort):
    numbers_list_raw = readfile(file)

    if sort:
        numbers_list_raw.sort()

    numbers_solving_equation = []
    if resolve_equation(numbers_list_raw, total, numvariables, numbers_solving_equation):
        return multiply(numbers_solving_equation)
    else:
        print("Equation not solved")


start_time = time.time()
print("- Test (no sort): " + str(main("../inputs/test.txt", 2020, 2, False)) + " [%s seconds]" % (
        time.time() - start_time))

start_time = time.time()
print("- Test (sort): " + str(main("../inputs/test.txt", 2020, 2, True)) + " [%s seconds]" % (time.time() - start_time))

start_time = time.time()
print("- Part One (no sort): " + str(main("../inputs/input.txt", 2020, 2, False)) + " [%s seconds]" % (
        time.time() - start_time))

start_time = time.time()
print("- Part One (sort): " + str(main("../inputs/input.txt", 2020, 2, True)) + " [%s seconds]" % (
        time.time() - start_time))

start_time = time.time()
print("- Part Two (no sort): " + str(main("../inputs/input2.txt", 2020, 3, False)) + " [%s seconds]" % (
        time.time() - start_time))

start_time = time.time()
print("- Part Two (sort): " + str(main("../inputs/input2.txt", 2020, 3, True)) + " [%s seconds]" % (
        time.time() - start_time))
