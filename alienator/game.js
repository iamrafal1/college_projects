let canvas;
let width;
let height;
let context;
let interval_id
let moveRight = false;
let moveUp = false;
let moveDown = false;
let moveLeft = false;
let baseWeapon = false;
let projectileSpeed = 10;
let projectiles = [];
let enemyProjectiles = [];
let shipSpeed = 7;
let player = {
    x : 240,
    y : 400,
    w : 50,
    l : 20
};
let lWing = {
    x : player.x - player.w +30,
    y : player.y + 20,
    w : 10,
    l : 20
};
let rWing = {
    x : player.x + player.w - 30,
    y : player.y + 20,
    w : 10,
    l : 20
};
let enemies = []
let lives = 3;
let level = 0;
let start = 0;
let colors = ["red","orange","yellow","green","blue","indigo","violet"]
let colorNumber = 0
let counter = 0;
let enemyXChange = 1;
let enemyYChange = 1;
let shootControl = 0;
let immunity = 29;
let shotAnimation = [];
let powerups = [];
let giftColor;
let weaponColor = "red";
let weaponLevel = 1
let tempShot = [];
let endChecker = 0;
let score = 0;

document.addEventListener('DOMContentLoaded', init, false);

function init() {
    canvas = document.querySelector('canvas');
    context = canvas.getContext('2d');
    width = canvas.width;
    height = canvas.height;
    window.addEventListener('keydown', activate, false);
    window.addEventListener('keyup', deactivate, false);
    interval_id = window.setInterval(draw, 33);
}

function draw() {
    context.clearRect(0, 0, width, height);
    context.font = "30px Arial";
    context.fillstyle = "white";
    context.fillText("Lives = " + lives, 350, 480);
    context.fillText("Score = " + score, 10, 480)
    context.fillText("" + (level + 1), 245, 30)

    //Checks if level ended (enemies are all dead - null)

    for (let j of enemies){
        if (j === null){
            endChecker += 1;
        }
    }
    if (endChecker === enemies.length && endChecker !== 0){
        level += 1;
        start = 0;
        enemyXChange = 1;
        enemyYChange = 1;
        counter = 0;
        enemies = [];
        projectiles = [];
        enemyProjectiles = [];
        shotAnimation = [];
        powerups = [];
        if (level % 5 === 0){
            lives += 1;
        }
        colorNumber += 1;
        if (colorNumber === 7){
            colorNumber =  0;
        }
        respawn();
        immunity = 29;
    }
    endChecker = 0;
    if (start === 0){
        enemyCreator();
        start = 1;
    }

    if (lives === 0) {
        stop();
        window.alert("You died! Your score was: " + (score + (level * 1000)))
        return;
    }

    if (immunity < 29){
      immunity += 1;
    }
    if (immunity % 3 !== 0){
        playerDraw();
    }
    weapons();
    collisionChecker();
    enemyDead()
    enemyDraw();

    //Animation for when enemy gets shot
    if (shotAnimation.length > 0){
        for (let i=0; i < shotAnimation.length; ++i){
            if (enemies[shotAnimation[i]] !== null){
            enemies[shotAnimation[i]].y += 5;
            }
            shotAnimation.splice(i, 1);
      }
    }
    enemyShooting();
    movement();
    enemyMovement();
}

//Checks if enemy died (hp <= 0)
function enemyDead(){
    for (let i=0; i < enemies.length; ++i) {
      if (enemies[i] === null){
          continue;
      }
      if (enemies[i].hp <= 0) {
              if (level % 5 !== 0){
                  score += 100
                }
              else{
                  score += 500
              }
              if (getRandomNumber(1,40) === 20){
                  let rand = getRandomNumber(1,3)
                  if (rand === 1){
                      giftColor = "red";
                  }
                  else if (rand === 2) {
                      giftColor = "yellow";
                  }
                  else if (rand === 3) {
                      giftColor = "green";
                  }
                  let gift = {
                      x: enemies[i].x,
                      y: enemies[i].y,
                      size: 10,
                      color: giftColor
                  };
                  powerups.push(gift);
              }
          enemies[i] = null;
          continue;
      }
    }
}

