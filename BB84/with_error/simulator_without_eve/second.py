file = open("data_collected_with_simulator_without_eve.txt", "r")

content = file.readlines()
alice = "["
bob = "["

for i in range(len(content)):
  splitted_line = content[i].split('\n')
  if i % 2 == 0:
    uno = splitted_line[0].split('alice key: ')
    dos = uno[1].split('[')
    tres = dos[1].split(']')
    alice += tres[0] + ", "
  elif i % 2 == 1:
    uno = splitted_line[0].split('bob key:   ')
    dos = uno[1].split('[')
    tres = dos[1].split(']')
    bob += tres[0] + ", "
    

alice += "]"
bob += "]"

alice = alice.split(", ]")[0] + "]\n"
bob = bob.split(", ]")[0] + "]\n"


# remove the double commas generated from not having any base in common
alice = alice.replace(",,", ",")
bob = bob.replace(",,", ",")
alice = alice.replace(", ,", ",")
bob = bob.replace(", ,", ",")


file_2 = open("simulator_without_eve_processed.txt", "a")
file_2.write(alice)
file_2.write(bob)
file_2.close()