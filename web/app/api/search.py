"""
세션 목록 조회, 질문 목록 조회 api를 관리하는 모듈입니다.
"""
from flask import Blueprint, request, jsonify, url_for, make_response
from app.manager.db_manager import mariadb_user_manager

mySession_bp = Blueprint('mySession', __name__, url_prefix="/search")
myQuestion_bp = Blueprint('myQuestion', __name__, url_prefix="/search")
myAnswer_bp = Blueprint('myAnswer', __name__, url_prefix="/search")
myPick_bp = Blueprint('myPick', __name__, url_prefix="/search")

@mySession_bp.route('/my_session')
def searchingMySessions():
    """
    """
    return

@myQuestion_bp.route('/my_question')
def searchingMyQuestions():
    """
    """
    return

@myAnswer_bp.route('/my_answer')
def searchingMyAnswers():
    """
    """
    return

@myPick_bp.route('/my_pick')
def searchingMyPick():
    """
    """
    return