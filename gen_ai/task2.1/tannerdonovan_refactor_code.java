// Task 2.1: Code Refactoring
// C++ Program to Implement Rock-Paper-Scissors
#include <cstdlib>
#include <ctime>
#include <iostream>
using namespace std;

// Enum for moves
enum Move { ROCK, PAPER, SCISSORS };

// Initialize random seed once
void initRandom() {
    srand(time(NULL));
}

// Get a random move for the computer
Move getComputerMove() {
    return static_cast<Move>(rand() % 3);
}

// Convert char input to Move enum
Move charToMove(char c) {
    switch (c) {
        case 'r': return ROCK;
        case 'p': return PAPER;
        case 's': return SCISSORS;
        default: throw invalid_argument("Invalid move");
    }
}

// Determine game result: 0 = draw, 1 = win, -1 = loss
int getResult(Move playerMove, Move computerMove) {
    if (playerMove == computerMove) return 0; // Draw
    if ((playerMove == ROCK && computerMove == SCISSORS) ||
        (playerMove == SCISSORS && computerMove == PAPER) ||
        (playerMove == PAPER && computerMove == ROCK)) {
        return 1; // Win
    }
    return -1; // Loss
}

// Convert Move to char for display
char moveToChar(Move move) {
    switch (move) {
        case ROCK: return 'r';
        case PAPER: return 'p';
        case SCISSORS: return 's';
    }
    return '?'; // Should never happen
}

int main() {
    char playerInput;
    initRandom();

    cout << "\n\n\n\t\t\tWelcome to Rock-Paper-Scissors Game\n";
    cout << "\n\t\tEnter r for ROCK, p for PAPER, and s for SCISSORS\n\t\t\t\t\t";

    // Get valid player move
    while (true) {
        cin >> playerInput;
        if (playerInput == 'r' || playerInput == 'p' || playerInput == 's') {
            break;
        }
        cout << "\t\t\tInvalid Move! Please enter r, p, or s." << endl;
    }

    Move playerMove = charToMove(playerInput);
    Move computerMove = getComputerMove();
    int result = getResult(playerMove, computerMove);

    // Display results
    if (result == 0) {
        cout << "\n\t\t\tGame Draw!\n";
    } else if (result == 1) {
        cout << "\n\t\t\tCongratulations! You won!\n";
    } else {
        cout << "\n\t\t\tComputer wins! Better luck next time.\n";
    }

    cout << "\t\t\tYour Move: " << moveToChar(playerMove) << endl;
    cout << "\t\t\tComputer's Move: " << moveToChar(computerMove) << endl;

    return 0;
}
