






import re

class PartOne:
  def __init__(self):
    self.vowels = "aeiou"
    self.alph = "abcdefghijklmnopqrstuvwxyz"
    self.dl_regex = self._double_letters_regex()

  def run(self):
    count = 0

    with open("2015/input_5.txt", "r") as f:
      for i in f.readlines():
        count += 1 if self.is_nice(i) else 0

    print(count)

  def is_nice(self, value):
    v = self.has_vowels(value)
    d = self.double_letters(value)
    p = self.pairs(value)

    return v and d and not p

  def has_vowels(self, value):
    count = sum(len(re.findall(fr"{i}", value)) for i in self.vowels)
    return count >= 3

  def double_letters(self, value):
    return re.search(self.dl_regex, value)

  def _double_letters_regex(self):
    # QUESTION: does this count if it's more than twice?
    pattern = [f"({i}{{2}})" for i in self.alph]
    return "|".join(pattern)

  def pairs(self, value):
    return re.search(r"(ab)|(cd)|(pq)|(xy)", value)
  

def main():
  one = PartOne()
  one.run()



if __name__ == "__main__":
  main()