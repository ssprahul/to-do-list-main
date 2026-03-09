from flask import Flask, render_template, request ,url_for,session,redirect
from pymongo import MongoClient

client=MongoClient('mongodb+srv://revanth200319:revanth200319@cluster0.zrtypbn.mongodb.net/')

db=client["TODOList"]
collectionform=db['sample']

app=Flask(__name__)

app.secret_key="revanth"

@app.route("/")
def home():
    return render_template("home.html")


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/registerverify',methods=["post"])
def registration():
    collectionform=db['formdata']
    name=request.form['name']
    username=request.form['username']
    email=request.form['email']
    password=request.form['password']
    phonenumber=request.form['phonenumber']
    collectionform.insert_one({
        'name':name,
        'username':username,
        'email':email,
        'password':password,
        'phonenumber':phonenumber  
    })
    return render_template("login.html",message="Registration Successful! Please Login.")


@app.route('/log',methods=["POST"])
def loginverify():
    collectionform=db['formdata']
    username=request.form['username']
    password=request.form['password']
    user=collectionform.find_one({
        'username':username,
        'password':password
    })
    if user:
        session['username']=user['username']
        return redirect(url_for('dashboard'))
    else:
        return render_template("login.html",message="Invalid Credentials! Please try again.")

@app.route('/add-task')
def add_task():
    return render_template("addtask.html")


@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html",message="You have been logged out successfully.")

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return render_template("login.html", message="Please login first.")
    collectiontasks = db['tasks']
    tasks = collectiontasks.find({
        'username': session['username']
    })
    return render_template("index.html",username=session['username'],tasks=tasks)

@app.route('/remove-task', methods=["POST"])
def remove_task():

    if 'username' not in session:
        return render_template("login.html", message="Please login first.")

    taskname = request.form.get("taskname")

    collectiontasks = db['tasks']

    collectiontasks.delete_one({
        'taskname': taskname,
        'username': session['username']
    })
    return redirect(url_for('dashboard'))




@app.route('/addtask',methods=["POST"])
def addtask():
    if 'username' not in session:
        return render_template("login.html",message="Please login to add tasks.")
    collectiontasks=db['tasks']
    taskname=request.form.get('taskname')
    status=request.form.get('status')
    priority=request.form.get('priority')
    collectiontasks.insert_one({
        'username':session['username'],
        'taskname':taskname,
        'status':status,
        'priority':priority
    })
    
    tasks=collectiontasks.find({'username':session['username']})
    return redirect(url_for('dashboard'))
    
if __name__ == "__main__":
    app.run(debug=True)