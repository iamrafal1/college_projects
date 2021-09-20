let canvas;
let context;
let height;
let width;
let point;
let direction;
let counter = 0;
let snake = {
    x : 10,
    y : 250,
    size : 10,
    xChange : 0,
    yChange : 0,
    dir : ''
};
let tail = [];
let interval_id;
let snack = {
    x : getRandomNumber(10, 490),
    y : getRandomNumber(10, 490),
    size : 10
};
let moveRight = false;
let moveUp = false;
let moveDown = false;
let moveLeft = false;
let score = 0;
let accumulator = 0;
let turnsy = [];
let turnsx = [];
let length = 1;
let adder = 0;

document.addEventListener('DOMContentLoaded', init, false);

function init() {
    canvas = document.querySelector('canvas');
    context = canvas.getContext('2d');
    width = canvas.width;
    height = canvas.height;
    let body_element = document.querySelector('body');
    let new_p_element = document.createElement('p');
    let new_text = document.createTextNode('Your score is:' + score);
    let new_p_element1 = document.createElement('p');
    let new_text1 = document.createTextNode('Your length is:' + length);
    new_p_element.appendChild(new_text);
    body_element.appendChild(new_p_element);
    new_p_element1.appendChild(new_text1);
    body_element.appendChild(new_p_element1);
    window.addEventListener('keydown', activate, false);
    interval_id = window.setInterval(draw, 33);
}

function draw(){
    context.clearRect(0, 0, width, height);
    turnsx.push(snake.x);
    turnsy.push(snake.y);
    context.fillStyle = 'yellow';
    context.fillRect(snake.x, snake.y, snake.size, snake.size);
    accumulator = 0;
    if (tail.length !== 0){
        for (let p of tail){
            p.x = turnsx[accumulator] ;
            p.y = turnsy[accumulator] ;

            context.fillRect(p.x, p.y, p.size, p.size);
            accumulator += 1;
        }
    }
    if (adder === 1){
    adder = 0;
    }
    context.fillStyle = "red";
    context.fillRect(snack.x, snack.y, snack.size, snack.size);
    turnsx.shift();
    turnsy.shift();


    if (snake.x + snake.size >= width ||
        snake.x <= width- width ||
        snake.y + snake.size >= height
         || snake.y <= height- height) {
        stop();
        window.alert('You dead bruh. Your score was: ' + score + ' and your length was: ' + length);
        return;
    }
    if (moveRight){
        snake.x += 5;
        snake.dir = 'right';

    }
    if (moveUp){
        snake.y -= 5;
        snake.dir = 'up';

    }
    if (moveLeft){
        snake.x -= 5;
        snake.dir = 'left';
    }
    if (moveDown){
        snake.y += 5;
        snake.dir = 'down';
    }
    if (collides(snack)) {
        adder = 0;
        score += 100;
        length += 5;
        document.querySelector('p').innerHTML = 'Your score is:' + score;
        document.querySelector('p + p').innerHTML = 'Your length is:' + length;
        snack.x = roundToTen(getRandomNumber(10,490));
        snack.y = roundToTen(getRandomNumber(10,490));

        for (let i in tail){
            if (i.x === snack.x && i.y === snack.y){
                snack.x = roundToTen(snack.x * 0.5);
            }
        }
        for (let i in tail){
            if (i.x === snack.x && i.y === snack.y){
                snack.x = roundToTen(snack.x * 0.5);
            }
        }
        adder += 1;
        for (let i = 0; i < 5; i += 1){
            let point = {
                x : snake.x,
                y : snake.y,
                size : 10,
                pointCounter: counter,
                dir : snake.dir
                }
            tail.push(point);
            turnsx.push(snake.x);
            turnsy.push(snake.y);;
            counter += 1;
        }
    }
    if (collidesSelf(snake) && adder === 0) {
    stop();
    window.alert('You dead bruh. Your score was: ' + score + ' and your length was: ' + length);
    return;
    }

}


function stop() {
    clearInterval(interval_id);
}

function activate(event) {
    let keyCode = event.keyCode;
    if (keyCode === 38 && moveDown === false){
        moveUp = true
        moveRight = false
        moveDown = false
        moveLeft = false
    }
    else if (keyCode === 39 && moveLeft === false){
        moveUp = false
        moveRight = true
        moveDown = false
        moveLeft = false
        }
    else if (keyCode === 40 && moveUp === false){
        moveUp = false
        moveRight = false
        moveDown = true
        moveLeft = false
        }
    else if (keyCode === 37 && moveRight == false){
        moveUp = false
        moveRight = false
        moveDown = false
        moveLeft = true
        }
}

function collidesSelf(self){
    for (let i of tail){
            if (self.x === i.x && self.y === i.y){
                return true;}
        }
    }

function collides(snack) {
    if (snake.x + snake.size < snack.x ||
        snack.x + snack.size < snake.x ||
        snake.y > snack.y + snack.size ||
        snack.y > snake.y + snake.size) {
        return false;
    }
    else {
        return true;
    }
}

function getRandomNumber(min, max) {
return Math.floor(Math.random() * (max - min + 10)) + min;
}

function roundToTen(number) {
return Math.round(number / 10) * 10;
}
