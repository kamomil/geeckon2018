import chess

POS_START_SIGN = b'S'
POS_END_SIGN = b'E'
OCCUPIED = b'\x01'
EMPTY = b'\x00'

def cateling_step(from1,from2, to1, to2, statuses):
    a = b''
    for i,stat in enumerate(statuses):
        if i == from1 or i == from2:
          a += EMPTY
        elif i == to1 or i == to2:
            a += OCCUPIED
        else:
            a += stat.to_bytes(1,byteorder='little')
    return a


def step(from_idx,to_idx,statuses):
    a = b''
    for i,stat in enumerate(statuses):
        if i == from_idx:
            a += EMPTY
        elif i == to_idx:
            a += OCCUPIED
        else:
            byts = stat.to_bytes(1,byteorder='little')
            a += byts
    return a

initial_board = OCCUPIED * 16 + EMPTY * (8 * 4) + OCCUPIED * 16

with open("/dev/pts/7",'wb') as serial_writer:
    position = initial_board


    serial_writer.write(POS_START_SIGN)
    position = step(12,28,position)#e2->e4
    serial_writer.write(position)
    serial_writer.write(POS_END_SIGN)

    serial_writer.write(POS_START_SIGN)
    position = step(52, 36, position)  # e7->e5
    serial_writer.write(position)
    serial_writer.write(POS_END_SIGN)

    serial_writer.write(POS_START_SIGN)
    position = step(5, 12, position)  # f1->f2
    serial_writer.write(position)
    serial_writer.write(POS_END_SIGN)

    serial_writer.write(POS_START_SIGN)
    position = step(61, 52, position)  # f8->e7
    serial_writer.write(position)
    serial_writer.write(POS_END_SIGN)

    serial_writer.write(POS_START_SIGN)
    position = step(6, 21, position)  # g1->f3
    serial_writer.write(position)
    serial_writer.write(POS_END_SIGN)

    serial_writer.write(POS_START_SIGN)
    position = step(62, 45, position)  # g8->f6
    serial_writer.write(position)
    serial_writer.write(POS_END_SIGN)

    serial_writer.write(POS_START_SIGN)
    position = step(4, 6, position)  # casteling
    serial_writer.write(position)
    serial_writer.write(POS_END_SIGN)