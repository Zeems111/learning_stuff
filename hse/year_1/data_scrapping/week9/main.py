'''from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

# python -m uvicorn main:app --reload 
app = FastAPI()
templates = Jinja2Templates(directory='templates')

def quadratic(a: int, b: int, c: int, x:int):
    return a * x ** 2 + b * x + c

def solve_quadratic(a: int, b: int, c: int):
    result = set()
    if a == 0 and b != 0:
        result.add(-c/b)
    elif a != 0:
        d = b**2 - 4 * a * c
        if d >= 0:
              d = d ** 0.5 / (2 * a)
              x = -b / (2 * a)
              result.add(x - d)
              result.add(x + d)
    return result

@app.get('/')
async def root(request: Request):
    return 'Welcome to Quadratic Solver!'

@app.get('/main')
async def root(request: Request):
    return templates.TemplateResponse("index.html", 
                                      {'request': request})

@app.get('/solve')
async def solve(a: int, b: int, c: int):
    result = solve_quadratic(a, b, c)
    return {'roots': result}

@app.post('/plot')
async def show_plot(request: Request, a: int=Form(), b: int=Form(), c: int=Form()):
    roots = list(solve_quadratic(a, b, c))
    x_min, x_max = -5, 5
    if a == 0 and b != 0:
        x_min, x_max = roots[0] - 5, roots[0] + 5
    elif a != 0 and roots:
        x_min, x_max = min(roots) - 5, max(roots) + 5
    elif a != 0:
        x_min, x_max = -b / (2 * a) - 5, -b / (2 * a) + 5
    x = np.linspace(x_min, x_max)
    
    fig = plt.figure()   
    plt.plot(x, quadratic(a, b, c, x), 
            label=f"Graph of {a}x^2 + {b}x + {c}\
            \nRoots: {list(map(lambda x: round(x, 2), roots))}")    
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    for root in roots:
        plt.text(root + 0.2, -1, str(round(root, 2)))
    plt.grid(True)
    plt.scatter(x=list(roots), y=[0]*len(roots), marker='o', c="red")
    pngImage = io.BytesIO()
    fig.savefig(pngImage)
    pngImageB64String = base64.b64encode(pngImage.getvalue()).decode('ascii')
    return templates.TemplateResponse("plot.html",
                                      {'request': request,
                                       "picture": pngImageB64String
                                       })
'''

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()

def solve(a, b, c):
    D = b**2 - 4*a*c
    if D > 0:
        return [(-b + np.sqrt(D))/(2*a), (-b - np.sqrt(D))/(2*a)]
    elif D == 0:
        return [-b/(2*a)]
    else:
        return []

@app.get("/solve", response_class=JSONResponse)
async def read_item(a: int, b: int, c: int):
    return {"roots": solve(a, b, c)}

@app.get("/main", response_class=HTMLResponse)
async def read_item():
    return """
    <html>
        <head>
            <title>Quadratic equation solver</title>
        </head>
        <body>
            <h1>Quadratic equation solver</h1>
            <form action="/solve" method="get">
                <label for="a">a:</label>
                <input type="text" id="a" name="a"><br><br>
                <label for="b">b:</label>
                <input type="text" id="b" name="b"><br><br>
                <label for="c">c:</label>
                <input type="text" id="c" name="c"><br><br>
                <input type="submit" value="Submit">
            </form>
            <form action="/plot" method="get">
                <label for="a">a:</label>
                <input type="text" id="a" name="a"><br><br>
                <label for="b">b:</label>
                <input type="text" id="b" name="b"><br><br>
                <label for="c">c:</label>
                <input type="text" id="c" name="c"><br><br>
                <input type="submit" value="Plot">
            </form>
        </body>
    </html>
    """

@app.get("/plot", response_class=HTMLResponse)
async def read_item(a: int, b: int, c: int):
    roots = solve(a, b, c)
    if len(roots) == 0:
        return "No roots"
    elif len(roots) == 1:
        x = np.linspace(roots[0]-1, roots[0]+1, 100)
        y = a*x**2 + b*x + c
        plt.plot(x, y)
    else:
        x1 = np.linspace(roots[0]-1, roots[0]+1, 100)
        y1 = a*x1**2 + b*x1 + c
        x2 = np.linspace(roots[1]-1, roots[1]+1, 100)
        y2 = a*x2**2 + b*x2 + c
        plt.plot(x1, y1)
        plt.plot(x2, y2)
    plt.savefig("plot.png")
    return """
    <html>
        <head>
            <title>Quadratic equation plot</title>
        </head>
        <body>
            <h1>Quadratic equation plot</h1>
            <img src="/plot.png" alt='sdfs'>
        </body>
    </html>
    """