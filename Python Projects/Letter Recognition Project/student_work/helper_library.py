"""This is the helper_library file, it defines two
functions meant to help you in writing Assessment 8.

PLEASE DO NOT EDIT THE CONTENTS OF THIS FILE
or your code will likely not work with the autograder.

You should not need to read through this file, but you
are free to if you wish. This code will give you a sneak-
preview of content we'll learn starting Week 10."""

def get_grids():
    """This function opens and parses the contents of
    letters.txt into a list of pixel grids, which are
    themselves nested lists of integers. That list is
    then returned.
    """
    with open("letters.dat") as f:
        lines = f.readlines()
        letter_grids = []
        current_letter_grid = []
        for i in range(len(lines)):
            if i % 6 == 0:
                continue
            line = list(lines[i].strip())
            # convert each item in the list to an int
            line = [int(x) for x in line]
            current_letter_grid.append(line)
            if i % 6 == 5:
                letter_grids.append(current_letter_grid)
                current_letter_grid = []
        return letter_grids


def get_letters():
    """This function opens and parses the content of
    letters.txt into a list of letter names, then returns
    that list."""
    with open("letters.dat") as f:
        lines = f.readlines()
        # get only the letter names with a slice
        letters = lines[::6]
        # make sure there is no extra whitespace on each letter
        letters = [letter.strip() for letter in letters]
        return letters


if __name__ == "__main__":
    print("""If you are seeing this, then you are trying to run helper_library directly. Instead of doing that, you should try to import helper_library in your own code file.""")
    grids = get_grids()
    print(grids)
    letters = get_letters()
    print(letters)
    # get the grid for 'H'
    print(grids[letters.index('H')])
