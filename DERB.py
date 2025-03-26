### DOCUMENTATION ###

# D.E.R.B stands for Data Encoded to Randomized Base

### BASE CONVERTER ###

def dec_to_base(num, base):
    """
        Converts a decimal number 'num' to base 'base'.
        
        Contains a set of 66 characters from the ascii library for base conversion.
        
        'base' must be between 11 and 66 (inclusive).
    """
    
    # A set of 66 ascii characters for base conversion
    chr_set = [chr(i) for i in range(33, 99)]
    
    ## SANITY CHECKS ##
    
    # Sanity Check - checks that base is an integer or string.
    if not isinstance(base, (int, str)):
        raise Exception("base needs to be an integer or a string.")
    
    # Sanity Check - if base is a string checks if it contains only integers 0-9. If it passes converts base to an integer.
    if isinstance(base, str):
        if not base.isdigit():
            raise Exception("base can only contain integers 0-9. Any other characters are not allowed.")
        else:
            base = int(base)
    
    # Sanity Check - checks that base is between 11 and 66
    if base < 11 or base > 66:
        raise Exception("base must be between 11 and 66 (inclusive)")
    
    # Sanity Check - checks that num is an integer or string.
    if not isinstance(num, (int, str)):
        raise Exception("num needs to be an integer or a string.")
    
    # Sanity Check - if num is a string checks if it contains only integers 0-9. If it passes converts num to an integer.
    if isinstance(num, str):
        if not num.isdigit():
            raise Exception("num can only contain integers 0-9. Any other characters are not allowed.")
        else:
            num = int(num)
    
    
    
    ## MAIN PROGRAM ##
    
    # Returns the the 0th character in chr_set if num is 0
    if not num:
        return chr_set[0]
    
    new_num = '' # Initializes a string that will eventually be returned as the base converted number.
    
    while num:
        new_num = chr_set[num % base] + new_num
        num //= base
    return new_num



def base_to_dec(num, base):
    """
        Converts a number 'num' of base 'base' to a decimal (base 10) number.
        
        Contains a set of 66 characters from the ascii library for base conversion.
        
        'base' must be between 11 and 66 (inclusive).
    """
    
    # A set of 66 ascii characters for base conversion
    chr_set = [chr(i) for i in range(33, 99)]
    
    
    
    ## SANITY CHECKS ##
    
    # Sanity Check - checks that base is an integer or string.
    if not isinstance(base, (int, str)):
        raise Exception("base needs to be an integer or a string.")
    
    # Sanity Check - if base is a string checks if it contains only integers 0-9. If it passes converts base to an integer.
    if isinstance(base, str):
        if not base.isdigit():
            raise Exception("base can only contain integers 0-9. Any other characters are not allowed.")
        else:
            base = int(base)
    
    # Sanity Check - checks that base is between 11 and 66
    if base < 11 or base > 66:
        raise Exception("base must be between 11 and 66 (inclusive)")
    
    # Sanity Check - checks that num is a string.
    if not isinstance(num, str):
        raise Exception("num needs to be a string.")
    
    # Sanity Check - ensures all characters in num are within the chr_set
    for c in num:
        if c not in chr_set:
            raise Exception(f"The inputted number of base {base} contains characters that do not exist in chr_set.")
    
    
    
    ## MAIN PROGRAM ##
    
    new_num = 0 # Initializes an integer that will eventually be returned as the decimal converted number.
    base_pow = 0 # Number that the base will be to the power of for base conversion.
    
    # Iterates through the string num converting each character per loop to decimal (base 10)
    for c in reversed(num):
        new_num += chr_set.index(c) * base**base_pow
        base_pow += 1
    
    return str(new_num)



### ENCODER ###

