""" This is a script that provides a number of functions to calculate
    the shortest path between two words.
"""

import argparse
import os
import sys
import time
from collections import deque


DICTIONARY = 'british-english'
WORDS_LIST = []


def create_words_list(length):
    """ Creates a list of valid words, out of the dictionary file.
        Transforms to lowercase and trims "'s".
        Also filters words by length

        Args:
                length: The length of the words we are looking for
    """
    with open(DICTIONARY, 'r') as dictionary:
        for line in dictionary:
            # Ignore words that contain "'s\n"
            if not line.endswith("'s\n"):
                # To lower case
                to_lower = line.strip('\n').lower()
                if len(to_lower) == length:
                    # Write to TRIMMED_DICTIONARY
                    WORDS_LIST.append(to_lower)

def get_args():
    """ Get the command line arguments. """

    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Release commands generator')

    parser.add_argument('-d', '--dictionary',
        dest='dictionary',
        help='The path to the dictionary file')

    parser.add_argument('-s', '--source',
        dest='source',
        help='The source word')

    parser.add_argument('-t', '--target',
        dest='target',
        help='The target word')

    args = parser.parse_args()

    return args


class Shortbread():
    """ Provides a number of functions to calculate the
        the shortest path between two words.
    """

    def __init__(self, source):
        """ Constructor. Initialises the queue and the pool that
            will store the visited nodes.

            Args:
                    source: A dictionary where:
                            a. The key is a word
                            b. The value is a list of words indicating a path
        """
        self.my_queue = deque([source])

        word = next(iter(source))
        self.visited_pool = [word]

    def hamming_dist(self, s1, s2):
        """ Calculates the Hamming distance between two words

            Args:
                    word1: The first word
                    word2: The second word

            Returns:
                    dist: The hamming distance between source and target
        """
        return sum(c1 != c2 for c1, c2 in zip(s1, s2))

    def visited(self, word):
        """ Works out whether we have already encountered a word during
            the search, by looking at the pool

            Args:
                    word: The word we are trying to validate

            Returns:
                    True if the word is already been visited. False otherwise
        """
        return word in self.visited_pool

    def search_nodes(self, source, target):
        """ Uses breadth first algorithm to work out the shortest
            path from one word to another.

            Args:
                    source: The word we want to transform
                    target: The word we want to transofm source to
        """
        # print "Number of words to be processed: {}".format(len(WORDS_LIST))

        # As long as the queue has elements keep looking
        while len(self.my_queue) > 0:
            
            # Remove the first item from the queue
            first = self.my_queue.popleft()

            # Items are dictionaries where:
            #   a. The key is a word
            #   b. The value is a list of words indicating the path we
            #      followed to reach this specific word.
            for key, values in first.items():
                word = key
                path = values

            for candidate in WORDS_LIST:
                if self.hamming_dist(word, candidate) == 1 and not self.visited(candidate):
                    
                    # Add the new word to the pool of visited nodes
                    if candidate not in self.visited_pool:
                        self.visited_pool.append(candidate)

                    # Create a new queue item and add it to the queue
                    new_path = path[:]
                    new_path.append(candidate)
                    new_word = {candidate: new_path}
                    self.my_queue.append(new_word)

                    # Quit immediately if the target word is found
                    if candidate == target:
                        print('Found path', new_word)
                        return


def run(source, target):
    """ Controler function.
        Instantiates a Shortbread objects and executes the algo.
    """
    start = time.time()

    length = len(target)

    # Initial setup
    create_words_list(length)

    # Start the algorithm
    shr = Shortbread(source)

    shr.search_nodes(source, target)

    # Calculate the time
    end = time.time()
    diff = end - start
    minutes, seconds = diff // 60, diff % 60

    print('Took {} min and {} sec'.format(minutes, seconds))


if __name__ == "__main__":

    args = get_args()

    DICTIONARY = args.dictionary

    source = {args.source: [args.source]}
    target = args.target

    run(source, target)
