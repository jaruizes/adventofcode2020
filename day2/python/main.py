import time


def readfile(filepath):
    """
    This function reads the file associated with filename and returns a list of patterns

    :param filepath: The path of the file containing the list of numbers
    :return: returns list of patterns
    """
    fileObj = open(filepath, "r")
    patterns = fileObj.read().splitlines()
    fileObj.close()
    return patterns


def validate_password_method_one(password, pattern):
    """
    This function validates the param password against the pattern:
    The lowest and highest number of times a given letter must appear for the password

    :param password: password to validate
    :param pattern: pattern used to validate the password
    :return: true/false whether the password is right or wrong
    """
    pattern_parts = pattern.split()
    character = pattern_parts[1]
    x = int(pattern_parts[0].split('-')[0])
    y = int(pattern_parts[0].split('-')[1])

    occurrences = password.count(character)

    return x <= occurrences <= y


def validate_password_method_two(password, pattern):
    """
    This function validates the param password against the pattern:
    Exactly one of positions given in the pattern must contain the given letter

    :param password: password to validate
    :param pattern: pattern used to validate the password
    :return: true/false whether the password is right or wrong
    """
    pattern_parts = pattern.split()

    x = int(pattern_parts[0].split('-')[0])
    y = int(pattern_parts[0].split('-')[1])
    character_expected = pattern_parts[1]
    try:
        character_in_x = password[x - 1]
        character_in_y = password[y - 1]
        if character_in_x == character_expected == character_in_y:
            return False

        if character_in_x == character_expected or character_in_y == character_expected:
            return True

    except IndexError:
        return False

    return False


def main(file, validation_method):
    """
    Main method
    :param file: file containing patterns andd passwords
    :param validation_method: method used to validate passwords
    :return:
    """
    patterns_and_passwords_list = readfile(file)
    passwords_ok = 0
    for pattern_and_password in patterns_and_passwords_list:
        pattern_and_password_parts = pattern_and_password.split(':')
        if validation_method(pattern_and_password_parts[1].strip(), pattern_and_password_parts[0].strip()):
            passwords_ok += 1

    return passwords_ok


## Asserts
assert main('../inputs/test.txt', validate_password_method_one) == 2
assert main('../inputs/test.txt', validate_password_method_two) == 1

start_time = time.time()
print(
    "- Part One (method 1): " + str(main('../inputs/input.txt', validate_password_method_one)) + " ok [%s seconds]" % (
                time.time() - start_time))

start_time = time.time()
print(
    "- Part Two (method 2): " + str(main('../inputs/input.txt', validate_password_method_two)) + " ok [%s seconds]" % (
                time.time() - start_time))
