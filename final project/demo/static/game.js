// Getting skin and level
const skinName = document.getElementById("skin").innerHTML
const levelId = document.getElementById("level").innerHTML

// Setting up for every level




// Canvas
const canvas = document.getElementById('gameCanvas')
const ctx = canvas.getContext('2d')
canvas.width = 800
canvas.height = 500
canvas.style.background = "linear-gradient(to bottom, lightblue, #548b85, black)"

if(levelId == 2)
{
    canvas.width = 1000
    canvas.height = 550
    canvas.style.background = "linear-gradient(to bottom, lightblue, rgb(139 135 84), black)"
}
else if(levelId == 3)
{
    canvas.width = 1200
    canvas.height = 700
    canvas.style.background = "linear-gradient(to bottom, #70bae7, rgb(4 40 5), rgb(4 40 5), black)"
}
else if(levelId == 4)
{
    canvas.width = 1200
    canvas.height = 700
    canvas.style.background = "linear-gradient(to bottom, rgb(27 175 86), rgb(0 0 0), rgb(4, 40, 5), black)"
}
else if(levelId == 5)
{
    canvas.width = screen.width
    canvas.height = 5 * screen.height / 6
    canvas.style.background = "linear-gradient(to bottom, rgb(203 34 34), rgb(0, 0, 0), rgb(149 17 17), black)"
}

let moneyMultiplier = 1
let score = 0
let gameFrame = 0
let gameSpeed = 1
let gameOver = false
let playerSpeed = 1
let lives = 3
let frameSpeed = 80
let frameSpeedTrash = 70
let moneySkinMultiplier = 1
let levelVariable = 100
let levelVariable2 = 0

ctx.font = '40px Georgia'

if(levelId == 2)
{
    moneyMultiplier = 5
    levelVariable = 150
}
else if(levelId == 3)
{
    moneyMultiplier = 25
    levelVariable = 200
    levelVariable2 = 200
}
else if(levelId == 4)
{
    moneyMultiplier = 125
    levelVariable = 200
    levelVariable2 = 200
}
else if(levelId == 5)
{
    moneyMultiplier = 450
    levelVariable = 300
    levelVariable2 = 400
}

// Mouse
let canvasPosition = canvas.getBoundingClientRect()
const mouse =
{
    x: canvas.width / 2,
    y: canvas.height / 2,
    click: false
}
canvas.addEventListener("mousedown", function(event){
    mouse.click = true
    mouse.x = event.x - canvasPosition.left
    mouse.y = event.y - canvasPosition.top
})
canvas.addEventListener("mouseup", function(){
    mouse.click = false
})


// Fish
const fishLeft = new Image()
fishLeft.src = 'static/fishSprite1.png'
const fishRight = new Image()
fishRight.src = 'static/fishSprite2.png'


