"""
This is the third set of exercises used in class.

The comments (marked by #) explain what you should do. Type your code below
each comment.
"""

# We will continue working with a text file, calculating frequencies and
# probabilities of words in a text. However, we will now expand this to an
# n-gram analysis of the text, which takes into account the context of the
# word.
# 
# Say we have the following sentence: "The boy kissed the frog."
# In the homework, you had to count occurrences, which would give the
# following dictionary: {"the": 2, "kissed": 1, "boy": 1, "frog": 1}
# Now, we will want to calculate the frequency of a word given a prefix, where
# by prefix, we mean the word or words that came before it. That is, we want to
# count how often a word follows a particular word or words.
#
# In order to count these occurrences, we'll make use of the built-in Counter
# object from the collections module. A Counter is just a dictionary, where the
# keys are the items being counted, and the values are their respective counts,
# exactly like the example dictionary above. The Counter object just supports
# some additional operations, which are specific to counting, most notably
# updating the dictionary of counts based on a list of items, and easily
# finding the most common items. The full description of this extension of
# regular dictionaries, can be found here:
# https://docs.python.org/3/library/collections.html#collections.Counter
#
# In order to include prefixes in the counts, we'll actually need to group
# together the counts for each prefix, which we'll also do using a dictionary.
# This means our main counting dictionary will have the prefixes as the keys,
# and as the value a separate Counter object for the counts of that prefix.
# Suppose we assume a prefix of size 1 for the example above.
# Then, the resulting counts should be: {"the": Counter("boy": 1, "frog": 1),
# "boy": Counter("kissed": 1), "kissed": Counter("the": 1), "frog": Counter()}
# 
# We can then later use this n-gram to generate sentences which sound (almost)
# English-like.


# We will use the package random and counter in this exercise. Later on,
# itertools will become useful. So we import this first:

import random
import itertools
from collections import Counter

# We will first operate with a fake text (only later will we substitute it
# with a book). We will assign the following list to a variable with a
# recognizable name:

temp_text = ["The boy kissed a frog.",
             "After kissing it, nothing happened and the boy got angry and left the frog where he kissed it.",
             "The frog never saw the boy and the boy kissed no frog since then."]

# 1. Write a function, split_text. The function takes a list of strings
# (sentences) and splits each sentence by spaces and converts all characters to
# lowercase.
# It should return a list of lists of words, such that each inner list
# corresponds to the words of one sentence.
# *Note:* For an extra challenge, you can try to write this function as a
# single list comprehension.

def split_text(text):
    """
    text: list of strings.
    """
    return [sentence.lower().split() for sentence in text]

# 2. Test that split_text works. The loop below should print one sentence,
# appearing as a list of words, per iteration.

test = split_text(temp_text)

for sentence in test:
    print(sentence)
    print("*********")

# A bigram is an n-gram model with a fixed prefix size of 1, meaning we're only 
# considering the occurrences of any two words together in the text, hence the
# name *bi*gram. The n-gram example given at the top of the file is also a
# bigram.
# Bigrams are easier to implement than general n-grams, so we'll start by just
# looking at those, and then expand to n-gram models later.

# 3. Create a function, update_bigrams, that gets two arguments: dict_to_update
# (a dictionary), and a sentence (a list). It updates the dictionary with the
# sentence as follows: for every pair of adjacent words A B in the sentence, it
# takes A as the key in the dictionary and updates the corresponding Counter
# value with an additional count for B. If A does not occur in the dictionary
# at all, a new Counter with the correct counts for B should be added to the
# dictionary.
# This a void function (nothing is returned).

def update_bigrams(dict_to_update, sentence):
    """
    dict_to_update: dictionary
    sentence: list

    """
    for i in range(len(sentence)-1):
        #if the word is in the dictionary, we only update the counter that is
        #tied to the word in the dictionary
        if sentence[i] in dict_to_update:
            dict_to_update[sentence[i]].update([sentence[i+1]])
        #otherwise, we will create a counter
        else:
            dict_to_update[sentence[i]] = Counter([sentence[i+1]])

# 4. Test the function using preprocessed_text. After looping through all sentences, 
# the statement below should evaluate as True.

bigram_dict = {}

preprocessed_text = split_text(temp_text)
for sentence in preprocessed_text:
    update_bigrams(bigram_dict, sentence)

