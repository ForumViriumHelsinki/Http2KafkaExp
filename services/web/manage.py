from flask.cli import FlaskGroup

from project import app  # , db, User

cli = FlaskGroup(app)


@cli.command("hello")
def print_hello():
    print("HELLO")


if __name__ == "__main__":
    cli()