// Setting skins up
if(skinName == "Dream")
{
    fishLeft.src= 'static/DreamSprite1.png'
    fishRight.src= 'static/DreamSprite2.png'
    lives = 23
    playerSpeed = 5
    moneySkinMultiplier = 50
}
else if(skinName == "Duck")
{
    fishLeft.src= 'static/DuckSprite1.png'
    fishRight.src= 'static/duckSprite2.png'
    lives = 99
    playerSpeed = 9
    moneySkinMultiplier = 99999
}
else if(skinName == "mrFish")
{
    fishLeft.src= 'static/mrFishSprite1.png'
    fishRight.src= 'static/mrFishSprite2.png'
    lives = 1
    playerSpeed = 2
    moneySkinMultiplier = 1500
}
else if(skinName == "fishRober")
{
    fishLeft.src= 'static/fishRoberSprite1.png'
    fishRight.src= 'static/fishRoberSprite2.png'
    lives = 10
    playerSpeed = 2
    moneySkinMultiplier = 1
}
else if(skinName == "gangstaFish")
{
    fishLeft.src= 'static/gangstaFishSprite1.png'
    fishRight.src= 'static/gangstaFishSprite2.png'
    moneySkinMultiplier = 2
}
else if(skinName == "deadFish")
{
    fishLeft.src= "static/deadFishSprite1.png"
    fishRight.src= 'static/deadFishSprite2.png'
    lives = 6
}
else if(skinName == "blobFish")
{
    fishLeft.src= 'static/blobFishSprite1.png'
    fishRight.src= 'static/blobFishSprite2.png'
    moneySkinMultiplier = 5
}
else if(skinName == "catfish")
{
    fishLeft.src= 'static/catfishSprite1.png'
    fishRight.src= 'static/catfishSprite2.png'
    moneySkinMultiplier = 2
}
else if(skinName == "Betafish")
{
    fishLeft.src = 'static/BetafishSprite1.png'
    fishRight.src = 'static/betaFishSprite2.png'
    moneySkinMultiplier = 5
    lives = 9
}
else if(skinName == "FlyingFish")
{
    fishLeft.src = 'static/FlyingFishSprite1.png'
    fishRight.src = 'static/flyingFishSprite2.png'
    moneySkinMultiplier = 10
    lives = 1
    playerSpeed = 3
}
else if(skinName == "Turtle")
{
    fishLeft.src = 'static/TurtleSprite1.png'
    fishRight.src = 'static/turtleSprite2.png'
    moneySkinMultiplier = 25
    lives = 9
    playerSpeed = 0.5
}
else if(skinName == "jellyfish")
{
    fishLeft.src = 'static/jellyfishSprite1.png'
    fishRight.src = 'static/jellyfishSprite2.png'
    moneySkinMultiplier = 10
    lives = 3
    playerSpeed = 0.2
}
else if(skinName == "Shark")
{
    fishLeft.src = 'static/SharkSprite1.png'
    fishRight.src = 'static/SharkSprite2.png'
    moneySkinMultiplier = 25
    playerSpeed = 3
}
else if(skinName == "fishMusk")
{
    fishLeft.src = 'static/fishMuskSprite1.png'
    fishRight.src = 'static/fishMuskSprite2.png'
    moneySkinMultiplier = 150
    playerSpeed = 5
}
else if(skinName == "DevFish")
{
    fishLeft.src = 'static/DevFishSprite1.png'
    fishRight.src = 'static/DevFishSprite2.png'
    lives = 420
    playerSpeed = 21
    moneySkinMultiplier = 1000
}

class Fish
{
    constructor()
    {
        this.x = canvas.width / 2
        this.y = canvas.height / 2
        this.radius = 50
        this.angle = 0
        this.frameX = 0
        this.frameY = 0
        this.frame = 0
        this.spriteWidth = 498
        this.spriteHeight = 327
    }
    update()
    {
        const dx = this.x - mouse.x
        const dy = this.y - mouse.y
        if(mouse.x != this.x)
        {
            this.x -= (dx * playerSpeed / 40)
        }
        if(mouse.y != this.y)
        {
            this.y -= (dy * playerSpeed / 40)
        }
        let theta = Math.atan2(dy, dx)
        this.angle = theta
    }
    draw()
    {
        if(mouse.click)
        {
            ctx.lineWidth = 0.1
            ctx.beginPath()
            ctx.moveTo(this.x, this.y)
            ctx.lineTo(mouse.x, mouse.y)
            ctx.stroke()
        }

        /*ctx.fillStyle = 'red'
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2)
        ctx.fill()
        ctx.closePath()*/

        //ctx.fillRect(this.x, this.y, this.radius, 10)

        // Controlling fish rotation movement
        ctx.save()
        ctx.translate(this.x, this.y)
        ctx.rotate(this.angle)
        if(this.x >= mouse.x)
        {
            ctx.drawImage(fishLeft, this.frameX * this.spriteWidth, this.frameY * this.spriteHeight,
                this.spriteWidth, this.spriteHeight, 0 - 65, 0 - 50, this.spriteWidth / 3.4, this.spriteHeight / 3.4)
        }
        else
        {
            ctx.drawImage(fishRight, this.frameX * this.spriteWidth, this.frameY * this.spriteHeight,
                this.spriteWidth, this.spriteHeight, 0 - 65, 0 - 50, this.spriteWidth / 3.4, this.spriteHeight / 3.4)
        }
        ctx.restore()
    }
}
const fish = new Fish()

// Coins
const coinsArray = []
const coinImage = new Image()
coinImage.src = 'static/fishCoin.png'
const coinImage5 = new Image()
coinImage5.src = 'static/fishCoin5.png'
const coinImage10 = new Image()
coinImage10.src = 'static/fishCoin10.png'

