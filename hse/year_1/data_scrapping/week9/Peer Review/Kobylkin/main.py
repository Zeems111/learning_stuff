import base64
import io
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

matplotlib.use('Agg')

app = FastAPI()

templates = Jinja2Templates(directory='templates')


def solve_equation(a, b, c):
    solutions = []
    discriminant = b * b - 4 * a * c

    if discriminant < 0:
        # No real roots
        return solutions

    sqrt_discriminant = math.sqrt(discriminant)

    # checking condition for discriminant
    if discriminant > 0:
        # Real, different roots
        solutions.append(
            (-b + sqrt_discriminant) / (2 * a)
        )
        solutions.append(
            (-b - sqrt_discriminant) / (2 * a)
        )

    elif discriminant == 0:
        # Real root
        solutions.append(-b / (2 * a))

    return sorted(solutions)


@app.get('/solve')
async def solve(a: int = 0, b: int = 0, c: int = 0):
    solutions = solve_equation(a, b, c)
    return {
        'roots': solutions,
    }


@app.get('/')
async def main(request: Request):

    return templates.TemplateResponse(
        'main.html',
        {
            'request': request,
        }
    )


@app.post('/plot')
async def solver_equation(
        request: Request,
        a: int = Form(...),
        b: int = Form(...),
        c: int = Form(...)
):
    solutions = solve_equation(a, b, c)

    # making a graph
    x = np.linspace(-5, 5, 100)
    y = a * (x ** 2) + b * x + c
    fig = plt.figure()
    plt.plot(x, y)
    plt.axhline(y=0, color='black', linestyle='-')
    plt.axvline(x=0, color='black', linestyle='-')
    for p in solutions:
        plt.plot(p, a * (p ** 2) + b * p + c, color='green', marker="o")

    png_image = io.BytesIO()
    fig.savefig(png_image)
    image_b64_encoding = base64.b64encode(png_image.getvalue()).decode('ascii')

    return templates.TemplateResponse(
        'plot.html',
        {
            'request': request,
            'roots': solutions,
            'graph': image_b64_encoding,
        }
    )
