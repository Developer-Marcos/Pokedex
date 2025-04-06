# Run this file to start the pokedex! Go to /pokedex

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

