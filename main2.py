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


def visited_to_counts(visited, counts):
  for i in range(len(visited)):
    if visited[i]: counts[i] += 1


def search(s, i, visited, ans, cur_word, longest_word, counts):
  if cur_word in words:
    ans.add(cur_word)
    if len(cur_word) > len(longest_word):
      longest_word = cur_word

    visited_to_counts(visited, counts)
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

  return (score(ans), longest_word, counts)


f = open("scrabble_words.txt", 'r')
words = f.read()
words = set([w.lower() for w in words.split()])

import random

def mutate2(thing):  #(s, (score, longest_word, counts))
  #return 20 mutations
  s = thing[0]
  score = thing[1][0]
  counts = thing[1][2]

  #15 replaces, 5 shuffles
  mutations = []

  #shuffle
  for _ in range(5):
    mutations.append(''.join(random.sample(s, len(s))))

  #replace
  smallest_indexes = sorted(range(19), key=lambda k: counts[k])
  for i in range(15):
    s2 = str(s)
    for j in range(len(smallest_indexes)):
      p = (19 - j) * (0.5 / 19)
      if random.uniform(0, 1) < p:  #if true, then replace current char
        s2 = s2[:smallest_indexes[j]] + chr(random.randint(ord('a'), ord('z'))) + s2[smallest_indexes[j] + 1:]
    mutations.append(s2)

  #print(mutations)
  return mutations


def evolve_batches(start):
  batch = [(start, search_start(start))]  #s, (score, longest_word, counts)
  best_score = 0
  best_s = ""
  batch_num = 0


  while True:
    new_batch = []
    avg_batch_score = 0
    for cur in batch:
      print(batch_num, cur[0], cur[1][0], cur[1][1])
      avg_batch_score += cur[1][0]
      if cur[1][0] > best_score:
        print("BEST!!!")
        best_score = cur[1][0]
        best_s = cur[0]
      children = mutate2(cur)
      children = [(c, search_start(c)) for c in children]
  
      new_batch.extend(children)

    avg_batch_score /= len(batch)
    print(batch_num, "AVG SCORE: ", avg_batch_score)

    new_batch.extend(batch)
  
    new_batch.sort(key=lambda x: -x[1][0])
    new_batch = new_batch[:min(len(new_batch), 20)]
    batch = new_batch
    batch_num += 1

evolve_batches(input("x: "))
