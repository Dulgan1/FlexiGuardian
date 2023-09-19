#!/usr/bin/python3
""" WSGI app for flexiguardian to run with Gunicorn"""
from app import app
if __name__ == '__main__':
    app.run()
