# Word Ladder

This is a script that provides a number of functions to calculate the shortest path between two words.

### The problem

The problem is commonly known as "Word ladder", hence the title.

You can find more information [here](https://en.wikipedia.org/wiki/Word_ladder)

### Usage

1. Make sure you have a dictionary file downloaded somewhere in your system. For linux and MacOS you will probably find such a file in /usr/share/dict/ directory. Alternatively just use the test dictionary provided.

2. Run the application from the root directory with the following command:

```
$ bin/word_ladder -d test_dictionary -s <source_word> -t <target_word>
```

Note: Depending on the format of the dictionary file that you provide, you might need to tweak create_words_list function.

## Authors

* **Christos Liontos**
