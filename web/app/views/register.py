from flask import Blueprint, render_template, request, jsonify

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=["GET"])
def register():
    return render_template('register.html')
