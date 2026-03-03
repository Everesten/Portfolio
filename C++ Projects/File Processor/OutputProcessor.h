/* CSCI 200: A3
 *
 * Author: Genevieve (Varka) Carter, supported by ChatGPT
 *
 * This makes an output processor class that is used by other files
 */

#ifndef OUTPUTPROCESSOR_H
#define OUTPUTPROCESSOR_H

#include <fstream>
#include <string>
#include <vector>

using namespace std;

// Analyzes word/letter frequencies and writes formatted reports.
class OutputProcessor {
private:
    ofstream fileOut; // Output file stream
    vector<string> allWords; // Cleaned words (punctuation removed)
    vector<string> uniqueWords; // Unique words found
    vector<unsigned int> wordCounts; // Word frequency counts
    vector<unsigned int> letterCounts; // Letter frequency counts
    unsigned int totalLetterCount; // Total letters counted
    unsigned int totalWordCount; // Total words processed

public:
    OutputProcessor(); // Default constructor
    bool openStream(); // Prompt user, open file for writing
    void analyzeWords(vector<string> rawWords, string punctuation); // Analyze and count words/letters
    void write(); // Write formatted results
    void closeStream(); // Close output stream
};

#endif // OUTPUTPROCESSOR_H