def encoder(istring):
    """
        Iterates through an inputted string to encode each character and return it as an encoded string with the key and delimiters.
        
        X and Y represent the base key.
        
        The returned encoded string will be in the format Y<encoded string>X
        
        A list of delimiters will be included that will be picked from at random and placed between encoded characters for decoding.
    """
    
    ## SANITY CHECKS ##
    
    # Sanity Check - checks that istring is a string
    if not isinstance(istring, str):
        raise Exception("istring must be a string.")
    
    # Sanity Check - checks that all characters in istring are in the ascii library
    if not istring.isascii():
        raise Exception("istring must contain only characters from the ascii library.")
    
    ## MAIN PROGRAM ##
    
    import random as random
    
    # A list of 27 delimiters pulled from the ascii library that aren't included in the chr_set for base conversion.
    delims = [chr(i) for i in range(99, 126)]
    
    # Turns the inputted string into a list for easier iteration through list comprehension.
    temp_list = list(istring)
    
    # Converts each character to their ascii decimal code value
    temp_list = [str(ord(c)) for c in temp_list]
    
    # Ensures all items are of length 3, if not adds adequate number of 0's behind the item to make it length 3
    temp_list = [i if len(i) == 3 else '0'*(3-len(i)) + i for i in temp_list]
    
    # Shifts the string one position to the left. Ex: XYZ becomes YZX
    temp_list = [i[1:] + i[0] for i in temp_list]
    
    # Converts the ascii codes to binary
    temp_list = [bin(int(i))[2:] for i in temp_list]
    
    # Generates the base for randomized base conversion (I chose 33-66 because the initial 11-66 was not producing enough variability when rbase rolled a low number.)
    rbase = random.randrange(33, 66)
    
    # Converts each character to its randomized base equivalent
    temp_list = [dec_to_base(i, rbase) for i in temp_list]
    
    # This will be the final string with the delimiters
    new_str = ''
    
    # Iterates through temp_list adding each character to new_str with a delimiter after it.
    while len(temp_list) > 1:
        new_str += temp_list.pop(0) + delims[random.randrange(len(delims))]
    
    # Adds on the last item to new_str outside of the loop so that the encrypted text doesn't end in a delimiter
    new_str += temp_list.pop()
    
    # Separates rbase into two parts for the key
    xbase = str(rbase)[0]
    ybase = str(rbase)[1]
    
    # Returns the encoded text with the delimiters as well as xbase and ybase as the key in the format ybase<encoded_text>xbase
    return ybase + new_str + xbase



## DECODER ##

def decoder(istring):
    """
        Decodes an inputted string that has been encoded by the D.E.R.B. Cipher.
    """
    
    ## SANITY CHECKS ##
    
    # Sanity Check - checks that istring is a string
    if not isinstance(istring, str):
        raise Exception("istring must be a string.")
    
    # Sanity Check - checks that all characters in istring are in the ascii library
    if not istring.isascii():
        raise Exception("istring must contain only characters from the ascii library.")
    
    
    
    ## MAIN PROGRAM ##
    
    import re # Used to allow for multiple delimiters with re.split(delimiters, text)
    
    # A list of 27 delimiters pulled from the ascii library that aren't included in the chr_set for base conversion.
    delims = [chr(i) for i in range(99, 126)]
    
    # Gets the key for the randomized base conversion from the string
    rbase = int(istring[-1] + istring[0])
    
    # Copies istring to a new_str to work with
    new_str = istring[1:-1]
    
    # Converts new_str to a list without the delimiters
    temp_list = re.split(fr"[{''.join(delims)}]+", new_str)
    
    # Uses base conversion on each item of temp_list with rbase as the base
    temp_list = [base_to_dec(i, rbase) for i in temp_list]
    
    # Converts each item of temp_list from binary to decimal
    temp_list = [str(int('0b' + i, 2)) for i in temp_list]
    
    # Ensures all items are of length 3, if not adds adequate number of 0's behind the item to make it length 3
    temp_list = [i if len(i) == 3 else '0'*(3-len(i)) + i for i in temp_list]
    
    # Shifts the string one position to the right. Ex: XYZ becomes ZYX
    temp_list = [i[2] + i[:2] for i in temp_list]
    
    # Converts all numbers to their ascii character equivalent
    temp_list = [chr(int(i)) for i in temp_list]
    
    # Returns the decoded string
    return ''.join(temp_list)

text = input("Enter any text from the ascii library:\n")
encoded_text = encoder(text)
print(f"\nEncoded String: \n{encoded_text}\n")
print(f"Decoded String: \n{decoder(encoded_text)}")
