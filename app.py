from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://anju:anju@localhost:5432/flaskpg-db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://anju:anju@localhost/students'
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50))
    student_course = db.Column(db.String(50))
    student_phone = db.Column(db.String(20))
    student_picture = db.Column(db.String(200))
    
    def __init__(self, student_name, student_course, student_phone, student_picture):
        self.student_name = student_name
        self.student_course = student_course
        self.student_phone = student_phone
        self.student_picture = student_picture

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        student_name = request.form['student_name']
        student_course = request.form['student_course']
        student_phone = request.form['student_phone']
        student_picture = request.form['student_picture']
        student = Student(student_name, student_course, student_phone , student_picture)

        try:
            db.session.add(student)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print("Error while saving to DB." + str(e))
    else:
        #students = Student.query.order_by(Student.date_created).all()
        students = Student.query.order_by(Student.student_id).all()
        return render_template('index.html', students=students)
    return render_template('index.html')


@app.route('/delete/<int:student_id>')
def delete(student_id):
    record_to_delete = Student.query.get_or_404(student_id)

    try:
        db.session.delete(record_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print("Error while delete from DB." + str(e))
        return 'There was a problem deleting the student.'


@app.route('/update/<int:student_id>', methods=['GET', 'POST'])
def update(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        student.student_name = request.form['student_name']
        student.student_course = request.form['student_course']
        student.student_phone = request.form['student_phone']
        student.student_picture = request.form['student_picture']
        student = Student(student.student_name, student.student_course, student.student_phone, student.student_picture)

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print("Error while update on DB." + str(e))
            return 'There was a problem updating the student.'

    else:
        return render_template('update.html', student=student)


if __name__ == '__main__':  # python interpreter assigns "__main__" to the file you run
    app.run(debug=True)