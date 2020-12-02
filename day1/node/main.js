const fs = require('fs')
const assert = require('assert');


const multiply = (numbers_solving_equation) => {
    let total = 1;
    numbers_solving_equation.forEach((number) => {
        total = total * number;
    });

    return total;
}

const solve_equation = (lst, total, numvariables, numbers_summing_total) => {
    for (let i=0; i < lst.length; i++) {
        const x = lst[i];
        const y = total - x;
        const list_without_x = [...lst];
        list_without_x.splice(i, 1);

        if (numvariables === 2) {
            if (list_without_x.indexOf(y) > -1) {
                numbers_summing_total.push(x);
                numbers_summing_total.push(y);
                return true;
            }
        } else {
            if (solve_equation(list_without_x, y, numvariables - 1, numbers_summing_total)) {
                numbers_summing_total.push(x);
                return true;
            }
        }
    }

    return false;
}

const main = (filepath, total, numvariables, sort) => {
    return new Promise((resolve, reject) => {
        fs.readFile(filepath, 'utf8', function (err, data) {
            if (err) {
                reject(err);
            }

            const numbers_summing_total = [];
            const numbers_list_raw = data.toString().split("\n").map(Number);
            if (sort) {
                numbers_list_raw.sort();
            }

            if (solve_equation(data.toString().split("\n").map(Number), total, numvariables, numbers_summing_total)) {
                const result = multiply(numbers_summing_total);
                resolve(result);
            } else {
                reject('Not found');
            }
        });
    });
}

const start1 = process.hrtime();
main('../inputs/test.txt', 2020, 2, false).then(result => {
    const hrend = process.hrtime(start1)

    assert.strictEqual(result, 514579);
    console.log('- Test (no sort): ' + result + ' [%dms]', hrend[1] / 1000000000);
});

const start2 = process.hrtime();
main('../inputs/test.txt', 2020, 3, true).then(result => {
    const hrend = process.hrtime(start2);

    assert.strictEqual(result, 241861950);
    console.log('- Test (sort): ' + result + ' [%dms]', hrend[1] / 1000000000);
});

const start3 = process.hrtime();
main('../inputs/input.txt', 2020, 2, false).then(result => {
    const hrend = process.hrtime(start3)
    console.log('- Part One (no sort): ' + result + ' [%dms]', hrend[1] / 1000000000);
});

const start4 = process.hrtime();
main('../inputs/input.txt', 2020, 2, true).then(result => {
    const hrend = process.hrtime(start4)
    console.log('- Part One (sort): ' + result + ' [%dms]', hrend[1] / 1000000000);
});

const start5 = process.hrtime();
main('../inputs/input2.txt', 2020, 3, false).then(result => {
    const hrend = process.hrtime(start5)
    console.log('- Part Two (no sort): ' + result + ' [%dms]', hrend[1] / 1000000000);
});

const start6 = process.hrtime();
main('../inputs/input2.txt', 2020, 3, true).then(result => {
    const hrend = process.hrtime(start6)
    console.log('- Part Two (sort): ' + result + ' [%dms]', hrend[1] / 1000000000);
});


