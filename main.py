from logging import debug
from website import create_app

# Create app
app = create_app()

if __name__ == "__main__":
    # Run app
    app.run(debug=True)
