from flask import Flask, render_template, redirect, session, request, url_for
from odeta import database

# Initialize database
db = database("my_database.db")
information = db('information')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed to use session

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/information', methods=["GET", "POST"])
def information_page():
    # Always redirect to the login page if the user is not logged in
    if not session.get('user'):
        return redirect('/login')

    if request.method == 'POST':
        try:
            # Capture the form data
            new_information = {
                "Student_Name": request.form.get('Student Name'),
                "Father_Name": request.form.get('Father Name'),
                "Address": request.form.get('Address'),
                "Amount": request.form.get('Amount'),
                "Join_Date": request.form.get('Join'),
                "Mob_No": request.form.get('mobile')
            }

            # Insert the new information into the database
            information.put(new_information)
            return redirect(url_for('information_page'))  # Redirect to the same page after submission
        except Exception as e:
            return str(e)  # Optionally return an error page or log the error

    # Fetch all data from the database to display in the template
    data = information.fetchall()
    return render_template('information.html', sachin=data)

@app.route('/location')
def location():
    return render_template('location.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Validate the username and password
        if request.form['uname'] == "Kirshan Choudhary" and request.form['password'] == "9950107996":
            # Store the user in the session after successful login
            session['user'] = {"name": request.form['uname']}
            return redirect(url_for('information_page'))  # Redirect to the information page
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html', error='')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Clear the user session
    return redirect(url_for('home'))  # Redirect to the home page after logout

@app.route('/information/delete', methods=['POST'])
def delete_information():
    
    record_id = request.form.get('record_id')

    try:
       
        information.delete(record_id)
        return redirect(url_for('information_page'))  
    except Exception as e:
        return str(e) 



if __name__ == '__main__':
    app.run(debug=True)