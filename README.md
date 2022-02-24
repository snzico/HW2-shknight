# while
While receives user input via standard input (stdin) and parses this input to an Abstract Syntax Tree (AST). The AST is then interpreted using Big Step semantics, and a value is returned to standard out (stdout) in the format:

Single statement:
{identifier → value}

Multiple Statement Solution:
{identifier1 → value1, identifier2 → value2}

Requirements:
- Installation of Python3
- pyinstaller (if running the Makefile - if using provided executable, pyinstaller has already been run)
  $ pip install pyinstaller

To create executable:
1. Open an instance of Terminal
2. Change the directory to hw2-shknight (location of while.py):
  $ cd "[ENTER BASE DIRECTORY]/hw2-shknight"
3. Create executable of while.py:
  $ make -f Makefile

To run while:
1. Open an instance of Terminal
2. Change the directory to hw2-shknight (if not already set):
  $ cd "[ENTER BASE DIRECTORY]/hw2-shknight"
3. Run the program with Python:
  $ while
4. Enter the statement you would like parsed and interpreted
