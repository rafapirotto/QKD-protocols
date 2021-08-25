from helpers import *
from qiskit import IBMQ, QuantumCircuit


def getChannelErrorRate(alice_bits, alice_bases):
    shots = 8192
    size = 5
    bob_bases = alice_bases

    print("Loading IBM account")
    my_provider = IBMQ.load_account()
    backend = my_provider.get_backend('ibmq_manila')

    print("\n")

    alice_states = get_states(alice_bits, alice_bases)
    size = len(alice_bits)
    circuit = QuantumCircuit(size, size)
    initialize_circuit_with_zeros(circuit)

    insert_states_in_circuit(circuit, alice_states)

    insert_measurements_according_to_base(bob_bases, circuit)

    errors = getStadistic(backend, circuit, shots, alice_bits)
    print("errores:", errors)

    save_circuit_image(circuit, "bb84_circuit")

    
    


