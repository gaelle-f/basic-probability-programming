def check_alphabet(list1, list2, amount=1000):
  word_freq = zip(list1, list2)
  alphabetically_sorted = sorted(word_freq, key=lambda tup: tup[0])
  final_sorted = sorted(alphabetically_sorted, key=lambda tup: tup[1], reverse=True)
  words, freq = zip(*final_sorted)
  if list(words) == list1:
    print("Alphabetically sorted")
  else:
    print("Not alphabetically sorted")

def check_overlap(list1, list2):
  # check percentage overlap with list1
  set1 = set(list1)
  set2 = set(list2)
  overlap = set1 & set2
  perc_overlap = float(len(overlap)) / len(set1) * 100 
  print('Percentage of overlap with respect to the golden list {}%'.format(perc_overlap))

def get_lists():
  textFile = str(input('Please enter the path to the text file you want to read: '))
  collected_frequencies = collect_frequencies(textFile)
  freq1, freq2 = find_frequent_words(collected_frequencies, amount=1000)
  return freq1, freq2


## read in golden list 
golden_list = []
path_gold_list = textFile = str(input('Please enter the path to golden_common.txt: '))
with open(path_gold_list, 'r') as f:
  for line in f:
    golden_list.append(line.strip())


list1, list2 = get_lists()
check_alphabet(list1, list2)
check_overlap(golden_list, list1)