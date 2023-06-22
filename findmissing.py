#input seed phrase separated by spaces; i.e., "? survey coin divide biology album harbor fee profit nest claw mammal shaft basic diesel crater scatter modify bottom excuse hawk undo negative balance"
seed_phrase = input("Please input your seed in words (separate by spaces) and leave ? as the missing word(s): ").lower()

import itertools
import hashlib

def get_possible(seed_phrase):

    seed_phrase = seed_phrase.split(" ")

    #check if 12, 15, 18, 21 or 24-word seed phrase combination as input or not
    if len(seed_phrase) not in [12, 15, 18, 21, 24]:
        print("Input seed phrase must be 12, 15, 18, 21, or 24 words. Please leave ? for missing word(s).")
        raise SystemExit(0)
    
    english = open("english.txt")

    word_list = english.read().split("\n")

    english.close()

    seed_phrase_index = [word_list.index(word) if word != "?" else word for word in seed_phrase]

    seed_phrase_binary = [format(number, "011b") if number != "?" else number for number in seed_phrase_index]

    num_missing_bits = int(11-(1/3)*(len(seed_phrase)))

    possible_word_bits = (bin(x)[2:].rjust(11, "0") for x in range(2**11))

    if seed_phrase_binary[-1] != "?":
        missing_bits_possible = (seed_phrase_binary[-1][0:num_missing_bits],)
        checksum = seed_phrase_binary[-1][-(11-num_missing_bits):]
    else:
        missing_bits_possible = (bin(x)[2:].rjust(num_missing_bits, "0") for x in range(2**num_missing_bits))
        checksum = ""

    possible_word_bits_combination = (combination for combination in itertools.product(possible_word_bits,repeat=seed_phrase[:-1].count("?")))

    partial_entropy = ("".join((combination.pop(0) if word == "?" else seed_phrase_local[index] for index,word in enumerate(seed_phrase_local))) if (seed_phrase_local := seed_phrase_binary[:-1]) and (combination := list(word_bits_combination)) else "".join(seed_phrase_local) for word_bits_combination in possible_word_bits_combination)

    entropy_possible = tuple(bit_combination + missing_bits for missing_bits in missing_bits_possible for bit_combination in partial_entropy )

    seed_phrase_binary_possible = (entropy + calc_checksum for entropy in entropy_possible if checksum == (calc_checksum := format(hashlib.sha256(int(entropy, 2).to_bytes(len(entropy) // 8, byteorder="big")).digest()[0],"08b")[:11-num_missing_bits]) or checksum == "")

    seed_phrase_possible = tuple(" ".join([word_list[int(binary[i:i+11],2)] for i in range(0, len(binary), 11)]) for binary in seed_phrase_binary_possible)
    
    return seed_phrase_possible

print(get_possible(seed_phrase))
