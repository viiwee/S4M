import logging
import random
import hashlib

repetitions = 21  # Should be odd, otherwise there is a small chance of a chunk going unchanged
matrix_width = 8  # Must be even
matrix_height = 8
matrix_salt_length = 4  # Bytes


matrix_str_length = (matrix_width * matrix_height * 2) - (matrix_salt_length * 2)  # Will give i for the length of the
# user input, in steps of the number of hex characters in each matrix. The number of hex characters per matrix will be
# 2*height*width - 4. The -4 takes care of the two salt bytes.
# There are two digits for each hex character. Ex: 00 is the value for NULL


def create_matrix(string):
    i = 0
    matrix = []
    for y in range(0, matrix_height):
        newrow = []
        for x in range(0, matrix_width):
            newrow.append(string[i:i + 2])
            i += 2
        matrix.append(newrow)
    return matrix


def create_matrix_array(input_string, pad_salt):
    if pad_salt:
        char_per_matrix = matrix_str_length
    else: # If we are not adding a salt or padding, add the length of the salt so that the matrix will also
        # pull that in
        char_per_matrix = matrix_str_length + 2 * matrix_salt_length
    total_per_matrix = matrix_width * matrix_height * 2
    matrix_array = []
    for i in range(0, len(input_string), char_per_matrix):  # This jumps by the length of an entire matrix at one

        # Create the string that this matrix will contain (Length of strings in 1 matrix)
        input_append = input_string[i:i + char_per_matrix]
        logging.debug('i: ' + str(i) + ' i+CPM: ' + str(i + char_per_matrix))
        # If padding & salting enabled, do that now
        if pad_salt:
            logging.debug('Salting. MSL: ' + str(matrix_str_length) + ' CPM: ' + str(char_per_matrix) + ' LOI: ' + str(len(input_append)))
            # Add padding
            if len(input_append) < total_per_matrix:
                diff = (char_per_matrix - len(input_append)) // 2  # Dividing by 2 so that append can append a whole hex char
                input_append += '00' * diff  # Append 00 as padding

            # Add Salt
            for j in range(0, matrix_salt_length):
                input_append += random.choice('0123456789abcdef') + random.choice('0123456789abcdef')
            # Debug and display only the last bytes that contain the salt
            logging.debug('Created salt: ' + input_append[matrix_str_length:matrix_str_length + 2*matrix_salt_length])

        # Convert the string to a matrix
        input_append = create_matrix(input_append)

        # Append the matrix to the list of matrices
        matrix_array.append(input_append)
    logging.debug('Created matrix_array: ' + str(matrix_array))
    return matrix_array


def create_key_matrix(key):
    matrix_length = matrix_height * matrix_width * 2
    key = key.encode()

    # Create the 16 byte key
    key = hashlib.sha512(key)
    hashkey = key.hexdigest()[:matrix_length]
    logging.debug('Hex key: ' + hashkey)

    # Create the key matrix
    k_matrix = create_matrix(hashkey)
    logging.debug('Key Matrix: ' + str(k_matrix))

    return k_matrix


def create_string(matrix, remove_salt):
    logging.debug('Converting ' + str(matrix))
    o_string = ''
    for i in matrix:  # Selects an entire matrix at once
        # logging.debug(i)
        byte_num = 0  # Reset the count of which byte of the matrix we are in. Since we are now in a new matrix.
        for j in i:  # Selects one row of the matrix
            # logging.debug(j)
            for k in j:  # Selects one byte of a row of the matrix
                # logging.debug('Byte num: ' + str(byte_num))
                if remove_salt and byte_num >= matrix_str_length // 2:
                    logging.debug('skip')
                    byte_num += 1
                    continue
                # logging.debug('Adding ' + k)
                o_string += k
                byte_num += 1  # Continue the count of which byte of the matrix we are on
    logging.debug('Create string final: ' + o_string)
    return o_string


