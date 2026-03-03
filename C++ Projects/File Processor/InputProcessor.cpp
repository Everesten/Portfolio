/* CSCI 200: A3
 *
 * Author: Genevieve (Varka) Carter, supported by ChatGPT
 *
 * This is an input processor for opening and looking through an inputted file
 */

#include "InputProcessor.h"
#include <iostream>
#include <string>

using namespace std;

InputProcessor::InputProcessor() = default;

// Prompts the user for an input filename and attempts to open it.

bool InputProcessor::openStream() {
    string inputFileName;
    cout << "Enter input filename: ";

    if (!getline(cin, inputFileName)) {
        cerr << "Failed to read filename.\n";
        return false;
    }

    if (inputFileName.empty()) {
        cerr << "No filename provided.\n";
        return false;
    }

    _fileIn.open(inputFileName);
    if (!_fileIn.is_open()) {
        cerr << "Could not open '" << inputFileName << "'.\n";
        return false;
    }

    return true;
}

/**
 * Reads every whitespace-separated word from the open file stream
 * and stores them in the _allWords vector.
 */

void InputProcessor::read() {
    _allWords.clear();
    string currentWord;

    while (_fileIn >> currentWord) {
        _allWords.push_back(currentWord);
    }
}

// Closes the input file stream if it is currently open.

void InputProcessor::closeStream() {
    if (_fileIn.is_open()) {
        _fileIn.close();
    }
}

// Returns a copy of the vector containing all words read from the input file.

vector<string> InputProcessor::getAllWords() const {
    return _allWords;
}
