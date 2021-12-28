import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///game.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Main page"""
    return render_template("index.html")   

@app.route("/about")
def about():
    return render_template("about.html")




def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register User"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("Missing username")
        check = db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))
        if len(check) == 1:
            if username == check[0]["username"]:
                return apology("Username already taken")
        password = request.form.get("password")
        c_password = request.form.get("confirmation")
        if not password:
            return apology("Missing password")
        elif not c_password:
            return apology("Missing confirm-password")
        elif password != c_password:
            return apology("Passwords don't match")
        elif len(password) < 6:
            return apology("Password should have at least 6 digits")
        meubom = 0
        seubom = 0
        for i in range(len(password)):
            papa = password[i].isalpha()
            if papa == True:
                meubom = 1
            popo = password[i].isdigit()
            if popo == True:
                seubom = 1
        if meubom == 0:
            return apology("Password does not contain letter")
        if seubom == 0:
            return apology("Password does not containt number")
        # Hashing passwords to store it in the database
        password = generate_password_hash(password)
        c_password = generate_password_hash(c_password)
        meubom = 0
        seubom = 0

        # actually inserting in the database
        db.execute("INSERT INTO users (username, hash) VALUES (? , ?)", username, password)
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/game", methods=["GET", "POST"])
@login_required
def game():
    if request.method == "GET":
        return redirect("/levels")
    else:
        if not request.form.get("coinTotal"):
            return apology("something went wrong", 408)
        else:    
            variable = request.form.get("coinTotal")
            text = "Congratz, you made"
            dolars = " dolars"
            cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            cash = cash[0]["cash"]
            cash = cash + int(variable)
            if(cash > 999999999):
                cash = 999999999
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
            return render_template("sucess.html", variable=variable, text=text, dolars=dolars)    



