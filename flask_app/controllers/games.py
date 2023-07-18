from flask_app import app
from flask import render_template, redirect, request

answers = ['Rabbit', 'Bananas', 'New Zealand' ]

@app.route("/game")
def game1():
    return render_template("game.html")

@app.route('/game/1', methods = ['POST'])
def question_1():
    answer = request.form['answer']
    if answer not in answers:
        return redirect('/gameover')
    return redirect('/game/2')

@app.route("/gameover")
def lose():
    return render_template("game_over.html")

@app.route("/game/2")
def game2():
    return render_template("game_two.html")

@app.route('/game/2', methods = ['POST'])
def question_2():
    answer = request.form['answer']
    if answer not in answers:
        return render_template('game_over.html')
    return redirect('/game/3')

@app.route("/game/3")
def game3():
    return render_template("game_three.html")

@app.route('/game/3', methods = ['POST'])
def question_3():
    
    answer = request.form['answer']
    if answer not in answers:
        return render_template('game_over.html')
    return redirect('/finish')

@app.route("/finish")
def finish():
    return render_template("finish.html")