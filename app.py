import urllib2,json

from flask import Flask, render_template, url_for, session, request, redirect
app = Flask(__name__)

location=[]
temperature=0

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
def home():
    if request.method=="GET":
        return render_template("home.html")
    else:
        print "222222222"
        print "location"
        print "ugh"

        location = request.form["javascript_data"]
        if location == None:
            print "YO"
        else:
            print "hi"
        latitude = location[0]
        longitude = location[1]
        #use api to search location
        #load information into climate

        url="http://api.openweathermap.org/data/2.5/find?lat=latitude&lon=longitude&cnt=10&units=Imperial&appid=48d99f11447bdb9eeecf3dc47ecc0f57"
        url=url.replace("latitude", latitude)
        url=url.replace("longitude", longitude)
        req = urllib2.urlopen(url)
        result = req.read()
        r = json.loads(result)

        if r.has_key("main"):
            main = r["main"]
            temperature = main["temp"]
        return render_template("climate.html",temperature=temperature)

@app.route('/climate')
def climate():
    return render_template("climate.html", location=location)


if __name__ == "__main__":
    app.debug = True # change to false when deploying
    app.secret_key = "yo"
    app.run(host="0.0.0.0", port=8000)
