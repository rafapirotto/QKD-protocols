from helpers import *
from qiskit import IBMQ

def b92():
  use_simulator = input("Run using simulator?(y/n): ").lower()
  shots = 1
  backend = QasmSimulator()
  accuracy = 100

  size = int(input("Enter desired length of bits: "))
  alice_bits = get_random_sequence_of_bits(size)
  bob_bits = get_random_sequence_of_bits(size)
    
  if use_simulator == "n":
    print("Loading IBM account")
    my_provider = IBMQ.load_account()
    backend = my_provider.get_backend('ibmq_manila')
    shots = int(input("Enter desired number of shots: "))
    accuracy = int(input("Enter desired accuracy: "))

  print("\n")

  alice_states = get_states_from_bits(alice_bits)
  bob_bases = get_bases_from_bits(bob_bits)
  size = len(alice_bits)
  circuit = QuantumCircuit(size, size)
  initialize_circuit_with_zeros(circuit)

  insert_states_in_circuit(circuit, alice_states)

  insert_measurements_according_to_base(bob_bases, circuit)

    # vector contains bob's measurements
  vector = get_measurements_result(backend, circuit, shots, accuracy, size)
    
  new_vector_alice = get_sub_vector(alice_bits, vector)
  new_vector_bob = get_sub_vector(bob_bits, vector)


  save_circuit_image(circuit, "b92_circuit_without_eve")
  print("\nB92 protocol without intervention\n")
  print(f"Alice bits:   {alice_bits}")
  print(f"Alice states: {alice_states}")
  print("\n")
  print(f"Bob bits:     {bob_bits}")
  print(f"Bob bases:    {bob_bases}\n")
  print(f"Vector:       {vector}\n")
  print(f"Vector Alice: {new_vector_alice}\n")
  print(f"Vector Bob:   {new_vector_bob}\n")
  print(f"The key is either Bob's vector or Alice's.\n")

  vector_choice = input("Use Alice's vector or Bob's as key?(a/b): ").lower()
  if vector_choice == 'a':
      for index, val in enumerate(new_vector_bob):
        if val == BIT_0:
          new_vector_bob[index] = BIT_1
        else:
          new_vector_bob[index] = BIT_0

  elif vector_choice == 'b':
      for index, val in enumerate(new_vector_alice):
        if val == BIT_0:
          new_vector_alice[index] = BIT_1
        else:
          new_vector_alice[index] = BIT_0

  alice_sifted_key = "".join(new_vector_alice)
  bob_sifted_key = "".join(new_vector_bob)
  print("\n")
  print(f"Alice sifted key: {alice_sifted_key}\n")
  print(f"Bob sifted key:   {bob_sifted_key}\n")

  privacy_amplification = input("Perform privacy amplification?(y/n): ").lower()
  if privacy_amplification == "y":
      perform_privacy_amplification(new_vector_alice, new_vector_bob)

  encrypt = input("Encrypt message?(y/n): ").lower()
  if encrypt == "y":
      message = input("Enter message: ")
      encrypted_message = encrypt_message(message)
      print(f"Encrypted message: {encrypted_message}")
      
      decrypt = input("Decrypt message?(y/n): ").lower()
      if decrypt == "y":
          decrypted_message = descrypt_message(encrypted_message)
          print(f"Decrypted message: {decrypted_message}")

