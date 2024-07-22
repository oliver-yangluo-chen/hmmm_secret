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
      longest_word = search(s, n, visited, ans, cur_word + s[n], longest_word, counts)
      visited[n] = False
      
  return longest_word
      

def score(ans):
  def to_int(x): return len(x)
  return sum(map(to_int, ans))

def search_start(s):
  ans = set()
  longest_word = ""
  counts = [0] * 19
  for start in range(19): 
    longest_word = search(s, start, [False] * 19, ans, "", longest_word, counts)

  return (score(ans), longest_word, counts)


f = open("scrabble_words.txt", 'r')
words = f.read()
words = set([w.lower() for w in words.split()])


import random

def mutate_s_replace(s, counts, children): #returns list of mutated s's
  mutations = []
  #replace lowest count chars
  smallest_indexes = sorted(range(19), key=lambda k: counts[k])

  steps = 0
  for i in smallest_indexes:
    for j in range(random.randint(0, 4)):
      if steps > children: return mutations

      s2 = s[:i] + chr(random.randint(ord('a'), ord('z'))) + s[i + 1:]
      mutations += [s2]
      steps += 1
      
  return mutations

def mutate_s_shuffle(s, children):
  mutations = []
  for i in range(children):
    mutations.append(''.join(random.sample(s,len(s))))
  return mutations
    
  
def num_children_replace(score):
  if score < 500: return 0
  if score < 1000: return 0
  if score < 1500: return 6
  if score < 2000: return 12
  if score < 2500: return 24
  if score < 3000: return 48
  return 100
  
def num_children_shuffle(score):
  if score < 500: return 0
  if score < 1000: return 0
  if score < 1500: return 2
  if score < 2000: return 4
  if score < 2500: return 8
  if score < 3000: return 16
  return 32

def gen_s():
  vowels = 'aeiou'  # random.choice can choose from any type of sequence
  consonants = 'bcdfghjklmnpqrstvwxyz'
  chars = []  # collects the choices

  num_vowels = random.randint(11,15)

  for i in range(num_vowels):
    chars.append(random.choice(vowels))
  for i in range(19-num_vowels):
    chars.append(random.choice(consonants))

  s = ''.join(chars)
  return ''.join(random.sample(s,len(s)))


def evolve_s(s):
  variants = [s]
  best_score = 0
  best_s = ""
  i = 0

  while True:
    cur_s = variants.pop(0)
    cur_ans = search_start(cur_s)
    cur_score = cur_ans[0]
    cur_longest_word = cur_ans[1]
    cur_counts = cur_ans[2]

    if i % 10 == 0: print(cur_s, cur_score, cur_longest_word)

    if cur_score > best_score:
      best_score = cur_score
      best_s = cur_s
      print("BEST: ", cur_s, cur_score, cur_longest_word, cur_counts)
      variants = [best_s]
      i = 0

      if best_score > 3500:
        f_best = open("best.txt", 'a')
        f_best.write(best_s + " " + str(best_score) + "\n")
        f_best.close()

    variants.extend(mutate_s_replace(cur_s, cur_counts, num_children_replace(cur_score)))
    variants.extend(mutate_s_shuffle(cur_s, num_children_shuffle(cur_score)))
    i += 1

    if i % 100 == 0:
      variants = [best_s]


    if i % 50 == 0: print(best_s)

    if i > 2000:
      evolve_s(gen_s())



    

#sbhieletmansirgefol
evolve_s(input("s: "))



