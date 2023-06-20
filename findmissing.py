#input seed phrase separated by spaces; i.e., "? survey coin divide biology album harbor fee profit nest claw mammal shaft basic diesel crater scatter modify bottom excuse hawk undo negative balance"
seed_phrase = input("Please input your 23 words (separate by spaces) and leave ? as the missing word: ").lower()

seed_phrase = seed_phrase.split(" ")

english = open("english.txt")

word_list = english.read().split("\n")

english.close()

seed_phrase_index = [word_list.index(word) if word != "?" else word for word in seed_phrase]

seed_phrase_binary = [format(number, "011b") if number != "?" else number for number in seed_phrase_index]

num_missing_bits = int(11-(1/3)*(len(seed_phrase)))

possible_word_bits = [bin(x)[2:].rjust(11, "0") for x in range(2**11)]

#check if there is a last word and saves information in variables depending on if there is a last word or not
if seed_phrase_binary[-1] == "?": #if the last word is missing, do this
    
    missing_bits_possible = [bin(x)[2:].rjust(num_missing_bits, "0") for x in range(2**num_missing_bits)]

    checksum = ""

    entropy_less_missing_bits_possible =  ["".join(seed_phrase_binary[:-1])]

else: #if the last word is not missing, do this

    missing_bits_possible = [seed_phrase_binary[-1][0:num_missing_bits]]
    
    checksum = seed_phrase_binary[-1][-(11-num_missing_bits):]

    entropy_less_missing_bits_possible = ["".join(word if word != "?" else word_bit for word in seed_phrase_binary[:-1]) for word_bit in possible_word_bits]

entropy_possible = [bit_combination + missing_bits for missing_bits in missing_bits_possible for bit_combination in entropy_less_missing_bits_possible]

#refer to SHA256 library for checksum
import hashlib

seed_phrase_binary_possible = [entropy + calc_checksum for entropy in entropy_possible if checksum == (calc_checksum := format(hashlib.sha256(int(entropy, 2).to_bytes(len(entropy) // 8, byteorder="big")).digest()[0],"08b")[:11-num_missing_bits]) or checksum == ""]

#output as possible seed phrases according to BIP39 wordlist
seed_phrase_word_possible = (" ".join([word_list[int(binary[i:i+11],2)] for i in range(0, len(binary), 11)]) for binary in seed_phrase_binary_possible)

print(list(seed_phrase_word_possible))