@app.route("/store", methods=["GET", "POST"])
@login_required
def store():
    if request.method == "GET":
        return render_template("store.html")
    else:
        # Level 1
        if request.form.get("BuyLevel1"):
            # Verify that the player has not already paid for cleaning up Level 1
            alreadyOwns = db.execute("SELECT level2 FROM levels WHERE userid = ?", session["user_id"])
            if not alreadyOwns:
                db.execute("INSERT INTO levels(userid) VALUES(?)", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["level2"] == 1:
                    return apology("you already cleaned this sea", "Brah")
            # Verify that player has money to clean
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 2500:
                return apology("you don't have enough money to clean this ocean", "Dude")
            # Cleaning
            db.execute("UPDATE levels SET level2 = 1 WHERE userid = ?", session["user_id"])
            newAmount = money[0]["cash"] - 2500
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return apology("you cleaned up the first ocean!", 69420)

        # Level 2
        if request.form.get("BuyLevel2"):
            # Verify that the player has not already paid for cleaning up Level 2
            alreadyOwns = db.execute("SELECT level3 FROM levels WHERE userid = ?", session["user_id"])
            if not alreadyOwns:
                db.execute("INSERT INTO levels(userid) VALUES(?)", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["level3"] == 1:
                    return apology("you already cleaned this sea", "Yo")
            # Verify that every other sea is cleaned
            alreadyCleaned = db.execute("SELECT level2 FROM levels WHERE userid = ?", session["user_id"])
            if alreadyCleaned[0]["level2"] == 0:
                return apology("you need to clean all the previous oceans first")
            # Verify that player has money to clean
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 25000:
                return apology("you don't have enough money to clean this ocean", "Bro")
            # Cleaning
            db.execute("UPDATE levels SET level3 = 1 WHERE userid = ?", session["user_id"])
            newAmount = money[0]["cash"] - 25000
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return apology("you cleaned up the second ocean!", 69420) 

        # Level 3
        if request.form.get("BuyLevel3"):
            # Verify that the player has not already paid for cleaning up Level 3
            alreadyOwns = db.execute("SELECT level4 FROM levels WHERE userid = ?", session["user_id"])
            if not alreadyOwns:
                db.execute("INSERT INTO levels(userid) VALUES(?)", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["level4"] == 1:
                    return apology("you already cleaned this sea", "Yo")
            # Verify that every other sea is cleaned
            alreadyCleaned = db.execute("SELECT level2, level3 FROM levels WHERE userid = ?", session["user_id"])
            if alreadyCleaned[0]["level2"] == 0 or alreadyCleaned[0]["level3"] == 0:
                return apology("you need to clean all the previous oceans first", "Brah")
            # Verify that player has money to clean
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 250000:
                return apology("you don't have enough money to clean this ocean", "Dude")
            # Cleaning
            db.execute("UPDATE levels SET level4 = 1 WHERE userid = ?", session["user_id"])
            newAmount = money[0]["cash"] - 250000
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return apology("you cleaned up the third ocean!", 69420)              

        # Level 4
        if request.form.get("BuyLevel4"):
            # Verify that the player has not already paid for cleaning up Level 4
            alreadyOwns = db.execute("SELECT level5 FROM levels WHERE userid = ?", session["user_id"])
            if not alreadyOwns:
                db.execute("INSERT INTO levels(userid) VALUES(?)", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["level5"] == 1:
                    return apology("you already cleaned this sea", "Bro")
            # Verify that every other sea is cleaned
            alreadyCleaned = db.execute("SELECT level2, level3, level4 FROM levels WHERE userid = ?", session["user_id"])
            if alreadyCleaned[0]["level2"] == 0 or alreadyCleaned[0]["level3"] == 0 or alreadyCleaned[0]["level4"] == 0:
                return apology("you need to clean all the previous oceans first", "Yo")
            # Verify that player has money to clean
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 25000000:
                return apology("you don't have enough money to clean this ocean", "hey")
            # Cleaning
            db.execute("UPDATE levels SET level5 = 1 WHERE userid = ?", session["user_id"])
            newAmount = money[0]["cash"] - 25000000
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return apology("you cleaned up the fourth ocean!", 69420)     
             

        # Level 5
        if request.form.get("BuyLevel5"):
            # Verify that the player has not already paid for cleaning up Level 4
            alreadyOwns = db.execute("SELECT position FROM finished WHERE userid = ?", session["user_id"])
            if alreadyOwns:
                return apology("you already finished everything at position {}".format(alreadyOwns[0]["position"]), "Bro")
            # Verify that every other sea is cleaned
            alreadyCleaned = db.execute("SELECT level2, level3, level4, level5 FROM levels WHERE userid = ?", session["user_id"])
            if alreadyCleaned[0]["level2"] == 0 or alreadyCleaned[0]["level3"] == 0 or alreadyCleaned[0]["level4"] == 0 or alreadyCleaned[0]["level5"] == 0:
                return apology("you need to clean all the previous oceans first", "hey")
            # Verify that player has money to clean
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 999999999:
                return apology("you don't have enough money to clean this ocean", "hey")
            # Cleaning
            db.execute("INSERT INTO finished(userid) VALUES(?)", session["user_id"])
            newAmount = money[0]["cash"] - 999999999
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return apology("you cleaned up the last ocean!", 69420)









        # DREAM
        if request.form.get("buyDream"):
            # Verify that player does not own Dream already
            alreadyOwns = db.execute("SELECT hasSkin FROM skins WHERE userid = ? AND skinName = 'Dream'", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["hasSkin"] == 1:
                    return apology("you already have Dream", "Bro")    
            # Verify that player has money to buy Dream
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 750000:
                return apology("you don't have enough money to buy Dream", "hey")
            # Buying dream
            db.execute("INSERT INTO skins(skinName, hasSkin, userid) VALUES(?, ?, ?)", "Dream", 1, session["user_id"])
            newAmount = money[0]["cash"] - 750000
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return render_template("/scs/dreamscs.html", text="You bought", variable="Dream")  
      
        # DUCK    
        if request.form.get("buyDuck"):
            alreadyOwns = db.execute("SELECT hasSkin FROM skins WHERE userid = ? AND skinName = 'Duck'", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["hasSkin"] == 1:
                    return apology("you already have THE DUCK", "Bro")
            # Verify money
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 999999999:
                return apology("you don't have enough money to buy THE DUCK", "Yo")
            # Buying THE DUCK
            db.execute("INSERT INTO skins(skinName , hasSkin, userid) VALUES (?, ?, ?)", "Duck", 1, session["user_id"])
            newAmount = money[0]["cash"] - 999999999
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return render_template("/scs/duckscs.html", text="You bought", variable="The Duck")    


        # Mr Fish
        if request.form.get("buymrFish"):
            alreadyOwns = db.execute("SELECT hasSkin FROM skins WHERE userid = ? AND skinName = 'mrFish'", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["hasSkin"] == 1:
                    return apology("you already have Mr. Fish", "Bruh")
            # Verify money
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 100000000:
                return apology("you don't have enough money to buy Mr. Fish", "Yo")
            # Buying Mr. Fish
            db.execute("INSERT INTO skins(skinName , hasSkin, userid) VALUES (?, ?, ?)", "mrFish", 1, session["user_id"])
            newAmount = money[0]["cash"] - 100000000
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return render_template("/scs/mrfishscs.html", text="You bought", variable="Mr. Fish") 


        # Fish Rober
        if request.form.get("buyfishRober"):
            alreadyOwns = db.execute("SELECT hasSkin FROM skins WHERE userid = ? AND skinName = 'fishRober'", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["hasSkin"] == 1:
                    return apology("you already have Fish Rober", "Dude")
            # Verify money
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 100000000:
                return apology("you don't have enough money to buy Fish Rober", "Bro")
            # Buying Fish Rober
            db.execute("INSERT INTO skins(skinName , hasSkin, userid) VALUES (?, ?, ?)", "fishRober", 1, session["user_id"])
            newAmount = money[0]["cash"] - 100000000
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return render_template("/scs/fishroberscs.html", text="You bought", variable="Fish Rober")  


        # Gangsta Fish
        if request.form.get("buygangstaFish"):
            alreadyOwns = db.execute("SELECT hasSkin FROM skins WHERE userid = ? AND skinName = 'gangstaFish'", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["hasSkin"] == 1:
                    return apology("you already have Gangsta Fish", "Dude")
            # Verify money
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 100:
                return apology("you don't have enough money to buy Gangsta Fish", "Bro")
            # Buying Gangsta Fish
            db.execute("INSERT INTO skins(skinName , hasSkin, userid) VALUES (?, ?, ?)", "gangstaFish", 1, session["user_id"])
            newAmount = money[0]["cash"] - 100
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return render_template("/scs/gangstascs.html", text="You bought", variable="Gangsta Fish")  

        # Dead Fish
        if request.form.get("buydeadFish"):
            alreadyOwns = db.execute("SELECT hasSkin FROM skins WHERE userid = ? AND skinName = 'deadFish'", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["hasSkin"] == 1:
                    return apology("you already have Dead Fish", "Bruh")
            # Verify money
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 100:
                return apology("you don't have enough money to buy Dead Fish", "Yo")
            # Buying Dead Fish
            db.execute("INSERT INTO skins(skinName , hasSkin, userid) VALUES (?, ?, ?)", "deadFish", 1, session["user_id"])
            newAmount = money[0]["cash"] - 100
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return render_template("/scs/deadscs.html", text="You bought", variable="Dead Fish")  


         # Blob Fish
        if request.form.get("buyblobFish"):
            alreadyOwns = db.execute("SELECT hasSkin FROM skins WHERE userid = ? AND skinName = 'blobFish'", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["hasSkin"] == 1:
                    return apology("you already have Blob Fish", "My dear fella")
            # Verify money
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 500:
                return apology("you don't have enough money to buy Blob Fish", "OI")
            # Buying Blob Fish
            db.execute("INSERT INTO skins(skinName , hasSkin, userid) VALUES (?, ?, ?)", "blobFish", 1, session["user_id"])
            newAmount = money[0]["cash"] - 500
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return render_template("/scs/blobscs.html", text="You bought", variable="Blob Fish")  


        # Catfish Fish
        if request.form.get("buycatfish"):
            alreadyOwns = db.execute("SELECT hasSkin FROM skins WHERE userid = ? AND skinName = 'catfish'", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["hasSkin"] == 1:
                    return apology("you already have Catfish", "Yo")
            # Verify money
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 500:
                return apology("you don't have enough money to buy Catfish", "Dude")
            # Buying Catfish Fish
            db.execute("INSERT INTO skins(skinName , hasSkin, userid) VALUES (?, ?, ?)", "catfish", 1, session["user_id"])
            newAmount = money[0]["cash"] - 500
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return render_template("/scs/catfishscs.html", text="You bought", variable="Catfish")  


         # Betafish Fish
        if request.form.get("buyBetafish"):
            alreadyOwns = db.execute("SELECT hasSkin FROM skins WHERE userid = ? AND skinName = 'Betafish'", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["hasSkin"] == 1:
                    return apology("you already have Betafish", "Bro")
            # Verify money
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 1500:
                return apology("you don't have enough money to buy Betafish", "Bruh")
            # Buying Betafish Fish
            db.execute("INSERT INTO skins(skinName , hasSkin, userid) VALUES (?, ?, ?)", "Betafish", 1, session["user_id"])
            newAmount = money[0]["cash"] - 1500
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return render_template("/scs/betafishscs.html", text="You bought", variable="Betafish")  


        # Flying fish Fish
        if request.form.get("buyflyingFish"):
            alreadyOwns = db.execute("SELECT hasSkin FROM skins WHERE userid = ? AND skinName = 'FlyingFish'", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["hasSkin"] == 1:
                    return apology("you already have Flying Fish", "Dude")
            # Verify money
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 25000:
                return apology("you don't have enough money to buy Flying Fish", "Bruh")
            # Buying Flying Fish
            db.execute("INSERT INTO skins(skinName , hasSkin, userid) VALUES (?, ?, ?)", "FlyingFish", 1, session["user_id"])
            newAmount = money[0]["cash"] - 25000
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return render_template("/scs/flyingfishscs.html", text="You bought", variable="Flyingfish")  


        # Turtle
        if request.form.get("buyTurtle"):
            alreadyOwns = db.execute("SELECT hasSkin FROM skins WHERE userid = ? AND skinName = 'Turtle'", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["hasSkin"] == 1:
                    return apology("you already have The Turtle", "Dude")
            # Verify money
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 100000:
                return apology("you don't have enough money to buy The Turtle", "Bruh")
            # Buying The turtle
            db.execute("INSERT INTO skins(skinName , hasSkin, userid) VALUES (?, ?, ?)", "Turtle", 1, session["user_id"])
            newAmount = money[0]["cash"] - 100000
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return render_template("/scs/turtlescs.html", text="You bought", variable="The Turtle")  

        # Jellyfish
        if request.form.get("buyjellyfish"):
            alreadyOwns = db.execute("SELECT hasSkin FROM skins WHERE userid = ? AND skinName = 'jellyfish'", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["hasSkin"] == 1:
                    return apology("you already have The Jellyfish", "Dude")
            # Verify money
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 15000:
                return apology("you don't have enough money to buy The Jellyfish", "Yo")
            # Buying The Jellyfish
            db.execute("INSERT INTO skins(skinName , hasSkin, userid) VALUES (?, ?, ?)", "jellyfish", 1, session["user_id"])
            newAmount = money[0]["cash"] - 15000
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return render_template("/scs/jellyfishscs.html", text="You bought", variable="Jellyfish")  

        # Shark
        if request.form.get("buyShark"):
            alreadyOwns = db.execute("SELECT hasSkin FROM skins WHERE userid = ? AND skinName = 'Shark'", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["hasSkin"] == 1:
                    return apology("you already have The Shark", "My friend")
            # Verify money
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 250000:
                return apology("you don't have enough money to buy The Shark", "Yo")
            # Buying The Jellyfish
            db.execute("INSERT INTO skins(skinName , hasSkin, userid) VALUES (?, ?, ?)", "Shark", 1, session["user_id"])
            newAmount = money[0]["cash"] - 250000
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return render_template("/scs/sharkscs.html", text="You bought", variable="The Shark")  

        # Fish Musk
        if request.form.get("buyFishMusk"):
            alreadyOwns = db.execute("SELECT hasSkin FROM skins WHERE userid = ? AND skinName = 'fishMusk'", session["user_id"])
            if alreadyOwns:
                if alreadyOwns[0]["hasSkin"] == 1:
                    return apology("you already have Fish Musk", "is this an easter egg?")
            # Verify money
            money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            if money[0]["cash"] < 25000000:
                return apology("you don't have enough money to buy Fish Musk", "Unfortunatly")
            # Buying The Jellyfish
            db.execute("INSERT INTO skins(skinName , hasSkin, userid) VALUES (?, ?, ?)", "fishMusk", 1, session["user_id"])
            newAmount = money[0]["cash"] - 25000000
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newAmount, session["user_id"])
            return render_template("/scs/fishmuskscs.html", text="You bought", variable="Fish Musk")  
                                       
                                 
            
                            


@app.route("/levels", methods=["GET", "POST"])
@login_required
def levels():
    if request.method == "GET":
        return render_template("levels.html")
    else:
        ## LEVEL 1
        if request.form.get("level1"):
            levels = db.execute("SELECT level1 FROM levels WHERE userid = ?", session["user_id"])
            if not levels:
                db.execute("INSERT INTO levels (userid) VALUES (?)", session["user_id"])
            skins = db.execute("SELECT skinName FROM skins WHERE userid = ?", session["user_id"])
            return render_template("skin.html", skins=skins, level="Level 1", code=1)
        
        if request.form.get("skinSelector1"):
            skin = request.form.get("skinSelector1")
            return render_template("game.html", skin=skin, level=1)

        ## LEVEL 2
        if request.form.get("level2"):
            levels = db.execute("SELECT level2 FROM levels WHERE userid = ?", session["user_id"])
            if not levels:
                return apology("You gotta start from the first sea!", 400)

            if levels[0]["level2"] == 0:
                return apology("you gotta clean up the previous seas first!", 000)

            skins = db.execute("SELECT skinName FROM skins WHERE userid = ?", session["user_id"])
            return render_template("skin.html", skins=skins, level="Level 2", code=2)

        if request.form.get("skinSelector2"):
            skin = request.form.get("skinSelector2")
            return render_template("game.html", skin=skin, level=2)

        ## LEVEL 3
        if request.form.get("level3"):
            levels = db.execute("SELECT level3 FROM levels WHERE userid = ?", session["user_id"])
            if not levels:
                return apology("You gotta start from the first sea!", 400)

            if levels[0]["level3"] == 0:
                return apology("you gotta clean up the previous seas first!", 000)

            skins = db.execute("SELECT skinName FROM skins WHERE userid = ?", session["user_id"])
            return render_template("skin.html", skins=skins, level="Level 3", code=3)

        if request.form.get("skinSelector3"):
            skin = request.form.get("skinSelector3")
            return render_template("game.html", skin=skin, level=3)

        ## LEVEL 4
        if request.form.get("level4"):
            levels = db.execute("SELECT level4 FROM levels WHERE userid = ?", session["user_id"])
            if not levels:
                return apology("You gotta start from the first sea!", 400)

            if levels[0]["level4"] == 0:
                return apology("you gotta clean up the previous seas first!", 000)

            skins = db.execute("SELECT skinName FROM skins WHERE userid = ?", session["user_id"])
            return render_template("skin.html", skins=skins, level="Level 4", code=4)

        if request.form.get("skinSelector4"):
            skin = request.form.get("skinSelector4")
            return render_template("game.html", skin=skin, level=4)
        
        ## LEVEL 5
        if request.form.get("level5"):
            levels = db.execute("SELECT level5 FROM levels WHERE userid = ?", session["user_id"])
            if not levels:
                return apology("You gotta start from the first sea!", 400)

            if levels[0]["level5"] == 0:
                return apology("you gotta clean up the previous seas first!", 000)

            skins = db.execute("SELECT skinName FROM skins WHERE userid = ?", session["user_id"])
            return render_template("skin.html", skins=skins, level="Level 5", code=5)

        if request.form.get("skinSelector5"):
            skin = request.form.get("skinSelector5")
            return render_template("game.html", skin=skin, level=5)



@app.route("/profile", methods = ["GET"])
@login_required
def profile():
    info = db.execute("SELECT username, cash FROM users WHERE id = ?", session["user_id"])
    cash = info[0]["cash"]
    name = info[0]["username"]
    position = db.execute("SELECT position FROM finished WHERE userid = ?", session["user_id"])
    if not position:
        finished = "You have yet to finish cleaning all the oceans!"
    else:
        finished = position[0]["position"]
    skins = db.execute("SELECT skinName FROM skins WHERE userid = ?", session["user_id"])    
    return render_template("profile.html", cash=cash, name=name, finished=finished, skins=skins)
    



# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
