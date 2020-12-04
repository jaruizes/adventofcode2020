import re


class Passport:
    __PASSPORT_REQUIRED_KEYS = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
    __EYE_COLORS_ALLOWED = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

    def __init__(self, passport_data, is_cid_optional):
        self.is_cid_optional = is_cid_optional
        self.data = passport_data

        self.__VALIDATORS = {
            'byr': self.__byr_validator,
            'iyr': self.__iyr_validator,
            'eyr': self.__eyr_validator,
            'hgt': self.__hgt_validator,
            'hcl': self.__hcl_validator,
            'ecl': self.__ecl_validator,
            'pid': self.__pid_validator
        }

    def is_valid(self, apply_field_validation):
        for key in self.__PASSPORT_REQUIRED_KEYS:
            if not apply_field_validation:
                if (key != 'cid' or (key == 'cid' and not self.is_cid_optional)) and self.data.get(key) is None:
                    return False
            else:
                if key != 'cid':
                    if self.data.get(key) is None:
                        return False
                    else:
                        validator = self.__VALIDATORS.get(key)
                        if not validator():
                            return False
                else:
                    if not self.is_cid_optional and self.data.get(key) is None:
                        return False

        return True

    def __byr_validator(self):
        """
        four digits; at least 1920 and at most 2002
        :return: True/False
        """
        byr = self.data.get('byr')
        return byr.isnumeric() and len(byr) == 4 and 1920 <= int(byr) <= 2002

    def __iyr_validator(self):
        """
        four digits; at least 2010 and at most 2020
        :return: True/False
        """
        iyr = self.data.get('iyr')
        return iyr.isnumeric() and len(iyr) == 4 and 2010 <= int(iyr) <= 2020

    def __eyr_validator(self):
        """
        four digits; at least 2020 and at most 2030.
        :return: True/False
        """
        eyr = self.data.get('eyr')
        return eyr.isnumeric() and len(eyr) == 4 and 2020 <= int(eyr) <= 2030

    def __hgt_validator(self):
        """
        a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
        :return: True/False
        """
        hgt = self.data.get('hgt')
        if 'cm' in hgt:
            hgt = hgt.replace('cm', '')
            if hgt.isnumeric() and 150 <= int(hgt) <= 193:
                return True

        if 'in' in hgt:
            hgt = hgt.replace('in', '')
            if hgt.isnumeric() and 59 <= int(hgt) <= 76:
                return True

        return False

    def __hcl_validator(self):
        """
        a # followed by exactly six characters 0-9 or a-f
        :return: True/False
        """
        hcl = self.data.get('hcl')
        return re.match(r"\#[a-f0-9]{6}", hcl)

    def __ecl_validator(self):
        """
        exactly one of: amb blu brn gry grn hzl oth.
        :return: True/False
        """
        ecl = self.data.get('ecl')
        return len(ecl) == 3 and ecl in self.__EYE_COLORS_ALLOWED

    def __pid_validator(self):
        """
        a nine-digit number, including leading zeroes.
        :return: True/False
        """
        pid = self.data.get('pid')
        return len(pid) == 9 and re.match(r"[0-9]{9}", pid)


def read_passports(passports_batch):
    file = open(passports_batch, "rb")
    lines = file.readlines()

    passports = []
    passport = {}
    for line in lines:
        content = line.decode('UTF-8').strip()
        if not content:
            passports.append(passport)
            passport = {}

        passport_fields = content.split()
        for field in passport_fields:
            field_parts = field.split(':')
            passport[field_parts[0]] = field_parts[1]

    passports.append(passport)
    file.close()
    return passports


def check(passports_batch, is_cid_optional, apply_field_validation):
    passports = read_passports(passports_batch)
    passports_valids = 0
    for passports_data in passports:
        passport = Passport(passports_data, is_cid_optional)
        if passport.is_valid(apply_field_validation):
            passports_valids += 1

    return passports_valids


## Asserts
assert check('../inputs/test.txt', True, False) == 2
assert check('../inputs/test_invalids.txt', True, True) == 0
assert check('../inputs/test_invalids_fields.txt', True, True) == 12
assert check('../inputs/test_valids.txt', True, True) == 4

print('Part one: ', check('../inputs/input.txt', True, False))
print('Part two: ', check('../inputs/input.txt', True, True))
