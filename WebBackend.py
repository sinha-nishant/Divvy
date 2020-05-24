from flask import Flask, redirect,url_for,render_template,request

app= Flask(__name__)


@app.route('/', methods=['POST','GET'])
def home():
    if request.method =="POST":
        date = request.form["date"]
        category= request.form["category"]
        location = request.form["loc"]
        Nishant = request.form["nishant"]
        Arjun = request.form["arjun"]
        Param = request.form["param"]
        newUserName= request.form["userName"]
        newUserTotal = request.form["userTotal"]
        total = request.form["total"]
        print("Date =", date)
        print("Category =", category)
        print("Location =", location)
        print("Nishant cost =", Nishant)
        print("Arjun cost =", Arjun)
        print("Param cost =", Param)
        print("Added user name =", newUserName)
        print("Added user total =", newUserTotal)
        print("Total cost =", total)


        return render_template("AddOrder.html")
    else:
        return render_template("AddOrder.html")

if __name__ =="__main__":
    app.run()