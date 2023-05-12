from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from flaskapp import db
from flaskapp.models import User
from flaskapp.users.utils import send_reset_email, solve

main = Blueprint('main', __name__)     


@main.route('/')
def index():
    return redirect(url_for('users.login'))
 
@main.route('/size_input') 
@login_required
def size_input():
    user = User.query.filter_by(username=current_user.username).first()
    
    cur_hist_unique = []
    if(user.history != ""):
        cur_hist = user.history.split(",")
        cur_hist_list = [line.split('@') for line in cur_hist]
        cur_hist_unique = list(set(tuple(sublist) for sublist in cur_hist_list))
        cur_hist_unique = [list(sublist) for sublist in cur_hist_unique]
        
    return render_template('matrix_size_input.html', title = "Home", history = cur_hist_unique)

@main.route('/matrix_input', methods=['POST', 'GET'])
@login_required
def matrix_input():
    size = int(request.form['size'])
    rent = int(request.form['rent'])
    return render_template('matrix_input.html', title = "Take user input", size=size, rent=rent)

@main.route('/output', methods=['POST', "GET"])
@login_required
def output():
    size = int(request.form['size'])
    rent = int(request.form['rent'])

    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            key = '{}-{}'.format(i, j)
            row.append(-float(request.form[key]))
        matrix.append(row)
    
    # print(matrix)
    for row in matrix:
        sum = 0
        for value in row:
            sum += value
        if sum != -rent:
            flash('Inputs for very users should add upto total rent.', 'danger') 
            return redirect(url_for('main.size_input'))
        
    final = solve(size, matrix, rent)
    user = User.query.filter_by(username=current_user.username).first()
    cur_hist = user.history

    hist = []
    cnt = 1
    for inf in final:
        s = "Roommate " + str(cnt) + " is alloted to room : " + str(inf[0] + 1) + " for rent: " + str(inf[1]) 
        cnt+=1
        hist.append(s)
        
    hist_str = ""
    for s in hist:
        hist_str += s + "@"

    if(len(cur_hist) == 0):
        user.history = hist_str
    else:
        user.history = cur_hist + "," + hist_str
    # print(current_user.username)
    db.session.commit()
    
    return render_template('output.html', title = "display output", final=final, size=size)
