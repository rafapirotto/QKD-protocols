from helpers import *
from qiskit import IBMQ

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

alice_bits = ['0', '1', '0', '0', '0', '1', '0', '1']
alice_bases = ['Z', 'Z', 'X', 'Z', 'Z', 'X', 'X', "X"]
alice_states = get_states(alice_bits, alice_bases)

bob_bases = ['Z', 'Z', 'X', 'X', 'X', 'Z', 'X', 'X']

circuit = QuantumCircuit(size, size)

insert_states_in_circuit(circuit, alice_states)

insert_measurements_according_to_base(bob_bases, circuit)

bob_measurements = get_measurements_result(backend, circuit, shots, accuracy, size)

same_bases_positions = get_same_bases_positions(alice_bases, bob_bases)

alice_raw_key = discard_different_positions(alice_bits, same_bases_positions)
bob_raw_key = discard_different_positions(bob_measurements, same_bases_positions)

save_circuit_image(circuit, "bb84_circuit")
print(f"\nAlice bits: {alice_bits}")
print(f"Alice bases: {alice_bases}")
print(f"Alice states: {alice_states}\n")
print(f"Bob bases: {bob_bases}")
print(f"Bob measurements: {bob_measurements}\n")
print(f"Same bases positions: {same_bases_positions}\n")
print(f"Alice raw key: {alice_raw_key}")
print(f"Bob raw key: {bob_raw_key}\n")



privacy_amplification = input("Perform privacy amplification?(y/n): ").lower()
if privacy_amplification == "y":
    bits_to_discard = int(input(f"Enter desired number of bits to compare (max:{len(alice_raw_key)}): "))
    accuracy = int(input("Enter desired accuracy: "))
    print("The compared bits will be discarded\n")

    perform_privacy_amplification(alice_raw_key, bob_raw_key, bits_to_discard, accuracy)


        