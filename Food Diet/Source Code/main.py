import datetime

from flask import Flask, redirect, render_template, request, session,flash
import pymysql
import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PROFILES_PATH = APP_ROOT + "/static/profile"
NUTRITION_FILES_PATH = APP_ROOT + "/static/nutrition_files"
DIET_FILES_PATH = APP_ROOT + "/static/diet_files"
conn = pymysql.connect(host="localhost", user="root", password="Venu@123", db="food_diet")
cursor = conn.cursor()
app = Flask(__name__)
app.secret_key="nutrition"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin_login")
def admin_head():
    return render_template("admin_login.html")


@app.route("/nutrition_login")
def nutrition_login():
    return render_template("nutrition_login.html")


@app.route("/user_login")
def user_login():
    return render_template("user_login.html")


@app.route("/nutrition_registration")
def nutrition_registration():
    return render_template("nutrition_registration.html")


@app.route("/nutrition_login_action", methods=["post"])
def nutrition_login_action():
    email= request.form.get("email")
    password = request.form.get("password")
    count = cursor.execute("select * from nutrition where email='" + str(email) + "' and password='" + str(password) + "' ")
    if count > 0:
        nutrition = cursor.fetchall()
        if nutrition[0][7] == "verified":
            session["nutrition_id"] = nutrition[0][0]
            session['role'] = "nutrition"
            return redirect("/nutrition_home")
        else:
            return render_template("message.html", message="Not Verified")
    else:
        return render_template("message.html", message="Invalid Email and password")


@app.route("/nutrition_registration_action", methods=['post'])
def nutrition_registration_action():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    about = request.form.get("about")

    count = cursor.execute(" select * from nutrition where email='"+str(email)+"' ")
    if count > 0:
        return render_template("message.html", message="Duplicate Mail")
    count = cursor.execute(" select * from nutrition where phone='" + str(phone) + "' ")
    if count > 0:
        return render_template("message.html", message="Duplicate Phone Number")

    picture = request.files.get("profile_picture")
    path = NUTRITION_FILES_PATH + "/" + picture.filename
    picture.save(path)
    cursor.execute(" insert into nutrition(name,email,phone,password,about,picture) values('"+str(name)+"', '"+str(email)+"', '"+str(phone)+"', '"+str(password)+"','"+str(about)+"','"+str(picture.filename)+"') ")
    conn.commit()
    return render_template("message.html", message="Nutrition Added SuccessFully")


@app.route("/user_registration")
def user_registration():
    return render_template("user_registration.html")


@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/user_registration_action", methods=['post'])
def user_registration_action():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    gender = request.form.get("gender")
    address = request.form.get("address")
    age = request.form.get("age")
    print(name)
    print(email)
    print(phone)
    print(password)

    count = cursor.execute(" select * from user where email='"+str(email)+"' ")
    if count > 0:
        return render_template("message.html", message="Duplicate Mail")
    count = cursor.execute(" select * from user where phone='" + str(phone) + "'")
    if count > 0:
        return render_template("message.html", message="Duplicate Phone Number")
    cursor.execute("insert into user(name,email,phone,password,gender,address,age) values('"+str(name)+"', '"+str(email)+"', '"+str(phone)+"', '"+str(password)+"','"+str(gender)+"','"+str(address)+"','"+str(age)+"') ")
    conn.commit()
    return render_template("message.html", message="User  Added SuccessFully")


@app.route("/view_nutrition")
def view_nutrition():
    cursor.execute("select * from nutrition")
    nutritions = cursor.fetchall()
    return render_template("view_nutrition.html", nutritions=nutritions)


@app.route("/verify_nutrition")
def verify_nutrition():
    nutrition_id = request.args.get("nutrition_id")
    print(nutrition_id)
    cursor.execute("update nutrition set status='verified' where nutrition_id='"+str(nutrition_id)+"' ")
    conn.commit()
    return redirect("/view_nutrition")