//returns object of each individual shot
function shot(){
  return{
      x: player.x + (player.l / 2),
      y: player.y,
      size: 2,
      dmg: 1
  }
}

//function that creates weapons and its upgrades
function weapons(){
  if (baseWeapon && shootControl === 0){
          for (let i=0; i < weaponLevel; ++i){
              tempShot.push(shot());
              if (i === 1){
                  tempShot[0].x = player.x;
                  tempShot[1].x = player.x + player.l;
              }
              else if (i === 2){
                  tempShot[2].x = player.x + (player.l / 2);
              }
              else if (i === 3){
                  tempShot[2].x = player.x + (player.l / 3);
                  tempShot[3].x = player.x + ((player.l / 3) * 2);
              }
              else if (i === 4){
                  tempShot[2].x = player.x + (player.l / 2);
                  tempShot[3].x = lWing.x;
                  tempShot[3].y = lWing.y + lWing.w;
                  tempShot[4].x = rWing.x + rWing.l;
                  tempShot[4].y = rWing.y + rWing.w;
              }
              else if (i === 5){
                  tempShot.push(shot());
                  tempShot[6].x = lWing.x + (lWing.l / 2);
                  tempShot[6].y = lWing.y + lWing.w;
                  tempShot[5].x = rWing.x + (rWing.l / 2);
                  tempShot[5].y = rWing.y + rWing.w;
                  break;
              }
          }
          for (let i=0; i < tempShot.length; ++i){
              projectiles.push(tempShot[i]);
          }
          tempShot = [];
          shootControl = 1;

  }
}

//draws player on canvas
function playerDraw(){
  context.fillStyle = "yellow";
  context.fillRect(player.x, player.y, player.l, player.w);
  context.fillRect(lWing.x, lWing.y, lWing.l, lWing.w);
  context.fillRect(rWing.x, rWing.y, rWing.l, rWing.w);
  context.fillStyle = "red";
  //draws bullets
  for (let i=0; i < projectiles.length; ++i){
      if (projectiles[i].y < 0 || projectiles[i].x < 0 || projectiles[i].x > width){
          projectiles.splice(i, 1);
      }
      else {
        projectiles[i].y -= projectileSpeed;
        context.fillRect(projectiles[i].x,projectiles[i].y,projectiles[i].size,projectiles[i].size )
      }
    }
  //draws powerups and checks if they collide with ship
  if (powerups){
      for (let i=0; i < powerups.length; ++i){
          if (powerups[i].y > height){
              powerups.splice(i, 1);
              continue;
          }
          if (shipCollision(player, powerups[i]) ||
              shipCollision(rWing, powerups[i]) ||
              shipCollision(lWing, powerups[i])){
                  if (powerups[i].color === "red"){
                      score += 1000
                      if (weaponLevel < 7){
                      weaponLevel += 1;
                    }
                  }
                  else if (powerups[i].color === "green"){
                      score += 1000;
                  }
                  else if (powerups[i].color === "yellow"){
                      score += 1000;
                  }
                  powerups.splice(i, 1);
                  continue;
              }
              powerups[i].y += 5;
              context.fillStyle = powerups[i].color;
              context.fillRect(powerups[i].x, powerups[i].y, powerups[i].size, powerups[i].size);
      }
  }
}

//Creates enemy shooting for normal enemies and bosses
function enemyShooting(){
    if (level % 5 !== 4){
        for (let i=0; i < enemies.length; ++i){
            if (enemies[i] === null){
                continue;
            }
            if (getRandomNumber(1,(1000 - (10 * level))) === 50) {
                let shot = {
                    x: enemies[i].x + 7,
                    y: enemies[i].y,
                    size: 6
                };
                enemyProjectiles.push(shot);
            }
        }
    }
    else{
      for (let i=0; i < enemies.length; ++i){
          if (enemies[i] === null){
              continue;
          }
          if (getRandomNumber(1,50) === 3) {
              let shot = {
                  x: enemies[i].x + getRandomNumber(0, enemies[i].size),
                  y: enemies[i].y + getRandomNumber(100, enemies[i].size),
                  size: 50
              };
              enemyProjectiles.push(shot);
          }
      }
    }
    for (let i=0; i < enemyProjectiles.length; ++i){
        context.fillStyle = "white";
        context.fillRect(enemyProjectiles[i].x,enemyProjectiles[i].y,enemyProjectiles[i].size,enemyProjectiles[i].size);
        enemyProjectiles[i].y += 2;
        if (enemyProjectiles[i].y >= height){
            enemyProjectiles.splice(i, 1);
        }
    }

}

