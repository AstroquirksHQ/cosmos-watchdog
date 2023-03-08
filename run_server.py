from src.api.app import app


def run():
    app.run(app.config["HOST"], app.config["PORT"], debug=app.config.get("DEBUG"))


if __name__ == "__main__":
    run()
