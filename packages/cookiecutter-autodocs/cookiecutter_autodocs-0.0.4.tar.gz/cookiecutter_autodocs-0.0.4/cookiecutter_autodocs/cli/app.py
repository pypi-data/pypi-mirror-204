from cookiecutter_autodocs.cli._async import AsyncTyper
from cookiecutter_autodocs.cli.generate import generate_app

app = AsyncTyper()

app.add_typer(generate_app, name="generate")
