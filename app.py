from flask import Flask, render_template, request, session, redirect
from myplace import Myplace
from bs4 import BeautifulSoup
import subprocess
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)

        uploaded_file = request.files['pic']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["pic"]=uploaded_file.filename


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into user (pic,username,email,phone,password,country_id,fakejob,fakebio) values (:pic,:username,:email,:phone,:password,:country_id,:fakejob,:fakebio)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from user')


        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['pic','username','email','phone','password','country_id','fakejob','fakebio']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['pic','username','email','phone','password','country_id','fakejob','fakebio']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['pic','username','email','phone','password','country_id','fakejob','fakebio']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from country')


        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_htmlcolorcode", methods=["GET","POST"])
def add_one_htmlcolorcode():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        one_user = query_db("insert into htmlcolorcode (content,user_id) values (:content,:user_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from htmlcolorcode')


        return render_template("htmlcolorcodeform.html", htmlcolorcodes=user, one_user=one_user, the_title="add new htmlcolorcode", touslesuser=touslesuser)


    touslesuser= query_db("select * from user")

    user = query_db('select * from htmlcolorcode')
    one_user = query_db("select * from htmlcolorcode limit 1", one=True)
    return render_template("htmlcolorcodeform.html", htmlcolorcodes=user, one_user=one_user, the_title="add new htmlcolorcode", touslesuser=touslesuser)

@app.route("/add_one_detectlanguage", methods=["GET","POST"])
def add_one_detectlanguage():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into detectlanguage (content,language) values (:content,:language)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from detectlanguage')


        return render_template("detectlanguageform.html", detectlanguages=user, one_user=one_user, the_title="add new detectlanguage")


    user = query_db('select * from detectlanguage')
    one_user = query_db("select * from detectlanguage limit 1", one=True)
    return render_template("detectlanguageform.html", detectlanguages=user, one_user=one_user, the_title="add new detectlanguage")

