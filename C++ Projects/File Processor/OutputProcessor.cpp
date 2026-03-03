/* CSCI 200: A3
 *
 * Author: Genevieve (Varka) Carter, supported by ChatGPT
 *
 * This program creates an output file that anazlyes a text 
 * document and gets various statistics
 */

#include "OutputProcessor.h"
#include <iostream>
#include <iomanip>
#include <cctype>

using namespace std;

const int ALPHABET_SIZE = 26;

/**
 * Default constructor.
 * Initializes counters to zero.
 */

OutputProcessor::OutputProcessor()
    : totalLetterCount(0), totalWordCount(0) {}

// Prompts the user for an output filename and attempts to open it.

bool OutputProcessor::openStream() {
    string outputFileName;
    cout << "Enter output filename: ";

    if (!getline(cin, outputFileName) || outputFileName.empty()) {
        cerr << "No filename provided.\n";
        return false;
    }

    fileOut.open(outputFileName);
    if (!fileOut.is_open()) {
        cerr << "Could not open '" << outputFileName << "' for writing.\n";
        return false;
    }

    return true;
}

/**
 * Cleans and analyzes words read from the input file.
 * - Removes punctuation
 * - Converts to uppercase
 * - Counts word and letter frequencies
 * - Builds a list of unique words in order of first appearance
 */

void OutputProcessor::analyzeWords(vector<string> rawWords, string punctuation) {
    // Reset all stored data before analysis
    allWords.clear();
    uniqueWords.clear();
    wordCounts.clear();
    letterCounts.assign(static_cast<size_t>(ALPHABET_SIZE), 0);
    totalLetterCount = 0;
    totalWordCount = 0;

    // Process each word in the input
    for (size_t i = 0; i < rawWords.size(); ++i) {
        const string& currentWord = rawWords[i];
        string cleanedWord;
        cleanedWord.reserve(currentWord.size());

        // Remove punctuation and convert to uppercase
        for (size_t k = 0; k < currentWord.size(); ++k) {
            unsigned char character = static_cast<unsigned char>(currentWord[k]);
            bool isPunctuation = false;

            for (size_t p = 0; p < punctuation.size(); ++p) {
                if (punctuation[p] == character) {
                    isPunctuation = true;
                    break;
                }
            }
            if (isPunctuation) continue;

            if (isalpha(character))
                cleanedWord.push_back(static_cast<char>(toupper(character)));
            else
                cleanedWord.push_back(static_cast<char>(character));
        }

        allWords.push_back(cleanedWord);
        if (cleanedWord.empty()) continue;

        // Count letters (A–Z)
        for (char c : cleanedWord) {
            if (c >= 'A' && c <= 'Z') {
                letterCounts[static_cast<size_t>(c - 'A')]++;
                totalLetterCount++;
            }
        }

        // Check if this cleaned word has already been seen
        int foundIndex = -1;
        for (size_t u = 0; u < uniqueWords.size(); ++u) {
            if (uniqueWords[u] == cleanedWord) {
                foundIndex = static_cast<int>(u);
                break;
            }
        }

        // Add new unique word or increment its count
        if (foundIndex < 0) {
            uniqueWords.push_back(cleanedWord);
            wordCounts.push_back(1);
        } else {
            wordCounts[static_cast<size_t>(foundIndex)]++;
        }

        totalWordCount++;
    }
}

/**
 * Writes the formatted report to the output file:
 *  - Total words and unique words
 *  - Word frequency table
 *  - Most/least frequent words
 *  - Letter frequency table
 *  - Most/least frequent letters
 */

