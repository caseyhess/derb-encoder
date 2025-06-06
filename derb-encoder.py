### DOCUMENTATION ###

# D.E.R.B. stands for Data Encoded to Randomized Base

#---------------------------------SEPARATOR---------------------------------#

### IMPORTS ###

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import os

#---------------------------------SEPARATOR---------------------------------#

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

#---------------------------------SEPARATOR---------------------------------#

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

def encode_to_file(ipath, opath):
    if not ipath and opath:
        error_popup('Missing input file')
    
    if not opath and ipath:
        error_popup('Missing output directory')
    
    if not opath and not ipath:
        error_popup('Missing input file\nand output directory')
    
    new_opath = opath + '/' + os.path.basename(ipath)[:-4] + ' - encoded.txt'
    with open(ipath, 'r') as fin:
        with open(new_opath, 'w') as fout:
            for line in fin:
                temp = line.rstrip()
                fout.write(encoder(temp) + '\n')
    
    error_popup('File has been encoded to \n' + new_opath)

#---------------------------------SEPARATOR---------------------------------#

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

def decode_to_file(ipath, opath):
    if not ipath and opath:
        error_popup('Missing input file')
    
    if not opath and ipath:
        error_popup('Missing output directory')
    
    if not opath and not ipath:
        error_popup('Missing input file\nand output directory')
        
    new_opath = opath + '/' + os.path.basename(ipath)[:-4] + ' - decoded.txt'
    with open(ipath, 'r') as fin:
        with open(new_opath, 'w') as fout:
            for line in fin:
                temp = line.rstrip()
                fout.write(decoder(temp) + '\n')
    
    error_popup('File has been decoded to \n' + new_opath)

#---------------------------------SEPARATOR---------------------------------#

## TKINTER GUI FUNCTIONS

def get_file_path(istring):
    """
        Opens a file explorer window setting the given string to the chosen file path.
    """
    
    file_path = filedialog.askopenfilename()
    
    # Sanity check to make sure opened file is a .txt
    if file_path[-1:-4:-1] != 'txt':
        error_popup('Chosen file is not a text file ending in .txt\nplease choose a different file.')
    
    elif file_path:
        istring.set(file_path)

def get_dir_path(istring):
    """
        Opens a file explorer window setting the given string to the chosen directory path.
    """
    
    dir_path = filedialog.askdirectory()
    
    if dir_path:
        istring.set(dir_path)


def error_popup(error_txt):
    """
        Displays an error popup with a related title and text telling the user what went wrong
    """
    
    popup = tk.Toplevel()
    popup.title("Error Window")
    tk.Label(popup, text=error_txt).pack(padx=20, pady=5)
    tk.Button(popup, text="Okay", command=popup.destroy).pack(pady=5)
    popup.grab_set()

#---------------------------------SEPARATOR---------------------------------#

## MAIN FUNCTION ##

def main():
    """
        Creates a gui for the user to input a file through text or windows explorer
        and choose an output file where the new encoded / decoded text file will be created.
    """
    
    root = tk.Tk() #create an instance of the root window
    root.title("D.E.R.B.") # Sets the window's title
    root.geometry('300x200') # Sets window size
    
    # Main Frame - Contains all frames
    main_frame = ttk.Frame(root, padding=10)
    main_frame.pack(expand=True)
    
    # Top Frame - File Paths
    top_frame = ttk.Frame(main_frame)
    top_frame.grid()
    
    # Creates the widgets that open the file needing to be encoded / decoded
    ttk.Label(top_frame, text="File to encode/decode:").grid(column=0, row=0, sticky='w')
    start_file_str = tk.StringVar()
    ttk.Entry(top_frame, textvariable=start_file_str).grid(column=0, row=1)
    ttk.Button(top_frame, text="Browse", command=lambda: get_file_path(start_file_str)).grid(column=2, row=1)
    
    # Creates the widgets that set the directory for the output file
    ttk.Label(top_frame, text="Output Directory:").grid(column=0, row=2, sticky='w')
    end_file_str = tk.StringVar()
    ttk.Entry(top_frame, textvariable=end_file_str).grid(column=0, row=3)
    ttk.Button(top_frame, text="Browse", command=lambda: get_dir_path(end_file_str)).grid(column=2, row=3)
    
    # Bottom Frame - Encode, Decode, Quit Buttons
    bottom_frame = ttk.Frame(main_frame, padding=15)
    bottom_frame.grid()
    
    # Creates the encode and decode buttons
    ttk.Button(bottom_frame, text="Encode", command=lambda: encode_to_file(start_file_str.get(), end_file_str.get())).grid(column=0, row=0)
    ttk.Button(bottom_frame, text="Decode", command=lambda: decode_to_file(start_file_str.get(), end_file_str.get())).grid(column=1, row=0)
    
    # Creates a quit button that closes the program
    ttk.Button(bottom_frame, text="Quit", command=root.destroy).grid(column=2, row=0)
    
    root.mainloop()
    

def test():
    root = tk.Tk()
    root.geometry('300x200')
    root.title('Separator Widget Demo')

    # top frame
    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
    ttk.Label(top_frame, text="Top frame").pack(pady=20)

    # create a horizontal separator
    separator = ttk.Separator(root, orient=tk.HORIZONTAL)
    separator.pack(side=tk.TOP, fill=tk.X, pady=5)

    # bottom frame
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    ttk.Label(bottom_frame, text="Bottom frame").pack(pady=20)

    root.mainloop()

#---------------------------------SEPARATOR---------------------------------#

main()