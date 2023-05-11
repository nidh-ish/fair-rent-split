from flask import render_template, request, url_for, redirect, flash
from flaskapp.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm 
from flaskapp.models import User
from flaskapp import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from typing import List
import scipy.optimize


def MinCostMatching(cost: List[List[int]], Lmate: List[int], Rmate: List[int]) -> int:
    n = len(cost)
    u = [min(row) for row in cost]
    v = [0] * n
    for j in range(n):
        v[j] = cost[0][j] - u[0]
        for i in range(1, n): 
            v[j] = min(v[j], cost[i][j] - u[i]) 
    Lmate = [-1] * n
    Rmate = [-1] * n
    mated = 0
    for i in range(n):
        for j in range(n):
            if Rmate[j] != -1:
                continue
            if abs(cost[i][j] - u[i] - v[j]) == 0:
                Lmate[i] = j
                Rmate[j] = i
                mated += 1
                break
    dist = [0] * n
    dad = [-1] * n
    seen = [0] * n
    while mated < n:
        s = next((i for i, x in enumerate(Lmate) if x == -1), None)
        dist = [cost[s][k] - u[s] - v[k] for k in range(n)]
        while True:
            j = min((k for k in range(n) if not seen[k]), key=lambda k: dist[k])
            seen[j] = 1
            if Rmate[j] == -1:
                break
            i = Rmate[j]
            for k in range(n):
                if seen[k]:
                    continue
                new_dist = dist[j] + cost[i][k] - u[i] - v[k]
                if dist[k] > new_dist:
                    dist[k] = new_dist
                    dad[k] = j
        if Rmate[j] != -1:
            break
        for k in range(n):
            if k == j or not seen[k]:
                continue
            i = Rmate[k]
            v[k] += dist[k] - dist[j]
            u[i] -= dist[k] - dist[j]
        u[s] += dist[j]
        while dad[j] >= 0:
            d = dad[j]
            Rmate[j] = Rmate[d]
            Lmate[Rmate[j]] = j
            j = d
        Rmate[j] = s
        Lmate[s] = j
        mated += 1
    value = sum(cost[i][Lmate[i]] for i in range(n))

    room_allot = []
    for i in range(len(Lmate)):
        room_allot.append((i,Lmate[i]))

    return room_allot

def lp(room_allot,inp_transpose,totalrent, inp):

    bound = []
    n = len(room_allot)
    for i in range(n):
        if int(room_allot[i][1]) <= n:
            mx = inp_transpose[i].pop(int(room_allot[i][1]))
            mx_new = max(inp_transpose[i])
            while mx_new >= mx:
                    inp_transpose[i].remove(mx_new)
                    if inp_transpose[i] == []:
                            mx_new = 0
                            break
                    mx_new = max(inp_transpose[i])
                    
            bound.append((mx_new,mx))

    c=[1 for x in range(n)]
    A_eq =[[1 for x in range(n)]]
    b_eq =[totalrent]
    res=scipy.optimize.linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bound, method='highs')


    utility = 0
    inp_transpose=[[0 for x in range(n)] for y in range(n)]
    
    for i in range(n):
        for j in range(n):
            inp_transpose[i][j]=inp[j][i]
    # print(inp_transpose)


    if type(res.x)!="<class 'list'>":
        res=[]
        for i in range(n):
            # print(i, int(room_allot[i][1]))
            res.append(inp_transpose[i][int(room_allot[i][1])])
            utility=-sum(res) - totalrent
    else:                
        for i in range(n):
            # print(i)
            utility+= (-inp[int(room_allot[i][1])][i]) - (res.x)[i]
    
    return utility

def solve(n, inp, rent):
    Lmate = [-1] * n
    Rmate = [-1] * n
    room_allot = MinCostMatching(inp, Lmate, Rmate)
    # print(room_allot)
    inp_transpose=[[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            inp_transpose[i][j]=inp[j][i]
    # print(inp_transpose)
    
    # utility = lp(room_allot, inp_transpose, rent, inp)
        # utility = lp(room_allot, inp_transpose, 1000, inp)
    utility = 0
    for i in range(n):
        utility += inp[i][room_allot[i][1]]
    utility = -utility - rent
    avg_utility = utility/n
    # print(utility, avg_utility)
    avg_utility = utility/n
   
    final_answer = []
    for i in range(n):
        final_answer.append([room_allot[i][1],round(-inp[i][room_allot[i][1]] - avg_utility,2)])

    # print(final_answer)

    return final_answer

@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('size_input'))
    form = RegistrationForm()
    if form.validate_on_submit( ):
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, history = '')
        db.session.add(user) 
        db.session.commit() 
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('size_input'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('size_input'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
 
@app.route("/logout") 
def logout():
    logout_user()
    return redirect(url_for('login')) 
 
@app.route('/size_input') 
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

@app.route('/matrix_input', methods=['POST', 'GET'])
@login_required
def matrix_input():
    size = int(request.form['size'])
    rent = int(request.form['rent'])
    return render_template('matrix_input.html', title = "Take user input", size=size, rent=rent)

@app.route('/output', methods=['POST', "GET"])
@login_required
def output():
    size = int(request.form['size'])
    rent = int(request.form['rent'])

    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            key = '{}-{}'.format(i, j)
            row.append(-int(request.form[key]))
        matrix.append(row)
    
    # print(matrix)
    for row in matrix:
        sum = 0
        for value in row:
            sum += value
        if sum != -rent:
            flash('Inputs for very users should add upto total rent.', 'danger') 
            return redirect(url_for('size_input'))
        
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
 
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender='mynotesappbyflask@gmail.com', recipients=[user.email])
    msg.body = 'To reset your password, go to the following link:' + str(url_for('reset_token', token=token, _external=True))
    mail.send(msg) 
  
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('size_input'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('size_input'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form) 

