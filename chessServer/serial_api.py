import serial
import logging
import chess

POS_START_SIGN = b'S'
POS_END_SIGN = b'E'
ON = 1
OFF = 0
serial_str = '/dev/tty16'
baud = 9600

# with serial.Serial(serial_str, baud) as ser:
#     while(True):
#         x = ser.read()
#         if(x == b'S'):
#             logging.debug("Serial: got new position")
#             for idx in range(64):
#                 pass #TODO
#

def new_position():
    pass

class Game():
    def __init__(self):
        self.board = chess.Board()

def start_playing():
    board = chess.Board()
    with serial.Serial(serial_str, baud) as ser:
        while(True):
            x = ser.read()
            if(x == POS_START_SIGN):
                logging.debug("Serial: got new position")
                from_square = None
                to_square = None
                moving_piece = None
                for idx in range(64):
                    status = ser.read()
                    # push(move)
                    curr_piece = board.piece_at(idx)

                    if status == 0:
                        #A piece in the current index is not there now - update the from_square
                        if curr_piece:
                            if not from_square:
                                from_square = idx
                                moving_piece = curr_piece
                            elif curr_piece.piece_type == chess.KING and\
                                    moving_piece.piece_type == chess.ROOK:
                                from_square = idx
                                moving_piece = curr_piece
                            elif curr_piece.piece_type == chess.ROOK and\
                                    moving_piece.piece_type == chess.KING:
                                pass #THIS IS PROBABLY CASTLING
                            else:
                                logging.error("Got invalid moves - consuming bytes until END_POSITION")
                                break
                    elif status == 1:
                        # The square in the current index used to be empty and now it is not - update the to_square
                        if not curr_piece:
                            if not to_square:
                                to_square = idx
                            elif curr_piece.piece_type == chess.KING:
                                from_square = idx
                                moving_piece = curr_piece
                            elif curr_piece.piece_type == chess.ROOK and \
                                    moving_piece.piece_type == chess.KING:
                                pass  # THIS IS PROBABLY CASTLING
                            else:
                                logging.error("Got invalid moves - consuming bytes until END_POSITION")
                                break

                x = ser.read()
                if ser.read() != POS_END_SIGN:
                    logging.error("didn't got END_POSITION_SIGN after reading 64 bytes")
                while(ser.read() != POS_END_SIGN):
                    pass







start_playing()
