const fs = require('fs')
const assert = require('assert');

const validate_password_method_one = (password, pattern) => {
   const pattern_parts = pattern.split(' ');
   const character = pattern_parts[1];
   const x = pattern_parts[0].split('-')[0];
   const y = pattern_parts[0].split('-')[1];

   const regex = new RegExp(character,"g")
   const occurrences = password.match(regex) ? password.match(regex).length : 0;
   return occurrences >= x && occurrences <= y;
}

const validate_password_method_two = (password, pattern) => {
    const pattern_parts = pattern.split(' ');
    const character = pattern_parts[1];
    const x = pattern_parts[0].split('-')[0];
    const y = pattern_parts[0].split('-')[1];
    const character_in_x = password.charAt(x - 1);
    const character_in_y = password.charAt(y - 1);

    if (character_in_x === character_in_y && character_in_x === character) {
        return false;
    }

    if (character_in_x === character || character_in_y === character) {
        return true
    }

    return false;
}

const main = (filepath, validation_method) => {
    return new Promise((resolve, reject) => {
        fs.readFile(filepath, 'utf8', function (err, data) {
            if (err) {
                reject(err);
            }

            const patterns_and_passwords_list = data.toString().split("\n");
            let passwords_ok = 0

            patterns_and_passwords_list.forEach((pattern_and_password) => {
                const pattern_and_password_parts = pattern_and_password.split(':')
                if (validation_method(pattern_and_password_parts[1].trimStart(), pattern_and_password_parts[0].trimStart())) {
                    passwords_ok++;
                }
            })

            resolve(passwords_ok);
        });
    });
}

const start1 = process.hrtime();
main('../inputs/test.txt', validate_password_method_one).then(result => {
    const hrend = process.hrtime(start1)

    assert.strictEqual(result, 2);
    console.log('- Test (method 1): ' + result + ' [%dms]', hrend[1] / 1000000000);
});

const start2 = process.hrtime();
main('../inputs/test.txt', validate_password_method_two).then(result => {
    const hrend = process.hrtime(start2)

    assert.strictEqual(result, 1);
    console.log('- Test (method 2): ' + result + ' [%dms]', hrend[1] / 1000000000);
});

const start3 = process.hrtime();
main('../inputs/input.txt', validate_password_method_one).then(result => {
    const hrend = process.hrtime(start3)
    console.log('- Part One (method 1): ' + result + ' [%dms]', hrend[1] / 1000000000);
});

const start4 = process.hrtime();
main('../inputs/input.txt', validate_password_method_two).then(result => {
    const hrend = process.hrtime(start3)
    console.log('- Part Two (method 2): ' + result + ' [%dms]', hrend[1] / 1000000000);
});

