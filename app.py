from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
import datetime
import cv2
import numpy as np
import base64

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["MONGO_URI"] = "mongodb://localhost:27017/face_attendance"
mongo = PyMongo(app)

# Database collections
students = mongo.db.students
attendance = mongo.db.attendance
admins = mongo.db.admins

# Load face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            student_data = {
                'name': request.form['name'],
                'roll_no': request.form['roll_no'],
                'email': request.form['email'],
                'face_image': request.form['face_image'],
                'approved': False,
                'registered_at': datetime.datetime.now()
            }
            students.insert_one(student_data)
            flash('Registration successful! Waiting for admin approval.')
            return redirect('/')
        except:
            flash('Registration failed!')
    return render_template('register.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin = admins.find_one({
            'username': request.form['username'],
            'password': request.form['password']
        })
        if admin:
            session['admin'] = True
            return redirect('/authorize-students')
        flash('Invalid credentials!')
    return render_template('admin_login.html')

@app.route('/authorize-students')
def authorize_students():
    if 'admin' not in session:
        return redirect('/admin-login')
    
    pending_students = students.find({'approved': False})
    return render_template('authorize.html', students=pending_students)

@app.route('/approve/<student_id>')
def approve(student_id):
    students.update_one({'_id': ObjectId(student_id)}, {'$set': {'approved': True}})
    return redirect('/authorize-students')

@app.route('/reject/<student_id>')
def reject(student_id):
    students.delete_one({'_id': ObjectId(student_id)})
    return redirect('/authorize-students')

@app.route('/mark-attendance', methods=['GET', 'POST'])
def mark_attendance():
    if request.method == 'POST':
        student = students.find_one({
            'name': request.form['name'],
            'roll_no': request.form['roll_no'],
            'approved': True
        })
        
        if not student:
            flash('Student not approved or invalid details!')
            return redirect('/mark-attendance')
        
        return render_template('face_capture.html', 
                            student_id=str(student['_id']))
    
    return render_template('mark_attendance.html')

@app.route('/verify-face', methods=['POST'])
def verify_face():
    try:
        student = students.find_one({'_id': ObjectId(request.form['student_id'])})
        img_data = request.form['image'].split(',')[1]
        nparr = np.frombuffer(base64.b64decode(img_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) > 0:
            # Fix: Use datetime instead of date
            today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            now = datetime.datetime.now()
            
            record = attendance.find_one({
                'student_id': student['_id'],
                'date': today
            })
            
            if not record:
                attendance.insert_one({
                    'student_id': student['_id'],
                    'check_in': now,
                    'check_out': None,
                    'date': today
                })
                return jsonify({
                    'success': True,
                    'message': f"Check-in recorded at {now.strftime('%Y-%m-%d %H:%M:%S')}",
                    'type': 'check_in'
                })
            else:
                attendance.update_one(
                    {'_id': record['_id']},
                    {'$set': {'check_out': now}}
                )
                return jsonify({
                    'success': True,
                    'message': f"Check-out recorded at {now.strftime('%Y-%m-%d %H:%M:%S')}",
                    'type': 'check_out'
                })
        
        return jsonify({'success': False, 'message': 'No face detected!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/view-attendance')
def view_attendance():
    records = attendance.aggregate([{
        '$lookup': {
            'from': 'students',
            'localField': 'student_id',
            'foreignField': '_id',
            'as': 'student'
        }
    }])
    return render_template('view_attendance.html', 
                        records=list(records))

if __name__ == '__main__':
    with app.app_context():
        if admins.count_documents({}) == 0:
            admins.insert_one({
                'username': 'admin',
                'password': 'admin123'
            })
    app.run(debug=True)