def xor_matrices(matrix1, matrix2):
    # logging.debug('Width: ' + str(matrix_width))
    # logging.debug('Height: ' + str(matrix_height))
    o_matrix = matrix2
    for y in range(0, matrix_height):
        for x in range(0, matrix_width):
            logging.debug('xor input matrix: ' + str(matrix2))
            m1 = int(matrix1[y][x], 16)  # Convert matrix 1's value to a hex value
            m2 = int(matrix2[y][x], 16)  # Convert matrix 2's value to a hex value
            logging.debug(
                'XOR: k_matrix[' + str(y) + '][' + str(x) + ']: ' + str(m1) + ' + i_matrix[' + str(y) + '][' + str(
                    x) + ']: ' + str(m2))
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
    for i in range(0, matrix_height):  # Goes through each row
        for j in range(0, matrix_width):  # Goes through each column
            column1 = int(k_matrix[i][j][0], 16) % matrix_width
            column2 = int(k_matrix[i][j][1], 16) % matrix_width
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
    for i in range(matrix_height - 1, -1, -1):  # Goes through each row
        for j in range(matrix_width - 1, -1, -1):  # Goes through each column
            column1 = int(k_matrix[i][j][0], 16) % matrix_width
            column2 = int(k_matrix[i][j][1], 16) % matrix_width
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
    for i in range(0, matrix_height):  # Goes through each row
        for j in range(0, matrix_width):  # Goes through each column
            row1 = int(k_matrix[i][j][0], 16) % matrix_height
            row2 = int(k_matrix[i][j][1], 16) % matrix_height
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
    for i in range(matrix_height - 1, -1, -1):  # Goes through each row
        for j in range(matrix_width - 1, -1, -1):  # Goes through each column
            row1 = int(k_matrix[i][j][0], 16) % matrix_height
            row2 = int(k_matrix[i][j][1], 16) % matrix_height
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
    for i in range(0, matrix_height):  # Goes through each row .
        for j in range(0, matrix_width, 2):  # Goes through each column
            column1 = int(k_matrix[i][j][0], 16) % matrix_width
            row1 = int(k_matrix[i][j][1], 16) % matrix_height

            column2 = int(k_matrix[i][j + 1][0], 16) % matrix_width
            row2 = int(k_matrix[i][j + 1][1], 16) % matrix_height
            logging.debug('key: ' + str(i) + ',' + str(j) + ' Replace block [' + str(row1) + ',' + str(column1) + '] '
                                                                                                                  ' with block [' + str(
                row2) + ',' + str(column2) + '] ')
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
    for i in range(matrix_height - 1, -1, -1):  # Goes through each row
        for j in range(matrix_width - 2, -1, -2):  # Goes through each column
            column1 = int(k_matrix[i][j][0], 16) % matrix_width
            row1 = int(k_matrix[i][j][1], 16) % matrix_height

            column2 = int(k_matrix[i][j + 1][0], 16) % matrix_width
            row2 = int(k_matrix[i][j + 1][1], 16) % matrix_height
            logging.debug('key: ' + str(i) + ',' + str(j) + ' Replace block [' + str(row1) + ','
                          + str(column1) + '] with block [' + str(row2) + ',' + str(column2) + '] ')
            logging.debug('before: ' + str(i_matrix[row1][column1]) + ',' + str(i_matrix[row2][column2]))
            temp = i_matrix[row1][column1]
            i_matrix[row1][column1] = i_matrix[row2][column2]
            i_matrix[row2][column2] = temp
            logging.debug('after: ' + str(i_matrix[row1][column1]) + ',' + str(i_matrix[row2][column2]))
    logging.debug('d_switch_block final matrix: ' + str(i_matrix))
    return i_matrix


def encrypt_matrix(plaintext_string, key, verbose):
    # Log the plaintext input
    if verbose: print('Input                   : ' + plaintext_string)

    plaintext_string = plaintext_string.encode().hex()
    k_matrix = create_key_matrix(key)
    input_array = create_matrix_array(plaintext_string, True)

    # Log plaintext array string
    if verbose: print('String before encryption: ' + create_string(input_array, False))

    for i in range(0, len(input_array)):
        logging.debug('Beginning encryption of Array ' + str(i) + ': ' + str(input_array[i]))
        i_matrix = input_array[i]
        for j in range(0, repetitions):
            i_matrix = xor_matrices(k_matrix, i_matrix)
            i_matrix = e_switch_column(k_matrix, i_matrix)
            i_matrix = e_switch_row(k_matrix, i_matrix)
            i_matrix = e_switch_block(k_matrix, i_matrix)
            logging.debug('Matrix ' + str(i) + ', Round: ' + str(j) + ': ' + str(i_matrix))
        input_array[i] = i_matrix
    o_string = create_string(input_array, False)

    # Log plaintext array string
    if verbose: print('String after encryption : ' + create_string(input_array, False))
    return o_string


def decrypt_matrix(encrypted_string, key, verbose):
    # Log the plaintext input
    if verbose: print('Input                   : ' + encrypted_string)

    k_matrix = create_key_matrix(key)
    input_array = create_matrix_array(encrypted_string, False)

    for i in range(0, len(input_array)):
        logging.debug('Beginning decryption of Array ' + str(i) + ': ' + str(input_array[i]))
        i_matrix = input_array[i]
        for j in range(0, repetitions):
            i_matrix = d_switch_block(k_matrix, i_matrix)
            i_matrix = d_switch_row(k_matrix, i_matrix)
            i_matrix = d_switch_column(k_matrix, i_matrix)
            i_matrix = xor_matrices(k_matrix, i_matrix)
            logging.debug('Matrix ' + str(i) + ', Round: ' + str(j) + ': ' + str(i_matrix))
        input_array[i] = i_matrix
    o_string = create_string(input_array, True)
    o_string = bytearray.fromhex(o_string)
    o_string = o_string.strip(b'\x00').decode()  # Strip padding off the string
    if verbose: print('String after decryption : ' + create_string(input_array, False))
    return o_string
