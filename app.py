from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "your_secret_key" 

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='sAmeer870@',  
            database='project'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "INSERT INTO students (roll_number, name, email, course) VALUES (%s, %s, %s, %s)"
                values = (roll_number, name, email, course)
                cursor.execute(query, values)
                connection.commit()
                flash("Student added successfully!", "success")
            except Error as e:
                flash(f"Error: {e}", "error")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        
        return redirect(url_for('home'))
    
    return render_template('home.html', action='add_student')

@app.route('/view_students')
def view_students():
    students = []
    connection = create_connection()
    
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM students"
            cursor.execute(query)
            students = cursor.fetchall()
        except Error as e:
            flash(f"Error: {e}", "error")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    return render_template('home.html', action='view_students', students=students)

@app.route('/update_student', methods=['GET'])
def update_student():
    return render_template('home.html', action='update_search')

@app.route('/find_student', methods=['POST'])
def find_student():
    roll_number = request.form['roll_number']
    student = None
    
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM students WHERE roll_number = %s"
            cursor.execute(query, (roll_number,))
            student = cursor.fetchone()
            
            if not student:
                flash("Student not found!", "error")
        except Error as e:
            flash(f"Error: {e}", "error")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    return render_template('home.html', action='update_student', student=student)

@app.route('/update_student_record', methods=['POST'])
def update_student_record():
    roll_number = request.form['roll_number']
    name = request.form['name']
    email = request.form['email']
    course = request.form['course']
    
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE students SET name = %s, email = %s, course = %s WHERE roll_number = %s"
            values = (name, email, course, roll_number)
            cursor.execute(query, values)
            connection.commit()
            flash("Student updated successfully!", "success")
        except Error as e:
            flash(f"Error: {e}", "error")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    return redirect(url_for('home'))

@app.route('/delete_student', methods=['GET'])
def delete_student():
    return render_template('home.html', action='delete_student')

@app.route('/delete_student_record', methods=['POST'])
def delete_student_record():
    roll_number = request.form['roll_number']
    
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            check_query = "SELECT * FROM students WHERE roll_number = %s"
            cursor.execute(check_query, (roll_number,))
            student = cursor.fetchone()
            
            if student:
                delete_query = "DELETE FROM students WHERE roll_number = %s"
                cursor.execute(delete_query, (roll_number,))
                connection.commit()
                flash("Student deleted successfully!", "success")
            else:
                flash("Student not found!", "error")
        except Error as e:
            flash(f"Error: {e}", "error")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)