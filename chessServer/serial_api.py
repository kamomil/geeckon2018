import serial
import logging
import chess

POS_START_SIGN = b'S'
POS_END_SIGN = b'E'
OCCUPIED = b'\x01'
EMPTY = b'\x00'
serial_str = '/dev/pts/6'
baud = 9600

def create_castling_move(board : chess.Board,from1,from2,to1,to2):
    valid_casteling = []
    legal_moves = list(board.legal_moves)
    for f in [from1,from2]:
        for t in [to1,to2]:
            m = chess.Move(f,t)
            if m in legal_moves and board.is_castling(m):
                valid_casteling.append(m)
    if len(valid_casteling) != 1:
        return None
    return valid_casteling[0]


def get_move(from_squares, to_squares,board):
    legal_moves = list(board.legal_moves)
    if len(from_squares) == 1:
        if len(to_squares) != 1:
            return None
        else:
            m = chess.Move(from_squares[0],to_squares[0])
            if m not in legal_moves:
                return None
            return m
    elif len(from_squares) == 2:
        if len(to_squares) != 2:
            return None
        else:
            return create_castling_move(board, from_squares[0],from_squares[1],to_squares[0],to_squares[1])
    else:
        return None

def belong_to_opponent(board : chess.Board,idx):
    if board.turn() != board.piece_at(idx):
        return True

def start_playing():
    logging.basicConfig(level=logging.DEBUG)
    board = chess.Board()
    with serial.Serial(serial_str, baud) as ser:
        from_squares = []
        to_squares = []
        during_castling = False
        while(True):
            x = ser.read()
            if(x == POS_START_SIGN):
                logging.debug("Serial: got new position")


                for idx in range(64):
                    status = ser.read()
                    logging.debug(f"got status {status}, type {type(status)}")
                    # push(move)
                    curr_piece = board.piece_at(idx)

                    # A piece in the current index is not there now - update the from_square
                    if status == EMPTY and curr_piece and not belong_to_opponent(board,from_squares[0]):
                        from_squares.append(idx)
                    # The square in the current index used to be empty and now it is not - update the to_square
                    elif status == OCCUPIED and not curr_piece:
                        to_squares.append(idx)
            else:
                logging.error(f"waited to START_SIGN and got {x}")
                continue

            if len(from_squares) and len(to_squares):
                if during_castling:
                    during_castling = False
                    continue

                m = get_move(from_squares,to_squares,board)
                if not m:
                    logging.error("Got invalid move! - read until END_SIGN")
                else:
                    if board.is_castling(m):
                        during_castling = True
                    logging.debug("Got move! pushing it")
                    from_squares = []
                    to_squares = []
                    board.push(m)
                    if board.is_checkmate():
                        print("Hurray! Game Ended!!")
                        break
            x = ser.read()
            if ser.read() != POS_END_SIGN:
                logging.error("didn't got END_POSITION_SIGN after reading 64 bytes")
            while(ser.read() != POS_END_SIGN):
                pass


start_playing()