@app.route("/user_login_action")
def user_login_action():
    email = request.args.get("email")
    password = request.args.get("password")
    count = cursor.execute("select * from user where email='"+str(email)+"' and password='"+str(password)+"' ")
    if count > 0:
        user = cursor.fetchall()
        session["user_id"] = user[0][0]
        session['role'] = "user"
        return redirect("/user_home")
    else:
        return render_template("message.html", message="Invalid Email and password")


@app.route("/user_home")
def user_home():
    return render_template("user_home.html")


@app.route("/admin_login_action", methods=['post'])
def admin_login_action():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "admin" and password == "admin":
      session['role'] = "admin"
      return redirect("/admin_home")
    else:
        return render_template("message.html", message="Invalid Email and password")


@app.route("/nutrition_home")
def nutrition_home():
    return render_template("nutrition_home.html")


@app.route("/add_diet")
def add_diet():
    return render_template("add_diet.html")


@app.route("/add_diet_action", methods=["post"])
def add_diet_action():
    diet_title = request.form.get("diet_title")
    age_from = request.form.get("age_from")
    age_to = request.form.get("age_to")
    instructions = request.form.get("instructions")
    about_diet = request.form.get("about_diet")
    age = request.form.get("age")
    calories_to_be_burn = request.form.get("calories_to_be_burn")
    calories_to_be_consume = request.form.get("calories_to_be_consume")
    diet_for = request.form.get("diet_for")
    nutrition_id = session["nutrition_id"]

    image = request.files.get("image")
    path = DIET_FILES_PATH + "/" + image.filename
    image.save(path)
    cursor.execute("insert into diet(diet_title, age_from, age_to,instructions,image,about_diet,status,diet_for,calories_to_be_burn,calories_to_be_consume,nutrition_id) values('" + str(
        diet_title) + "', '" + str(age_from) + "', '" + str(age_to) + "', '" + str(instructions) + "','" + str(image.filename) + "','" + str(about_diet) + "','" + str('diet_added') + "' ,'" + str(diet_for) + "','" + str(calories_to_be_burn) + "','" + str(calories_to_be_consume) + "','" + str(nutrition_id) + "') ")
    conn.commit()
    return render_template("message.html", message="Added successfully")


@app.route("/view_diet")
def view_diet():
    name = request.args.get("name")
    role = session['role']
    if  name  == None:
        name = ""
    if role == 'nutrition':
        if name == "":
            cursor.execute("select * from diet where nutrition_id= '" + str(session["nutrition_id"]) + "' ")
        elif name != "":
            cursor.execute(" select * from diet where diet_title like '%" + str(name) + "%' and nutrition_id= '" + str(session["nutrition_id"]) + "' ")
        diets = cursor.fetchall()
    elif role == 'user':
        if name == "":
            cursor.execute("select * from diet")
        elif name != "":
            cursor.execute(" select * from diet where diet_title like '%"+str(name)+"%'")
        diets = cursor.fetchall()
    return render_template("view_diet.html",getAvgRating=getAvgRating,getIsFollowed=getIsFollowed, get_user_diet_by_diet_id=get_user_diet_by_diet_id, diets=diets, get_exercise_timings_by_diet_id=get_exercise_timings_by_diet_id, get_food_timings_by_diet_id=get_food_timings_by_diet_id)


def getIsFollowed(diet_id):
    count = cursor.execute("select * from user_diet where diet_id='"+str(diet_id)+"' and user_id='"+str(session['user_id'])+"' and status='Following'")
    return count


def get_user_diet_by_diet_id(diet_id):
    cursor.execute("select * from user_diet where diet_id='"+str(diet_id)+"' and user_id='"+str(session['user_id'])+"' and status='Following'")
    user_diets = cursor.fetchall()
    print(user_diets,'dhdrtgr')
    return user_diets


@app.route("/exercise_timings")
def exercise_timings():
    diet_id = request.args.get("diet_id")
    return render_template("exercise_timings.html", diet_id=diet_id)


