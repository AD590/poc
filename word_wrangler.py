
#Mini Project__Week 5

#http://www.codeskulptor.org/#user36_SqbFYKV8qtddGUf.py

"""
Student code for Word Wrangler game
"""
import random
import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"

# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    if len(list1) == 0:
        return []
    new_list = [list1[0]]
    for item in list1:
        if item != new_list[-1]:
            new_list.append(item)
    return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    intersect_list = []
    for item in list1:
        if item in list2:
            intersect_list.append(item)
    return intersect_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    list1 = list(list1)
    list2 = list(list2)
    new_list = []
    while len(list1) != 0 and len(list2) != 0:
        if list1[0] < list2[0]:
            new_list.append(list1.pop(0))
        else :
            new_list.append(list2.pop(0))
    new_list.extend(list1)
    new_list.extend(list2)
    return new_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    middle = len(list1)/2
    return merge(merge_sort(list1[:middle]), merge_sort(list1[middle:]))

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
    rest_strings = gen_all_strings(word[1:])
    new_strings = []
    for item in rest_strings:
        for index in range(len(item) + 1):
            tmp = list(item)
            tmp.insert(index,word[0])
            new_strings.append(''.join(tmp))
    
    return rest_strings + new_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    #url = codeskulptor.file2url(WORDFILE)
    #dic_file = urllib2.urlopen(url)
    dic_file = urllib2.urlopen('https://codeskulptor-assets.commondatastorage.googleapis.com/assets_scrabble_words3.txt')
    dic_list = []
    for line in dic_file.readlines():
        dic_list.append(line[:-1])
    return dic_list

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
#run()


print merge_sort([])

