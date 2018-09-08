import serial
import logging
import chess

POS_START_SIGN = b'S'
POS_END_SIGN = b'E'
ILEGAL_MOVE = b'X'
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

def belong_to_opponent(board : chess.Board,piece):
    if board.turn != piece.color:
        return True

#the Arduino runs in an infinite loop, every time a square status changes it updates us
#so one move is read sent to us according the following:

#1) two board positions in case of normal move - (empty,occupied)
#2) 3 board positions in case of a move that eat opponents' piece: (empty,empty,occupied)
#3) 4 board positions in case of casteling: (empty,occupied,empty,occupied)

# we read the board until we have at least one 'from_square' and one 'to_square'
# once we do, we update the board according to the square.
# if we have a castling move we assume the move start by moving the king
# then we turn the 'during_castling' flag to indicate consuming the move of the ROOK

#in case of a move that takes an opponents' piece, we ignore the first empty square we
# read since this is the eaten piece removed from the board and not the moving piece

def start_playing():
    logging.basicConfig(level=logging.DEBUG)
    board = chess.Board()
    print(board)
    eaten_idx = None
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
                    logging.debug(f"{idx}: got status {status}")
                    # push(move)
                    curr_piece = board.piece_at(idx)

                    # A piece in the current index is not there now - update the from_square
                    if status == EMPTY and curr_piece:
                        if belong_to_opponent(board,curr_piece):
                            eaten_idx = idx
                        else:
                            from_squares.append(idx)
                    # The square in the current index used to be empty and now it is not - update the to_square
                    elif status == OCCUPIED and not curr_piece:
                        to_squares.append(idx)

                    elif status == OCCUPIED and curr_piece and idx == eaten_idx:
                        to_squares.append(idx)
                        eaten_idx = None
                    from_squares = list(set(from_squares))
                    to_squares = list(set(to_squares))

                    logging.debug(f"{idx}: from: {from_squares}, to {to_squares}")
            else:
                logging.error(f"waited to START_SIGN and got {x}")
                continue
            logging.debug(f"from: {from_squares}, to {to_squares}")
            if len(from_squares) and len(to_squares):
                if during_castling:
                    logging.debug("Done with casteling")
                    from_squares = []
                    to_squares = []
                    board.push(during_castling)
                    during_castling = None
                    print(board)

                else:
                    m = get_move(from_squares,to_squares,board)
                    if not m:
                        logging.error("Got invalid move! - read until END_SIGN")
                        logging.error(f"from: {from_squares}, to {to_squares}")
                        ser.write(ILEGAL_MOVE)
                        during_castling = None
                        from_squares = []
                        to_squares = []
                    elif board.is_castling(m) and len(from_squares) == 1 and len(to_squares) == 1:
                        during_castling = m
                        from_squares = []
                        to_squares = []
                        logging.debug("Duoring casteling")
                    else:
                        logging.debug("Got move! pushing it")
                        from_squares = []
                        to_squares = []
                        board.push(m)
                        print(board)
                        if board.is_checkmate():
                            print("Hurray! Game Ended!!")
                            break
            else:
                pass
                logging.debug(f"from: {from_squares}, to {to_squares}")
            x = ser.read()
            if x != POS_END_SIGN:
                logging.error(f"didn't got END_POSITION_SIGN after reading 64 bytes: {x}")
            while(x != POS_END_SIGN):
                x = ser.read()


start_playing()
