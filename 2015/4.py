import hashlib



def find_hash(salt, size):
  i = 0
  value = "1" * size

  while value[0:size] != "0" * size:
    i += 1
    value = hashlib.md5(f"{salt}{i}".encode()).hexdigest()

  print(i)

def main():
  salt = "bgvyzdsv"

  find_hash(salt, 5)
  find_hash(salt, 6)

if __name__ == "__main__":
  main()