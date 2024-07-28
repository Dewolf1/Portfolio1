from flask import Flask, render_template, request,session,redirect,flash
from flask_mail import Mail
import json



with open("config.json","r") as c:
    params = json.load(c)["params"]


local_server = True
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail = Mail(app)


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/getme", methods= ["GET","POST"])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        mail.send_message('New message from ' + name,
                            sender=email,
                            recipients=[params['gmail-user']],
                            body=f"Name: {name} \n\n Subject: {subject} \n\n Message: {message}")
        flash("Thank you, we will get back to you as soon as we can.")

        return render_template('contact.html', params=params)
    else:
        return render_template('contact.html', params=params)


@app.route("/service")
def service():
    return render_template("service-details.html")

