from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

content = {'name':'server test123123',
           'list': {'question':1, 'answer':2, 'saving':3}
           }

@home_bp.route('/home')
def home():
    return render_template('home.html', **content)
