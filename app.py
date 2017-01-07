from flask import Flask, render_template, url_for, session, request, redirect
app = Flask(__name__)


@app.route('/home')
def home():
    return render_template("home.html")




if __name__ == "__main__":
    app.debug = True # change to false when deploying
    app.secret_key = "yo"
    app.run(host="0.0.0.0", port=8001)
