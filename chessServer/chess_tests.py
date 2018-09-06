import chess

POS_START_SIGN = b'S'
POS_END_SIGN = b'E'
OCCUPIED = b'\x01'
EMPTY = b'\x00'

def step(from_idx,to_idx,statuses):
    a = []
    for i,stat in enumerate(statuses):
        if i == from_idx:
          a.append(b'\x00')
        elif i == to_idx:
            a.append(b'\x01')
        else:
            a.append(stat)
    return a

initial_board = OCCUPIED * 16 + EMPTY * (8 * 4) + OCCUPIED * 16

with open("/dev/pts/7",'wb') as serial_writer:
    position = initial_board

    serial_writer.write(POS_START_SIGN)
    position = step(12,28,position)#e2->e4
    serial_writer.write(b''.join(position))
    serial_writer.write(POS_END_SIGN)

    serial_writer.write(POS_START_SIGN)
    position = step(52, 36, position)  # e2->e4
    serial_writer.write(b''.join(position))
    serial_writer.write(POS_END_SIGN)

    serial_writer.write(POS_START_SIGN)
    position = step(5, 12, position)  # e2->e4
    serial_writer.write(b''.join(position))
    serial_writer.write(POS_END_SIGN)

    serial_writer.write(POS_START_SIGN)
    position = step(61, 52, position)  # e2->e4
    serial_writer.write(b''.join(position))
    serial_writer.write(POS_END_SIGN)

    serial_writer.write(POS_START_SIGN)
    position = step(6, 21, position)  # e2->e4
    serial_writer.write(b''.join(position))
    serial_writer.write(POS_END_SIGN)

    serial_writer.write(POS_START_SIGN)
    position = step(62, 45, position)  # e2->e4
    serial_writer.write(b''.join(position))
    serial_writer.write(POS_END_SIGN)

    serial_writer.write(POS_START_SIGN)
    position = step(4, 6, position)  # e2->e4
    serial_writer.write(b''.join(position))
    serial_writer.write(POS_END_SIGN)