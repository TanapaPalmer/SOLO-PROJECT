from flask_app import app
from flask import render_template, redirect, request, session, flash

answers = ['22 minutes', 'Canberra', '6 or 7 days', 'bumblebee', 'New Zealand' ]

@app.route("/game")
def game():
    return render_template("game.html")

@app.route('/game/1', methods = ['POST'])
def question_1():
    answer = request.form['answer_1']
    # if answer == 'answer_1':
    #     return render_template('loose.html')
    return redirect('/game/2')


@app.route("/game/2")
def game_two():
    return render_template("game_two.html")

# @app.route('/game/2', methods = ['POST'])
# def question_2():
#     answer = request.form['answer_2']
#     if answer != 'answer_2':
#         return render_template('loose.html')
#     return redirect('/game/3') 

# @app.route('/game/3', methods = ['POST'])
# def question_3():
#     answer = request.form['answer_2']
#     if answer == 'answer_3':
#         return render_template('loose.html')
#     return render_template("finish.html")