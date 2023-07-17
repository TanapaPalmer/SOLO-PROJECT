from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.comment import Comment
from flask_app.models import comment
from flask_app.models.fact import Fact
from flask_app.models.user import User
# from flask_app.models import fact, user

# @app.route("/comment")
# def comment():
#     return render_template("comment.html")

# @app.route('/comment/create', methods=['POST'])
# def comment_on_fact():
#     if 'user_id' in session:
#         if comment.Comment.validate_comment(request.form):
#             data = {
#                 'comment' : request.form['comment'],
#                 'user_id' : session['user_id'],
#                 'fact_id' : request.form['fact_id']
#             }
#         return redirect('/show')
#     return redirect('/dashboard')


# @app.route('/comment/<int:id>')
# def comment(id):
#     if 'fact_id' not in session:
#         return redirect('/dashboard')
#     fact = Fact.get_id({"id":session['fact_id']})

#     return render_template('comment.html', fact=fact, comment=Comment.get_id({'id':id}))


@app.route('/comment')
def comments():
    if 'user_id' not in session:
        return redirect('/dashboard')
    user = User.get_by_id({"id":session['user_id']})
    fact = Fact.get_by_id({"id":session['user_id']})

    return render_template('comment.html', user=user, fact=fact)


@app.route('/comment/process', methods=['POST'])
def comment_process():
    if 'user_id' not in session:
        return redirect('/dashboard')
    if not Comment.validate_comment(request.form):
        return redirect('/comment')

    data = {
        'user_id' : session['user_id'],  
        'fact_id' : request.form['fact_id'],  
        'comment' : request.form['comment']
    }
    Comment.save_comment(data)
    return redirect('/show')

@app.route('/delete/comment/<int:id>')
def delete_comment(id):
    if 'user_id' not in session:
        return redirect('/')

    Comment.delete_comment({'id':id})
    return redirect('/show')
