from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import comment

@app.route('/comment/create', methods=['POST'])
def comment_on_fact():
    if 'user_id' in session:
        if comment.Comment.validate_comment(request.form):
            data = {
                'comment' : request.form['comment'],
                'user_id' : session['user_id'],
                'fact_id' : request.form['fact_id']
            }
        return redirect('/show')
    return redirect('/dashboard')