class Coins
{
    constructor()
    {
        this.x = Math.random() * canvas.width
        this.y = (Math.random() * canvas.height - 450) - levelVariable2
        this.radius = 15
        this.speed = -(Math.random() * 6 + 1) * gameSpeed
        this.distance = 1000
        this.counted = false
        this.sound = 'coinSound'
        this.value = Math.random()
        if(levelId == 1 || levelId == 2 || levelId == 3)
        {
            if(this.value < 0.2)
            {
                this.value = 5
            }
            else
            {
                this.value = 1
            }
        }
        else{
            if(this.value < 0.2)
            {
                this.value = 5
            }
            else if(this.value > 0.2 && this.value < 0.25)
            {
                this.value = 10
            }
            else
            {
                this.value = 1
            }
        }
    }
    update()
    {
        this.y -= this.speed
        const dx = this.x - fish.x
        const dy = this.y - fish.y
        this.distance = Math.sqrt(dx*dx + dy*dy)
    }
    draw()
    {
        /*ctx.fillStyle = 'transparent'
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2)
        ctx.fill()
        ctx.closePath()
        ctx.stroke()*/
        if(this.value == 1)
        {
            ctx.drawImage(coinImage, this.x - 29, this.y - 19, 60, 45)
        }
        else if(this.value == 5)
        {
            ctx.drawImage(coinImage5, this.x - 29, this.y - 19, 60, 45)
        }
        else if(this.value == 10)
        {
            ctx.drawImage(coinImage10, this.x - 29, this.y - 19, 60, 45)
        }
    }
}

const coinSound = document.createElement('audio')
coinSound.src = '/static/coin.wav'

// Trash
const trashArray = []
const trashPlasticBag = new Image()
trashPlasticBag.src = 'static/plasticBag.png'
const trashMetalCan = new Image()
trashMetalCan.src = 'static/metalCan.png'
const trashBag = new Image()
trashBag.src = 'static/trashBag.png'
const nuclearWaste = new Image()
nuclearWaste.src = 'static/nuclearWaste.png'
const fishingNet = new Image()
fishingNet.src = 'static/fishingNet.png'
class Trash
{
    constructor()
    {
        this.x = Math.random() * canvas.width
        this.y = (Math.random() * canvas.height - 450) - levelVariable2
        this.radius = Math.random()

        if(levelId == 1 || levelId == 2 || levelId == 3)
        {
            if(this.radius < 0.3)
            {
                this.radius = 20
            }
            else if(this.radius > 0.3 && this.radius < 0.6)
            {
                this.radius = 30
            }
            else
            {
                this.radius = 40
            }
        }
        else if(levelId == 4)
        {
            if(this.radius < 0.25){
                this.radius = 20
            }
            else if(this.radius > 0.25 && this.radius < 0.5){
                this.radius = 30
            }
            else if(this.radius > 0.5 && this.radius < 0.75){
                this.radius = 40
            }
            else{
                this.radius = 50
            }
        }
        else{
            if(this.radius < 0.2){
                this.radius = 20
            }
            else if(this.radius > 0.2 && this.radius < 0.4){
                this.radius = 30
            }
            else if(this.radius > 0.4 && this.radius < 0.6){
                this.radius = 40
            }
            else if(this.radius > 0.6 && this.radius < 0.8){
                this.radius = 50
            }
            else{
                this.radius = 60
            }
        }

        this.speed = - (Math.random() * 5 + 1) * gameSpeed
        this.distance = 1000
        this.counted = false
        this.sound = trashSound
    }
    update()
    {
        this.y -= this.speed
        const dx = this.x - fish.x
        const dy = this.y - fish.y
        this.distance = Math.sqrt(dx*dx + dy*dy)
    }
    draw()
    {
        /*ctx.fillStyle = 'blue'
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2)
        ctx.fill()
        ctx.closePath()
        ctx.stroke()*/
        if(this.radius == 40)
        {
            ctx.drawImage(trashBag, this.x - 45, this.y - 60, 100, 100)
        }
        else if(this.radius == 30)
        {
            ctx.drawImage(trashPlasticBag, this.x - 35, this.y - 45, 80, 80)
        }
        else if(this.radius == 20)
        {
            ctx.drawImage(trashMetalCan, this.x - 35, this.y - 45, 70, 70)
        }
        else if(this.radius == 50)
        {
            ctx.drawImage(nuclearWaste, this.x - 50, this.y - 50, 100, 100)
        }
        else{
            ctx.drawImage(fishingNet, this.x - 55, this.y - 55, 120, 120)
        }
    }
}

const trashSound = document.createElement('audio')
trashSound.src = '/static/TailWhip.flac'

