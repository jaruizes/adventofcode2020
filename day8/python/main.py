class AdventCodeExecutor:
    def __init__(self):
        self.instructions_executors = {'acc': self.__acc, 'nop': self.__nop, 'jmp': self.__jmp}

    def execute(self, instructions):
        self.__init_execution_variables()
        while not self.__finish(instructions):
            instruction = instructions[self.current_line].split()
            self.executed_lines.append(self.current_line)
            self.instructions_executors[instruction[0]](instruction[1])

        return {'code': self.execution_code, 'accumulator': self.accumulator}

    def __init_execution_variables(self):
        self.accumulator = 0
        self.current_line = 0
        self.executed_lines = []
        self.execution_code = 0

    def __finish(self, instructions):
        if self.__is_infinite_loop():
            self.execution_code = -1
            return True

        if self.__is_the_instructions_end(instructions):
            self.execution_code = 0
            return True

        return False

    def __nop(self, argument):
        self.current_line += 1
        return

    def __acc(self, argument):
        self.accumulator += int(eval(argument))
        self.current_line += 1

    def __jmp(self, argument):
        self.current_line += int(eval(argument))

    def __is_infinite_loop(self):
        return self.current_line in self.executed_lines

    def __is_the_instructions_end(self, instructions):
        return self.current_line >= len(instructions)


def read_commands(filepath):
    instructions_file = open(filepath, "r")
    instructions = instructions_file.read().splitlines()
    instructions_file.close()
    return instructions


def get_accumulator_value(filepath):
    instructions = read_commands(filepath)
    advent_executor = AdventCodeExecutor()
    return advent_executor.execute(instructions)['accumulator']


def get_potential_fixed_code(instructions, line_to_fix):
    instructions_fixed = instructions.copy()
    instruction_to_fix = instructions_fixed[line_to_fix]
    if 'nop' in instruction_to_fix:
        instructions_fixed[line_to_fix] = instruction_to_fix.replace('nop', 'jmp')
    if 'jmp' in instruction_to_fix:
        instructions_fixed[line_to_fix] = instruction_to_fix.replace('jmp', 'nop')

    return instructions_fixed


def get_accumulator_value_in_fixed_code(filepath):
    instructions = read_commands(filepath)
    advent_executor = AdventCodeExecutor()
    for i in range(len(instructions)):
        instruction = instructions[i]
        if 'jmp' in instruction or 'nop' in instruction:
            potential_fixed_code = get_potential_fixed_code(instructions, i)
            result = advent_executor.execute(potential_fixed_code)

            if result['code'] == 0:
                return result['accumulator']


## Asserts
assert get_accumulator_value('../inputs/test.txt') == 5
assert get_accumulator_value_in_fixed_code('../inputs/test.txt') == 8

print('Part one: ' + str(get_accumulator_value('../inputs/input.txt')))
print('Part two: ' + str(get_accumulator_value_in_fixed_code('../inputs/input.txt')))
