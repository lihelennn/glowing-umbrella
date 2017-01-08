import urllib2,json

from flask import Flask, render_template, url_for, session, request, redirect
app = Flask(__name__)

location=[]
temperature=0

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.args.get("submit") != "sub":
        return render_template("home.html")
    else:
        print "hello"
        location = [1,1]
        print location
        return redirect(url_for('climate',lat=location[0], lon=location[1]))


@app.route('/climate', methods=['GET', 'POST'])
def climate():
    temperature = 0
    latitude = request.args.get("lat")
    longitude = request.args.get("lon")
    print latitude
    print longitude
    #use api to search location
    #load information into climate

    url="http://api.openweathermap.org/data/2.5/find?lat=latitude&lon=longitude&cnt=10&units=Imperial&appid=48d99f11447bdb9eeecf3dc47ecc0f57"
    url=url.replace("latitude", "1")
    url=url.replace("longitude", "1")
    req = urllib2.urlopen(url)
    result = req.read()
    r = json.loads(result)
    for key in r:
        print key[0]
        if key[0] == "m":
            main = key
            temperature = main["temp"]
            print "HELLO"
            return render_template("climate.html",temperature=temperature)
    print "UGHH"
    return render_template("home.html")


if __name__ == "__main__":
    app.debug = True # change to false when deploying
    app.secret_key = "yo"
    app.run(host="0.0.0.0", port=8000)
