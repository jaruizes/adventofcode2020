const fs = require('fs')
const assert = require('assert');

class Game {
    constructor(definition_file) {
        this.x = 0;
        this.y = 0;
        this.trees = 0;
        this.finished = false;
        this.board = this.read_board(definition_file);
    }

    move(offset_x, offset_y) {
        this.x = this.x + offset_x;

        while (this.x > this.board[0].length - 1) {
            this.expand_board();
        }

        this.y = this.y + offset_y;
        if (this.y > this.board.length - 1) {
            this.finished = true;
            return;
        }

        const row = this.board[this.y];
        if (row.charAt(this.x) === '#') {
            this.trees++;
        }

        return;
    }

    expand_board() {
        const expanded_board = [];
        for(let i = 0; i < this.board.length; i++) {
            const row = this.board[i];
            expanded_board.push(row.concat(row));
        }

        this.board = expanded_board;
    }

    count_trees() {
        return this.trees;
    }

    is_finished() {
        return this.finished;
    }

    read_board(definition_file) {
        const data = fs.readFileSync(definition_file);
        return data.toString().split("\n");
    }
}

const multiply = (numbers_solving_equation) => {
    let total = 1;
    numbers_solving_equation.forEach((number) => {
        total = total * number;
    });

    return total;
}

const play = (definition_file, movements, result_function) => {
    const trees = [];
    for (let i = 0; i < movements.length; i++) {
        const movement = movements[i];
        const game = new Game(definition_file);
        const offset_x = parseInt(movement[0]);
        const offset_y = parseInt(movement[1]);

        while (!game.is_finished()) {
            game.move(offset_x, offset_y);
        }

        trees.push(game.count_trees());
    }

    return result_function(trees);
}

assert.strictEqual(play('../inputs/test.txt', [[3, 1]], multiply), 7);
assert.strictEqual(play('../inputs/test.txt', [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]], multiply), 336);

console.log('Part one: ', play('../inputs/input.txt', [[3, 1]], multiply));
console.log('Part two: ', play('../inputs/input.txt', [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]], multiply));
