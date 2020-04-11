import logging


def create_matrix(string, width, height):
    i = 0
    matrix = []
    for y in range(0, height):
        newrow = []
        for x in range(0, width):
            newrow.append(string[i:i+2])
            i += 2
        matrix.append(newrow)
    return matrix


def xor_matrices(matrix1, matrix2):
    matrix_width = len(matrix1[0])
    matrix_height = len(matrix1[0])
    # logging.debug('Width: ' + str(matrix_width))
    # logging.debug('Height: ' + str(matrix_height))
    o_matrix = matrix2
    for y in range(0, matrix_height):
        for x in range(0, matrix_width):
            # logging.debug('XOR ' + str(hex(int(matrix1[y][x], 16))) + ' + ' + str(hex(int(matrix2[y][x], 16))))
            m1 = int(matrix1[y][x], 16)  # Convert matrix 1's value to a hex value
            m2 = int(matrix2[y][x], 16)  # Convert matrix 2's value to a hex value
            output = hex(m1 ^ m2)[2:]  # Bitwise XOR on the values of m1 and m2
            if len(output) < 2:  # If the hex returned a value less than 8 (in decimal),
                # add a 0 so it is still two digits
                output = '0' + output
            o_matrix[y][x] = output
    logging.debug('Finished Bitwise XOR: ' + str(o_matrix))
    return o_matrix


def e_switch_column(k_matrix, i_matrix):
    logging.debug('Beginning switchColumn')
    logging.debug('e_switch_column initial matrix: ' + str(i_matrix))
    matrix_width = len(k_matrix[0])
    matrix_height = len(k_matrix[0])
    for i in range(0, matrix_height):  # Goes through each row
        for j in range(0, matrix_width):  # Goes through each column
            column1 = int(k_matrix[i][j][0], 16) % 4
            column2 = int(k_matrix[i][j][1], 16) % 4
            logging.debug('key: ' + str(i) + ',' + str(j) + ' Replace column ' + str(column1) +
                          ' with column ' + str(column2))
            for k in range(0, matrix_height):  # Runs the column switch on each row of the columns selected
                # logging.debug('before: ' + str(i_matrix[k]))
                temp = i_matrix[k][column1]
                i_matrix[k][column1] = i_matrix[k][column2]
                i_matrix[k][column2] = temp
                # logging.debug('after: ' + str(i_matrix[k]))
    logging.debug('e_switch_column final matrix: ' + str(i_matrix))
    return i_matrix

def d_switch_column(k_matrix, i_matrix):
    logging.debug('Beginning decrypt_switchColumn')
    logging.debug('d_switch_column initial matrix: ' + str(i_matrix))
    matrix_width = len(k_matrix[0])
    matrix_height = len(k_matrix[0])
    for i in range(matrix_height - 1, -1, -1):  # Goes through each row
        for j in range(matrix_width - 1, -1, -1):  # Goes through each column
            column1 = int(k_matrix[i][j][0], 16) % 4
            column2 = int(k_matrix[i][j][1], 16) % 4
            # logging.debug('key: ' + str(i) + ',' + str(j) + ' Replace column ' + str(column1) +
            #               ' with column ' + str(column2))
            for k in range(0, matrix_height):  # Runs the column switch on each row of the columns selected
                # logging.debug('before: ' + str(i_matrix[k]))
                temp = i_matrix[k][column1]
                i_matrix[k][column1] = i_matrix[k][column2]
                i_matrix[k][column2] = temp
                # logging.debug('after: ' + str(i_matrix[k]))
    logging.debug('d_switch_column final matrix: ' + str(i_matrix))
    return i_matrix


def e_switch_row(k_matrix, i_matrix):
    logging.debug('Beginning switch_row')
    logging.debug('e_switch_row initial matrix: ' + str(i_matrix))
    matrix_width = len(k_matrix[0])
    matrix_height = len(k_matrix[0])
    for i in range(0, matrix_height):  # Goes through each row
        for j in range(0, matrix_width):  # Goes through each column
            row1 = int(k_matrix[i][j][0], 16) % 4
            row2 = int(k_matrix[i][j][1], 16) % 4
            logging.debug('key: ' + str(i) + ',' + str(j) + ' Replace row ' + str(row1) +
                          ' with row ' + str(row2))
            for k in range(0, matrix_width):  # Runs the row switch on each column of the rows selected
                # logging.debug('before: ' + str(i_matrix[k]))
                temp = i_matrix[row1][k]
                i_matrix[row1][k] = i_matrix[row2][k]
                i_matrix[row2][k] = temp
                # logging.debug('after: ' + str(i_matrix[k]))
    logging.debug('e_switch_row final matrix: ' + str(i_matrix))
    return i_matrix

