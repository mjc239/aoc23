NUMBERS = {'one': 1,
           'two': 2,
           'three': 3,
           'four': 4,
           'five': 5,
           'six': 6,
           'seven': 7,
           'eight': 8,
           'nine': 9}


def first_digit_in_word(word):
    for c in word:
        if c.isdigit():
            return c


def last_digit_in_word(word):
    for i in range(len(word)):
        c = word[-i - 1]
        if c.isdigit():
            return c


def first_number_in_word(word):
    for i in range(len(word)):
        # If next character is a digit, return it
        if word[i].isdigit():
            return int(word[i])
        else:
            # Check for number words ending here
            # All numbers have 3, 4, or 5 characters
            for j in [5, 4, 3]:
                # Find subword ending with this character
                start = max(0, i - j + 1)
                subword = word[start:i + 1]

                if subword in NUMBERS:
                    return NUMBERS[subword]

    raise (ValueError('No number found in word!'))


def last_number_in_word(word):
    for i in range(len(word)):
        pos = -i - 1
        # If next character is a digit, return it
        if word[pos].isdigit():
            return int(word[pos])
        else:
            # Check for number words starting here
            # All numbers have 3, 4, or 5 characters
            for j in [5, 4, 3]:
                # Find subword starting with this character
                end = pos + j if pos + j < 0 else None
                subword = word[pos:end]

                if subword in NUMBERS:
                    return NUMBERS[subword]

    raise (ValueError('No number found in word!'))