@app.route("/exercise_timings1")
def exercise_timings1():
    diet_id = request.args.get("diet_id")
    exercise_title = request.args.get("exercise_title")
    exercise_timings = request.args.get("exercise_timings")
    calories_should_brun = request.args.get("calories_should_brun")
    cursor.execute(
        "insert into exercise_timings(exercise_title, exercise_time, calories_should_burn,diet_id) values('" + str(
            exercise_title) + "', '" + str(exercise_timings) + "', '" + str(calories_should_brun) + "', '" + str(diet_id) + "') ")
    conn.commit()
    return render_template("message.html", message="Timings Added successfully")


@app.route("/food_timings")
def food_timings():
    diet_id = request.args.get("diet_id")
    return render_template("food_timings.html", diet_id=diet_id)


@app.route("/food_timings1")
def food_timings1():
    diet_id = request.args.get("diet_id")
    food_title = request.args.get("food_title")
    food_timings = request.args.get("food_timings")
    calories_should_take = request.args.get("calories_should_take")
    cursor.execute(
        "insert into food_timings(food_time_title, food_time, calories_can_taken,diet_id) values('" + str(
            food_title) + "', '" + str(food_timings) + "', '" + str(calories_should_take) + "', '" + str(diet_id) + "') ")
    conn.commit()
    return render_template("message.html", message="Timings Added successfully")


def get_exercise_timings_by_diet_id(diet_id):
    cursor.execute("select * from exercise_timings where diet_id='"+str(diet_id)+"'")
    exercise_timings = cursor.fetchall()
    return exercise_timings


def get_food_timings_by_diet_id(diet_id):
    cursor.execute("select * from food_timings where diet_id='"+str(diet_id)+"'")
    food_timings = cursor.fetchall()
    return food_timings


@app.route("/add_food_diet")
def add_food_diet():
    return render_template("add_food_diet.html")


@app.route("/add_food_diet1", methods=['post'])
def add_food_diet1():
    food_name = request.form.get("food_name")
    quantity = request.form.get("quantity")
    units = request.form.get("units")
    preparation_process = request.form.get("preparation_process")
    propagation_time = request.form.get("propagation_time")
    calories = request.form.get("calories")
    food_timing_id = request.form.get("food_timing_id")
    image = request.files.get("image")
    path = DIET_FILES_PATH + "/" + image.filename
    image.save(path)
    count = cursor.execute("select * from food_in_diet where food_timing_id = '" + str(food_timing_id) + "'")
    if count == 0:
        cursor.execute("insert into food_in_diet(food_name,quantity,units,preparation_process,propagation_time,calories,food_timing_id,image) value('" + str(food_name) + "', '" + str(quantity) + "', '" + str(units) + "', '" + str(preparation_process) + "', '" + str(propagation_time) + "', '" + str(calories) + "', '" + str(food_timing_id) + "', '" + str(image.filename) + "')")
        conn.commit()
        return redirect("/view_diet")
    else:
        return render_template("admin_msg.html", message="For This Time, Food Diet already exist")


@app.route("/food_diet")
def food_diet():
    diet_id = request.args.get("diet_id")
    food_timing_id = request.args.get("food_timing_id")
    if food_timing_id is None:
        sql = "select * from food_in_diet where food_timing_id in(select food_timing_id from food_timings where diet_id = '"+str(diet_id)+"')"
        sql2 = "select * from food_timings where diet_id = '"+str(diet_id)+"'"
    else:
        sql = "select * from food_in_diet where food_timing_id='"+str(food_timing_id)+"'"
        sql2 = "select * from food_timings where diet_id = '" + str(diet_id) + "'"
    # cursor.execute("select * from food_in_diet where food_timing_id in(select food_timing_id from food_timings where diet_id = '"+str(diet_id)+"')")
    cursor.execute(sql2)
    food_timings = cursor.fetchall()
    cursor.execute(sql)
    food_in_diets = cursor.fetchall()
    return render_template("food_diet.html", food_timing_id=food_timing_id,food_in_diets=food_in_diets, get_user_diet_by_diet_id=get_user_diet_by_diet_id, food_timings=food_timings, get_food_timings_by_food_timing_id=get_food_timings_by_food_timing_id)


