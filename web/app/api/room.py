"""
    세션에 대한 api를 관리하는 모듈입니다.
"""
from flask import Blueprint, request, make_response, jsonify
from flask_socketio import join_room, leave_room
from app.manager.db_manager import mariadb_user_manager, mariadb_admin_manager, 
from app.manager.chat_manager import ChatManager
from app.manager.llm_manager import llmManager

createSession_bp = Blueprint('create_session', __name__, url_prefix='/room')
joinRoom_bp = Blueprint('join_room', __name__, url_prefix='/room')
sendtoLLM_bp = Blueprint('sendtollm', __name__, url_prefix='/room')

@createSession_bp.route('/create')
def craete_sesison():
    """
    session을 만드는 
    """
    ChatManager.create_room()    
    return 

@joinRoom_bp.route('/join', methods=["GET"])
def user_join_room():
    """
    session 페이지 진입시 사용자 정보를 보내고 웹소켓을 연결합니다.
    """
    
    data = request.get_json()

@sendtoLLM_bp.route('/llm', method=["POST"])
def send_to_llm():
    """
    사용자가 보내려 하는 메세지를 llm로 보냅니다.

    request : {
        user_key :
        text (str): 
        }
    """
    request_data = request.get_json()
    response_data = {}

    response = 