from flask import Flask, flash, url_for, render_template, request , redirect, session
from flask_mysqldb import MySQL
from flask import request


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'gadissuci25'
app.config['MYSQL_DB'] = 'tugas_millenia_db'

mysql = MySQL(app)



@app.route('/', methods=['GET', 'POST'])
def login():
    
    msg = 'wrong id_user or password'
    # Check if "id user" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'id_user' in request.form and 'password' in request.form:
        # Create variables for easy access
        id_user = request.form['id_user']
        password = request.form['password']
         # Check if account exists using MySQL
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM tb_user WHERE id_user = %s AND password = %s', (id_user, password,))
        # Fetch one record and return result
        account = cur.fetchone()
        
        print(id_user)
        
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id_user'] = account[0]
            session['email'] = account[2]
            session['nama'] = account[1]
            

            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect email/password!'
    return render_template('index.html', msg='')



# @app.route('/')
# def Index():
    
#     return render_template('index.html')



@app.route('/checklist')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM tb_cheklist")
    data = cur.fetchall()
    cur.close()
    

    return render_template('index2.html', list=data )



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        
        nama = request.form['nama']
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO tb_cheklist VALUES (NULL, %s)', [nama])
        mysql.connection.commit()
        return redirect(url_for('home'))



@app.route('/delete/<string:id>', methods = ['GET'])
def delete(id):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tb_cheklist WHERE id=%s", (id))
    mysql.connection.commit()
    return redirect(url_for('home'))



@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        
        
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE tb_cheklist
               SET  nama=%s 
               WHERE id=%s
            """, ( nama, id))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('home' ))





# if __name__ == "__main__":
#     app.run(debug=True)

import werkzeug.serving
werkzeug.serving.run_simple("localhost", 8001, app)


# nodemon --exec python3 __init__.py 
