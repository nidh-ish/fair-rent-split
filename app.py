from flask import Flask, render_template, request
from typing import List
import scipy.optimize

app = Flask(__name__)


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
            mx = inp_transpose[i].pop(int(room_allot[i][1])) #Removing the price which the person (to whom that room has been allotted) bid for that room
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
    print(inp_transpose)


    if type(res.x)!="<class 'list'>":
        res=[]
        for i in range(n):
            print(i, int(room_allot[i][1]))
            res.append(inp_transpose[i][int(room_allot[i][1])])
            utility=-sum(res) - totalrent
    else:                
        for i in range(n):
            print(i)
            utility+= (-inp[int(room_allot[i][1])][i]) - (res.x)[i]
    
    return utility

def solve(n, inp, rent):
    Lmate = [-1] * n
    Rmate = [-1] * n
    room_allot = MinCostMatching(inp, Lmate, Rmate)
    print(room_allot)
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
    print(utility, avg_utility)
    avg_utility = utility/n
   
    final_answer = []
    for i in range(n):
        final_answer.append([room_allot[i][1],round(-inp[i][room_allot[i][1]] - avg_utility,2)])

    # print(final_answer)

    return final_answer



@app.route('/')
def index():
    return render_template('matrix_size_input.html')

@app.route('/matrix_input', methods=['POST', 'GET'])
def matrix_input():
    size = int(request.form['size'])
    rent = (request.form['rent'])
    return render_template('matrix_input.html', size=size, rent=rent)

@app.route('/matrix_display', methods=['POST', "GET"])
def matrix_display():
    size = int(request.form['size'])
    rent = int(request.form['rent'])
    # rent = 10
    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            key = '{}-{}'.format(i, j)
            row.append(-int(request.form[key]))
        matrix.append(row)
    final = solve(size, matrix, rent)
    print(final)
    return render_template('matrix_display.html', final=final,size=size)

if(__name__ == "__main__"):
    app.run()