function handleCoins()
{
    if(gameFrame % frameSpeed == 0)
    {
        coinsArray.push(new Coins())
    }
    if(gameFrame % 120 == 0)
    {
        gameSpeed += 0.1
    }
    if(gameFrame % 50 == 0)
    {
        frameSpeed--
        if(frameSpeed <= 0)
        {
            frameSpeed = 80
        }
    }
    if(skinName == 'fishRober')
    {
        if(gameFrame % 4 == 0)
        {
            score += 75 * moneyMultiplier
        }
    }
    for(let i = 0; i < coinsArray.length; i++)
    {
        coinsArray[i].draw()
        coinsArray[i].update()
        if(coinsArray[i].y > 700)
        {
            coinsArray.splice(i, 1)
            i--
        }
        if(coinsArray[i])
        {
            if(coinsArray[i].distance != null)
            {
                if(coinsArray[i].distance < coinsArray[i].radius + fish.radius)
                {
                    if(!coinsArray[i].counted)
                    {
                        score += moneyMultiplier * moneySkinMultiplier * coinsArray[i].value
                        coinsArray[i].counted = true
                        coinsArray.splice(i, 1)
                        coinSound.play()
                        i--
                    }
                }
            }
        }
    }
}

function handleTrash()
{
    if(gameFrame % frameSpeedTrash == 0)
    {
        trashArray.push(new Trash())
    }
    if(gameFrame % 50 == 0)
    {
        frameSpeedTrash--
        if(frameSpeedTrash <= 0)
        {
            frameSpeedTrash = 70
        }
    }
    for(let i = 0; i < trashArray.length; i++)
    {
        trashArray[i].draw()
        trashArray[i].update()
        if(trashArray[i].y > 700)
        {
            trashArray.splice(i, 1)
            i--
        }
        if(trashArray[i])
        {
            if(trashArray[i].distance != null)
            {
                if(trashArray[i].distance < trashArray[i].radius + fish.radius)
                {
                    if(!trashArray[i].counted)
                    {
                        if(skinName == 'catfish')
                        {
                            if(trashArray[i].radius == 20)
                            {
                                if(trashArray[i].counted == false)
                                {
                                    score += 10 * moneyMultiplier
                                    trashArray[i].counted = true
                                    trashArray.splice(i, 1)
                                    coinSound.play()
                                    i--
                                }

                            }
                            else{
                                if(trashArray[i].radius == 20 || trashArray[i].radius == 30 || trashArray[i].radius == 40)
                                {
                                    lives--
                                }
                                else if(trashArray[i].radius == 50)(
                                    lives -= 3
                                )
                                else{
                                    lives -= 5
                                }

                                if(lives < 1)
                                {
                                    handleGameOver()
                                }
                                trashArray[i].counted = true
                                trashArray.splice(i, 1)
                                trashSound.play()
                                i--
                            }
                        }
                        else{
                            if(trashArray[i].radius == 20 || trashArray[i].radius == 30 || trashArray[i].radius == 40)
                            {
                                lives--
                            }
                            else if(trashArray[i].radius == 50)(
                                lives -= 3
                            )
                            else{
                                lives -= 5
                            }
                            if(lives < 1)
                            {
                                handleGameOver()
                            }
                            trashArray[i].counted = true
                            trashArray.splice(i, 1)
                            trashSound.play()
                            i--
                        }
                    }
                }
            }
        }
    }
}

// Repeating backgrounds
const background = new Image()
background.src = 'static/background1.png'

const BG =
{
    x1: 0,
    x2: canvas.width,
    y: 0,
    width: canvas.width,
    height: canvas.height
}

function handleBackground()
{
    BG.x1 -= gameSpeed
    if(BG.x1 < - BG.width)
    {
        BG.x1 = BG.width
    }
    BG.x2 -=gameSpeed
    if(BG.x2 < - BG.width)
    {
        BG.x2 = BG.width
    }
    ctx.drawImage(background, BG.x1, BG.y, BG.width, BG.height)
    ctx.drawImage(background, BG.x2, BG.y, BG.width, BG.height)
}

// Game over
function handleGameOver()
{
    ctx.fillStyle = 'white'
    ctx.fillText('GAME OVER, you collected ' + score + ' coins', 130, 250)
    gameOver = true

}

// Animation
function animate()
{
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    handleBackground()
    fish.draw()
    fish.update()
    ctx.fillStyle = "black"
    ctx.fillText("score: " + score, 10, 45)
    ctx.fillText("lives: " + lives, (2 * canvas.width / 3) + levelVariable, 45)
    if(trashArray != null)
    {
        handleTrash()
    }
    if(coinsArray != null)
    {
        handleCoins()
    }
    gameFrame++
    if(!gameOver)
    {
        requestAnimationFrame(animate)
    }
    else
    {
        document.getElementById("coinTotalId").value = score
        document.formCoins.submit()
    }
}
animate()


canvas.addEventListener("resize", function(){
    canvasPosition = canvas.getBoundingClientRect()
})