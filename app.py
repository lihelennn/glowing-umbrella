import urllib2,json, information

from flask import Flask, render_template, url_for, session, request, redirect
app = Flask(__name__)

location=[]
temperature=0
fives = ["2016", "2015", "2014", "2013", "2012", "2011", "2010", "2005", "2000"]

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.args.get("submit") != "sub":
        print "yooyooooo"
        return render_template("home.html")
    else:
        location = [35,140]
        #location = request.form["javascript_data"]
        if location == None:
            location = [40.71, -74.01]
            msg = "We cannot detect where you are, but here are the temperatures for 10002, USA"
            return redirect(url_for('climate',lat=location[0], lon=location[1], msg=msg))
        return redirect(url_for('climate',lat=location[0], lon=location[1]))


@app.route('/climate', methods=['GET', 'POST'])
def climate():
    msg=""
    info = information.getRandomInfo()
    if request.args.get("information") == "information":
        info = information.getRandomInfo()

    if request.args.get("msg") == "We cannot detect where you are, but here are the temperatures for 10002, USA":
        msg = "We cannot detect where you are, but here are the temperatures for 10002, USA"
    else:
        msg = ""
    if request.args.get("submit") != "sub":
        temperature = 0
        latitude = request.args.get("lat")
        longitude = request.args.get("lon")
        #use api to search location
        #load information into climate

        url="http://api.openweathermap.org/data/2.5/weather?lat=latitude&lon=longitude&units=imperial&appid=48d99f11447bdb9eeecf3dc47ecc0f57"
        url=url.replace("latitude", latitude)
        url=url.replace("longitude", longitude)
        req = urllib2.urlopen(url)
        result = req.read()
        r = json.loads(result)
        for key in r.keys():
            if key == "main":
                main = r[key]
                temperature = main['temp']
                return render_template("climate.html",temperature=temperature, msg=msg, info=info)
    else:
        tempAvg2015=""
        tempAvg2010=""
        tempAvg2005=""
        tempAvg2000=""
        zipcode=request.args.get("zip")
        #if zipcode == "":
        #    msg = "please submit a zipcode"
        countrycode=request.args.get("country")
        #if countrycode == "":
        #    msg = "please submit a country code"
        for i in range(len(fives)):
            historyYear = fives[i]
            urlHistory= "https://api.weathersource.com/v1/5f7b808d57d0226ddfa9/history_by_postal_code.json?period=day&postal_code_eq=zipcode&country_eq=US&timestamp_eq=YEAR-02-02-10T00:00:00-05:00&fields=tempAvg"
            urlHistory=urlHistory.replace("zipcode", zipcode)
            urlHistory=urlHistory.replace("YEAR", historyYear)
            req = urllib2.urlopen(urlHistory)
            result = req.read()
            r = json.loads(result)
            if r != []:
                r = r[0]
                for key in r.keys():
                    if historyYear == "2016":
                        tempAvg2016 = r[key]
                    elif historyYear == "2015":
                        tempAvg2015= r[key]
                    elif historyYear == "2014":
                        tempAvg2014 = r[key]
                    elif historyYear == "2013":
                        tempAvg2013 = r[key]
                    elif historyYear == "2012":
                        tempAvg2012 = r[key]
                    elif historyYear == "2011":
                        tempAvg2011 = r[key]
                    elif historyYear == "2010":
                        tempAvg2010 = r[key]
                    elif historyYear == "2005":
                        tempAvg2005 = r[key]
                    elif historyYear == "2000":
                        tempAvg2000 = r[key]


        url="http://api.openweathermap.org/data/2.5/weather?zip=zipcode,countrycode&units=imperial&appid=48d99f11447bdb9eeecf3dc47ecc0f57"
        url=url.replace("zipcode", zipcode)
        url=url.replace("countrycode", countrycode)
        req = urllib2.urlopen(url)
        result = req.read()
        r = json.loads(result)
        for key in r.keys():
            if key == "main":
                main = r[key]
                temperature = main['temp']
                print "HELLO"
                return render_template("climate.html",temperature=temperature, msg=msg, tempAvg2016=tempAvg2016,tempAvg2015=tempAvg2015, tempAvg2014=tempAvg2014, tempAvg2013=tempAvg2013, tempAvg2012=tempAvg2012, tempAvg2011=tempAvg2011,tempAvg2010=tempAvg2010, tempAvg2005=tempAvg2005,tempAvg2000=tempAvg2000, info=info)
        return render_template("home.html")



if __name__ == "__main__":
    app.debug = True # change to false when deploying
    app.secret_key = "yo"
    app.run(host="0.0.0.0", port=8000)