//respawns player
function respawn() {
  player.x = 240;
  player.y = 400;
  lWing.x = player.x - player.w +30;
  lWing.y = player.y + 20 ;
  rWing.x = player.x + player.w - 30;
  rWing.y = player.y + 20
  immunity = 0;
}
//Checks collision of various game elements
function collisionChecker() {

    for (let i=0; i < enemies.length; ++i) {
        if (enemies[i] === null){
            continue;
        }
        if (immunity >= 29){
            if (shipCollision(player, enemies[i]) ||
                shipCollision(rWing, enemies[i]) ||
                shipCollision(lWing, enemies[i])) {
                lives -= 1;
                weaponLevel -= 3;
                if (weaponLevel < 1){
                    weaponLevel = 1
                }
                respawn();
            }
        }
        for (let j=0; j < projectiles.length; ++j) {
            if (collision(projectiles[j], enemies[i])) {
                projectiles.splice(j, 1);
                enemies[i].hp -= 1;
                if (enemies[i]){
                    shotAnimation.push(i);
                    enemies[i].y -= 5;
                }
            }
        }
    }
    if (immunity >= 29){
        for (let i=0; i < enemyProjectiles.length; ++i) {
            if (shipCollision(player, enemyProjectiles[i]) ||
                shipCollision(rWing, enemyProjectiles[i]) ||
                shipCollision(lWing, enemyProjectiles[i])){
                  enemyProjectiles.splice(i, 1);
                  lives -= 1;
                  respawn();
                }
        }
}   }

//checks collision between square target and unit
function collision(unit, target) {
  if (unit.x + unit.size < target.x ||
      target.x + target.size < unit.x ||
      unit.y > target.y + target.size ||
      target.y > unit.y + unit.size) {
      return false;
  }
  else {
      return true;
  }
}

//checks collision between rectangular unit and square target
function shipCollision(unit, target) {
  if (unit.x + unit.l < target.x ||
      target.x + target.size < unit.x ||
      unit.y > target.y + target.size ||
      target.y > unit.y + unit.w) {
      return false;
  }
  else {
      return true;
  }
}

//Creates enemies per level
function enemyCreator(){
    let xChange = 0;
    let yChange = 0;
    if (level % 5 === 0){
        for (let i = 0; i < 40; i += 1){
          if (i === 10 || i === 20 || i ==30){
              yChange += 40
              xChange = 0
          }
          let enemy = {
             x: 20 + xChange,
             y: 50 + yChange,
             size: 20,
             hp: 5 + (5*level)
          }
          if (enemy.hp > 100){
              enemy.hp = 100
          }
        xChange += 40;
        enemies.push(enemy);
        }
    }
    else if(level % 5 === 4){
            let boss = {
                x: 100,
                y: 100,
                size: 200,
                hp: 100 + (10*level),
            }
            enemies.push(boss)
      }
    else if (level % 5 === 1){
            for (let i = 0; i < 40; i += 1){
              if (i === 10 || i === 20 || i ==30){
                  yChange += 40
                  xChange = 0
              }
              let enemy = {
                 x: 60 + xChange,
                 y: 50 + yChange,
                 size: 20,
                 hp: 5 + (5*level)
              }
              if (enemy.hp > 100){
                  enemy.hp = 100
              }
            xChange += 40;
            enemies.push(enemy);
          }
      }
    else if (level % 5 === 2){
        for (let i = 0; i < 40; i += 1){
          if (i === 10 || i === 20 || i ==30){
              yChange += 40
              xChange = 0
          }
          let enemy = {
             x: 20 + xChange,
             y: 50 + yChange,
             size: 20,
             hp: 5 + (5*level)
          }
          if (enemy.hp > 100){
              enemy.hp = 100
          }
        xChange += 40;
        enemies.push(enemy);
        }
    }
    else if (level % 5 === 3){
          for (let i = 0; i < 80; i += 1){
            if (i % 10 === 0){
                yChange += 20
                xChange = 0
            }
            let enemy = {
               x: 20 + xChange,
               y: 50 + yChange,
               size: 10,
               hp: 5 + (5*level)
            }
            if (enemy.hp > 100){
                enemy.hp = 100
            }
          xChange += 40;
          enemies.push(enemy);
          }
    }
}

