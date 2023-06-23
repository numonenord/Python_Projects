from random import choice

"""WORLDE GAME"""

# readWords(filename) takes a single value, a string,
# the name of a file that contains a list of 5-letter words (one per
# line) consisting of the university of 5-letter words for the Wordle
# puzzle. It returns a list of words.
def readWords(filename='words.dat'):
    infile = open(filename, "r")
    S = infile.read().split()
    return S
    
# evalGuess(guess, target) takes two equal-length
# lower-case strings representing the user's latest guess and the
# hidden target word, respectively. It returns a feedback string that is
# equal in length to both word and target, consisting of either upper
# or lower case characters from word or the '.' character.
def evalGuess(guess, target):
    L = []
    S = []
    count = 0
    for i in guess:
        if i == target[count]:
            L.append(i.upper())
            S.append(i.lower())
        elif i in target and S.count(i) < target.count(i):
            L.append(i.lower())
        else:
            L.append(".")
        count += 1
    return "".join(L)

# wordle(S) takes a list of words, S, and randomly
# selects a target word for this round from S. It then manages game
# play, and returns True (meaning the user would like to play another
# round) or False (meaning that the user does not wish to play another
# round).
def wordle(S):
    target=choice(S)       	# Target word to guess
    feedback = '.'*5			# Initial feedback is empty
    history = ""			# String history of word + feedback
    n = 6				# Remaining guesses

    # Print opening banner
    print('Welcome to Wordle!')
    print('Enter your guess, or ? for history; + for new game; or . to exit')

    # Repeat while guesses remain (or user quits with '+' or '.'
    # input). The general idea of this main game loop is to prompt the
    # user for a guess, then process the guess accordingly.
    while n > 0: 
        # Uncomment the following line to enable "cheat mode." Cheat
        # mode reveals the hidden target word
        #
        #print("Cheat: {}".format(target))  # Cheat mode!

        # Prompt the user for a guess. 
        #
        guess = input("\nWordle[{}]: '{}' >  ".format(7-n, feedback))

        # The next conditional statement breaks down game management
        # into an appropriately ordered series of outcomes.
        #
        if guess in '.+': 
            # Abort game Here
            return guess == "+"

        elif guess=='?':
            # Print out the guess history.
            print("History: " + history)

        elif guess not in S:
            # User's guess is not in S: this is an illegal
            # guess.
            print("Unrecognized word: " + str(guess))

        elif str((set(guess)^set(target))&set(target).intersection(feedback.lower())) != "set()":
            # The user's guess does not make use of all the letters
            # that are already known to be in the target word.
            print("Guess must contain " + str((set(guess)^set(target))&set(target).intersection(feedback.lower())))
                
        else:

            # Detect whether the guess matches the target word,
            # and if so, print an appropriate remark and exit
            # the function with the appropriate Boolean value.
            history = list(history)
            history.append("\n " + str(7-n) + ": " + guess + " => " + feedback)
            feedback = evalGuess(guess,target)
            history = "".join(history)
            n = n-1
            if target == guess:
                print("Good job, that is correct!")
                return True

    # The user has run out of
    # guesses. Assume they want to play another game, and return the
    # appropriate Boolean value.
    print("Sorry, no dice...\n{}".format(history))
    return True

if __name__ == '__main__':
    # Read in the list of legal 5-letter words and then continue
    # playing the game until wordle() returns False.
    while wordle(S=readWords('words.dat')):
        print("Let's play again!\n")
