alice = ['1', '1', '1', '1', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '1', '1', '0']
bob = ['1', '1', '1', '1', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '1', '1', '0']


errors = 0

for i in range(len(alice)):
  if alice[i] != bob[i]:
    errors += 1


print("\n---Error caused by Quantum channel in simulator---")
print(f"errors count: {errors}")
print(f"errors percentage: {100*errors/len(alice)}%")
print(f"Sample size: {len(alice)}")