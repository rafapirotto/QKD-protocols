from bb84 import bb84


for i in range(100):
  print(i + 1)
  bb84(simulator=False, accuracy=100, spy=False, size=5)