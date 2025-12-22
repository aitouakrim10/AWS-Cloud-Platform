import game_manager
from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from config import JWT_SECRET
from db import Base, engine
from auth import auth_bp
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = JWT_SECRET
CORS(app, origins="*")
socketio = SocketIO(app, cors_allowed_origins="*")

Base.metadata.create_all(bind=engine)

chess_game = game_manager.ChessGame()
connected_players = {}  # sid -> player_id

app.register_blueprint(auth_bp)

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")
    emit('game_state', chess_game.get_game_state())


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in connected_players:
        player_id = connected_players.pop(sid)
        print(f"Player {player_id} disconnected")
    print(f"Client disconnected: {sid}")


@socketio.on('join_game')
def handle_join_game(data):
    player_name = data.get('player_name', f'Player_{request.sid[:6]}')
    result = chess_game.add_player(player_name)
    
    if "added" in result.lower():
        player_id = len(chess_game.players) - 1  # 0 for white, 1 for black
        connected_players[request.sid] = player_id
        color = "white" if player_id == 0 else "black"
        emit('player_assigned', {'player_id': player_id, 'color': color, 'message': result})
    else:
        emit('player_assigned', {'player_id': -1, 'color': 'spectator', 'message': result})
    
    # Broadcast updated game state to all clients
    socketio.emit('game_state', chess_game.get_game_state())

@socketio.on('make_move')
def handle_make_move(data):
    sid = request.sid
    if sid not in connected_players:
        emit('move_result', {'success': False, 'message': 'You are not a player'})
        return
    
    player_id = connected_players[sid]
    move_uci = data.get('move_uci')
    
    result = chess_game.make_move(player_id, move_uci)
    success = "accepted" in result.lower()
    
    emit('move_result', {'success': success, 'message': result})
    
    if success:
        # Broadcast updated game state to all clients
        socketio.emit('game_state', chess_game.get_game_state())
        
        if chess_game.game_over:
            socketio.emit('game_over', {
                'winner': chess_game.winner,
                'result': chess_game.board.result()
            })

@socketio.on('get_state')
def handle_get_state():
    emit('game_state', chess_game.get_game_state())


@socketio.on('reset_game')
def handle_reset_game():
    global chess_game, connected_players
    chess_game = game_manager.ChessGame()
    connected_players = {}
    socketio.emit('game_reset', {'message': 'Game has been reset'})
    socketio.emit('game_state', chess_game.get_game_state())


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)


