from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app=Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres123@localhost/institute'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://flbkyrsudtcdkb:137b6a0124d64919d1a04144413773b6e3d123f34684a96d225f7be6bb29e83c@ec2-54-90-13-87.compute-1.amazonaws.com:5432/dfdvq49i0u2lnr?sslmode=require'

db=SQLAlchemy(app)
app.secret_key="hello"
app.permanent_session_lifetime= timedelta(minutes=5)



class Marks(db.Model):
    __tablename__="marks"
    mname_=db.Column(db.String(120), primary_key=True)
    math=db.Column(db.Integer)
    physics=db.Column(db.Integer)
    chemistry=db.Column(db.Integer)
    computer=db.Column(db.Integer)
    english=db.Column(db.Integer)

    def __init__(self,mname_):#,math,physics,chemistry,computer,english):
        self.mname_=mname_
        self.math=-1
        self.physics=-1
        self.chemistry=-1
        self.computer=-1
        self.english=-1

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    name_ = db.Column(db.String(120), unique=True)
    clas_ = db.Column(db.String(120))
    dob_ = db.Column(db.String(120))
    address_ = db.Column(db.String(120))
    vaccinated_ = db.Column(db.String(120))

    def __init__(self, name_, clas_, dob_, address_, vaccinated_):
        self.name_ = name_
        self.clas_ = clas_
        self.dob_ = dob_
        self.address_ = address_
        self.vaccinated_ = vaccinated_

staff = [[1, "A", "Math", "11 Feb 1980", "123 candy street"],
         [2, "B", "Physics", "17 Nov 1985", "234 apple street"],
         [3, "C", "Chemistry", "26 Mar 1976", "345 star apartments"],
         [4, "D", "Computer Science", "05 May 1984", "567 new street"],
         [5, "E", "English", "21 Oct 1982", "798 old apartments"]]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=['POST','GET'])
def login():
    if request.method=='POST':
        center =request.form["center"]
        name =request.form["name"]
        if center=="Staff":
            for i in range(5):
                if staff[i][1]==name:
                    session.permanent=True
                    session["value"]=i
                    return redirect(url_for("teacher"))
            flash("Name is not valid!","info")
            return redirect(url_for("login"))
        else:
            found_name=Student.query.filter_by(name_=name).first()
            if found_name:
                session.permanent=True
                session["stude"]=found_name.name_
                return redirect(url_for("student"))
            flash("Name is not valid!", "info")
            return redirect(url_for("login"))
    else:
        #flash("Please enter all details", "info")
        return render_template("login.html")

@app.route("/student_add", methods=['POST','GET'])
def student_add():
    if request.method=='POST':
        name = request.form["name"]
        clas = request.form["class"]
        dob = request.form["dob"]
        address = request.form["address"]
        vaccinated = request.form["vaccinated"]
        stud=Student(name,clas,dob,address,vaccinated)
        db.session.add(stud)
        db.session.commit()
        mar=Marks(name)
        db.session.add(mar)
        db.session.commit()
        flash("Student added successfully", "info")
        return redirect(url_for("teacher"))
    else:
        return render_template("student_add.html")

@app.route("/teacher", methods=['POST','GET'])
def teacher():
    if "value" in session:
        i=session["value"]
        if request.method=='POST':
            mk=request.form['dob']
            nam=request.form['submit']
            new_mk=Marks.query.filter_by(mname_=nam).first()
            if i==0:
                new_mk.math=mk
                db.session.commit()
            elif i==1:
                new_mk.physics = mk
                db.session.commit()
            elif i==2:
                new_mk.chemistry = mk
                db.session.commit()
            elif i==3:
                new_mk.computer = mk
                db.session.commit()
            else:
                new_mk.english = mk
                db.session.commit()
            return redirect(url_for("teacher"))
        else:
            v1=Student.query.filter_by(vaccinated_="yes",clas_="10-A").count()
            c1=Student.query.filter_by(clas_="10-A").count()
            v2=Student.query.filter_by(vaccinated_="yes",clas_="10-B").count()
            c2=Student.query.filter_by(clas_="10-B").count()
            v3=Student.query.filter_by(vaccinated_="yes",clas_="11-A").count()
            c3=Student.query.filter_by(clas_="11-A").count()
            v4=Student.query.filter_by(vaccinated_="yes",clas_="11-B").count()
            c4=Student.query.filter_by(clas_="11-B").count()
            v5=Student.query.filter_by(vaccinated_="yes",clas_="12-A").count()
            c5=Student.query.filter_by(clas_="12-A").count()
            x1="Online"
            x2="Online"
            x3="Online"
            x4="Online"
            x5="Online"
            if v1==c1:
                x1="Offline"

            if v2==c2:
                x2="Offline"
            if v3==c3:
                x3="Offline"
            if v4==c4:
                x4="Offline"
            if v5==c5:
                x5="Offline"
            return render_template("teacher.html",values=staff[i],results=Student.query.order_by(Student.id).all(),mks=Marks.query.all(),c=Student.query.count(),x1=x1,x2=x2,x3=x3,x4=x4,x5=x5)
    else:
        return redirect(url_for("login"))

@app.route("/student", methods=['POST','GET'])
def student():
    if "stude" in session:
        n=session["stude"]
        return render_template("student.html",values=Student.query.filter_by(name_=n).first(),results=Marks.query.filter_by(mname_=n).first())
    else:
        return redirect(url_for("login"))

@app.route("/student_edit", methods=['POST','GET'])
def student_edit():
    if "stude" in session:
        n = session["stude"]
        if request.method=='POST':
            dob=request.form["dob"]
            address=request.form["address"]
            vaccinated=request.form["vaccinated"]
            new_details = Student.query.filter_by(name_=n).first()
            new_details.dob_=dob
            db.session.commit()
            new_details.address_ = address
            db.session.commit()
            new_details.vaccinated_ = vaccinated
            db.session.commit()
            flash("Details edited successfully", "info")
            return redirect(url_for("student"))
        else:
            return render_template("student_edit.html",values=Student.query.filter_by(name_=n).first())
    else:
        return redirect(url_for("login"))

@app.route("/student_delete", methods=['POST','GET'])
def student_delete():
    if request.method == 'POST':
        name = request.form["name"]
        Student.query.filter_by(name_=name).delete()
        db.session.commit()
        Marks.query.filter_by(mname_=name).delete()
        db.session.commit()
        flash("Student deleted successfully", "info")
        return redirect(url_for("teacher"))
    else:
        return render_template("student_delete.html")

@app.route("/marks", methods=['POST','GET'])
def marks():
    return render_template("marks.html")

if __name__=='__main__':
    db.create_all()
    app.debug=True
    app.run()
