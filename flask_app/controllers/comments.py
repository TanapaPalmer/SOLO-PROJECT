from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.comment import Comment
from flask_app.models.fact import Fact
from flask_app.models.user import User

# ---------------------------------------------------
# CREATE COMMENT PAGE - USERS CAN CREATE A COMMENT

@app.route('/comment/<int:id>')
def comments(id):
    if 'user_id' not in session:
        return redirect('/dashboard')
    user = User.get_by_id({"id":session['user_id']})
    fact = Fact.get_fact_by_id({"id": id})
    return render_template('comment.html', user=user, fact=fact)

@app.route('/comment/process/<int:id>', methods=['POST'])
def comment_process(id):
    if 'user_id' not in session:
        return redirect('/dashboard')
    if not Comment.validate_comment(request.form):
        return redirect(f'/comment/{id}')
    data = {
        'user_id' : session['user_id'],  
        'fact_id' : request.form['fact_id'],  
        'comment' : request.form['comment']
    }
    Comment.save_comment(data)
    return redirect(f"/show/{request.form['fact_id']}")

# ---------------------------------------------------
# DELETE - USERS CAN DELETE THEIR COMMENTS

@app.route('/delete/comment/<int:id>')
def delete_comment(id):
    if 'user_id' not in session:
        return redirect('/')

    Comment.delete_comment({'id':id})
    return redirect('/show')