//Moves enemies
function enemyMovement(){
    if (level % 5 === 0){
        for (let j of enemies){
            if (j === null){
                continue;
            }
            j.x += enemyXChange;
            }
            if (counter < 80){
                counter += 1;
            }
            else{
                counter = 0;
                enemyXChange *= -1
            }
    }
    else if(level % 5 === 1){
        for (let j of enemies){
            if (j === null){
                continue;
            }
            j.y += enemyYChange;
            }
            if (counter < 100){
                counter += 1;
            }
            else{
                counter = 0;
                enemyYChange *= -1
            }
    }
    else if(level % 5 === 2){
        for (let j of enemies){
            if (j === null){
                continue;
            }
            j.y += enemyYChange;
            j.x += enemyXChange;
            }
            if (counter < 80){
                counter += 1;
            }
            else{
                counter = 0;
                enemyYChange *= -1;
                enemyXChange *= -1;
            }
        }
    else if(level % 5 === 3){
        for (let j of enemies){
            if (j === null){
                continue;
            }
                j.y += enemyYChange;
                j.x += enemyXChange;
                }
                if (counter < 80){
                    counter += 1;
                }
                else{
                    counter = 0;
                    enemyXChange *= -1;
                    enemyYChange *= -1;
                }
      }
      else if (level % 5 === 4){
        for (let j of enemies){
            if (j === null){
                continue;
            }
                j.x += enemyXChange;
                }
                if (counter < 80){
                    counter += 1;
                }
                else{
                    counter = 0;
                    enemyXChange *= -1;
                }
      }
}

//Draws enemies
function enemyDraw(){
  context.fillStyle = "" + colors[colorNumber]
  for (let j of enemies){
      if (j === null){
          continue;
      }
      context.fillRect(j.x,j.y,j.size,j.size )
  }
}

//Moves player
function movement(){
  if (moveRight){
      if (rWing.x + rWing.l < 500){
          player.x += shipSpeed;
          rWing.x += shipSpeed;
          lWing.x += shipSpeed;
      }
  }
  if (moveLeft){
      if (lWing.x > 0){
          player.x -= shipSpeed;
          rWing.x -= shipSpeed;
          lWing.x -= shipSpeed;
      }
  }
  if (moveUp){
      if (player.y > 50){
          player.y -= shipSpeed;
          rWing.y -= shipSpeed;
          lWing.y -= shipSpeed;
      }
  }
  if (moveDown){
      if (player.y + player.w < 450){
          player.y += shipSpeed;
          rWing.y += shipSpeed;
          lWing.y += shipSpeed;
      }
  }
}

function activate(event){
    let keyCode = event.keyCode;
    if (keyCode === 38){
        moveUp = true;
    }
    else if (keyCode === 39){
        moveRight = true
    }
    else if (keyCode === 40){
        moveDown = true
    }
    else if (keyCode === 37){
        moveLeft = true
    }
    else if (keyCode === 32){
        baseWeapon = true
    }
}
function deactivate(event){
    let keyCode = event.keyCode;
    if (keyCode === 38){
        moveUp = false
    }
    else if (keyCode === 39){
        moveRight = false
    }
    else if (keyCode === 40){
        moveDown = false
    }
    else if (keyCode === 37){
        moveLeft = false
    }
    else if (keyCode === 32){
        baseWeapon = false
        shootControl = 0
    }
}

function stop() {
  clearInterval(interval_id);
  window.removeEventListener('keydown', activate);
  window.removeEventListener('keyup', deactivate);
}




function getRandomNumber(min, max) {
return Math.floor(Math.random() * (max - min + 1)) + min;
}
