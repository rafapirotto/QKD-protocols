file = open("data_collected_with_simulator_and_eve.txt", "r")

content = file.readlines()
alice = "["
bob = "["
eve = "["

for i in range(len(content)):
  splitted_line = content[i].split('\n')
  if i % 3 == 0:
    uno = splitted_line[0].split('alice key: ')
    dos = uno[1].split('[')
    tres = dos[1].split(']')
    alice += tres[0] + ", "
  elif i % 3 == 1:
    uno = splitted_line[0].split('eve key:   ')
    dos = uno[1].split('[')
    tres = dos[1].split(']')
    eve += tres[0] + ", "
  elif i % 3 == 2:
    uno = splitted_line[0].split('bob key:   ')
    dos = uno[1].split('[')
    tres = dos[1].split(']')
    bob += tres[0] + ", "
    

alice += "]"
eve += "]"
bob += "]"

alice = alice.split(", ]")[0] + "]\n"
eve = eve.split(", ]")[0] + "]\n"
bob = bob.split(", ]")[0] + "]\n"


file_2 = open("simulator_with_eve_processed.txt", "a")
file_2.write(alice)
file_2.write(eve)
file_2.write(bob)
file_2.close()