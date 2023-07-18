from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.comment import Comment
from flask_app.models.fact import Fact
from flask_app.models.user import User
from flask_app.controllers import comments
from flask_app.controllers import games

# ---------------------------------------------------
# SHOW PAGE - SHOW ALL FACTS

@app.route('/show')
def home():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')
        
    return render_template('show.html', user=user, facts=Fact.get_all())

# ---------------------------------------------------
# SHOW EACH FACT BY ID - USERS CAN VIEW EACH FACT

@app.route('/show/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/dashboard')
    data = {
        'id' : id
    }
    return render_template('view.html', fact=Fact.get_users_facts_comments_by_user_id(data))

# ---------------------------------------------------
# CREATE FACT PAGE - USERS CAN CREATE A FACT

@app.route('/create')
def create():
    if 'user_id' not in session:
        return redirect('/dashboard')
    user = User.get_by_id({"id":session['user_id']})
    return render_template('create.html', user=user)


@app.route('/create/process', methods=['POST'])
def process():
    if 'user_id' not in session:
        return redirect('/dashboard')
    if not Fact.validate_fact(request.form):
        return redirect('/create')
    data = {
        'user_id': session['user_id'],
        'fact': request.form['fact'],
        'resource': request.form['resource']
    }
    Fact.save(data)
    return redirect('/show')

# ---------------------------------------------------
# EDIT AND UPDATE PAGE - USERS CAN EDIT AND UPDATE THEIR FACTS

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/dashboard')
    user = User.get_by_id({"id":session['user_id']})
    return render_template('edit.html', user=user, fact=Fact.get_users_facts_comments_by_user_id({'id': id}))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if 'user_id' not in session:
        return redirect('/dashboard')
    if not Fact.validate_fact(request.form):
        return redirect(f'/edit/{id}')
    data = {
        'id': id,
        'user_id': session['user_id'],
        'fact': request.form['fact'],
        'resource': request.form['resource'],
    }
    Fact.update(data)
    return redirect('/show')

# ---------------------------------------------------
# DELETE - USERS CAN DELETE THEIR FACTS

@app.route('/delete/fact/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/dashboard')
    Fact.delete({'id':id})
    return redirect('/show')