#include <cstdlib>
#include <ctime>
#include <iostream>
using namespace std;

// Enum representing possible moves in the game
enum Move { ROCK, PAPER, SCISSORS };

// Seeds the random number generator with the current time
// to ensure different outcomes on each run
void initRandom() {
    srand(time(NULL));
}

// Generates a random move for the computer (ROCK, PAPER, or SCISSORS)
Move getComputerMove() {
    return static_cast<Move>(rand() % 3);
}

// Converts user input character ('r', 'p', 's') to a Move enum
// Throws an exception if the input is invalid
Move charToMove(char c) {
    switch (c) {
        case 'r': return ROCK;
        case 'p': return PAPER;
        case 's': return SCISSORS;
        default: throw invalid_argument("Invalid move");
    }
}

// Determines the result of the game
// Returns 0 for a draw, 1 if the player wins, and -1 if the computer wins
int getResult(Move playerMove, Move computerMove) {
    if (playerMove == computerMove) return 0; // Draw
    if ((playerMove == ROCK && computerMove == SCISSORS) ||
        (playerMove == SCISSORS && computerMove == PAPER) ||
        (playerMove == PAPER && computerMove == ROCK)) {
        return 1; // Player wins
    }
    return -1; // Computer wins
}

// Converts a Move enum to its corresponding character ('r', 'p', 's')
char moveToChar(Move move) {
    return "rps"[move];  // Simplified to directly return 'r', 'p', or 's'
}

int main() {
    char playerInput; // Holds the player's move input
    initRandom(); // Seed random number generator

    // Display game instructions
    cout << "\n\n\n\t\t\tWelcome to Rock-Paper-Scissors Game\n";
    cout << "\n\t\tEnter r for ROCK, p for PAPER, and s for SCISSORS\n\t\t\t\t\t";

    // Prompt user for a valid move
    while (true) {
        cin >> playerInput;
        if (playerInput == 'r' || playerInput == 'p' || playerInput == 's') {
            break;
        }
        cout << "\t\t\tInvalid Move! Please enter r, p, or s." << endl;
    }

    // Determine moves and result
    Move playerMove = charToMove(playerInput);
    Move computerMove = getComputerMove();
    int result = getResult(playerMove, computerMove);

    // Display game result
    if (result == 0) {
        cout << "\n\t\t\tGame Draw!\n";
    } else if (result == 1) {
        cout << "\n\t\t\tCongratulations! You won!\n";
    } else {
        cout << "\n\t\t\tComputer wins! Better luck next time.\n";
    }

    // Show player and computer moves
    cout << "\t\t\tYour Move: " << moveToChar(playerMove) << endl;
    cout << "\t\t\tComputer's Move: " << moveToChar(computerMove) << endl;

    return 0;
}
