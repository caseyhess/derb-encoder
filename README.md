# D.E.R.B. - Data Encoded to Randomized Base
This is a python app packaged as an executable that contains an encoder and decoder using the D.E.R.B. encryption method.

![GUI Preview](https://i.imgur.com/gTmx88N.png)

## Features
- Custom Encryption Method
- Encoding / Decoding Text Files
- Simple, Functional GUI (thanks tkinter)
- File Explorer
- Open Source!

## Setup
Download DERB.exe from the [latest release](https://github.com/caseyhess/D.E.R.B./releases) and run it!

If you would like to run the python file itself that is also available.

## Usage
Once you run DERB.exe you will be greeted by the GUI with a few different buttons to press.
- The entry box under `File to encode/decode:` is where your input text file path goes. You can paste a file path in or hit the `browse` button to the right to open the file explorer allowing you to select a file.
- The entry box under `Output Directory:` is where the output directory path goes. Same as above, hitting browse allows you to navigate to a directory of your choice and select it that way. You can also paste in the path if you'd prefer.
- The `Encode` button will run the encryption method on your input file and begin writing line by line the encoded text to a new file in the output directory named `<input file> - encoded.txt` where `<input file>` will be the name of your input file.
- The `Decode` button will do the same as above but instead of encoding the input file, it will decode it, writing to a new file in the output directory.
- The `Quit` button simply closes the application.
### NOTE: Currently D.E.R.B. only supports input .txt files and the characters inside need to be within the [ASCII 128](https://www.ascii-code.com/) character set. This will include all letters A-Z, numbers 0-9, and most common symbols. Click the link if you want to see the full list of characters in the ASCII 128 character set.

## License
#### Full license available [here](https://github.com/caseyhess/D.E.R.B./blob/main/LICENSE)
#### This project is licensed under the terms of the **MIT** license.