def get_food_timings_by_food_timing_id(food_timing_id):
    cursor.execute("select * from food_timings where food_timing_id='"+str(food_timing_id)+"'")
    food_timings = cursor.fetchall()
    return food_timings[0]


def get_exercise_timings_by_exercise_timing_id(exercise_timing_id):
    cursor.execute("select * from exercise_timings where exercise_timing_id='"+str(exercise_timing_id)+"'")
    exercise_timings = cursor.fetchall()
    return exercise_timings[0]


@app.route("/exercise_diet")
def exercise_diet():
    diet_id = request.args.get("diet_id")
    print(diet_id)
    cursor.execute("select * from exercise_timings where diet_id = '"+str(diet_id)+"'")
    exercise_timings = cursor.fetchall()
    print(exercise_timings)
    cursor.execute("select * from exercise_in_diet where exercise_timing_id in(select exercise_timing_id from exercise_timings where diet_id = '"+str(diet_id)+"')")
    exercise_in_diets = cursor.fetchall()
    print(exercise_in_diets)
    return render_template("exercise_diet.html", exercise_in_diets=exercise_in_diets, exercise_timings=exercise_timings, get_exercise_timings_by_exercise_timing_id=get_exercise_timings_by_exercise_timing_id)


@app.route("/add_exercise_diet")
def add_exercise_diet():
    return render_template("add_exercise_diet.html")


@app.route("/add_exercise_diet1", methods=['post'])
def add_exercise_diet1():
    exercise_timing_id = request.form.get("exercise_timing_id")
    exercise_name = request.form.get("exercise_name")
    duration = request.form.get("duration")
    calories_burn = request.form.get("calories_burn")
    image = request.files.get("image")
    path = DIET_FILES_PATH + "/" + image.filename
    image.save(path)
    count = cursor.execute("select * from exercise_in_diet where exercise_timing_id = '" + str(exercise_timing_id) + "'")
    if count == 0:
        cursor.execute("insert into exercise_in_diet(exercise_name,duration,calories_burn,exercise_timing_id,image) value('" + str(exercise_name) + "', '" + str(duration) + "', '" + str(calories_burn) + "', '" + str(exercise_timing_id) + "', '" + str(image.filename) + "')")
        conn.commit()
        return redirect("/view_diet")
    else:
        return render_template("admin_msg.html", message="For This Time, Exercise Diet already exist")


@app.route("/follow_diet")
def follow_diet():
    diet_id = request.args.get("diet_id")
    user_id = session['user_id']
    count = cursor.execute("select * from user_diet where user_id = '"+str(user_id)+"' and status = 'Following'")
    if count > 0:
        cursor.execute("update user_diet set status = 'Un Followed' where user_id = '"+str(user_id)+"' and status = 'Following'")
        conn.commit()
    cursor.execute("insert into user_diet(status,diet_id,user_id) value('Following', '" + str(diet_id) + "', '" + str(user_id) + "')")
    conn.commit()
    return redirect("/view_following_diet")

@app.route("/un_follow_diet")
def un_follow_diet():
    user_id = session['user_id']
    diet_id = request.args.get("diet_id")
    cursor.execute(
        "update user_diet set status = 'Un Followed' where user_id = '" + str(user_id) + "' and status = 'Following' and diet_id='"+str(diet_id)+"'")
    conn.commit()
    return redirect("/view_following_diet")


