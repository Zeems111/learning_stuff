# main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = FastAPI()

def solve_quadratic_equation(a, b, c):
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        root1 = (-b + np.sqrt(discriminant)) / (2*a)
        root2 = (-b - np.sqrt(discriminant)) / (2*a)
        return [root1, root2]
    elif discriminant == 0:
        root = -b / (2*a)
        return [root]
    else:
        return []

@app.get("/solve")
async def solve(a: int, b: int, c: int):
    roots = solve_quadratic_equation(a, b, c)
    return {"roots": roots}

@app.get("/")
async def main(request: Request):
    content = """
    <form action="/plot" method="post">
        a: <input type="text" name="a"><br>
        b: <input type="text" name="b"><br>
        c: <input type="text" name="c"><br>
        <input type="submit" value="Submit">
    </form>
    """
    return HTMLResponse(content=content)

@app.post("/plot")
async def plot(request: Request, a: int = Form(...), b: int = Form(...), c: int = Form(...)):
    x = np.linspace(-10, 10, 400)
    y = a*x**2 + b*x + c
    roots = solve_quadratic_equation(a, b, c)

    plt.plot(x, y)
    plt.scatter(roots, [0]*len(roots), color='red')
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    content = f"""
    <img src="data:image/png;base64,{plot_data}">
    """
    return HTMLResponse(content=content)