print(bigram_dict == {'it,': Counter({'nothing': 1}), 'boy': Counter({'kissed':
    2, 'and': 1, 'got': 1}), 'frog': Counter({'never': 1, 'since': 1, 'where':
        1}), 'saw': Counter({'the': 1}), 'happened': Counter({'and': 1}),
    'since': Counter({'then.': 1}), 'angry': Counter({'and': 1}), 'nothing':
    Counter({'happened': 1}), 'and': Counter({'the': 2, 'left': 1}), 'never':
    Counter({'saw': 1}), 'he': Counter({'kissed': 1}), 'kissing':
    Counter({'it,': 1}), 'no': Counter({'frog': 1}), 'after':
    Counter({'kissing': 1}), 'kissed': Counter({'it.': 1, 'no': 1, 'a': 1}),
    'left': Counter({'the': 1}), 'where': Counter({'he': 1}), 'the':
    Counter({'boy': 4, 'frog': 2}), 'a': Counter({'frog.': 1}), 'got':
    Counter({'angry': 1})})
    
# We want to generalize our strategy to n-grams. For this we will create a new
# function, update_ngram, with 3 arguments: ngram_dict, sentence, prefix.
# Prefix encodes the size of prefix to use, where the sequence of words that
# form the prefix should be stored together in a *tuple*.
#
# *Note:* The word sequence must be a tuple (and cannot be a list), as the
# sequence needs to be hashable to be inserted in the dictionary. Mutable
# types, like a list, can never be made hashable, therefore an immutable type,
# like a tuple, must be used as the the dictionary key.
# 
# For example, a trigram uses a prefix of size 2, and would therefore look like
# {("the", "boy"): Counter("kissed": 1), ("boy", "kissed"): Counter("the": 1), 
# ("kissed", "the"): Counter("frog": 1)}


# 5. Write the function update_ngram, which should work like update_bigrams,
# but it allows a sequence of any number of words to appear as the prefix. How
# many words should be as the prefix used is given by the prefix argument.

def update_ngrams(dict_to_update, sentence, prefix=1):
    """
    dict_to_update: dictionary
    sentence: list
    prefix: int (size of prefix to use)
    """
    if prefix < len(sentence):
        for i in range(len(sentence)-prefix):
            words = tuple(sentence[i:i+prefix])
            #if the words are in the dictionary, we only update the counter
            #that is tied to the words in the dictionary
            if words in dict_to_update:
                dict_to_update[words].update([sentence[i+prefix]])
            #otherwise, we have to create a counter
            else:
                dict_to_update[words] = Counter([sentence[i+prefix]])

# 6. Test update_ngrams with prefix=2 using preprocessed_text.
# After looping through all sentences, the statement below should 
# evaluate as True.

ngram_dict = {}

preprocessed_text = split_text(temp_text)
for sentence in preprocessed_text:
    update_ngrams(ngram_dict, sentence, 2)

print(ngram_dict == {('got', 'angry'): Counter({'and': 1}), ('left', 'the'):
        Counter({'frog': 1}), ('boy', 'kissed'): Counter({'no': 1, 'a': 1}),
        ('boy', 'and'): Counter({'the': 1}), ('kissed', 'a'):
        Counter({'frog.': 1}), ('kissed', 'no'): Counter({'frog': 1}),
        ('the', 'frog'): Counter({'never': 1, 'where': 1}),
        ('nothing', 'happened'): Counter({'and': 1}), ('frog', 'since'):
        Counter({'then.': 1}), ('happened', 'and'): Counter({'the': 1}),
        ('boy', 'got'): Counter({'angry': 1}), ('angry', 'and'):
        Counter({'left': 1}), ('saw', 'the'): Counter({'boy': 1}),
        ('kissing', 'it,'): Counter({'nothing': 1}), ('frog', 'where'):
        Counter({'he': 1}), ('frog', 'never'): Counter({'saw': 1}),
        ('and', 'the'): Counter({'boy': 2}), ('and', 'left'):
        Counter({'the': 1}), ('no', 'frog'): Counter({'since': 1}),
        ('it,', 'nothing'): Counter({'happened': 1}), ('the', 'boy'):
        Counter({'kissed': 2, 'and': 1, 'got': 1}), ('never', 'saw'):
        Counter({'the': 1}), ('he', 'kissed'): Counter({'it.': 1}),
        ('where', 'he'): Counter({'kissed': 1}), ('after', 'kissing'):
        Counter({'it,': 1})})

# 7. Create a new function, create_prob_ngrams, which takes an ngram_dict as
# its argument and returns a dictionary in which each prefix shows the
# *probability* that the prefix is followed by a particular word. That is,
# instead of storing a Counter of occurrences for each prefix, each prefix
# should have a corresponding dictionary of probabilities, giving the
# probability of that a particular word follows the prefix. 
# Note that by doing this, you create conditional probabilities: the
# probabilities that some words appear, given the prefix.

def create_prob_ngrams(ngram_dict):
    """
    ngram_dict: dictionary
    sentence: list

    """
    ngram_prob = {}
    for prefix in ngram_dict:
        total = sum(ngram_dict[prefix].values())
        ngram_prob[prefix] = {word: ngram_dict[prefix][word]/total
                                for word in ngram_dict[prefix]}

    return ngram_prob

# 8. Test the function. The following should evaluate to True.

