from bb84 import bb84
from helpers import get_states

run_example = input("Run example?(y/n): ").lower()

if run_example == "y":
    alice_bits = ['0', '1', '0', '0', '0', '1', '0', '1']
    alice_bases = ['Z', 'Z', 'X', 'Z', 'Z', 'X', 'X', "X"]
    alice_states = get_states(alice_bits, alice_bases)
    bob_bases = ['Z', 'Z', 'X', 'X', 'X', 'Z', 'X', 'X']

    bb84(alice_bits, alice_bases, bob_bases) 
else:
    bb84()