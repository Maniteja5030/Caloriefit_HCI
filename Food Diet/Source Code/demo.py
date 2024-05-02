import datetime
import time
from playsound import playsound
from winotify import Notification
from flask import Flask,request,render_template,redirect,session

from Mail import send_email


app = Flask(__name__)
app.secret_key="nutrition"

import pymysql
conn = pymysql.connect(host="localhost", user="root", password="Venu@123", db="food_diet")
cursor = conn.cursor()

@app.route("/")
def index():
    cursor.execute("select * from food_timings where diet_id in (select diet_id from user_diet where user_id = '" + str(session['user_id']) + "' and status = 'Following')")
    food_timings = cursor.fetchall()
    conn.commit()
    cursor.execute("select * from exercise_timings where diet_id in (select diet_id from user_diet where user_id = '" + str(session['user_id']) + "' and status = 'Following')")
    exercise_timings = cursor.fetchall()
    conn.commit()
    cursor.execute("select * from user where user_id = '" + str(session['user_id']) + "'")
    user = cursor.fetchone()
    conn.commit()

    while True:
        time.sleep(1)
        currentTime = datetime.datetime.now().strftime("%H:%M")
        currentTime = datetime.datetime.strptime(currentTime, "%H:%M")

        for food_timing in food_timings:
            notify_time = food_timing[2]
            print(notify_time)
            notify_time = datetime.datetime.strptime(notify_time,"%H:%M")
            diff = notify_time - currentTime
            seconds = diff.seconds
            minutes = seconds / 3600
            if minutes < 30:
                count = cursor.execute("select * from beforeNotify where user_id='"+str(session['user_id'])+"' and status='Notified' and food_timing_id='"+str(food_timing[0])+"'")
                if count == 0:

                    send_email("Food Alert"," "+str(food_timing[1])+" Diet \n Time : "+str(food_timing[2])+" ",user[2])
                    toast = Notification(app_id="Diet Alert",
                                         title="Food Alert",
                                         msg=""+str(food_timing[1])+" Diet \n Time : "+str(food_timing[2])+"!",
                                         icon=r"c:\path\to\icon.png")

                    toast.show()
                    playsound('song.wav')
                    cursor.execute("insert into beforeNotify(user_id,status,food_timing_id) values('"+str(session['user_id'])+"','Notified',"+str(food_timing[0])+")")
                    conn.commit()
            elif minutes > 0 and minutes < 2:
                count = cursor.execute("select * from equalNotify where user_id='"+str(session['user_id'])+"' and status='Notified' and food_timing_id='"+str(food_timing[0])+"'")
                if count == 0:
                    send_email("Food Alert", " " + str(food_timing[1]) + " Diet \n Time : " + str(food_timing[2]) + " ",user[2])
                    toast = Notification(app_id="Diet Alert",
                                         title="Food Alert",
                                         msg="" + str(food_timing[1]) + " Diet \n Time : " + str(food_timing[2]) + "!",
                                         icon=r"c:\path\to\icon.png")

                    toast.show()
                    playsound('song.wav')
                    cursor.execute("insert into equalNotify(user_id,status,food_timing_id) values('" + str(session['user_id']) + "','Notified','"+str(food_timing[0])+"')")
                    conn.commit()

        for exercise_timing in exercise_timings:
             notify_exercise = exercise_timing[2]
             print(notify_exercise)
             notify_exercise = datetime.datetime.strptime(notify_exercise, "%H:%M")
             diff = notify_exercise - currentTime
             seconds = diff.seconds
             minutes = seconds / 3600
             print(minutes)
             if minutes < 30:
                 count = cursor.execute("select * from beforeNotify where user_id='" + str(session['user_id']) + "' and status='Notified' and exercise_timing_id='" + str(exercise_timing[0]) + "'")
                 if count == 0:
                     send_email("Exercise Alert", " " + str(exercise_timing[1]) + " Diet \n Time : " + str(exercise_timing[2]) + " ",user[2])
                     toast = Notification(app_id="Diet Alert",
                                          title="Exercise Alert",
                                          msg="" + str(exercise_timing[1]) + " Diet \n Time : " + str(exercise_timing[2]) + "!",
                                          icon=r"c:\path\to\icon.png")

                     toast.show()
                     playsound('song.wav')
                     cursor.execute("insert into beforeNotify(user_id,status,exercise_timing_id) values('" + str(
                         session['user_id']) + "','Notified'," + str(exercise_timing[0]) + ")")
                     conn.commit()
             elif minutes > 0 and minutes < 2:
                 count = cursor.execute("select * from equalNotify where user_id='" + str(session['user_id']) + "' and status='Notified' and exercise_timing_id='" + str(exercise_timing[0]) + "'")
                 if count == 0:
                     send_email("Exercise Alert"," " + str(exercise_timing[1]) + " Diet \n Time : " + str(exercise_timing[2]) + " ",user[2])
                     toast = Notification(app_id="Diet Alert",
                                          title="Exercise Alert",
                                          msg="" + str(exercise_timing[1]) + " Diet \n Time : " + str(
                                              exercise_timing[2]) + "!",
                                          icon=r"c:\path\to\icon.png")

                     toast.show()
                     playsound('song.wav')
                     cursor.execute("insert into equalNotify(user_id,status,exercise_timing_id) values('" + str(session['user_id']) + "','Notified','" + str(exercise_timing[0]) + "')")
                     conn.commit()

    return render_template("index.html")



app.run(debug=True,port=80,host="0.0.0.0")