from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.messages import Message

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) #Inicializando instancia de Bcrypt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    
    pwd = bcrypt.generate_password_hash(request.form['password'])
    formulario = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pwd
    }
    
    id  = User.save(formulario)
    session['user_id'] = id #Guardando en sesion el identificador
    return redirect ('/wall')


@app.route('/login', methods = ['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("E-mail no encontrado", "login")
        return redirect('/')
    
    #Comparando la contraseña encriptada con la contraseña de LOGIN
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password incorrecto", "login")
        return redirect('/')
    
    session['user_id'] = user.id
    return redirect('/wall')


@app.route('/wall')
def wall():
    if 'user_id' not in session:
        return redirect('/')
    
    formulario = {
        "id": session['user_id']
    }
    
    user = User.get_by_id(formulario) #El usuario que inicio sesión
    users = User.get_all() #Lista de todos los usuarios
    messages =  Message.get_user_messages(formulario) 
    
    return render_template('wall.html', user = user, users = users, messages = messages)


@app.route('/logout')
def logout():
    session.clear() #Elimine la sesión
    return redirect ('/')