nexts = {
    0: [1, 3, 4],
    1: [0, 4, 5, 2],
    2: [1, 5, 6],
    3: [0, 4, 7, 8],
    4: [0, 1, 5, 9, 8, 3],
    5: [1, 2, 6, 9, 10, 4],
    6: [2, 5, 10, 11],
    7: [3, 8, 12],
    8: [3, 4, 9, 13, 12, 7],
    9: [4, 5, 10, 14, 13, 8],
    10: [5, 6, 11, 15, 14, 9],
    11: [6, 10, 15],
    12: [7, 8, 13, 16],
    13: [8, 9, 14, 17, 16, 12],
    14: [9, 10, 15, 18, 17, 13],
    15: [10, 11, 14, 18],
    16: [12, 13, 17],
    17: [16, 13, 14, 18],
    18: [17, 14, 15]
}


def get_next(i):
  return nexts[i]


def visited_to_counts(visited, counts, weight):
  for i in range(len(visited)):
    if visited[i]: counts[i] += weight


def search(s, i, visited, ans, cur_word, longest_word, counts):
  if cur_word in words:
    ans.add(cur_word)
    if len(cur_word) > len(longest_word):
      longest_word = cur_word

    visited_to_counts(visited, counts, len(cur_word))
    #print(cur_word)
  if len(cur_word) == 8:
    return longest_word
  visited[i] = True

  for n in get_next(i):
    if not visited[n]:
      longest_word = search(s, n, visited, ans, cur_word + s[n], longest_word,
                            counts)
      visited[n] = False

  return longest_word


def score(ans):

  def to_int(x):
    return len(x)

  return sum(map(to_int, ans))


def search_start(s):
  ans = set()
  longest_word = ""
  counts = [0] * 19
  for start in range(19):
    longest_word = search(s, start, [False] * 19, ans, "", longest_word,
                          counts)

  return (score(ans),longest_word, counts)


f = open("scrabble_words.txt", 'r')
words = f.read()
words = set([w.lower() for w in words.split()])

import random

def gen_s():
  vowels = 'aeiou'  # random.choice can choose from any type of sequence
  consonants = 'bcdfghjklmnpqrstvwxyz'
  chars = []  # collects the choices

  num_vowels = random.randint(6, 8)

  for i in range(num_vowels):
    chars.append(random.choice(vowels))
  for i in range(19-num_vowels):
    chars.append(random.choice(consonants))

  s = ''.join(chars)
  return ''.join(random.sample(s,len(s)))


best_score = 0
best_s = ""
best_longest_word = ""


i = 0
while True:
  i += 1
  s = gen_s()
  ans = search_start(s)
  cur_score = ans[0]
  longest_word = ans[1]

  if cur_score > best_score:
    best_score = cur_score
    best_s = s
    best_longest_word = longest_word

    print("NEW BEST: ", best_s, best_score, best_longest_word)

  if i % 500 == 0: 
    print("best: ", best_s, best_score, best_longest_word)
