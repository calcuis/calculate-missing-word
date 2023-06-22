## findmissing
**Calculate the possible missing word**

This is an extension part of calculating the possible last word; it can be used to find any missing word in 12, 15, 18, 21 or 24-word seed phrase.

The code performs a series of operations on a user-provided seed phrase. It attempts to fill in a missing word in the seed phrase by generating all possible combinations and calculating their checksums.

**User Input**: The user is prompted to input a seed phrase, where the missing word is represented by a question mark (?). The input is converted to lowercase and stored in the variable `seed_phrase`.
```
seed_phrase = input("Please input your seed in words (separate by spaces) and leave ? as the missing word(s): ").lower()
```

**Splitting the Seed Phrase**: The `seed_phrase` is split into individual words using the `split(" ")` function, and the resulting list is stored back in `seed_phrase`.
```
seed_phrase = seed_phrase.split(" ")
```

**Possible seed phrase combination***: Check if 12, 15, 18, 21 or 24-word seed phrase combination as input or not
```
    if len(seed_phrase) not in [12, 15, 18, 21, 24]:
        print("Input seed phrase must be 12, 15, 18, 21, or 24 words. Please leave ? for missing word(s).")
        raise SystemExit(0)
```

**Reading Word List**: The code opens a file named "english.txt" (presumably containing a list of English words) and reads its contents. The words are then split into a list using the newline character ("\n") as the delimiter. The resulting word list is stored in the variable `word_list`. The file is subsequently closed.
```
english = open("english.txt")
word_list = english.read().split("\n")
english.close()
```

**Indexing the Seed Phrase**: Each word in seed_phrase is replaced with its corresponding index in the word_list. If the word is a question mark (?), it remains unchanged. The list comprehension `[word_list.index(word) if word != "?" else word for word in seed_phrase]` generates a new list called `seed_phrase_index`, which stores the indices or question marks.
```
seed_phrase_index = [word_list.index(word) if word != "?" else word for word in seed_phrase]
```

**Converting Indices to Binary**: The indices in `seed_phrase_index` are converted to binary representations. The binary numbers are formatted to have 11 bits using the `format` function. If the index is a question mark (?), it remains unchanged. The resulting list is stored in the variable `seed_phrase_binary`.
```
seed_phrase_binary = [format(number, "011b") if number != "?" else number for number in seed_phrase_index]
```

**Calculating the Number of Missing Bits**: The variable `num_missing_bits` is calculated based on the formula `int(11 - (1/3) * len(seed_phrase))`. It represents the number of bits required to represent the missing word.
```
num_missing_bits = int(11-(1/3)*(len(seed_phrase)))
```

**Generating Possible Word Bits**: All possible binary combinations with 11 bits are generated using the `range(2**11)` function. Each binary number is converted to a string, and if necessary, it is left-padded with zeros to ensure it has exactly 11 bits. The resulting list is stored in the variable `possible_word_bits`.
```
possible_word_bits = [bin(x)[2:].rjust(11, "0") for x in range(2**11)]
```

**Handling the Last Word**: If the last word in the seed_phrase is missing (indicated by "?"), the code proceeds to this block. It generates all possible combinations of missing bits (based on num_missing_bits) and stores them in the list `missing_bits_possible`. An empty string is assigned to checksum, and a new list called `entropy_less_missing_bits_possible is created`, containing all bits except the last word.
```
if seed_phrase_binary[-1] == "?": #if the last word is missing, do this
    missing_bits_possible = [bin(x)[2:].rjust(num_missing_bits, "0") for x in range(2**num_missing_bits)]
    checksum = ""
    entropy_less_missing_bits_possible =  ["".join(seed_phrase_binary[:-1])]
```

**Handling Non-Last Word**: If the last word is not missing, the code executes this block. It assigns the first num_missing_bits bits of the last word to `missing_bits_possible`, and the remaining bits are assigned to checksum. The `entropy_less_missing_bits_possible` list is created similarly as in the previous case.
```
else: #if the last word is not missing, do this
    missing_bits_possible = [seed_phrase_binary[-1][0:num_missing_bits]]
    checksum = seed_phrase_binary[-1][-(11-num_missing_bits):]
    entropy_less_missing_bits_possible = ["".join(word if word != "?" else word_bit for word in seed_phrase_binary[:-1]) for word_bit in possible_word_bits]
```

**Generating Entropy Possibilities**: The code combines each missing bit combination with each entropy combination (except the missing bits) to form all possible entropy combinations. The resulting list is stored in the variable `entropy_possible`.
```
entropy_possible = [bit_combination + missing_bits for missing_bits in missing_bits_possible for bit_combination in entropy_less_missing_bits_possible]
```

**Importing hashlib**: The `hashlib` module is imported to calculate the checksums of the entropy combinations.
```
import hashlib
```

**Calculating Checksums**: The code iterates over each entropy combination in `entropy_possible`. It calculates the checksum for each entropy combination using the SHA-256 hash algorithm from `hashlib`. The checksum is obtained by converting the hashed value to binary and taking the first 11 bits. The calculated checksum is stored in the variable `calc_checksum`. The entropy combination is appended with `calc_checksum` to form `entropy + calc_checksum`.

**Filtering Possible Binary Combinations**: The list comprehension `[entropy + calc_checksum for entropy in entropy_possible if checksum == (calc_checksum := format(hashlib.sha256(int(entropy, 2).to_bytes(len(entropy) // 8, byteorder="big")).digest()[0],"08b")[:11-num_missing_bits]) or checksum == ""]` filters the entropy_possible list. It checks if the calculated checksum matches the provided checksum or if there is no provided checksum. Only the valid combinations are stored in the `seed_phrase_binary_possible` list.
```
seed_phrase_binary_possible = [entropy + calc_checksum for entropy in entropy_possible if checksum == (calc_checksum := format(hashlib.sha256(int(entropy, 2).to_bytes(len(entropy) // 8, byteorder="big")).digest()[0],"08b")[:11-num_missing_bits]) or checksum == ""]
```

**Converting Binary Combinations to Words**: For each binary combination in `seed_phrase_binary_possible`, the code extracts 11-bit segments and converts them to their corresponding word indices using the `word_list`. The resulting words are joined together with spaces using a generator expression. The resulting generator object is stored in `seed_phrase_word_possible`.
```
seed_phrase_word_possible = (" ".join([word_list[int(binary[i:i+11],2)] for i in range(0, len(binary), 11)]) for binary in seed_phrase_binary_possible)
````

**Printing Possible Word Combinations**: The `seed_phrase_word_possibl`e generator object is converted to a list, and the list of possible word combinations is printed using the print statement.
```
print(list(seed_phrase_word_possible))
```

In summary, the code takes a seed phrase with a missing word and attempts to find all possible words that could fill the missing slot by generating combinations, calculating their checksums, and checking them against the provided or empty checksum.
