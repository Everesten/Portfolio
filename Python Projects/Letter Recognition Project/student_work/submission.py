import helper_library

def get_input_grids():
    i = 0
    all_grids = []
    while i < 5:
        row = input()
        if row == "DONE":
            return -1
        row = row.split(" ")
        i += 1
        all_grids.append(row)
    
    
    return all_grids

def split_input_grids(input_grids):
    letters = []
    column_offset = 0

    for i, row in enumerate(input_grids):
        for item in row:
            if item != "1" and item != "0":
                return -1
        input_grids[i] = [int(x) for x in row]

    for row_offset in range(len(input_grids)//5):
        while column_offset < len(input_grids[0]):
            letter = []
            for r in range(row_offset, row_offset+5):
                letter.append(input_grids[r][column_offset:column_offset + 5])
            letters.append(letter)
            column_offset += 6
    return letters

def compute_scores(templates, letter_grid):
    scores = []
    for letter_template in templates:
        correct = 0
        i = 0
        for line_template in letter_template:
            x = 0
            for pixel_template in line_template:
                if letter_grid[i][x] == pixel_template: 
                    correct += 1
                x += 1
            i += 1

        scores.append(correct)
    
    return scores

def extract_letter(letters, computed_scores):
    highest_val = 0
    for item in computed_scores:
        if item > highest_val:
            highest_val = item
    
    return letters[computed_scores.index(highest_val)]

if __name__ == "__main__":
    templates = helper_library.get_grids()
    letters = helper_library.get_letters()
    word = ""

    input_grids = get_input_grids()
    if input_grids == -1:
        print("OUTPUT ERROR: Invalid grid entered")
    else:
        split_grids = split_input_grids(input_grids)
        if split_grids == -1:
            print("OUTPUT ERROR: Invalid pixel value encountered")
        else:
            letter_count = len(split_grids)
            for grid in split_grids:
                score_list = compute_scores(templates, grid)
                letter = extract_letter(letters, score_list)
                word += str(letter)
            print(f"OUTPUT {letter_count} Letters entered")
            print("OUTPUT", word)