from helpers import *
from qiskit import IBMQ


def bb84():
    use_simulator = input("Run using simulator?(y/n): ").lower()
    shots = 1
    backend = QasmSimulator()
    accuracy = 100

    size = int(input("Enter desired length of bits (max:29): "))
    alice_bits = get_random_sequence_of_bits(size)
    alice_bases = get_random_sequence_of_bases(size)
    bob_bases = get_random_sequence_of_bases(size)

    if use_simulator == "n":
        print("Loading IBM account")
        my_provider = IBMQ.load_account()
        backend = my_provider.get_backend('ibmq_manila')
        shots = int(input("Enter desired number of shots: "))
        accuracy = int(input("Enter desired accuracy: "))

    print("\n")

    alice_states = get_states(alice_bits, alice_bases)
    size = len(alice_bits)
    circuit = QuantumCircuit(size, size)
    initialize_circuit_with_zeros(circuit)

    insert_states_in_circuit(circuit, alice_states)

    insert_measurements_according_to_base(bob_bases, circuit)

    bob_measurements = get_measurements_result(backend, circuit, shots, accuracy, size)

    same_bases_positions = get_same_bases_positions(alice_bases, bob_bases)

    alice_sifted_key = discard_different_positions(alice_bits, same_bases_positions)
    bob_sifted_key = discard_different_positions(bob_measurements, same_bases_positions)

    save_circuit_image(circuit, "bb84_circuit_without_eve")
    print("\nBB84 protocol without intervention\n")
    print(f"Alice bits:       {alice_bits}")
    print(f"Alice bases:      {alice_bases}")
    print(f"Alice states:     {alice_states}\n")
    print(f"Bob bases:        {bob_bases}")
    print(f"Bob measurements: {bob_measurements}\n")
    print(f"Same bases positions: {same_bases_positions}\n")
    print(f"Alice sifted key: {alice_sifted_key}")
    print(f"Bob sifted key:   {bob_sifted_key}\n")

    privacy_amplification = input("Perform privacy amplification?(y/n): ").lower()
    if privacy_amplification == "y":
        perform_privacy_amplification(alice_sifted_key, bob_sifted_key)

    encrypt = input("Encrypt message?(y/n): ").lower()
    if encrypt == "y":
        message = input("Enter message: ")
        encrypted_message = encrypt_message(message)
        print(f"Encrypted message: {encrypted_message}")
       
        decrypt = input("Decrypt message?(y/n): ").lower()
        if decrypt == "y":
            decrypted_message = descrypt_message(encrypted_message)
            print(f"Decrypted message: {decrypted_message}")
