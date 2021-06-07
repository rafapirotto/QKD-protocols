from helpers import *

print("\nBB84 without Eve\n")

backend_input = input("Run using simulator?(y/n): ").lower()
size = int(input("Enter desired length of bits: "))
threshold = int(input("Enter desired threshold: "))
shots = int(input("Enter desired number of shots: "))
print("\n")

backend = QasmSimulator()

if backend_input == "n":
    my_provider = IBMQ.load_account()
    backend = my_provider.get_backend('ibmq_16_melbourne')

alice_bits = get_random_sequence_of_bits(size)
alice_bases = get_random_sequence_of_bases(size)

# example:
# alice_bits = ['0','1','0','0', '0', '1','0','1']
# alice_bases = ['Z', 'Z', 'H', 'Z', 'Z', 'H', 'H', "H"]
alice_states = get_states(alice_bits, alice_bases)

circuit = QuantumCircuit(size, size)

insert_states_in_circuit(circuit, alice_states)

bob_bases = get_random_sequence_of_bases(size)
# bob_bases = ['Z', 'Z', 'H', 'H', 'H', 'Z','H','H']

make_measurements(bob_bases, circuit)

counts = get_counts(circuit, backend, shots)

key = get_key(counts, shots, threshold, size)


print(f"\nAlice bits: {alice_bits}")
print(f"Alice bases: {alice_bases}")
print(f"Alice states: {alice_states}\n")
print(f"Bob bases: {bob_bases}\n")
print(f"Key: {key}\n")

save_circuit_image(circuit, "bb84_circuit")





