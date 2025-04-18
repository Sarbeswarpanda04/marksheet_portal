from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
import os  
import mysql.connector
from flask_mail import Mail, Message
import random
import re
import smtplib

app = Flask(__name__)
app.secret_key = 'S@rb3sw@r_OTP_Se$$ion_Key_123!'  # Replace with a strong secret key

# Flask-Mail Configuration
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='sarbeswarpanda143@gmail.com',        # Replace with your email
    MAIL_PASSWORD='bfwtduylcewbalmp'            # Replace with your app password
)
mail = Mail(app)

# # MySQL DB Connection
# def get_db_connection():
#     return mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='Sarbeswar@123',                 # Your MySQL root password
#         database='marksheet_portal'               # Your database name
#     )
    
# MySQL DB Connection
def get_db_connection():
    return mysql.connector.connect(
        host='mysql-d8d8c8a-sarbeswarpanda143-36cb.f.aivencloud.com',
        user='avnadmin',
        port=25309,
        password='AVNS__Nh9xl2rlVgCUarubfp',                 # Your MySQL root password
        database='marksheet_portal'               # Your database name
    )
  
    
# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("Login POST received")

        user_type = request.form.get('role')  # 'student' or 'admin'
        username = request.form.get('username')
        password = request.form.get('password')

        print("Username:", username)
        print("Password:", password)

        # Student validation
        if user_type == 'student':
            if not (username.isdigit() and len(username) == 10):
                flash("Registration number must be a 10-digit number.", 'danger')
                return redirect(url_for('login'))

        # Password pattern validation
        if not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$', password):
            flash("Password must be alphanumeric with at least one special character.", 'danger')
            return redirect(url_for('login'))

        # Connect to DB and validate user
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        user = None

        # if user_type == 'student':
        #     cursor.execute("SELECT * FROM students WHERE reg_no = %s AND password = %s", (username, password))
        #     user = cursor.fetchone()
        # elif user_type == 'admin':
        #     cursor.execute("SELECT * FROM admins WHERE admin_id = %s AND password = %s", (username, password))
        #     user = cursor.fetchone()
        
        if user_type == 'student':
          query = "SELECT * FROM students WHERE registration_number = %s AND password = %s"
          print("Executing query:", query, "with params:", (username, password))
          cursor.execute(query, (username, password))
          user = cursor.fetchone()
        elif user_type == 'admin':
          query = "SELECT * FROM admin WHERE admin_id = %s AND password = %s"
          print("Executing query:", query, "with params:", (username, password))
          cursor.execute(query, (username, password))
          user = cursor.fetchone()
        else:
            flash("Invalid user type.", "danger")
            return redirect(url_for('login'))

        print("User from DB:", user)

        cursor.close()
        conn.close()

        if user:
            session['username'] = username
            session['user_type'] = user_type
            session['email'] = user['email']
            
                     # Add role-specific identifiers
            if user_type == 'admin':
                session['admin_id'] = user['admin_id']  # Store admin_id for admin users
            elif user_type == 'student':
                session['student_id'] = user['id']  # Store student_id for student users
            

            otp = str(random.randint(100000, 999999))
            session['otp'] = otp

            print("Session values:", dict(session))

            try:
                msg = Message('Your OTP for Login', sender=app.config['MAIL_USERNAME'], recipients=[user['email']])
                msg.html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body {{
                            font-family: 'Arial', sans-serif;
                            background-color: #f4f4f4;
                            color: #333;
                            padding: 20px;
                            margin: 0;
                            font-size: 16px;
                            line-height: 1.5;
                            text-align: center;
                            
                        }}
                        .container {{
                            max-width: 600px;
                            margin: 0 auto;
                            background: #ffffff;
                            padding: 20px;
                            border-radius: 8px;
                            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                            
                        }}
                        h1 {{
                            color: #007bff;
                            font-size: 2rem;
                            margin-bottom: 20px;
                        }}
                        p {{
                            line-height: 1.6;
                            font-size: 1rem;
                            margin: 10px 0;
                        }}
                        .otp {{
                            font-size: 1.5rem;
                            font-weight: bold;
                            color: #28a745;
                            margin: 20px 0;
                        }}
                        .footer {{
                            margin-top: 20px;
                            font-size: 0.9rem;
                            color: #666;
                            text-align: center;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Marksheet Management Portal</h1>
                        <p>Dear {user['name']},</p>
                        <p>We have received a login request for your account. To proceed, please use the following One-Time Password (OTP):</p>
                        <p class="otp">{otp}</p>
                        <p>This OTP is valid for the next 10 minutes. If you did not request this, please ignore this email or contact support immediately.</p>
                        <p>Thank you,<br>The Marksheet Management Portal Team</p>
                        <div class="footer">
                            <p>© 2025 Marksheet Management Portal. All rights reserved.</p>
                        </div>
                    </div>
                </body>
                </html>
                """
                 # Attach a file (e.g., a PDF or image)
                file_path = "static/images/hero-bg.jpg"  # Path to the file you want to attach
                if os.path.exists(file_path):
                    with app.open_resource(file_path) as attachment:
                        msg.attach("hero-bg.jpg", "application/pdf", attachment.read())
                else:
                    print("Attachment file not found:", file_path)  
 
                mail.send(msg) # Send the email with the OTP

                flash('OTP sent to your email.', 'info')  # Use 'info' for OTP sent message
                print("✅ Email sent successfully.")
                return redirect(url_for('verify_otp'))  # ✅ MISSING RETURN ADDED HERE!
            except Exception as e:
                print("❌ Failed to send email:", e)
                flash('Failed to send OTP. Please try again later.', 'danger')
                return redirect(url_for('login'))

        else:
            flash('Invalid credentials. Try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')





# ---------------- OTP VERIFICATION ----------------
# @app.route('/verify_otp', methods=['GET', 'POST'])
# def verify_otp():
#     if request.method == 'POST':
#         entered_otp = request.form.get('otp')
#         if entered_otp == session.get('otp'):
#             flash('Login Successful!', 'success')
#             if session['user_type'] == 'student':
#                 return redirect(url_for('student_dashboard'))
#             else:
#                 return redirect(url_for('admin_dashboard'))
#         else:
#             flash('Invalid OTP. Please try again.', 'danger')
#             return redirect(url_for('verify_otp'))

#     return render_template('verify_otp.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form.get('otp_input')
        session_otp = session.get('otp')

        if entered_otp == session_otp:
            flash('OTP verified successfully!', 'success')

            # Redirect based on role
            if session.get('user_type') == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash('Incorrect OTP. Please try again.', 'danger')
            return redirect(url_for('verify_otp'))

    return render_template('verify_otp.html')




# ---------------- DASHBOARDS ----------------

@app.route('/student_dashboard')
def student_dashboard():
    # Ensure the user is logged in and is a student
    if 'student_id' not in session or session.get('user_type') != 'student':
        flash('Unauthorized access. Please log in as a student.', 'danger')
        return redirect(url_for('login'))

    # Fetch student details
    username = session['student_id']  # Use student ID for fetching details
    # username = session['username']  # Use registration number for fetching details
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get student info
    cursor.execute("SELECT * FROM students WHERE registration_number = %s", (username,))
    student = cursor.fetchone()

    # Get exam records for the student
    cursor.execute("""
        SELECT exams.name AS exam_name, subjects.name AS subject_name, marks.marks
        FROM marks
        JOIN exams ON marks.exam_id = exams.id
        JOIN subjects ON marks.subject_id = subjects.id
        WHERE marks.student_id = %s
        ORDER BY exams.name, subjects.name
    """, (student['id'],))
    records = cursor.fetchall()

    # Get percentage (simplified logic)
    cursor.execute("SELECT AVG(marks) FROM marks WHERE student_id = %s", (student['id'],))
    percentage = cursor.fetchone()['AVG(marks)'] or 0

    conn.close()

    # Pass data to the template
    return render_template('student_dashboard.html',
                           student=student,
                           records=records,
                           percentage=round(percentage, 2))


@app.route('/edit-admin-profile', methods=['GET', 'POST'])
def edit_admin_profile():
    # Ensure the admin is logged in
    if 'admin_id' not in session:
        flash('Please log in to access this feature.', 'danger')
        return redirect(url_for('login'))

    admin_id = session['admin_id']  # Get the logged-in admin's ID from the session

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Get updated details from the form
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']

        # Update the admin details in the database
        cursor.execute("""
            UPDATE admin
            SET name = %s, email = %s, mobile = %s, password = %s
            WHERE admin_id = %s
        """, (name, email, mobile, password, admin_id))
        conn.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    # Fetch the admin's current details for the form
    cursor.execute("SELECT * FROM admin WHERE admin_id = %s", (admin_id,))
    admin = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('edit_admin_profile.html', admin=admin)




@app.route('/change-admin-password', methods=['POST'])
def change_admin_password():
    # Ensure the admin is logged in
    if 'admin_id' not in session:
        return jsonify({'status': 'error', 'message': 'Please log in to change your password.'}), 401

    admin_id = session['admin_id']  # Get the logged-in admin's ID from the session

    # Get form data
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    # Validate new password
    if new_password != confirm_password:
        return jsonify({'status': 'error', 'message': 'New passwords do not match.'}), 400

    if not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$', new_password):
        return jsonify({'status': 'error', 'message': 'Password must be at least 6 characters, contain letters, numbers, and symbols.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Verify current password
    cursor.execute("SELECT password FROM admin WHERE admin_id = %s", (admin_id,))
    admin = cursor.fetchone()

    if not admin or admin['password'] != current_password:
        return jsonify({'status': 'error', 'message': 'Current password is incorrect.'}), 400

    # Update the password
    cursor.execute("UPDATE admin SET password = %s WHERE admin_id = %s", (new_password, admin_id))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Password updated successfully.'})





# @app.route('/admin-dashboard')
# def admin_dashboard():
#     # Ensure the admin is logged in
#     if 'admin_id' not in session:
#         flash('Please log in to access the dashboard.', 'danger')
#         return redirect(url_for('login'))

#     admin_id = session['admin_id']  # Get the logged-in admin's ID from the session

#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)

#     # Fetch admin details
#     cursor.execute("SELECT name, profile_photo FROM admin WHERE admin_id = %s", (admin_id,))
#     admin = cursor.fetchone()

#     # Fetch dashboard statistics
#     cursor.execute("SELECT COUNT(*) AS total_students FROM students")
#     total_students = cursor.fetchone()['total_students']

#     cursor.execute("SELECT COUNT(*) AS total_subjects FROM subjects")
#     total_subjects = cursor.fetchone()['total_subjects']

#     cursor.execute("SELECT COUNT(*) AS total_exams FROM exams")
#     total_exams = cursor.fetchone()['total_exams']

#     # Example placeholder for the latest marksheet
#     cursor.execute("SELECT MAX(generated_date) AS latest_mark FROM marksheet")
#     latest_mark = cursor.fetchone()['latest_mark'] or "No marksheet available"

#     cursor.close()
#     conn.close()

#     return render_template(
#         "admin_dashboard.html",
#         admin=admin,
#         total_students=total_students,
#         total_subjects=total_subjects,
#         total_exams=total_exams,
#         latest_mark=latest_mark
#     )



# @app.route('/admin-dashboard')
# def admin_dashboard():
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute("SELECT COUNT(*) FROM students")
#     total_students = cursor.fetchone()[0]

#     cursor.execute("SELECT COUNT(*) FROM subjects")
#     total_subjects = cursor.fetchone()[0]

#     cursor.execute("SELECT COUNT(*) FROM exams")
#     total_exams = cursor.fetchone()[0]

#     #Example placeholder for latest marksheet
#     latest_mark = "Final_Exam_Results_2023"
#     #cursor.execute("SELECT exam_id, student_id, generated_date FROM marksheet ORDER BY generated_date DESC LIMIT 1")      
    

#     conn.close()

#     return render_template("admin_dashboard.html",
#                            total_students=total_students,
#                            total_subjects=total_subjects,
#                            total_exams=total_exams,
#                            latest_mark=latest_mark)








@app.route('/admin-dashboard')
def admin_dashboard():
    # Ensure the admin is logged in
    if 'admin_id' not in session:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('login'))

    admin_id = session['admin_id']  # Get the logged-in admin's ID from the session

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch admin details
    cursor.execute("SELECT name, profile_photo FROM admin WHERE admin_id = %s", (admin_id,))
    admin = cursor.fetchone()

    # Fetch dashboard statistics
    cursor.execute("SELECT COUNT(*) AS total_students FROM students")
    total_students = cursor.fetchone()['total_students']

    cursor.execute("SELECT COUNT(*) AS total_subjects FROM subjects")
    total_subjects = cursor.fetchone()['total_subjects']

    cursor.execute("SELECT COUNT(*) AS total_exams FROM exams")
    total_exams = cursor.fetchone()['total_exams']

    cursor.execute("SELECT MAX(generated_date) AS latest_mark FROM marksheet")
    latest_mark = cursor.fetchone()['latest_mark'] or "No marksheet available"

    cursor.close()
    conn.close()

    return render_template(
        "admin_dashboard.html",
        admin=admin,
        total_students=total_students,
        total_subjects=total_subjects,
        total_exams=total_exams,
        latest_mark=latest_mark
    )
    
    
    
    
    
@app.route('/student-profile')
def student_profile():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Use dictionary=True for named columns
    cursor.execute("SELECT * FROM students ORDER BY id DESC")  # Fetch all students
    students = cursor.fetchall()  # Fetch all students from the database
    conn.close()  
    return render_template('student_profile.html', students=students)

import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename



UPLOAD_FOLDER = 'static/images/student_photos'  # Directory to save uploaded files
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'png', 'jpg', 'jpeg', 'gif', 'webp'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images', 'student_photos')  # Ensure the path is correct


os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add-student', methods=['POST'])
def add_student():
    name = request.form['name']
    student_class = request.form['student_class']  # input name in form must be 'student_class'
    dob = request.form['dob']
    father_name = request.form['father_name']
    mother_name = request.form['mother_name']
    registration_number = request.form['registration_number']
    roll_no = request.form['roll_no']
    email = request.form['email']
    password = request.form['password']

    profile_photo = request.files['profile_photo']
    filename = ''
    if profile_photo and allowed_file(profile_photo.filename):
        filename = secure_filename(profile_photo.filename)
        profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students (name, `class`, dob, profile_photo, father_name, mother_name, registration_number, roll_no, password, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (name, student_class, dob, filename, father_name, mother_name, registration_number, roll_no, password, email))

    conn.commit()
    conn.close()
    
    flash('Student added successfully!', 'success')
    return redirect(url_for('student_profile'))




import pandas as pd  # Add this import for handling Excel/CSV files

@app.route('/bulk-upload-students', methods=['POST'])
def bulk_upload_students():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('student_profile'))

    file = request.files['file']

    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('student_profile'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            # Read the file using pandas
            if filename.endswith('.csv'):
                data = pd.read_csv(file_path)
            elif filename.endswith('.xlsx'):
                data = pd.read_excel(file_path)
            else:
                flash('Unsupported file format. Please upload a CSV or Excel file.', 'danger')
                return redirect(url_for('student_profile'))

            # Iterate through the rows and insert into the database
            conn = get_db_connection()
            cursor = conn.cursor()

            for _, row in data.iterrows():
                cursor.execute("""
                    INSERT INTO students (name, `class`, dob, profile_photo, father_name, mother_name, registration_number, roll_no, password, email)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['name'],
                    row['class'],
                    row['dob'],
                    row.get('profile_photo', ''),  # Optional field
                    row['father_name'],
                    row['mother_name'],
                    row['registration_number'],
                    row['roll_no'],
                    row['password'],
                    row['email']
                ))

            conn.commit()
            cursor.close()
            conn.close()

            flash('Students uploaded successfully!', 'success')
        except Exception as e:
            print("Error during bulk upload:", e)
            flash('An error occurred during bulk upload. Please check your file format.', 'danger')

        # Remove the uploaded file after processing
        os.remove(file_path)

    return redirect(url_for('student_profile'))


