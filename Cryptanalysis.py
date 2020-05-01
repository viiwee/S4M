import _S4M
import csv

def gen_hex_dict():
    def gen_all_hex():
        i = 0
        while i < 16 ** 2:
            yield "{:02X}".format(i)
            i += 1
    hex_dict = {}
    for value in gen_all_hex():
        hex_dict[value] = 0
    #  for value in hex_dict:
        #  print(str(value) + ": " + str(hex_dict[value]))
    return hex_dict


def split_output(string):
    n = 2
    parsed_hex = [(string[i:i+n]).upper() for i in range(0, len(string), n)]
    return parsed_hex


def count_hex(hex_string, hex_dict):
    for value in hex_string:
        hex_dict[value] += 1


def cryptanalysis(n, diff_keys, diff_msg):
    try:
        with open('10-million-password-list-top-1000000.txt') as dictionary:
            hex_dict = gen_hex_dict()  # Generate a dictionary of all hex values so we can count the numbers of each
            counter = 0  # Set a counter so we only generate a specific number of strings
            for msg in dictionary:  # Select one line out of the dictionary
                if counter >= n:
                    break
                if diff_keys and diff_msg:
                    key = dictionary.__next__()  # Select the word right after the first one
                    # print("dKdM: key: " + key + " msg: " + msg)
                elif diff_keys and not diff_msg:
                    key = msg
                    msg = "doesnt change"
                    # print("dKsM: key: " + key + " msg: " + msg)
                elif not diff_keys and diff_msg:
                    key = "This is a simple key that does not change!"
                    # print("sKdM: key: " + key + " msg: " + msg)
                elif not diff_keys and not diff_msg:
                    key = "This is a simple key that does not change!"
                    msg = "msg"
                    # print("sKsM: key: " + key + " msg: " + msg)
                else:
                    print('Error')
                output = _S4M.encrypt_matrix(msg, key, False)  # Create an encrypted string from a password
                output = split_output(output)  # Parse into each hex value
                count_hex(output, hex_dict)
                counter += 1

    except StopIteration:
        print("End")  # do whatever you need to do with line1 alone
    return hex_dict


def write_to_csv(dictionary, csv_file):
    try:
        with open(csv_file, 'w') as csvfile:
            for key in dictionary.keys():
                csvfile.write("%s,%s\n" % (key, dictionary[key]))
    except IOError:
        print("I/O error")


num = 1000
#write_to_csv(cryptanalysis(num, True, True), "difK_difM.csv")
#write_to_csv(cryptanalysis(num, True, False), "difK_sameM.csv")
#write_to_csv(cryptanalysis(num, False, True), "sameK_difM.csv")
write_to_csv(cryptanalysis(num, False, False), "sameK_sameM.csv")

