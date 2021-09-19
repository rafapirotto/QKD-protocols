from helpers import *
from qiskit import IBMQ

# eva va a estar presente siempre
def bb84(simulator=True, accuracy=100, size=5, spy=True):
    shots = 8192

    alice_bits = get_random_sequence_of_bits(size)
    alice_bases = get_random_sequence_of_bases(size)
    bob_bases = alice_bases
    

    alice_states = get_states(alice_bits, alice_bases)
    circuit = QuantumCircuit(size, size)
    insert_states_in_circuit(circuit, alice_states)


    if simulator:
        backend = QasmSimulator()
    else:
        print("Loading IBM account")
        my_provider = IBMQ.load_account()
        backend = my_provider.get_backend('ibmq_manila')

    # Eve makes measurements
    if spy:
        eve_bases = get_random_sequence_of_bases(size)
    else:
        eve_bases = alice_bases

    insert_measurements_according_to_base(eve_bases, circuit)
    circuit.barrier()
    eve_measurements = get_measurements_result(backend, circuit, shots, accuracy, size)
    states_for_bob = get_states(eve_measurements, eve_bases)
    insert_states_in_circuit_2(circuit, eve_bases)

    insert_measurements_according_to_base(bob_bases, circuit)
    bob_measurements = get_measurements_result(backend, circuit, shots, accuracy, size)

    same_bases_positions = get_same_bases_positions(alice_bases, bob_bases)

    alice_sifted_key = discard_different_positions(alice_bits, same_bases_positions)
    bob_sifted_key = discard_different_positions(bob_measurements, same_bases_positions)

    if spy:
        eve_sifted_key = discard_different_positions(eve_measurements, same_bases_positions)

    save_circuit_image(circuit, "bb84_circuit")

    # guardar keys en archivo
    if simulator:
        if spy:
            file = open("data_collected_with_simulator_and_eve.txt", "a")
        else:
            file = open("data_collected_with_simulator_without_eve.txt", "a")
    else:
        if spy:
            file = open("data_collected_with_real_machine_and_eve.txt", "a")
        else:
            file = open("data_collected_with_real_machine_without_eve.txt", "a")

    file.write(f"alice key: {alice_sifted_key}\n")
    if spy:
        # eva va a estar presente siempre, sin embargo, si no espia, no me interesa su informacion, entonces no la guardo
        file.write(f"eve key:   {eve_sifted_key}\n")
    file.write(f"bob key:   {bob_sifted_key}\n")
    file.close()
