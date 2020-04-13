import logging
import _S4M
import argparse

# Begin log
logging.basicConfig(filename='S4M-Main.log', level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Beginning of Program')


# Parse arguments
parser = argparse.ArgumentParser()
encrypt_decrypt_group = parser.add_mutually_exclusive_group()
encrypt_decrypt_group.add_argument('-e', '--encrypt', help='Encrypt an input string', type=str)
encrypt_decrypt_group.add_argument('-d', '--decrypt', help='Decrypt an input string', type=str)
parser.add_argument('-v', '--verbose', help='Display verbose output', action='store_true')
parser.add_argument('key', help='Key to be used for encryption/decryption', type=str)
args = parser.parse_args()


# Call encryption or decryption
if args.encrypt:
    print(_S4M.encrypt_matrix(args.encrypt, args.key, args.verbose))
elif args.decrypt:
    print(_S4M.decrypt_matrix(args.decrypt, args.key, args.verbose))

exit()
