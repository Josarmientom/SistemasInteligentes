const Otello = {
    init(n) {
        this.size = n
        this.turn = 1
        this.rival = 2
        this.posibilities_array = []
        this.board(n)
        this.start_game()
        this.print()
        this.posibilities()
    },
    board(n) {
        matrix = []
        for (let i = 0; i < n; i++) {
            matrix.push([])
            for (let j = 0; j < n; j++) {
                matrix[i].push(0)
            }
        }
        this.matrix = matrix
    },
    start_game() {
        let n = this.size
        this.matrix[Math.floor(n / 2) - 1][Math.floor(n / 2) - 1] = 1
        this.matrix[Math.floor(n / 2)][Math.floor(n / 2)] = 1
        this.matrix[Math.floor(n / 2) - 1][Math.floor(n / 2)] = 2
        this.matrix[Math.floor(n / 2)][Math.floor(n / 2) - 1] = 2
    },
    print() {
        for (let i = 0; i < this.matrix.length; i++) {
            console.log(this.matrix[i])
        }
    },
    play(i, j) {
        //if (!([i, j] in this.posibilities_array)) {
        //    console.log('Invalid move')
        //    return
        //}
        this.matrix[i][j] = this.turn
        this.change(i, j, 'up')
        this.change(i, j, 'down')
        this.change(i, j, 'right')
        this.change(i, j, 'upright')
        this.change(i, j, 'upleft')
        this.change(i, j, 'left')
        this.change(i, j, 'downleft')
        this.change(i, j, 'downright')
        this.print()
        let tmp = this.turn
        this.turn = this.rival
        this.rival = tmp
        this.posibilities()
    },
    posibilities() {
        this.posibilities_array = []
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                if (this.matrix[i][j] == this.turn) {
                    this.check(0, i, j, 'up')
                    this.check(0, i, j, 'down')
                    this.check(0, i, j, 'right')
                    this.check(0, i, j, 'upright')
                    this.check(0, i, j, 'upleft')
                    this.check(0, i, j, 'left')
                    this.check(0, i, j, 'downleft')
                    this.check(0, i, j, 'downright')
                }
            }
        }
    },
    check(count, i, j, dir) {
        if (dir == 'up'){
            if (j + 1 < this.size){
                if (this.matrix[i][j + 1] == 0 && count > 0) {
                    if (!([i, j + 1] in this.posibilities_array)) {
                        this.posibilities_array.push([i, j + 1])
                    }
                }
                else if (this.matrix[i][j + 1] == this.rival) {
                    this.check(count + 1, i, j + 1, dir)
                }
            }
        } else if (dir == 'down'){
            if (j - 1 >= 0){
                if (this.matrix[i][j - 1] == 0 && count > 0) {
                    if (!([i, j - 1] in this.posibilities_array)) {
                        this.posibilities_array.push([i, j - 1])
                    }
                }
                else if (this.matrix[i][j - 1] == this.rival) {
                    this.check(count + 1, i, j - 1, dir)
                }
            }
        } else if (dir == 'right'){
            if (i + 1 < this.size){
                if (this.matrix[i + 1][j] == 0 && count > 0) {
                    if (!([i + 1, j] in this.posibilities_array)) {
                        this.posibilities_array.push([i + 1, j])
                    }
                }
                else if (this.matrix[i + 1][j] == this.rival) {
                    this.check(count + 1, i + 1, j, dir)
                }
            }
        } else if (dir == 'left'){
            if (i - 1 >= 0){
                if (this.matrix[i - 1][j] == 0 && count > 0) {
                    if (!([i - 1, j] in this.posibilities_array)) {
                        this.posibilities_array.push([i - 1, j])
                    }
                }
                else if (this.matrix[i - 1][j] == this.rival) {
                    this.check(count + 1, i - 1, j, dir)
                }
            }
        } else if (dir == 'upleft'){
            if (i - 1 >= 0 && j + 1 < this.size){
                if (this.matrix[i - 1][j + 1] == 0 && count > 0) {
                    if (!([i - 1, j + 1] in this.posibilities_array)) {
                        this.posibilities_array.push([i - 1, j + 1])
                    }
                }
                else if (this.matrix[i - 1][j + 1] == this.rival) {
                    this.check(count + 1, i - 1, j + 1, dir)
                }
            }
        } else if (dir == 'upright'){
            if (i + 1 < this.size && j + 1 < this.size){
                if (this.matrix[i + 1][j + 1] == 0 && count > 0) {
                    if (!([i + 1, j + 1] in this.posibilities_array)) {
                        this.posibilities_array.push([i + 1, j + 1])
                    }
                }
                else if (this.matrix[i + 1][j + 1] == this.rival) {
                    this.check(count + 1, i + 1, j + 1, dir)
                }
            }
        } else if (dir == 'downleft'){
            if (i - 1 >= 0 && j - 1 >= 0){
                if (this.matrix[i - 1][j - 1] == 0 && count > 0) {
                    if (!([i - 1, j - 1] in this.posibilities_array)) {
                        this.posibilities_array.push([i - 1, j - 1])
                    }
                }
                else if (this.matrix[i - 1][j - 1] == this.rival) {
                    this.check(count + 1, i - 1, j - 1, dir)
                }
            }
        } else if (dir == 'downright'){
            if (i + 1 < this.size && j - 1 >= 0){
                if (this.matrix[i + 1][j - 1] == 0 && count > 0) {
                    if (!([i + 1, j - 1] in this.posibilities_array)) {
                        this.posibilities_array.push([i + 1, j - 1])
                    }
                }
                else if (this.matrix[i + 1][j - 1] == this.rival) {
                    this.check(count + 1, i + 1, j - 1, dir)
                }
            }
        }
    },
    change(i, j, dir) {
        if( dir == 'up'){
            if (j + 1 < this.size){
                if (this.matrix[i][j + 1] == this.rival) {
                    this.matrix[i][j + 1] = this.turn
                    this.change(i, j + 1, dir)
                }
            }
        } else if (dir == 'down'){
            if (j - 1 >= 0){
                if (this.matrix[i][j - 1] == this.rival) {
                    this.matrix[i][j - 1] = this.turn
                    this.change(i, j - 1, dir)
                }
            }
        } else if (dir == 'right'){
            if (i + 1 < this.size){
                if (this.matrix[i + 1][j] == this.rival) {
                    this.matrix[i + 1][j] = this.turn
                    this.change(i + 1, j, dir)
                }
            }
        } else if (dir == 'left'){
            if (i - 1 >= 0){
                if (this.matrix[i - 1][j] == this.rival) {
                    this.matrix[i - 1][j] = this.turn
                    this.change(i - 1, j, dir)
                }
            }
        } else if (dir == 'upleft'){
            if (i - 1 >= 0 && j + 1 < this.size){
                if (this.matrix[i - 1][j + 1] == this.rival) {
                    this.matrix[i - 1][j + 1] = this.turn
                    this.change(i - 1, j + 1, dir)
                }
            }
        } else if (dir == 'upright'){
            if (i + 1 < this.size && j + 1 < this.size){
                if (this.matrix[i + 1][j + 1] == this.rival) {
                    this.matrix[i + 1][j + 1] = this.turn
                    this.change(i + 1, j + 1, dir)
                }
            }
        } else if (dir == 'downleft'){
            if (i - 1 >= 0 && j - 1 >= 0){
                if (this.matrix[i - 1][j - 1] == this.rival) {
                    this.matrix[i - 1][j - 1] = this.turn
                    this.change(i - 1, j - 1, dir)
                }
            }
        } else if (dir == 'downright'){
            if (i + 1 < this.size && j - 1 >= 0){
                if (this.matrix[i + 1][j - 1] == this.rival) {
                    this.matrix[i + 1][j - 1] = this.turn
                    this.change(i + 1, j - 1, dir)
                }
            }
        }
    }

}

Otello.init(8)
for (i = 0; i < Otello.size; i++) {
    console.log(Otello.posibilities_array[i])
}
Otello.play(3, 5)
for (i = 0; i < Otello.size; i++) {
    console.log(Otello.posibilities_array[i])
}
Otello.play(2, 5)