def d_switch_row(k_matrix, i_matrix):
    logging.debug('Beginning decrypt_switchRow')
    logging.debug('d_switch_row initial matrix: ' + str(i_matrix))
    matrix_width = len(k_matrix[0])
    matrix_height = len(k_matrix[0])
    for i in range(matrix_height - 1, -1, -1):  # Goes through each row
        for j in range(matrix_width - 1, -1, -1):  # Goes through each column
            row1 = int(k_matrix[i][j][0], 16) % 4
            row2 = int(k_matrix[i][j][1], 16) % 4
            logging.debug('key: ' + str(i) + ',' + str(j) + ' Replace row ' + str(row1) +
                          ' with row ' + str(row2))
            for k in range(0, matrix_width):  # Runs the column switch on each row of the columns selected
                # logging.debug('before: ' + str(i_matrix[k]))
                temp = i_matrix[row1][k]
                i_matrix[row1][k] = i_matrix[row2][k]
                i_matrix[row2][k] = temp
                # logging.debug('after: ' + str(i_matrix[k]))
    logging.debug('d_switch_row final matrix: ' + str(i_matrix))
    return i_matrix


def e_switch_block(k_matrix, i_matrix):
    logging.debug('Beginning e_switch_block')
    logging.debug('e_switch_block initial matrix: ' + str(i_matrix))
    matrix_width = len(k_matrix[0])
    matrix_height = len(k_matrix[0])
    for i in range(0, matrix_height):  # Goes through each row .
        for j in range(0, matrix_width, 2):  # Goes through each column
            column1 = int(k_matrix[i][j][0], 16) % 4
            row1 = int(k_matrix[i][j][1], 16) % 4

            column2 = int(k_matrix[i][j+1][0], 16) % 4
            row2 = int(k_matrix[i][j+1][1], 16) % 4
            logging.debug('key: ' + str(i) + ',' + str(j) + ' Replace block [' + str(row1) + ',' + str(column1) + '] '
                          ' with block [' + str(row2) + ',' + str(column2) + '] ')
            logging.debug('before: ' + str(i_matrix[row1][column1]) + ',' + str(i_matrix[row2][column2]))
            temp = i_matrix[row1][column1]
            i_matrix[row1][column1] = i_matrix[row2][column2]
            i_matrix[row2][column2] = temp
            logging.debug('after: ' + str(i_matrix[row1][column1]) + ',' + str(i_matrix[row2][column2]))
    logging.debug('e_switch_block final matrix: ' + str(i_matrix))
    return i_matrix

def d_switch_block(k_matrix, i_matrix):
    logging.debug('Beginning decrypt_switchBlock')
    logging.debug('d_switch_block initial matrix: ' + str(i_matrix))
    matrix_width = len(k_matrix[0])
    matrix_height = len(k_matrix[0])
    for i in range(matrix_height - 1, -1, -1):  # Goes through each row
        for j in range(matrix_width - 2, -1, -2):  # Goes through each column
            column1 = int(k_matrix[i][j][0], 16) % 4
            row1 = int(k_matrix[i][j][1], 16) % 4

            column2 = int(k_matrix[i][j + 1][0], 16) % 4
            row2 = int(k_matrix[i][j + 1][1], 16) % 4
            logging.debug('key: ' + str(i) + ',' + str(j) + ' Replace block [' + str(row1) + ','
                          + str(column1) + '] with block [' + str(row2) + ',' + str(column2) + '] ')
            logging.debug('before: ' + str(i_matrix[row1][column1]) + ',' + str(i_matrix[row2][column2]))
            temp = i_matrix[row1][column1]
            i_matrix[row1][column1] = i_matrix[row2][column2]
            i_matrix[row2][column2] = temp
            logging.debug('after: ' + str(i_matrix[row1][column1]) + ',' + str(i_matrix[row2][column2]))
    logging.debug('d_switch_block final matrix: ' + str(i_matrix))
    return i_matrix


def encrypt_matrix(input_array, k_matrix):
    for i in range(0, len(input_array)):
        logging.debug('Beginning encryption of Array ' + str(i) + ': ' + str(input_array[i]))
        i_matrix = input_array[i]
        for j in range(0, 20):
            i_matrix = xor_matrices(k_matrix, i_matrix)
            i_matrix = e_switch_column(k_matrix, i_matrix)
            i_matrix = e_switch_row(k_matrix, i_matrix)
            i_matrix = e_switch_block(k_matrix, i_matrix)
            logging.debug('Matrix ' + str(i) + ', Round: ' + str(j) + ': ' + str(i_matrix))
        input_array[i] = i_matrix
    return input_array


def decrypt_matrix(input_array, k_matrix):
    for i in range(0, len(input_array)):
        logging.debug('Beginning decryption of Array ' + str(i) + ': ' + str(input_array[i]))
        i_matrix = input_array[i]
        for j in range(0, 20):
            i_matrix = d_switch_block(k_matrix, i_matrix)
            i_matrix = d_switch_row(k_matrix, i_matrix)
            i_matrix = d_switch_column(k_matrix, i_matrix)
            i_matrix = xor_matrices(k_matrix, i_matrix)
            logging.debug('Matrix ' + str(i) + ', Round: ' + str(j) + ': ' + str(i_matrix))
        input_array[i] = i_matrix
    return input_array