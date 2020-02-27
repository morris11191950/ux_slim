import os

from app import create_app

app = create_app()

# print("I am in ux.py")

if __name__ == '__main__':
    app.ux_slim()
