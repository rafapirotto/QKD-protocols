from bb84 import bb84


for i in range(10):
  print(i + 1)
  bb84(simulator=True, accuracy=100, spy=False, size=5)
