import urllib2, json, time, information

from flask import Flask, render_template, url_for, session, request, redirect
app = Flask(__name__)

location=[]
temperature=0
fives = ["2016", "2015", "2014", "2013", "2012", "2011", "2010"]

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    msg=""
    if request.args.get("submit") != "sub":
        return render_template("home.html")
    else:
        if request.args.get("data") != None:
            location = request.args.get("data")
            return redirect(url_for('climate',lat=location[0], lon=location[1], msg=msg))
        else:
            print "no it is not"
            return redirect(url_for('climate',lat=30, lon=-100, msg="Loading for something else"))


#use api to search location
#load information into climate
#loads the current/past temperatures of the location
@app.route('/climate')
def climate():
    #location = request.form["data"]
    todayDate = time.strftime("%m-%d")
    zipcodeGiven = False
    msg=request.args.get("msg")
    if msg == None:
        msg=""
    tempAvg2016=""
    tempAvg2015=""
    tempAvg2014=""
    tempAvg2013=""
    tempAvg2012=""
    tempAvg2011=""
    tempAvg2010=""
    info = information.getRandomInfo()

    #if user requests new info...this does not work yet
    if request.args.get("information") == "information":
        info = information.getRandomInfo()

    try:
        if request.args.get("submit") != "sub":
            temperature = 0
            latitude = request.args.get("lat")
            longitude = request.args.get("lon")
            urlZip="http://ziplocate.us/api/v1/reverse/latitude,longitude"
            urlZip=urlZip.replace("latitude", latitude)
            urlZip=urlZip.replace("longitude", longitude)
            print urlZip
            req = urllib2.urlopen(urlZip)
            result = req.read()
            r = json.loads(result)
            zipcode = r["zip"]
            print zipcode
        else:
            zipcodeGiven = True
            zipcode=request.args.get("zip")
            countrycode=request.args.get("country")

        for i in range(len(fives)):
            historyYear = fives[i]

            urlHistory= "https://api.weathersource.com/v1/5f7b808d57d0226ddfa9/history_by_postal_code.json?period=day&postal_code_eq=zipcode&country_eq=US&timestamp_eq=YEAR-DAYT00:00:00-05:00&fields=tempAvg"
            urlHistory=urlHistory.replace("zipcode", zipcode)
            urlHistory=urlHistory.replace("YEAR", historyYear)
            urlHistory=urlHistory.replace("DAY", todayDate)
            print urlHistory

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
    except:
            print "Something went wrong"

    todayDate = time.strftime("%A, %B %d, %Y")

    if not zipcodeGiven:
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
                return render_template("climate.html", todayDate=todayDate, temperature=temperature, info=info, msg=msg, tempAvg2016=tempAvg2016,tempAvg2015=tempAvg2015, tempAvg2014=tempAvg2014, tempAvg2013=tempAvg2013, tempAvg2012=tempAvg2012, tempAvg2011=tempAvg2011,tempAvg2010=tempAvg2010)
    else:
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
                return render_template("climate.html", todayDate=todayDate,temperature=temperature, info=info, msg=msg, tempAvg2016=tempAvg2016,tempAvg2015=tempAvg2015, tempAvg2014=tempAvg2014, tempAvg2013=tempAvg2013, tempAvg2012=tempAvg2012, tempAvg2011=tempAvg2011,tempAvg2010=tempAvg2010)
    return render_template("home.html")



if __name__ == "__main__":
    app.debug = True # change to false when deploying
    app.secret_key = "yo"
    app.run(host="0.0.0.0", port=8000)
