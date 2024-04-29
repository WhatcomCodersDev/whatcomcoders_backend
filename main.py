from app import create_flask_app

app = create_flask_app()

if __name__ == "__main__":
    app.run(debug=True, port=app.config["PORT"], host="0.0.0.0")