void OutputProcessor::write() {
    if (!fileOut.is_open()) {
        cerr << "Output file not open.\n";
        return;
    }

    //  Totals 
    fileOut << "Read in " << totalWordCount << " words\n";
    fileOut << "Encountered " << uniqueWords.size() << " unique words\n";

    if (totalWordCount == 0) {
        fileOut.flush();
        return;
    }

    //  Determine column widths 
    int columnWidthWord = 0;
    for (const string& word : uniqueWords) {
        if (static_cast<int>(word.size()) > columnWidthWord)
            columnWidthWord = static_cast<int>(word.size());
    }

    unsigned int maxWordCount = 0;
    for (unsigned int count : wordCounts) {
        if (count > maxWordCount)
            maxWordCount = count;
    }

    int columnWidthCount = 1;
    {
        unsigned int x = maxWordCount;
        int digits = 1;
        while (x >= 10) { x /= 10; ++digits; }
        if (digits > columnWidthCount) columnWidthCount = digits;
    }

    //  Word Frequency Table 
    for (size_t i = 0; i < uniqueWords.size(); ++i) {
        fileOut << left  << setw(columnWidthWord) << uniqueWords[i]
                << " : "
                << right << setw(columnWidthCount) << wordCounts[i]
                << '\n';
    }

    //  Identify Most and Least Frequent Words 
    int indexMostFrequent = -1;
    int indexLeastFrequent = -1;
    bool firstWord = true;
    unsigned int highestCount = 0;
    unsigned int lowestCount = 0;

    for (int i = 0; i < static_cast<int>(uniqueWords.size()); ++i) {
        unsigned int count = wordCounts[static_cast<size_t>(i)];
        if (count > highestCount) {
            highestCount = count;
            indexMostFrequent = i;
        }
        if (firstWord || count < lowestCount) {
            lowestCount = count;
            indexLeastFrequent = i;
            firstWord = false;
        }
    }

    //  Print Most/Least Frequent Words 
    if (indexMostFrequent >= 0 && indexLeastFrequent >= 0) {
        const string& mostWord  = uniqueWords[static_cast<size_t>(indexMostFrequent)];
        const string& leastWord = uniqueWords[static_cast<size_t>(indexLeastFrequent)];
        unsigned int mostCount  = wordCounts[static_cast<size_t>(indexMostFrequent)];
        unsigned int leastCount = wordCounts[static_cast<size_t>(indexLeastFrequent)];

        int columnWordWidth = static_cast<int>(mostWord.size());
        if (static_cast<int>(leastWord.size()) > columnWordWidth)
            columnWordWidth = static_cast<int>(leastWord.size());

        int columnCountWidth = 1;
        {
            unsigned int m = mostCount, l = leastCount;
            int dm = 1, dl = 1;
            while (m >= 10) { m /= 10; ++dm; }
            while (l >= 10) { l /= 10; ++dl; }
            columnCountWidth = (dm > dl) ? dm : dl;
        }

        fileOut << " Most Frequent Word: "
                << left  << setw(columnWordWidth)  << mostWord << ' '
                << right << setw(columnCountWidth) << mostCount << " ( "
                << fixed << setprecision(3)
                << (100.0 * double(mostCount) / double(totalWordCount)) << "%)\n";

        fileOut << " Least Frequent Word: "
                << left  << setw(columnWordWidth)  << leastWord << ' '
                << right << setw(columnCountWidth) << leastCount << " ( "
                << fixed << setprecision(3)
                << (100.0 * double(leastCount) / double(totalWordCount)) << "%)\n";
    }

    //  Letter Frequency Table 
    int totalColumnWidth = columnWidthWord + 3 + columnWidthCount; // " : " is 3 chars
    char oldFill = fileOut.fill();

    for (int i = 0; i < ALPHABET_SIZE; ++i) {
        char letter = static_cast<char>('A' + i);
        fileOut << left << letter;
        fileOut << setfill('.') << setw(totalColumnWidth - 1)
                << right << letterCounts[static_cast<size_t>(i)] << '\n';
        fileOut << setfill(oldFill);
    }

    //  Identify Most and Least Frequent Letters (alphabetical tie-break) 
    int indexMostLetter = 0;
    int indexLeastLetter = 0;

    for (int i = 1; i < ALPHABET_SIZE; ++i) {
        if (letterCounts[static_cast<size_t>(i)] >
            letterCounts[static_cast<size_t>(indexMostLetter)]) {
            indexMostLetter = i;
        }
        if (letterCounts[static_cast<size_t>(i)] <
            letterCounts[static_cast<size_t>(indexLeastLetter)]) {
            indexLeastLetter = i;
        }
    }

    fileOut << " Most Frequent Letter: "
            << static_cast<char>('A' + indexMostLetter) << ' '
            << right << setw(columnWidthCount)
            << letterCounts[static_cast<size_t>(indexMostLetter)]
            << " ( " << fixed << setprecision(3)
            << (100.0 * double(letterCounts[static_cast<size_t>(indexMostLetter)]) /
                double(totalWordCount)) << "%)\n";

    fileOut << " Least Frequent Letter: "
            << static_cast<char>('A' + indexLeastLetter) << ' '
            << right << setw(columnWidthCount)
            << letterCounts[static_cast<size_t>(indexLeastLetter)]
            << " ( " << fixed << setprecision(3)
            << (100.0 * double(letterCounts[static_cast<size_t>(indexLeastLetter)]) /
                double(totalWordCount)) << "%)\n";

    fileOut.flush();
}

// Closes the output file stream if it is currently open.

void OutputProcessor::closeStream() {
    if (fileOut.is_open()) {
        fileOut.close();
    }
}
