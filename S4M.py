import sys
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import logging
import _S4M
import random

# Begin log
logging.basicConfig(filename='S4M-Main.log', level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Beginning of Program')

# Set Constants
matrix_width = 4
matrix_height = 4
matrix_salt_length = 2  # Bytes
matrix_str_length = matrix_width * matrix_height * 2 - (matrix_salt_length * 2)  # Will give i for the length of the user
# input, in steps of the number of hex characters in each matrix. The number of hex characters per matrix will be
# 2*height*width - 4. The -4 takes care of the two salt bytes.
# There are two digits for each hex character. Ex: 00 is the value for NULL

# Create fake inputs
usr_input = 'matthew fisher is a purdue student studying cybersecurity'.encode()
key = 'cnit370'.encode()

# Convert usr_input to hex
usr_input = usr_input.hex()

# Create the 16 byte key
key = SHA256.new(key).digest()
hashkey = key.hex()[:32]
logging.debug('Hex key: ' + hashkey)

# Create the key matrix
k_matrix = _S4M.create_matrix(hashkey, matrix_width, matrix_height)
logging.debug('Key Matrix: ' + str(k_matrix))

# Split input into an array
input_array = []
for i in range(0, len(usr_input), matrix_str_length):

    # Create the string that this matrix will contain
    input_append = usr_input[i:i + matrix_str_length]

    # Add padding
    if len(input_append) < matrix_str_length:
        diff = (matrix_str_length - len(input_append)) // 2  # Dividing by 2 so that append can append a whole hex char
        input_append += '00' * diff  # Append 00 as padding

    # Add Salt
    for j in range(0, matrix_salt_length*2):
        input_append += random.choice('0123456789abcdef')
    logging.debug('Created salt: ' + input_append[28:32])  # 28:32 so that it selects the last 2 bytes

    # Convert the string to a matrix
    input_append = _S4M.create_matrix(input_append, matrix_width, matrix_height)

    # Append the matrix to the list of matrices
    input_array.append(input_append)
logging.debug('input_array: ' + str(input_array))

# Print matrix before encryption
print(input_array)

# Send each matrix for encrypting
input_array = _S4M.encrypt_matrix(input_array, k_matrix)
print(input_array)

# Print matrix after decryption
print(_S4M.decrypt_matrix(input_array, k_matrix))




# For decoding
test_hex = '72736563757269747900000000000000'
test_string = bytearray.fromhex(test_hex)
stripped_test = test_string.strip(b'\x00')
print(str(stripped_test.decode()))

