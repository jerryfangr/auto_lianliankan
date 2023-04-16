
def check_horizontal(x1: 'int', y1: 'int', x2: 'int', y2: 'int', type_matrix: 'list'):
    '''
    check if two items can be linked horizontally
    args:
        x1, y1: the first block's coordinate
        x2, y2: the second block's coordinate
        type_matrix: the block's type matrix(coordinate axis)
    return:
        (bool): can connect or not
    '''

    # judge if two items are in the same row
    if x1 != x2:
        return False

    startY = min(y1, y2)
    endY = max(y1, y2)

    # judge if two items are adjacent
    if (endY - startY) == 1:
        return True

    # judge if the path between two items is available(only 0 in the path)
    for i in range(startY+1, endY):
        if type_matrix[x1][i] != 0:
            return False

    return True


def check_vertical(x1: 'int', y1: 'int', x2: 'int', y2: 'int', type_matrix: 'list'):
    '''
    check if two items can be linked vertically
    args:
        x1, y1: the first block's coordinate
        x2, y2: the second block's coordinate
        type_matrix: the block's type matrix(coordinate axis)
    return:
        (bool): can connect or not
    '''

    # judge if two items are in the same column
    if y1 != y2:
        return False

    startX = min(x1, x2)
    endX = max(x1, x2)

    # judge if two items are adjacent
    if (endX - startX) == 1:
        return True

    # judge if the path between two items is available(only 0 in the path)
    for i in range(startX+1, endX):
        if type_matrix[i][y1] != 0:
            return False

    return True


def check_turn_once(x1: 'int', y1: 'int', x2: 'int', y2: 'int', type_matrix: 'list'):
    '''
    check if two items can be linked with one turn
    args:
        x1, y1: the first block's coordinate
        x2, y2: the second block's coordinate
        type_matrix: the block's type matrix(coordinate axis)
    return:
        (bool): can connect or not
    '''

    # judge if two items are in the same row or column
    if x1 != x2 and y1 != y2:
        # coordinate of the turn point
        cx = x1
        cy = y2
        dx = x2
        dy = y1
        # judge if the turn point is available
        if type_matrix[cx][cy] == 0:
            if check_horizontal(x1, y1, cx, cy, type_matrix) and check_vertical(cx, cy, x2, y2, type_matrix):
                return True
        if type_matrix[dx][dy] == 0:
            if check_vertical(x1, y1, dx, dy, type_matrix) and check_horizontal(dx, dy, x2, y2, type_matrix):
                return True
    return False


def check_turn_twice(x1: 'int', y1: 'int', x2: 'int', y2: 'int', type_matrix: 'list'):
    '''
    check if two items can be linked with two turns
    args:
        x1, y1: the first block's coordinate
        x2, y2: the second block's coordinate
        type_matrix: the block's type matrix(coordinate axis)
    return:
        (bool): can connect or not
    '''

    # find all the available turn points
    for i in range(0, len(type_matrix)):
        for j in range(0, len(type_matrix[1])):
            # skip the block which is not empty
            if type_matrix[i][j] != 0:
                continue
            
            # skip the block which is not in the same row or column with the two items
            if i != x1 and i != x2 and j != y1 and j != y2:
                continue

            # skip the block which is the intersection of the two items
            if (i == x1 and j == y2) or (i == x2 and j == y1):
                continue

            if check_turn_once(x1, y1, i, j, type_matrix) and (check_horizontal(i, j, x2, y2, type_matrix) or check_vertical(i, j, x2, y2, type_matrix)):
                return True

            if check_turn_once(i, j, x2, y2, type_matrix) and (check_horizontal(x1, y1, i, j, type_matrix) or check_vertical(x1, y1, i, j, type_matrix)):
                return True

    return False


def check_can_link(x1: 'int', y1: 'int', x2: 'int', y2: 'int', type_matrix: 'list'):
    '''
    judge two block can connect or not
    args:
        x1, y1: the first block's coordinate
        x2, y2: the second block's coordinate
        type_matrix: the block's type matrix(coordinate axis)
    return:
        (bool): can connect or not
    '''

    # jump over the empty block
    if type_matrix[x1][y1] == 0 or type_matrix[x2][y2] == 0:
        return False

    # jump over the same block
    if x1 == x2 and y1 == y2:
        return False

    # jump over the different type block
    if type_matrix[x1][y1] != type_matrix[x2][y2]:
        return False

    # check the block can connect or not
    if check_horizontal(x1, y1, x2, y2, type_matrix):
        return True
    if check_vertical(x1, y1, x2, y2, type_matrix):
        return True
    if check_turn_once(x1, y1, x2, y2, type_matrix):
        return True
    if check_turn_twice(x1, y1, x2, y2, type_matrix):
        return True

    return False