@app.route("/view_following_diet")
def view_following_diet():
    cursor.execute("select * from diet where diet_id in(select diet_id from user_diet where user_id = '"+str(session['user_id'])+"' and status = 'Following')")
    diets = cursor.fetchall()
    # cursor.execute("select * from food_timings where diet_id in (select diet_id from user_diet where user_id = '"+str(session['user_id'])+"' and status = 'Following')")
    # food_timings = cursor.fetchall()
    # for food_timing in food_timings:
    #     currentDate = datetime.datetime.now()
    #     currentDate = str(currentDate)
    #     currentDate = currentDate[11:-10]
    #     currentDate = datetime.datetime.strptime(currentDate, "%H:%M")
    #     food_timing = datetime.datetime.strptime(str(food_timing[2]), "%H:%M")
    #     if food_timing >= currentDate:
    #         print("hii")
    #         flash("time ")
    #
    #     print(currentDate)
    return render_template("view_following_diet.html", get_user_diet_by_diet_id=get_user_diet_by_diet_id, diets=diets,
                           get_exercise_timings_by_diet_id=get_exercise_timings_by_diet_id,
                           get_food_timings_by_diet_id=get_food_timings_by_diet_id,getIsFollowed=getIsFollowed,getIsRated=getIsRated)

@app.route("/update_user_food")
def update_user_food():
    food_in_diet_id = request.args.get("food_in_diet_id")
    quantity = request.args.get("quantity")
    date = request.args.get("date")
    calories = request.args.get("calories")
    cursor.execute("select * from user_diet where user_id = '"+str(session['user_id'])+"' and status = 'Following'")
    userDiet = cursor.fetchone()
    user_diet_id = userDiet[0]
    totalCalories = int(quantity) * int(calories)
    cursor.execute("insert into user_food (quantity,date,user_diet_id,food_in_diet_id,totalCalories)values('"+str(quantity)+"','"+str(date)+"','"+str(user_diet_id)+"','"+str(food_in_diet_id)+"','"+str(totalCalories)+"')")
    conn.commit()
    return redirect("/view_following_diet")

@app.route("/update_user_exercise")
def update_user_exercise():
    exercise_in_diet_id = request.args.get("exercise_in_diet_id")
    calories = request.args.get("calories")
    number_of_sets = request.args.get("number_of_sets")
    date = request.args.get("date")
    calories = request.args.get("calories")
    cursor.execute("select * from user_diet where user_id = '" + str(session['user_id']) + "' and status = 'Following'")
    userDiet = cursor.fetchone()
    user_diet_id = userDiet[0]
    totalCalories = int(number_of_sets) * int(calories)
    cursor.execute("insert into user_exercise (number_of_sets,date,user_diet_id,exercise_in_diet_id,totalCalories)values('" + str(
        number_of_sets) + "','" + str(date) + "','" + str(user_diet_id) + "','" + str(exercise_in_diet_id) + "','" + str(
        totalCalories) + "')")
    conn.commit()
    return redirect("/view_following_diet")

@app.route("/viewSummary")
def viewSummary():
    diet_id = request.args.get("diet_id")
    print(diet_id)
    cursor.execute("select * from user_diet where diet_id='"+str(diet_id)+"'and status='Following' and user_id = '"+str(session['user_id'])+"'")
    userDiet = cursor.fetchone()
    user_diet_id = userDiet[0]
    date = request.args.get('date')
    cursor.execute("select * from user_exercise where user_diet_id='"+str(user_diet_id)+"' and date='"+str(date)+"'")
    user_exercises = cursor.fetchall()
    cursor.execute("select * from user_food where user_diet_id='" + str(user_diet_id) + "' and date='" + str(date) + "'")
    user_foods = cursor.fetchall()
    return render_template("viewSummary.html",get_exercise_user_exercise_by_id=get_exercise_user_exercise_by_id,get_diet_by_id=get_diet_by_id,get_food_timing_in_diet_by_id=get_food_timing_in_diet_by_id,int=int,user_exercises=user_exercises,user_foods=user_foods,diet_id=diet_id,get_food_in_diet_by_id=get_food_in_diet_by_id,get_exercise_in_diet_by_id=get_exercise_in_diet_by_id)

