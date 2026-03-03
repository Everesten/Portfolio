class Prompt:
    
    # Initializes object, assigning the prompt's attributes

    def __init__(self, prompt, simple, openEnd, real, character):
        self.prompt = prompt
        self.simple = simple
        self.openEnd = openEnd
        self.real = real
        self.character = character

    # Allows final step to get the prompt

    def get_Prompt(self):
        return self.prompt
    
    # Allows the sorter function to sort by the type of preference

    def get_Type(self, typeP):
        if typeP == 'simpleP':
            return self.simple
        if typeP == 'openEndP':
            return self.openEnd
        if typeP == 'realP':
            return self.real
        if typeP == 'charP':
            return self.character

# Reads through the prompt file, with the attributes

with open('prompts.csv', 'r') as bigPromptList:

    fixedPromptList = []

    for line in bigPromptList.readlines():
        line = line.strip().split(',')

        # Looking at each item in the csv line, then assigning the item to the correct attribute value

        prompt = line[0]
        simple = line[1] 
        openEnd = line[2] 
        real = line[3] 
        character = line[4]

        # Makes an object out of the assigned variables above

        prompt = Prompt(prompt, simple, openEnd, real, character)
        fixedPromptList.append(prompt)

def sorter(typeP, Pref, fixedPromptList):        
    
    # Makes a list that'll only be affected inside a call to this function
    
    flexPromptList = []

    for prompt in fixedPromptList:

        # If the user answers "yes" then the program adds any prompts with the attribute as "TRUE" to the flex list
        if Pref == "Y":
            if prompt.get_Type(typeP) == 'TRUE':
                flexPromptList.append(prompt)

        # If the user answers "no" then the program adds any prompts with the attribute as "FALSE" to the flex list
        elif Pref == "N":
            if prompt.get_Type(typeP) == 'FALSE':
                flexPromptList.append(prompt)
    
    # Returns the newly adjusted flex list

    return flexPromptList

if __name__ == "__main__":

    # Asks the user about their preferences

    simplePref = input("Do you like simple prompts? Y/N")

    # Tells sorter to look at the simple preference attribute of the prompts, what the user answered, and the "fixed list" 
    # After the sorter function finishes, it reassigns the "fixed list" to the "flex list" returned by the function

    fixedPromptList = sorter('simpleP', simplePref, fixedPromptList)

    # Same as above comments

    openEndPref = input("Do you like open ended prompts? Y/N")

    fixedPromptList = sorter('openEndP', openEndPref, fixedPromptList)

    realPref = input("Do you like realistic prompts? Y/N")

    fixedPromptList = sorter('realP', realPref, fixedPromptList)

    charPref = input("Do you like character-focused prompts? Y/N")

    fixedPromptList = sorter('charP', charPref, fixedPromptList)

    # For each of the remaining prompts, it gets the "prompt" attribute and prints it

    for prompt in fixedPromptList:
        print(prompt.get_Prompt())