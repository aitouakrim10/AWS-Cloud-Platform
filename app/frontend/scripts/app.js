// Game state
let board = null;
let game = new Chess();
let playerColor = null;
let playerId = null;
let isSpectator = true;
let pendingState = null;

// WebSocket connection (will be set after board init)
let socket = null;

// Initialize the board
function initBoard() {
    const config = {
        draggable: true,
        position: 'start',
        onDragStart: onDragStart,
        onDrop: onDrop,
        onSnapEnd: onSnapEnd,
        pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png'
    };
    board = Chessboard('board', config);
}

// Only allow dragging own pieces on own turn
function onDragStart(source, piece, position, orientation) {
    // Don't allow moves if game is over
    if (game.game_over()) return false;
    
    // Spectators can't move
    if (isSpectator) return false;
    
    // Only allow moving pieces on your turn
    if (playerColor === 'white' && piece.search(/^b/) !== -1) return false;
    if (playerColor === 'black' && piece.search(/^w/) !== -1) return false;
    
    // Check if it's your turn
    const currentTurn = game.turn() === 'w' ? 'white' : 'black';
    if (currentTurn !== playerColor) return false;
    
    return true;
}

// Handle piece drop
function onDrop(source, target) {
    // Check if move is legal locally first
    const move = game.move({
        from: source,
        to: target,
        promotion: 'q' // Always promote to queen for simplicity
    });
    
    // Illegal move
    if (move === null) return 'snapback';
    
    // Send move to server
    const moveUci = source + target + (move.promotion || '');
    socket.emit('make_move', { move_uci: moveUci });
}

// Update board position after piece snap animation
function onSnapEnd() {
    board.position(game.fen());
}

// Update game state from server
function updateGameState(state) {
    if (!board) {
        pendingState = state;
        return;
    }
    game.load(state.board_fen);
    board.position(state.board_fen);
    
    // Update UI info
    updateStatus(state);
}

// Update status display
function updateStatus(state) {
    const turnText = state.current_turn === 0 ? 'White' : 'Black';
    let statusText = `Current turn: ${turnText}`;
    
    if (state.game_over) {
        if (state.winner === null) {
            statusText = 'Game Over - Draw!';
        } else {
            statusText = `Game Over - ${state.winner === 0 ? 'White' : 'Black'} wins!`;
        }
    }
    
    document.getElementById('status').textContent = statusText;
    
    // Update player info
    const playerInfo = isSpectator 
        ? 'You are spectating' 
        : `You are playing as ${playerColor}`;
    document.getElementById('player-info').textContent = playerInfo;
}

// UI helper functions
function showMessage(message, type = 'info') {
    const msgEl = document.getElementById('messages');
    msgEl.textContent = message;
    msgEl.className = type;
    setTimeout(() => { msgEl.textContent = ''; }, 3000);
}

// Button handlers
function joinGame() {
    const playerName = document.getElementById('player-name').value || 'Anonymous';
    socket.emit('join_game', { player_name: playerName });
}

function resetGame() {
    socket.emit('reset_game');
}

// Initialize when page loads
$(document).ready(function() {
    initBoard();
    
    // Connect to WebSocket after board is ready
    socket = io('http://localhost:5000');
    
    // Set up socket event handlers
    socket.on('connect', () => {
        console.log('Connected to server');
        document.getElementById('connection-status').textContent = 'Connected';
        document.getElementById('connection-status').className = 'connected';
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
        document.getElementById('connection-status').textContent = 'Disconnected';
        document.getElementById('connection-status').className = 'disconnected';
    });

    socket.on('game_state', (state) => {
        console.log('Game state received:', state);
        updateGameState(state);
    });

    socket.on('player_assigned', (data) => {
        console.log('Player assigned:', data);
        playerId = data.player_id;
        playerColor = data.color;
        isSpectator = data.color === 'spectator';
        
        // Orient board based on player color
        if (board) {
            if (playerColor === 'black') {
                board.orientation('black');
            } else {
                board.orientation('white');
            }
        }
        
        showMessage(data.message);
    });

    socket.on('move_result', (data) => {
        console.log('Move result:', data);
        if (!data.success) {
            socket.emit('get_state');
            showMessage(data.message, 'error');
        }
    });

    socket.on('game_over', (data) => {
        console.log('Game over:', data);
        const winner = data.winner === 0 ? 'White' : data.winner === 1 ? 'Black' : 'Nobody';
        showMessage(`Game Over! ${winner} wins! (${data.result})`);
    });

    socket.on('game_reset', (data) => {
        console.log('Game reset:', data);
        game.reset();
        if (board) {
            board.position('start');
        }
        isSpectator = true;
        playerColor = null;
        playerId = null;
        showMessage(data.message);
    });
    
    // Apply any pending state
    if (pendingState) {
        updateGameState(pendingState);
        pendingState = null;
    }
});
