from app import app
from flask import render_template, request, redirect,url_for,flash, session
from app.forms import SignUp,SignIn
from app.dbmodels import User,History
from datetime import timedelta
from app.model import dlmodel
from app import db
from flask_login import login_user,logout_user,login_required
import os   

from werkzeug.utils import secure_filename

app.permanent_session_lifetime = timedelta(minutes=5)   

app.config["AUDIO_UPLOAD"]="input"
app.config["ALLOWED_AUDIO_EXTENSION"]="WAV"
app.config['SECRET_KEY'] = 'ser_key'
def allowed_audio(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".",1)[1]

    if ext.upper() in app.config["ALLOWED_AUDIO_EXTENSION"]:
        return True
    else:
        return False


@app.route("/", methods=["GET", "POST"])
@app.route('/home')
def home_page():

    if request.method == "POST":
        if request.files:
            audio = request.files["audio"]
            if audio.filename == "":
                print("audiofile must have filename")
                flash(f"audiofile must have filename", category="warning")
                return redirect(request.url)

            if not allowed_audio(audio.filename):
                print("Audio File format is not allowed please upload .wav file only")
                flash(f"Audio File format is not allowed please upload .wav file only", category="danger")
                return redirect(request.url)
            else:
                filename = secure_filename(audio.filename)
                audio.save(os.path.join(app.config["AUDIO_UPLOAD"], filename))
                audio_files=os.listdir(app.config["AUDIO_UPLOAD"])  
                flash("Your file is uploaded Successfully", category="success")
                return render_template("base.html",files=audio_files )

            #print("Audio file saved") 
            #return redirect(request.url)
    audio_files=os.listdir(app.config["AUDIO_UPLOAD"])   
    return render_template("base.html",files=audio_files)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/sign-up", methods=["GET","POST"])
def sign_up(): 
    form = SignUp() 
    if form.validate_on_submit():

        user_to_create= User(email=form.email.data,
                            username=form.username.data, 
                            first_name=form.firstname.data, 
                            last_name=form.lastname.data,
                            password= form.password1.data )
        
        db.session.add(user_to_create)
        db.session.commit()
        print("Data Added to db")
        return redirect(url_for('sign_in'))

    if form.errors !={}:# No errors from validations
        for err_msg in form.errors.values():
            flash(f'There is a error:{err_msg}',category='danger') 

    return render_template("sign-up.html",form=form)


@app.route("/sign-in", methods=["GET","POST"])
def sign_in():

    form = SignIn()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first() 
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
                login_user(attempted_user)
                session.permanent = True
                session["user"] = attempted_user.username
                flash(f'You are logged in as: {attempted_user.username}', category='success')
                return redirect(url_for('profile'))
       
        else:
            flash(f'Username or Password are not matcged!',category='danger')

    return render_template("sign-in.html", form=form)

@app.route("/profile")
@login_required
def profile():

    if "user" in session:
        users = User.query.filter_by(username=session["user"]).first()
        if users:
            users = User.query.filter_by(username=session["user"]).first()
            history = History.query.filter_by(data_id=users.id).all()
            return render_template("public/profile.html",users=users,histories=history)
        
    return redirect(url_for('sign_in'))

@app.route('/logout')
def logout_page():
    logout_user()
    flash(f"You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route("/prediction",methods=["GET","POST"])
@login_required
def prediction():
    if request.method == "POST":
        if "user" in session:
            file_name=request.form['file']
            users = User.query.filter_by(username=session["user"]).first()
            predictions = dlmodel(file_name=file_name)
            history_of_user = History(file_name=file_name,
                                      emotion=predictions[1],
                                      gender = predictions[0],
                                      data_id=users.id)
            db.session.add(history_of_user)
            db.session.commit()
            print("data added to DB")
            return render_template("prediction.html",predictions=predictions)
        
@app.route('/delete/<int:id>')
def delete(id):

    history_to_delete=History.query.get_or_404(id)

    try:
        db.session.delete(history_to_delete)
        db.session.commit()
        return redirect(url_for('profile'))
    except:
        flash(f"There is Problem deleting the history")
        return redirect(url_for('profile'))

@app.route('/deleteall/<int:data_id>')
def delete_all(data_id):

    history = History.query.filter_by(data_id=data_id).delete()
    flash(f"{ history} histories are deleted",category='success')
    db.session.commit()
    return redirect(url_for('profile'))