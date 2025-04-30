# Online-Face-Attendance

This is a Flask-based web application for managing student attendance using face recognition. Students register with their face data, and attendance is marked automatically through live webcam face verification.

🚀 Features

👨‍🎓 Student Registration with Face Image
✅ Admin Authorization for Student Accounts
📸 Real-time Face Detection for Attendance
🕒 Automatic Check-In and Check-Out Time Logging
📅 Daily Attendance Records Viewable by Admin
🔒 Admin Login Panel
🛠️ Technologies Used

Python 3
Flask – Web Framework
OpenCV – Face Detection
MongoDB – NoSQL Database
HTML/CSS/JavaScript – Frontend
Bootstrap – Styling
📂 Project Structure

face-attendance/
├── templates/             # HTML templates
├── static/                # JS, CSS, assets
├── app.py                 # Main Flask app
├── requirements.txt       # Dependencies
└── README.md              # Project info
🧑‍💻 Getting Started

🔧 Prerequisites
Python 3.13.1
MongoDB installed and running locally
pip (Python package installer)
📥 Installation
Clone the repository
git clone https://github.com/your-username/face-attendance.git
cd face-attendance
Install dependencies
pip install -r requirements.txt
Start MongoDB
Make sure MongoDB is running locally on localhost:27017.

Run the Flask app
python app.py
Visit in browser
Open http://localhost:5000 or
http://<your-ip>:5000 to access from other devices.

📝 How It Works

Student fills out registration form with name, roll number, and face image (via webcam).
Admin reviews the list of pending students and approves or rejects them.
Once approved, students can mark attendance using facial recognition.
System automatically logs check-in and check-out times per day.
Admin can view all attendance records from the dashboard.
🔐 Default Admin Credentials

Username: admin
Password: admin123
(These can be changed in the database.)
📸 Face Capture Notes

Webcam access is required for face registration and attendance.
Uses Haar Cascade classifier for face detection (via OpenCV).
🧊 TODOs & Future Improvements

Face Recognition (currently only detection is implemented)
Student Login for viewing personal attendance
Email notifications on check-in/check-out
Attendance analytics and export to Excel/CSV


