# ChessGUIProject
This program was developed in Python (3.4) using the PySide package, a wrapper around the Qt framework.

This program allows a game of chess to be played between two people. 
The program is able to validate moves, determine the state of the game and supports all necessary moves in chess (promotion, en passant etc).

Please refer to the PDF found in the docs folder to find out more about this program and its development. The code is also heavily documented, and can also be used to find out more about the program.

Due to the fact that the program only has to calculate all valid moves of one piece, and asssess the game state after each move, focus was put on the algorithm's correctness, rather than speed.
To develop this further, this could be turned into a HCI-compliant project, with the ability to plug in other chess engines, or develop my own.
In addition, rewriting the move generation with a focus on speed, would require the use of concurrency and memory-saving data structures such as bitboards, a task which C++ is better suited for.

