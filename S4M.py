import sys
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import logging
import _S4M
import random

# Begin log
logging.basicConfig(filename='S4M-Main.log', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
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
usr_input_plain = usr_input.decode()
key = 'cnit370'.encode()

# Convert usr_input to hex
usr_input = usr_input.hex()

initial_hex = usr_input

# Create the 16 byte key
key = SHA256.new(key).digest()
hashkey = key.hex()[:32]
logging.debug('Hex key: ' + hashkey)

# Create the key matrix
k_matrix = _S4M.create_matrix(hashkey, matrix_width, matrix_height)
logging.debug('Key Matrix: ' + str(k_matrix))

# Split input into an array
input_array = _S4M.create_matrix_array(usr_input, matrix_str_length, matrix_width, matrix_height, True)

# Print matrix before encryption
print('Input: ' + usr_input_plain)
print('Inital hex before encryp: ' + str(initial_hex))
print('Matrix before encryption: ' + str(input_array))

# Send each matrix for encrypting
encrypted_string = _S4M.encrypt_matrix(input_array, k_matrix)
print('String after encyption: ' + encrypted_string)

# Print matrix after decryption

print('Final output: ' + _S4M.decrypt_matrix(encrypted_string, k_matrix).decode('utf-8'))


