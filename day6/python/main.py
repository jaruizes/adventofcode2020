def read_anwers(answers_file):
    file = open(answers_file, "rb")
    lines = file.readlines()

    answers = []
    answer = []
    for line in lines:
        content = line.decode('UTF-8').strip()
        if not content:
            answers.append(answer)
            answer = []
        else:
            answer.append(content)

    answers.append(answer)
    file.close()
    return answers


def process_anyone_answered_yes(answers):
    total = 0
    for answer_block in answers:
        unique_answers = set()
        for answer_person in answer_block:
            for answer in answer_person:
                unique_answers.add(answer)

        total += len(unique_answers)

    return total


def process_everyone_answered_yes(answers):
    total = 0
    for answer_block in answers:
        persons_in_block = len(answer_block)
        answers_detailed = {}
        for answer_person in answer_block:
            for answer in answer_person:
                current_value = 0
                if len(answers_detailed) > 0 and answer in answers_detailed:
                    current_value = answers_detailed.get(answer)

                answers_detailed[answer] = current_value + 1

        for answer in answers_detailed.keys():
            if answers_detailed[answer] == persons_in_block:
                total += 1

    return total


## Asserts
assert process_anyone_answered_yes(read_anwers('../inputs/test.txt')) == 11
assert process_everyone_answered_yes(read_anwers('../inputs/test.txt')) == 6

print('Part one: ' + str(process_anyone_answered_yes(read_anwers('../inputs/input.txt'))))
print('Part two: ' + str(process_everyone_answered_yes(read_anwers('../inputs/input.txt'))))
