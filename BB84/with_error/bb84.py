from helpers import *
from qiskit import IBMQ


def bb84(eve_is_present=False, simulator=True, accuracy=100, size=5):
    shots = 8192

    alice_bits = get_random_sequence_of_bits(size)
    alice_bases = get_random_sequence_of_bases(size)
    bob_bases = get_random_sequence_of_bases(size)
    

    alice_states = get_states(alice_bits, alice_bases)
    circuit = QuantumCircuit(size, size)
    initialize_circuit_with_zeros(circuit)
    insert_states_in_circuit(circuit, alice_states)


    if simulator:
        backend = QasmSimulator()
    else:
        print("Loading IBM account")
        my_provider = IBMQ.load_account()
        backend = my_provider.get_backend('ibmq_manila')

    # Eve makes measurements
    if eve_is_present:
        eve_bases = get_random_sequence_of_bases(size)
        insert_measurements_according_to_base(eve_bases, circuit)
        circuit.barrier()
        eve_measurements = get_measurements_result(backend, circuit, shots, accuracy, size)
        eve_states_for_bob = get_states(eve_measurements, eve_bases)
        reset_circuit(circuit, size)
        insert_states_in_circuit(circuit, eve_states_for_bob)

    insert_measurements_according_to_base(bob_bases, circuit)
    bob_measurements = get_measurements_result(backend, circuit, shots, accuracy, size)

    same_bases_positions = get_same_bases_positions(alice_bases, bob_bases)

    alice_raw_key = discard_different_positions(alice_bits, same_bases_positions)
    bob_raw_key = discard_different_positions(bob_measurements, same_bases_positions)

    if eve_is_present:
        eve_raw_key = discard_different_positions(eve_measurements, same_bases_positions)

    save_circuit_image(circuit, "bb84_circuit")

    # guardar keys en archivo
    if simulator:
        if eve_is_present:
            file = open("data_collected_with_simulator_and_eve.txt", "a")
        else:
            file = open("data_collected_with_simulator_without_eve.txt", "a")
    else:
        if eve_is_present:
            file = open("data_collected_with_real_machine_and_eve.txt", "a")
        else:
            file = open("data_collected_with_real_machine_without_eve.txt", "a")

    file.write(f"alice key: {alice_raw_key}\n")
    if eve_is_present:
        file.write(f"eve key:   {eve_raw_key}\n")
    file.write(f"bob key:   {bob_raw_key}\n")
    file.close()

    print(f"alice key: {alice_raw_key}")
    if eve_is_present:
        print(f"eve key:   {eve_raw_key}")
    print(f"bob key:   {bob_raw_key}")
