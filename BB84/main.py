from helpers import *

print("\nBB84 without Eve\n")

use_simulator = input("Run using simulator?(y/n): ").lower()
size = int(input("Enter desired length of bits: "))
accuracy = 100
shots = 1
backend = QasmSimulator()

if use_simulator == "n":
    print("Loading IBM account")
    my_provider = IBMQ.load_account()
    backend = my_provider.get_backend('ibmq_16_melbourne')
    shots = int(input("Enter desired number of shots: "))
    accuracy = int(input("Enter desired accuracy: "))

print("\n")

alice_bits = get_random_sequence_of_bits(size)
alice_bases = get_random_sequence_of_bases(size)
# alice_bits = ['0','1','0','0', '0', '1','0','1']
# alice_bases = ['Z', 'Z', 'X', 'Z', 'Z', 'X', 'X', "X"]
alice_states = get_states(alice_bits, alice_bases)

bob_bases = get_random_sequence_of_bases(size)
# bob_bases = ['Z', 'Z', 'X', 'X', 'X', 'Z','X','X']

circuit = QuantumCircuit(size, size)

insert_states_in_circuit(circuit, alice_states)

make_measurements(bob_bases, circuit)

counts = get_counts(circuit, backend, shots)

same_bases_positions = get_same_bases_positions(alice_bases, bob_bases)

key = get_key(counts, shots, accuracy, same_bases_positions)

print(f"\nAlice bits: {alice_bits}")
print(f"Alice bases: {alice_bases}")
print(f"Alice states: {alice_states}\n")
print(f"Bob bases: {bob_bases}\n")
print(f"Same bases positions: {same_bases_positions}\n")
print(f"Key: {key}\n")

save_circuit_image(circuit, "bb84_circuit")