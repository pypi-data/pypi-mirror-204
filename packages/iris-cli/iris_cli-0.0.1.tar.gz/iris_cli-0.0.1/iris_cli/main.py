import requests
import typer
from dotenv import dotenv_values

app = typer.Typer()
config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}


@app.command()
def ping():
    print("pong")


@app.command()
def goodbye(name: str, formal: bool = typer.Option(False, "--formal", "-f")):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


@app.command()
def post_get_predict(sepal_length: float,
                     sepal_width: float,
                     petal_length: float,
                     petal_width: float):
    response = requests.post(f'{config["URL"]}/predict_flower',
                             json={"sepal_length": sepal_length,
                                   "sepal_width": sepal_width,
                                   "petal_length": petal_length,
                                   "petal_width": petal_width})
    print(response.json())


if __name__ == "__main__":
    app()
