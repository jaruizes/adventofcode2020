EXPECTED_RESULTS_PART_ONE = [71, 51, 26, 437, 12240, 13632]
EXPECTED_RESULTS_PART_TWO = [231, 51, 46, 1445, 669060, 23340]


def read_operations(filepath):
    operations_file = open(filepath, "r")
    operations = operations_file.read().splitlines()
    operations_file.close()

    return operations


def execute_operations(operations, method):
    operation_results = []
    for operation in operations:
        operation_list = list(operation.replace(' ', ''))
        res = method(operation_list)
        operation_results.append(res)

    return sum(operation_results)


def eval_operation(operation):
    operation_sign = None
    total = None
    while operation:
        o = operation.pop(0)
        if o == "*" or o == "+":
            operation_sign = o
            continue
        elif o == ")":
            return total
        else:
            if o == "(":
                subtotal = eval_operation(operation)
            else:
                subtotal = int(o)

            if operation_sign == "+":
                total += subtotal
            elif operation_sign == "*":
                total *= subtotal
            else:
                total = subtotal

    return total


def eval_operation2(operation):
    operation_sign = None
    total = None
    while operation:
        o = operation.pop(0)
        if o == "+":
            operation_sign = o
            continue
        elif o == "*":
            return total * eval_operation2(operation)
        elif o == ")":
            return total
        else:
            if o == "(":
                subtotal = eval_operation2(operation)
            else:
                subtotal = int(o)
            if operation_sign == "+":
                total += subtotal
            else:
                total = subtotal

    return total


## Asserts
assert execute_operations(read_operations("../inputs/test.txt"), eval_operation) == sum(EXPECTED_RESULTS_PART_ONE)
assert execute_operations(read_operations("../inputs/test.txt"), eval_operation2) == sum(EXPECTED_RESULTS_PART_TWO)

print("Part one: " + str(execute_operations(read_operations("../inputs/input.txt"), eval_operation)))
print("Part two: " + str(execute_operations(read_operations("../inputs/input.txt"), eval_operation2)))