def get_food_in_diet_by_id(food_in_diet_id):
    print(food_in_diet_id)
    cursor.execute("select * from food_in_diet where food_in_diet_id='"+str(food_in_diet_id)+"'")
    food_in_diet = cursor.fetchall()
    return food_in_diet[0]

def get_exercise_in_diet_by_id(exercise_in_diet_id):
    cursor.execute("select * from exercise_in_diet where exercise_in_diet_id='" + str(exercise_in_diet_id) + "'")
    user_exercise_in = cursor.fetchall()
    return user_exercise_in[0]

def get_food_timing_in_diet_by_id(food_timing_id):
    cursor.execute("select * from food_timings where food_timing_id='"+str(food_timing_id)+"'")
    food_timing = cursor.fetchall()
    return food_timing[0]

def get_diet_by_id(diet_id):
    cursor.execute("select * from diet where diet_id='"+str(diet_id)+"'")
    diet = cursor.fetchall()
    return diet[0]

def get_exercise_user_exercise_by_id(exercise_timing_id):
    cursor.execute("select * from exercise_timings where exercise_timing_id='"+str(exercise_timing_id)+"'")
    exercise_timing = cursor.fetchall()
    return exercise_timing[0]

@app.route("/giveRating")
def giveRating():
    diet_id = request.args.get("diet_id")
    return render_template("giveRating.html",diet_id=diet_id)

@app.route("/giveRatingAction",methods=['post'])
def giveRatingAction():
    diet_id = request.form.get("diet_id")
    rating = request.form.get("rating")
    review = request.form.get("review")
    cursor.execute("select * from user_diet where diet_id='"+str(diet_id)+"'and status='Following' and user_id = '"+str(session['user_id'])+"'")
    user_diet = cursor.fetchone()
    user_diet_id = user_diet[0]
    cursor.execute("insert into review (review,rating,date,user_diet_id) values('"+str(review)+"','"+str(rating)+"','"+str(datetime.datetime.now())+"','"+str(user_diet_id)+"')")
    conn.commit()
    return redirect("/view_following_diet")


def getIsRated(diet_id):
    cursor.execute("select * from user_diet where diet_id='" + str(diet_id) + "'and status='Following' and user_id = '" + str(session['user_id']) + "'")
    conn.commit()
    user_diet = cursor.fetchone()
    user_diet_id = user_diet[0]
    count = cursor.execute("select * from review where user_diet_id='"+str(user_diet_id)+"'")
    conn.commit()
    return count

@app.route("/viewRatings")
def viewRatings():
    diet_id = request.args.get("diet_id")
    cursor.execute( "select * from user_diet where diet_id='" + str(diet_id) + "'and status='Following' and user_id = '" + str(session['user_id']) + "'")
    conn.commit()
    user_diet = cursor.fetchone()
    user_diet_id = user_diet[0]
    cursor.execute("select * from review where  user_diet_id='"+str(user_diet_id)+"'")
    review = cursor.fetchall()
    return render_template("viewRatings.html",review=review[0])

def getAvgRating(diet_id):
    cursor.execute("select avg(rating) as rating from review where user_diet_id  in (select user_diet_id from user_diet where diet_id='"+str(diet_id)+"')")
    rating = cursor.fetchone()
    return rating[0]

@app.route("/getReviews")
def getReviews():
    diet_id = request.args.get("diet_id")
    cursor.execute("select * from review where user_diet_id  in (select user_diet_id from user_diet where diet_id='"+str(diet_id)+"')")
    reviews = cursor.fetchall()
    return render_template("getReviews.html",reviews=reviews,get_user_by_reviewId=get_user_by_reviewId)

def get_user_by_reviewId(user_diet_id):
    cursor.execute("select * from user_diet where user_diet_id='"+str(user_diet_id)+"'")
    user_diet = cursor.fetchone()
    user_id = user_diet[2]
    cursor.execute("select * from user where user_id='"+str(user_id)+"'")
    user = cursor.fetchone()
    return user

app.run(debug=True)