from flask import Flask, render_template, send_from_directory
from dotenv import load_dotenv
from sqlalchemy import URL
import os


# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
app.template_folder = os.path.join(project_dir, 'templates')
app.static_folder = os.path.join(project_dir, 'static')

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=bool(os.environ.get('DEBUG')))