ngram_prob = create_prob_ngrams(ngram_dict)

print(ngram_prob == {('got', 'angry'): {'and': 1.0}, ('kissed', 'a'):
        {'frog.': 1.0}, ('the', 'frog'): {'where': 0.5, 'never': 0.5},
        ('nothing', 'happened'): {'and': 1.0}, ('boy', 'and'): {'the': 1.0},
        ('angry', 'and'): {'left': 1.0}, ('no', 'frog'): {'since': 1.0},
        ('frog', 'where'): {'he': 1.0}, ('happened', 'and'): {'the': 1.0},
        ('left', 'the'): {'frog': 1.0}, ('after', 'kissing'): {'it,': 1.0},
        ('frog', 'never'): {'saw': 1.0}, ('boy', 'got'): {'angry': 1.0},
        ('frog', 'since'): {'then.': 1.0}, ('saw', 'the'): {'boy': 1.0},
        ('kissed', 'no'): {'frog': 1.0}, ('the', 'boy'):
        {'kissed': 0.5, 'and': 0.25, 'got': 0.25}, ('never', 'saw'):
        {'the': 1.0}, ('it,', 'nothing'): {'happened': 1.0}, ('and', 'the'):
        {'boy': 1.0}, ('boy', 'kissed'): {'a': 0.5, 'no': 0.5},
        ('and', 'left'): {'the': 1.0}, ('where', 'he'): {'kissed': 1.0},
        ('he', 'kissed'): {'it.': 1.0}, ('kissing', 'it,'): {'nothing': 1.0}})

# 8. Finally, we will consider the function select_word. This function takes a
# dictionary and randomly selects a word. The random selection is based on
# probability: words with a higher probability are selected more likely
# (Hint: to do this, select a random number between 0 and 1, and match it
# against the *cumulative* probability of words).
# (Another hint: to select the random number, consult the package random and
# the documentation on Python:
# https://docs.python.org/3/library/random.html
# To get to the cumulative probability, you have to cumulate
# probabilities of words. There are various tools in itertools for tasks
# like that. Find a handy function here:
# https://docs.python.org/3/library/itertools.html

def select_word(words):
    """
    words: dictionary, each word having a probability.
    """
    prob = random.uniform(0, 1)
    words_values = list(zip(*words.items()))
    for i, cum_prob in enumerate(itertools.accumulate(words_values[1])):
        if prob < cum_prob:
            return words_values[0][i]
    return words_values[0][-1]

# 9. Now, it is time to use the actual text file. Create a new function
# load_and_split_text. The function opens a file and returns a list of lists of
# words. That is, for every line, it splits the line by spaces and converts the
# letters to lower case. The function should return the complete list of split
# sentences
# *Note:* For an extra challenge, you can try to write this function as a
# single list comprehension.

def load_and_split_text(textfile):
    """
    textfile: name of textfile
    """
    with open(textfile) as text:
        return [line.lower().split() for line in text]

full_book = load_and_split_text("test.txt")

# 10. Create an ngram_dict and ngram_prob that is based on the text file.

ngram_dict = {}

for sentence in full_book:
    update_ngrams(ngram_dict, sentence, 1)

ngram_prob = create_prob_ngrams(ngram_dict)

# 11. Finally, you should be able to generate a sentence that is somewhat
# English-like, using the created ngram_prob. Start with the word "the"
# and let select_word select the next word. Then input the selected word
# as the following prefix, and so on. Create a "sentence" of length 10.

target_word = "the"
print(target_word)

for _ in range(10):
    if (target_word, ) in ngram_prob:
        target_word = select_word(ngram_prob[(target_word, )])
        print(target_word)
    else:
        break

# 12. As an extra, we can calculate a second dictionary, for trigram
# (specifying prefix=2). We can then proceed as follows:
# let trigram prob. dictionary select the next word, and if it fails, we fall
# back on bigram. This way, the generated sentence becomes much more natural.

print("Combining bigrams and trigrams")

ngram_dict_trigram = {}

for sentence in full_book:
    update_ngrams(ngram_dict_trigram, sentence, 2)

ngram_prob_trigram = create_prob_ngrams(ngram_dict_trigram)

# Next, generate a sentence using the bigram and trigram probabilities, 
# starting with the words "napoleon said"

target_words = ("napoleon", "said")
print(target_words[0])

for _ in range(15):
    if target_words in ngram_prob_trigram:
        target_words = (target_words[1],
            select_word(ngram_prob_trigram[target_words]))
    else:
        #if two words are not as prefix in trigram, we'll switch to bigram
        if target_words[1] in ngram_prob:
            target_words = (target_words[1],
            select_word(ngram_prob[(target_words[1], )]))
        else:
            break #if preceding words are not found, break (this happens when
        #you get to a word which was only used at the end of line)
    print(target_words[0])

