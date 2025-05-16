from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "<h1>PDF/Image to Excel Converter</h1><p>Welcome to the homepage!</p>" 