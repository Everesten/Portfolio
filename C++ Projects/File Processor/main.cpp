/* CSCI 200: A3
 *
 * Author: Genevieve (Varka) Carter, supported by ChatGPT
 *
 * This program reads through an inputted files, analyzes it,
 * then outputs a file with the analysis.
 */

#include "InputProcessor.h"
#include "OutputProcessor.h"

#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main() {
    // Named constants (avoid magic strings and numbers)
    const string PUNCTUATION = "?!.,;:\"()_-'&[]";
    const int INPUT_OPEN_FAIL  = 1;
    const int OUTPUT_OPEN_FAIL = 2;

    // Create and open the input processor
    InputProcessor inputProcessor;
    if (!inputProcessor.openStream()) {
        cerr << "Shutting down...\n";
        return INPUT_OPEN_FAIL;
    }

    // Read words, then close input
    inputProcessor.read();
    inputProcessor.closeStream();

    // Retrieve all words
    vector<string> inputWords = inputProcessor.getAllWords();

    // Analyze and write results
    OutputProcessor outputProcessor;
    outputProcessor.analyzeWords(inputWords, PUNCTUATION);

    // Open output file
    if (!outputProcessor.openStream()) {
        cerr << "Shutting down...\n";
        return OUTPUT_OPEN_FAIL;
    }

    // Write results and close
    outputProcessor.write();
    outputProcessor.closeStream();

    cout << "Analysis complete, check file for results\n";
    return 0; // Success
}
