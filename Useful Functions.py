# Partition a list into chunks of n size.
def partitionList(lst, n):
    """
    lst: List to be partitioned
    n: Size of each chunk
    """
    return [lst[i:i + n] for i in range(0, len(lst), n)]


# Implement the classic coding challenge 'FizzBuzz'.
def fizzBuzz(n):
    """
    n: The number up to which to play FizzBuzz
    """
    return ['FizzBuzz' if i % 15 == 0 else 'Fizz' if i % 3 == 0 else 'Buzz' if i % 5 == 0 else i for i in range(1, n+1)]


# Generate all permutations of a list.
from itertools import permutations
def permute(lst):
    """
    lst: List of elements to permute
    """
    return list(permutations(lst))

# Implement the 0/1 knapsack problem using dynamic programming.
def knapsack(weights, values, W):
    """
    weights: List of weights of the items
    values: List of values of the items
    W: Maximum weight
    """
    n = len(weights)
    K = [[0 for w in range(W+1)] for i in range(n+1)]
    for i in range(n+1):
        for w in range(W+1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif weights[i-1] <= w:
                K[i][w] = max(values[i-1] + K[i-1][w-weights[i-1]], K[i-1][w])
            else:
                K[i][w] = K[i-1][w]
    return K[n][W]


# Calculate the Levenshtein distance between two strings.
def levenshteinDistance(s1, s2):
    """
    s1: First string
    s2: Second string
    """
    if len(s1) < len(s2):
        return levenshteinDistance(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

# findSum(L, min, max) takes a list, L, itself
# containing lists or tuples of integers, and returns the first
# element of L whose elements add up to a number between min
# (inclusive) and max (exclusive). If no such sequence exists,
# findSum() returns False.
def findSum(L, min, max):
    for x in L:
        if sum(x) in range(min,max):
            return x
    return False

# extendListByMinMaxElements(L) takes a list, L, of
# nonnegative integers and modifies L by removing its smallest element
# and then adding that number of copies of the largest element of L to
# the end of L.
def extendListByMinMaxElements(L):
    L.extend([max(L)]*min(L))
    L.remove(min(L))

# smooshOdds(n) takes a nonnegative integer, n, and
# returns a new integer consisting only of the odd digits in n.
def smooshOdds(n):
     return int("".join([i for i in list(str(n)) if int(i)%2!=0]))

# tests words for vowels
def vPattern(S):
   return [i in ["a","e","i","o","u"] for i in S.lower()]

# checkPalindrome(string) checks if a string is a palindrome
def checkPalindrome(string):
    return string == string[::-1]

# rotateList(L, n) rotates a list, L, n places to the right
def rotateList(L, n):
    return L[-n:] + L[:-n]

# countLetters(word) returns a dictionary with the count of each letter in a string
def countLetters(word):
    return {letter: word.count(letter) for letter in set(word)}

# getDiagonal(matrix) returns the main diagonal of a matrix
def getDiagonal(matrix):
    return [matrix[i][i] for i in range(len(matrix))]

# flattenList(L) takes a list of lists and returns a flattened list
def flattenList(L):
    return [item for sublist in L for item in sublist]

# numToBinary(n) converts a decimal number to binary
def numToBinary(n):
    return bin(n).replace("0b", "")

# binaryToNum(b) converts a binary number to decimal
def binaryToNum(b):
    return int(b, 2)

# sumEvenDigits(n) returns the sum of even digits in a number
def sumEvenDigits(n):
    return sum(int(digit) for digit in str(n) if int(digit) % 2 == 0)

# capitalizeVowels(string) capitalizes all vowels in a string
def capitalizeVowels(string):
    return ''.join(c.upper() if c in 'aeiou' else c for c in string)

# mergeDicts(d1, d2) merges two dictionaries
def mergeDicts(d1, d2):
    return {**d1, **d2}

