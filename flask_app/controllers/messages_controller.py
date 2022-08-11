from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.messages import Message


@app.route('/message/send', methods=['POST'])
def send():
    if 'id' in session:
        data={
            'message':request.form['message'],
            'sender_id':session['id'],
            'recipient_id':request.form['recipient_id']
        }
        if Message.validate(data):
            Message.create(data)
        else:
            flash('*something went wrong, please try again', 'message_errors')
        return redirect('/wall')
    else:
        flash('*please login', 'login_errors')
        return redirect('/')

@app.route('/message/delete<int:message_id>')
def delete_message(message_id):
    if 'id' in session:
        data={
            'id':message_id
        }
        Message.delete(data)
        return redirect('/wall')
    else:
        flash('*please log in', 'login_errors')
        return redirect('/')