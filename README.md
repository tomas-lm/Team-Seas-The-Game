# TEAM SEAS - THE GAME
#### Video Demo: <https://youtu.be/hjFSL6oa2lo>
#### Description:
Hey reader, hope you are having a great day! So... Team Seas - The game is a web application game developed in python(flask), html, css and javascript.
This application is made with the objective of bringing awareness about the necessity of cleaning our oceans in a fun way...
the game works like this:
The user starts in a ocean as a fish, every coin the user grabs adds up to their total money... after grabbing some amount
of money the user gets to start using the store to increase their money earning rate, like, for example, buying the gangsta fish
which multiplies every coin by 2. Throughout the game the user will have to make multiple choices around which fish to buy or if its
worth it to clean the sea immediately or to save up some more, and the levels get progressivly harder. After cleaning up all
the seas the user gets a finishing position showing them how many people finished in front of them.
So... how does the code work?
The projects folder includes the final project folder, which includes two foldes... the work_env one is from the python
software I used, setting up the enviroment for the programming (I used Visual Studio Code + Anaconda Interpreter).
The other folder is demo which includes the code... Inside demo we have **app.py** which is the main application we also have
**game.db**, templates and static folders.

**app.py** -> This application is made with Flask, using a good part of the code I made during Week 9 of CS50 for the register
and log in systems, apart from that it has a *game route*, a *profile route*, a *levels route*, a *store route* and an *about route*:
*the game route* supports both Get and Post, Get renders the **game.js** file in the **game.html** template and post handles the database
updates to update the users cash after they finish each run of the game.
*the profile route* supports only get method and it renders the **profile.html** file with some information retrieved from **game.db** database
about the users: username, cash, position (if finished) and fish they already bought
*the levels route* supports both Get and Post, Get renders the **levels.html** template and Post handles the level selecting
not allowing users to access the next ocean if they have not cleaned the previous, it does that by consulting the **game.db** database
in the *levels table*
*the store route* supports both Get and Post, Get renders the **store.html** template and Post handles the buying operations
cheking the **game.db** database in the *skins table*, the *users table* and the *levels table* to allow or not the user to buy
a new fish or a new level, and to update the database if they do buy it.
*the about route* supports only Get, and it renders the **about.html** template which has a **counter.js** javascript file made by me
that updates the innerHTML of the file making a counter that counts down to the 1st of January of 2022.

**game.db** -> This is the database in which everything is being stored it has 4 tables: *users table*, *skins table*, *levels table*
and the *finished table*
*the users table* stores id (primary key integer), cash (integer), username (text), hash(text)
*the skins table* stores skinId(primary key integer), hasSkin (integer), skinName(text), userid(foreign key (id from users) integer)
*the levels table* stores level1, level2, level3, level4, level5 (all integers) and userid(foreign key (id from users) integer)
*the finished table* stores position(primary key integer) and userid(foreign key(id from users) integer)
this database is made to be able to store if the levels are or not finished (by saving 0 or 1 in the integer) same with the skins
I decided to go with integer instead of BLOB for if I wanted (and I plan to) make harder versions of the level once they are finished
I could just increase the integer value and I wouldnt need to create another table

the templates folder contains all the templates including a folder called scs which also contains a bunch of templates
those inside the scs folder are special made meme generator like the apology function from helpers so I could give a personal
touch to the buying event for each fish in the store

the static folder contains all the sprites, the sound effects, the css's and both javascript files *counter.js* and *game.js*.
The sprites are all made by me using Adobe Photoshop, there is usually 2 sprites for each fish one normal the other upsidedown and that is for
the way the draw function works in the draw method inside the fish at the *game.js* file, which rotates the image according to the
angle calculated between the place you clicked vs the place the fish is. There is also the trash sprites and icons.
The *game.js* is a JavaScript Game based on a canvas, it basically grabs a canvas on the HTML, set its width and height and from it
it tracks using the getBoundingClientRect() function and eventListeners the position on the canvas in which the user clicked and it slowly changes
the Fish position towards that position. The Trash and Coins have their own class, with a constructor a draw and an update method
*the constructor* are taking care of the main properties the object has, like radius (it could be 20,30,40,50 or 60) for trashes,
position x, position y, gameframe.x, gameframe.y, value (for coins), distance and sound.
*the draw* function draw's the object on top of a circle (which is the real hitbox for the fishes), and scales it
*the update* function handles all the middle game changes like movement
after that we have the handleTrash and handleCoins function which create multiple coins and trash according to the gameframe
push them inside an array and calculate using pitagoras theorem the distance between each array object to the fish, if a collision happens
in that case, the distance between the two objects is less than the sum of their radius then it peforms a collision action...
if it is a coin it adds to the score, if it is a trash it removes from the lives variable
at the end of the program we have the animate function which is a recursive function, that calls all other functions and it only
stops calling itself if the gameOver variable is set to true, and that happens once the lives are less than 1.
Depending on the fish and the level the multiplier variables change, they are all definied on the top of the *game.js* file and
they are used to give each fish and level their special skill... So like the Catfish can eat cans, so inside the collision detector of the
handleTrash method I check if the fish is a catfish and if it is instead of losing a life you get extra 10 coins!
The *counter.js* file is the Javascript file that handles the counter on the about page that is counting down until 1st of January of 2022
it works by calculating the amount of seconds between the future time and the now time and displaying the days hours minutes according to basic operations
like a minute is 60 seconds and an hour is 60 minutes.
The wav files were downloaded from a free sound effect website.

The project was based on Team Seas which is a website in which you can donate 1 dollar and with it 1 pound of trash will be removed out of the ocean
this project was created by youtubers- Mr Beast and Mark Rober (which both got fishes inspired by them), the goal was to reach
30 million pounds removed before January 1st 2022 and that's why the counter counts down to that day

Special thanks to my friends which helped me play test the game and make some balance patches on the fishes so the users in which will
play the game in the future could have a better experience, the game is designed to have a fast upgrade cycle so the user wont get
easily bored by getting stuck at the same stage for a long time and at the same time it also goes to show how much money is 1 billion or 1 million
or even a thousand dollars, and that sometimes we don't really understand the difference when it comes to big numbers, but through the game you do
because you gotta work for the money.

The information towards the most polluted seas in the world came from this website -> https://www.pollutionsolutions-online.com/news/water-wastewater/17/breaking-news/what-are-the-most-polluted-seas/55998
if you want to check out their research and information towards the necessity of making the seas cleaner for other species and even our own!

Hope you enjoyed my project as much as I enjoyed doing it and doing this amazing course!

This was #Team Seas - The Game - CS50x2021