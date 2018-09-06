"""
Student code for Word Wrangler game

The merge, merge_sort, and gen_all_strings functions should stand alone.
Actually running the program requires external modules.
"""

import urllib2
#import codeskulptor
#import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.
    """
    res = []
    for item in list1:
        if item not in res:
            res.append(item)
    return res

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    return [item for item in list1 if item in list2]

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.
    """
    index1 = 0
    index2 = 0
    res = []
    while len(res) < len(list1) + len(list2):
        if index1 >= len(list1):
            return res + list2[index2:]
        elif index2 >= len(list2):
            return res + list1[index1:]
        if list1[index1] <= list2[index2]:
            res.append(list1[index1])
            index1 += 1
        elif list2[index2] < list1[index1]:
            res.append(list2[index2])
            index2 += 1
    return res
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.
    """
    if len(list1) < 2:
        return list1
    return merge(merge_sort(list1[:int(len(list1)/2)]), merge_sort(list1[int(len(list1)/2):]))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return ['']
    res = []
    other_strings = gen_all_strings(word[1:])
    for string in other_strings:
        for index in range(len(string)+1):
            new_string = [string[:index], word[0], string[index:]]
            res.append(''.join(new_string))
    return res + other_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    dictfile = urllib2.urlopen('http://codeskulptor-assets.commondatastorage.googleapis.com/' + filename)
    return [line[:-1] for line in dictfile]

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

    