from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

templates_dir = os.path.dirname(os.path.dirname(__file__))
templates_dir = os.path.join(templates_dir, 'src', 'templates')

app = Flask(__name__, template_folder=templates_dir)

#Rutas de la aplicación

@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM blog_db")
    myresult = cursor.fetchall()
    
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

#Ruta para guardar usuarios en la base de datos
@app.route('/user', methods = ['POST'])
def addUser():
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']
    
    if username and name and password:
        cursor = db.database.cursor()
        sql = "INSERT INTO blog_db (username, name, password) VALUES (%s, %s, %s)"
        data = (username, name, password)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM blog_db WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']
    
    if username and name and password:
        cursor = db.database.cursor()
        sql = "UPDATE blog_db SET username = %s, name = %s, password = %s WHERE id = %s"
        data = (username, name, password, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=4000)