from helpers import *
from qiskit import IBMQ

def e91(alice_bases=None, bob_bases=None):
  use_simulator = input("Run using simulator?(y/n): ").lower()
  shots = 1
  backend = QasmSimulator()
  accuracy = 100

  if alice_bases is None:
    size = int(input("Enter desired length of bits: "))
    alice_bases = get_random_sequence_of_bases(size)
    bob_bases = get_random_sequence_of_bases(size)
    
  if use_simulator == "n":
    print("Loading IBM account")
    my_provider = IBMQ.load_account()
    backend = my_provider.get_backend('ibmq_16_melbourne')
    shots = int(input("Enter desired number of shots: "))
    accuracy = int(input("Enter desired accuracy: "))

  print("\n")

  size = len(alice_bases)
  circuit = QuantumCircuit(2*size, 2*size)

  insert_states_in_circuit(circuit, size)

  insert_measurements_according_to_base(alice_bases, bob_bases, circuit)

  save_circuit_image(circuit, "e91_circuit")

  measurements = get_measurements_result(backend, circuit, shots, accuracy, 2*size)
  same_bases_positions = get_same_bases_positions(alice_bases, bob_bases)

  alice_measurements = measurements['alice']
  bob_measurements = measurements['bob']

  alice_raw_key = discard_different_positions(alice_measurements, same_bases_positions)
  bob_raw_key = discard_different_positions(bob_measurements, same_bases_positions)
  print('\n')
  print("E91 protocol without intervention\n")
  print("alice bases:", alice_bases)
  print("bob bases:  ", bob_bases)
  print('\n')
  print("alice measurements: ", measurements["alice"])
  print("bob measurements:   ", measurements["bob"])
  print("same_bases_positions: ", same_bases_positions)
  print('\n')
  print("alice_raw_key", alice_raw_key)
  print("bob_raw_key  ", bob_raw_key)

  privacy_amplification = input("Perform privacy amplification?(y/n): ").lower()
  if privacy_amplification == "y":
      bits_to_discard = int(input(f"Enter desired number of bits to compare (max:{len(alice_raw_key)}): "))
      accuracy = int(input("Enter desired accuracy: "))
      print("The compared bits will be discarded\n")

      perform_privacy_amplification(alice_raw_key, bob_raw_key, bits_to_discard, accuracy)

  encrypt = input("Encrypt message?(y/n): ").lower()
  if encrypt == "y":
      message = input("Enter message: ")
      encrypted_message = encrypt_message(message)
      print(f"Encrypted message: {encrypted_message}")
      
      decrypt = input("Decrypt message?(y/n): ").lower()
      if decrypt == "y":
          decrypted_message = descrypt_message(encrypted_message)
          print(f"Decrypted message: {decrypted_message}")

  