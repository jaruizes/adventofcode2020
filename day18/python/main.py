def read_operations(filepath):
    operations_file = open(filepath, "r")
    operations = operations_file.read().splitlines()
    operations_file.close()

    return operations


def execute_operations(operations, factor_precedence):
    operation_results = []
    for operation in operations:
        operation_results.append(eval_operation(list(operation.replace(' ', '')), factor_precedence))

    return sum(operation_results)


def eval_operation(operation, factor_precedence):
    operation_sign = None
    total = None
    while operation:
        o = operation.pop(0)
        if o == "*" or o == "+":
            if not factor_precedence:
                operation_sign = o
                continue
            else:
                if o == "+":
                    operation_sign = o
                    continue
                elif o == "*":
                    return total * eval_operation(operation, factor_precedence)
        elif o == ")":
            return total
        else:
            if o == "(":
                subtotal = eval_operation(operation, factor_precedence)
            else:
                subtotal = int(o)

            if operation_sign == "+":
                total += subtotal
            elif operation_sign == "*":
                total *= subtotal
            else:
                total = subtotal

    return total


## Asserts
EXPECTED_RESULTS_PART_ONE = [71, 51, 26, 437, 12240, 13632]
EXPECTED_RESULTS_PART_TWO = [231, 51, 46, 1445, 669060, 23340]
assert execute_operations(read_operations("../inputs/test.txt"), False) == sum(EXPECTED_RESULTS_PART_ONE)
assert execute_operations(read_operations("../inputs/test.txt"), True) == sum(EXPECTED_RESULTS_PART_TWO)

print("Part one: " + str(execute_operations(read_operations("../inputs/input.txt"), False)))
print("Part two: " + str(execute_operations(read_operations("../inputs/input.txt"), True)))