@app.route('/delete-student/<int:id>', methods=['POST'])
def delete_student(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete the student from the database
        cursor.execute("DELETE FROM students WHERE id = %s", (id,))
        conn.commit()

        cursor.close()
        conn.close()

        flash('Student deleted successfully.', 'success')
    except Exception as e:
        print("Error deleting student:", e)
        flash('Failed to delete student. Please try again.', 'danger')

    return redirect(url_for('student_profile'))


@app.route('/edit-student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Get updated details from the form
        name = request.form['name']
        student_class = request.form['student_class']
        roll_no = request.form['roll_no']
        registration_number = request.form['registration_number']
        father_name = request.form['father_name']
        mother_name = request.form['mother_name']
        dob = request.form['dob']
        email = request.form['email']
        password = request.form['password']

        # Check if a new profile photo is uploaded
        profile_photo = request.files.get('profile_photo')
        if profile_photo and allowed_file(profile_photo.filename):
            filename = secure_filename(profile_photo.filename)
            profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Update the student with the new photo
            cursor.execute("""
                UPDATE students
                SET name = %s, class = %s, roll_no = %s, registration_number = %s,
                    father_name = %s, mother_name = %s, dob = %s, email = %s, profile_photo = %s
                WHERE id = %s
            """, (name, student_class, roll_no, registration_number, father_name, mother_name, dob, email, filename, id))
        else:
            # Update the student without changing the photo
            cursor.execute("""
                UPDATE students
                SET name = %s, class = %s, roll_no = %s, registration_number = %s,
                    father_name = %s, mother_name = %s, dob = %s, email = %s, password = %s
                WHERE id = %s
            """, (name, student_class, roll_no, registration_number, father_name, mother_name, dob, email, password, id))

        conn.commit()
        flash('Student details updated successfully.', 'success')
        return redirect(url_for('student_profile'))

    # Fetch the student details for the modal
    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cursor.fetchone()

    # Convert DOB to YYYY-MM-DD format
    if student and student['dob']:
        student['dob'] = student['dob'].strftime('%Y-%m-%d')

    cursor.close()
    conn.close()

    return jsonify(student)




@app.route('/subject-class', methods=['GET', 'POST'])
def subject_class_management():
    # Ensure the admin is logged in
    if 'admin_id' not in session:
        flash('Please log in to access this feature.', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Add a new subject or class
        name = request.form['name']
        code = request.form.get('code')  # Optional for classes
        type = request.form['type']  # 'subject' or 'class'

        if type == 'subject':
            cursor.execute("INSERT INTO subjects (name, code) VALUES (%s, %s)", (name, code))
        elif type == 'class':
            cursor.execute("INSERT INTO classes (name) VALUES (%s)", (name,))
        conn.commit()
        flash(f'{type.capitalize()} added successfully!', 'success')
        return redirect(url_for('subject_class_management'))

    # Fetch all subjects and classes
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()

    cursor.execute("SELECT * FROM classes")
    classes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('subject_class_management.html', subjects=subjects, classes=classes)


@app.route('/edit-subject-class/<string:type>/<int:id>', methods=['POST'])
def edit_subject_class(type, id):
    # Ensure the admin is logged in
    if 'admin_id' not in session:
        return jsonify({'status': 'error', 'message': 'Please log in to edit.'}), 401

    name = request.form['name']
    code = request.form.get('code')  # Optional for classes

    conn = get_db_connection()
    cursor = conn.cursor()

    if type == 'subject':
        cursor.execute("UPDATE subjects SET name = %s, code = %s WHERE id = %s", (name, code, id))
    elif type == 'class':
        cursor.execute("UPDATE classes SET name = %s WHERE id = %s", (name, id))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'status': 'success', 'message': f'{type.capitalize()} updated successfully!'})


@app.route('/delete-subject-class/<string:type>/<int:id>', methods=['POST'])
def delete_subject_class(type, id):
    # Ensure the admin is logged in
    if 'admin_id' not in session:
        return jsonify({'status': 'error', 'message': 'Please log in to delete.'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()

    if type == 'subject':
        cursor.execute("DELETE FROM subjects WHERE id = %s", (id,))
    elif type == 'class':
        cursor.execute("DELETE FROM classes WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'status': 'success', 'message': f'{type.capitalize()} deleted successfully!'})


# @app.route('/edit-student/<int:id>', methods=['GET', 'POST'])
# def edit_student(id):
#     conn = get_db_connection()
#     student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()

#     if request.method == 'POST':
#         name = request.form['name']
#         student_class = request.form['class']
#         roll_no = request.form['roll_no']
#         reg_no = request.form['registration_number']

#         conn.execute('''
#             UPDATE students
#             SET name = ?, class = ?, roll_no = ?, registration_number = ?
#             WHERE id = ?
#         ''', (name, student_class, roll_no, reg_no, id))
#         conn.commit()
#         conn.close()
#         return redirect(url_for('student_profile'))

#     conn.close()
#     return render_template('edit_student.html', student=student)

@app.route('/student-detail/<int:student_id>')
def student_detail(student_id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    conn.close()
    return render_template('student_detail.html', student=student)


@app.route('/student/<int:id>', methods=['GET', 'POST'])
def view_individual_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get student info
    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = cursor.fetchone()

    # Get exam records for the student
    cursor.execute("""
        SELECT exams.name AS exam_name, subjects.name AS subject_name, marks.marks
        FROM marks
        JOIN exams ON marks.exam_id = exams.id
        JOIN subjects ON marks.subject_id = subjects.id
        WHERE marks.student_id = ?
        ORDER BY exams.name, subjects.name
    """, (id,))
    records = cursor.fetchall()

    # Get percentage (simplified logic)
    cursor.execute("SELECT AVG(marks) FROM marks WHERE student_id = ?", (id,))
    percentage = cursor.fetchone()[0] or 0

    conn.close()

    return render_template("student_dashboard_admin_side.html",
                           student=student,
                           records=records,
                           percentage=round(percentage, 2))



# @app.route('/add-student', methods=['POST'])
# def add_student():
#     name = request.form['name']
#     student_class = request.form['class']
#     dob = request.form['dob']
#     roll_no = request.form['roll_no']
#     reg_no = request.form['registration_no']
#     father = request.form['father_name']
#     mother = request.form['mother_name']
#     password = request.form['password']
#     profile = request.files['profile_photo']
    
#     profile_path = ''
#     if profile:
#         profile_path = os.path.join('static/uploads', profile.filename)
#         profile.save(profile_path)

#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO students (name, class, dob, roll_no, registration_number, father_name, mother_name, password, profile_photo)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """, (name, student_class, dob, roll_no, reg_no, father, mother, password, profile_path))
#     conn.commit()
#     conn.close()
#     return redirect('/student-profile')


# @app.route('/admin/dashboard')
# def admin_dashboard():
#     cur = mysql.connection.cursor()

#     # Fetch counts
#     cur.execute("SELECT COUNT(*) FROM students")
#     total_students = cur.fetchone()[0]

#     cur.execute("SELECT COUNT(*) FROM subjects")
#     total_subjects = cur.fetchone()[0]

#     cur.execute("SELECT COUNT(*) FROM exams")
#     total_exams = cur.fetchone()[0]

#     cur.execute("SELECT exam_id, student_id, generated_date FROM marksheet ORDER BY generated_date DESC LIMIT 1")
#     latest_marksheet = cur.fetchone()

#     cur.close()

#     return render_template('admin_dashboard.html',
#                            total_students=total_students,
#                            total_subjects=total_subjects,
#                            total_exams=total_exams,
#                            latest_marksheet=latest_marksheet)


# ---------------- FORGOT PASSWORD ----------------
# @app.route('/forgot-password', methods=['GET', 'POST'])
# def forgot_password():
#     if request.method == 'POST':
#         user_type = request.form.get('user_type')
#         username = request.form.get('username')

#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)

#         if user_type == 'student':
#             cursor.execute("SELECT * FROM students WHERE reg_no = %s", (username,))
#         else:
#             cursor.execute("SELECT * FROM admins WHERE admin_id = %s", (username,))

#         user = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         if user:
#             session['reset_user'] = username
#             session['reset_type'] = user_type
#             session['reset_email'] = user['email']

#             otp = str(random.randint(100000, 999999))
#             session['reset_otp'] = otp

#             msg = Message('OTP for Password Reset', sender='your_email@gmail.com', recipients=[user['email']])
#             msg.body = f"Your OTP for password reset is: {otp}"
#             mail.send(msg)

#             flash('OTP sent to your email.', 'info')
#             return redirect(url_for('reset_otp_verify'))
#         else:
#             flash('User not found.', 'danger')
#             return redirect(url_for('forgot_password'))

#     return render_template('forgot_password.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username')
        user_type = request.form.get('role')  # 'student' or 'admin'

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if user_type == 'student':
            cursor.execute("SELECT * FROM students WHERE reg_no = %s", (username,))
        elif user_type == 'admin':
            cursor.execute("SELECT * FROM admin WHERE admin_id = %s", (username,))
        else:
            flash("Invalid role", "danger")
            return redirect(url_for('forgot_password'))

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            otp = str(random.randint(100000, 999999))
            session['reset_otp'] = otp
            session['reset_username'] = username
            session['reset_user_type'] = user_type
            session['reset_email'] = user['email']

            try:
                msg = Message('OTP for Password Reset', sender=app.config['MAIL_USERNAME'], recipients=[user['email']])
                msg.body = f"Your OTP for resetting your password is: {otp}"
                mail.send(msg)
                flash("OTP sent to your email.", "info")
                return redirect(url_for('verify_reset_otp'))
            except Exception as e:
                print("Email error:", e)
                flash("Failed to send OTP. Try again later.", "danger")
                return redirect(url_for('forgot_password'))
        else:
            flash("No account found for given username.", "danger")
            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')




@app.route('/verify_reset_otp', methods=['GET', 'POST'])
def verify_reset_otp():
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        if entered_otp == session.get('reset_otp'):
            flash("OTP verified! Set your new password.", "success")
            return redirect(url_for('reset_password'))
        else:
            flash("Incorrect OTP. Try again.", "danger")
            return redirect(url_for('verify_reset_otp'))
    return render_template('verify_reset_otp.html')


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('reset_password'))

        if not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$', new_password):
            flash("Password must be at least 6 characters, contain letters, numbers, and symbols.", "danger")
            return redirect(url_for('reset_password'))

        username = session.get('reset_username')
        user_type = session.get('reset_user_type')

        conn = get_db_connection()
        cursor = conn.cursor()

        if user_type == 'student':
            cursor.execute("UPDATE students SET password = %s WHERE reg_no = %s", (new_password, username))
        elif user_type == 'admin':
            cursor.execute("UPDATE admin SET password = %s WHERE admin_id = %s", (new_password, username))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Password updated successfully. You can now login!", "success")
        return redirect(url_for('login'))

    return render_template('reset_password.html')



@app.route('/new-password', methods=['GET', 'POST'])
def create_new_password():
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        username = session.get('reset_user')
        user_type = session.get('reset_type')

        conn = get_db_connection()
        cursor = conn.cursor()

        if user_type == 'student':
            cursor.execute("UPDATE students SET password = %s WHERE reg_no = %s", (new_password, username))
        else:
            cursor.execute("UPDATE admin SET password = %s WHERE admin_id = %s", (new_password, username))

        conn.commit()
        cursor.close()
        conn.close()

        flash('Password updated successfully. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('new_password.html')


# ---------------- FEEDBACK ----------------
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Feedback submitted successfully.', 'success')
        return redirect(url_for('feedback'))

    return render_template('feedback.html')


@app.route('/admin/feedback')
def admin_feedback():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM feedback")
    feedbacks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin_feedback.html', feedbacks=feedbacks)




# ----------------  ----------------


# ---------------- BASIC PAGES ----------------
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch top 3 students based on percentage
    cursor.execute("""
        SELECT name, roll_no, percentage, profile_photo 
        FROM students 
        ORDER BY percentage DESC 
        LIMIT 3
    """)
    top_students = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', top_students=top_students)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/features')
def features():
    return render_template('features.html')


@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')


@app.route('/terms-and-conditions')
def terms_and_conditions():
    return render_template('terms_and_conditions.html')


@app.route('/help')
def help_page():
    return render_template('help.html')





# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))


# ---------------- RUN FLASK ----------------
# if __name__ == '__main__':
#     app.run(debug=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)