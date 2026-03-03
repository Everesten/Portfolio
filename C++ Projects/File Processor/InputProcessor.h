/* CSCI 200: A3
 *
 * Author: Genevieve (Varka) Carter, supported by ChatGPT
 *
 * This makes an input processor class that is used by other files
 */

#ifndef INPUTPROCESSOR_H
#define INPUTPROCESSOR_H

#include <fstream>
#include <string>
#include <vector>

using namespace std;

// Handles reading words from a user-specified input file.
class InputProcessor {
private:
    ifstream _fileIn; // Input file stream
    vector<string> _allWords; // All words read from the file

public:
    InputProcessor(); // Default constructor
    bool openStream(); // Prompt user, open file for reading
    void read(); // Read words into _allWords
    void closeStream(); // Close file stream if open
    vector<string> getAllWords() const; // Return all words read
};

#endif // INPUTPROCESSOR_H
