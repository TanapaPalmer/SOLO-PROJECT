from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.fact import Fact, User
from flask_app.models import fact, user

# @app.route('/show')
# def home():
#     if 'user_id' not in session:
#         return redirect('/')
#     user = {
#         'id' : session['user_id']
#     }
#     all_facts = fact.Fact.get_all()
#     return render_template('show.html', user=user, facts=Fact.get_by_id())

@app.route('/show')
def home():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')
        
    return render_template('show.html', user=user, facts=Fact.get_all())

# @app.route('/show')
# def home():
#     if 'user_id' not in session:
#         return render_template('show.html',
#             user = user.User.get_by_id({"id":session['user_id']}),
#             all_facts = fact.Fact.get_all()
#             )
#     return redirect('/dashboard')


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

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/dashboard')
    
    user = User.get_by_id({"id":session['user_id']})

    return render_template('edit.html', user=user, fact=Fact.get_by_id({'id': id}))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if 'user_id' not in session:
        return redirect('/dashboard')
    if not Fact.validate_fact(request.form):
        return redirect(f'/edit/{id}')

    data = {
        'id': id,
        'fact': request.form['fact'],
        'resource': request.form['resource'],
    }
    Fact.update(data)
    return redirect('/show')


@app.route('/delete/<int:fact_id>')
def delete(fact_id):
    if 'user_id' not in session:
        return redirect('/')

    Fact.delete({'id':fact_id})
    return redirect('/show')


@app.route('/show/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/')
    
    user = User.get_by_id({"id":session['user_id']})
    
    return render_template('each_fact.html', user=user, fact=Fact.get_by_id({'id': id}))