from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import QasmSimulator
from qiskit.tools.monitor import job_monitor
from qiskit.tools.visualization import circuit_drawer
from random import randint, sample
from constants import *
from onetimepad import decrypt, encrypt
import sys


def get_random_sequence_of_bits(size):
    simulator = QasmSimulator()
    circuit = QuantumCircuit(size, size)

    for i in range(size):
        circuit.h([i])
        circuit.measure([i], [i])

    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    job_monitor(job)
    result = job.result()
    counts = result.get_counts(circuit)
    str_sequence = next(iter(counts))

    return list(str_sequence)


def get_random_sequence_of_bases(size):
    bit_sequence = get_random_sequence_of_bits(size)
    bases = [Z_BASE if bit == BIT_0 else X_BASE for bit in bit_sequence]

    return bases


def get_state(bit, base):
    if bit == BIT_0:
        if base == Z_BASE:
            return STATE_0
        elif base == X_BASE:
            return STATE_PLUS
    if bit == BIT_1:
        if base == Z_BASE:
            return STATE_1
        elif base == X_BASE:
            return STATE_MINUS


def get_states(bits, bases):
    states = []

    for i in range(len(bits)):
        state = get_state(bits[i], bases[i])
        states.append(state)

    return states


def insert_states_in_circuit(circuit, states):
    for i in range(len(states)):
        state = states[i]

        if state == STATE_0:
            pass
        elif state == STATE_1:
            circuit.x([i])
        elif state == STATE_PLUS:
            circuit.h([i])
        elif state == STATE_MINUS:
            circuit.x([i])
            circuit.h([i])

    circuit.barrier()


def measure_in_z(circuit, i):
    circuit.measure([i], [i])


def measure_in_x(circuit, i):
    circuit.h([i])
    measure_in_z(circuit, i)


def insert_measurements_according_to_base(bases, circuit):
    for i in range(len(bases)):
        base = bases[i]

        if base == Z_BASE:
            measure_in_z(circuit, i)
        elif base == X_BASE:
            measure_in_x(circuit, i)


def get_counts(circuit, backend, shots):
    compiled_circuit = transpile(circuit, backend)
    job = backend.run(compiled_circuit, shots=shots)
    job_monitor(job)
    result = job.result()
    counts = result.get_counts(circuit)

    return counts


def get_measurements_result(backend, circuit, shots, accuracy, size):
    measurements = []
    counts = get_counts(circuit, backend, shots)
    value_list = counts.items()

    for i in range(size):
        zeros = 0
        ones = 0

        for (key, value) in value_list:
            if key[i] == BIT_1:
                ones += value
            elif key[i] == BIT_0:
                zeros += value

        if ones > zeros:
            if ones * 100 / shots >= accuracy:
                measurements.append(BIT_1)
            else:
                random_number = str(randint(0, 1))
                measurements.append(random_number)
        elif zeros >= ones:
            if zeros * 100 / shots >= accuracy:
                measurements.append(BIT_0)
            else:
                random_number = str(randint(0, 1))
                measurements.append(random_number)

    measurements.reverse()
    return measurements


def get_same_bases_positions(first_bases, second_bases):
    positions = []
    bases_length = len(first_bases)

    for i in range(bases_length):
        first_base = first_bases[i]
        second_base = second_bases[i]

        if first_base == second_base:
            positions.append(i)

    return positions


def save_circuit_image(circuit, file_name):
    diagram = circuit_drawer(
        circuit, output="mpl", style={"backgroundcolor": "#EEEEEE"}
    )
    diagram.savefig(f"{file_name}.png", format="png")


def discard_different_positions(arr, correct_positions):
    corrected_array = []

    for i in correct_positions:
        corrected_array.append(arr[i])

    return corrected_array


# check_for_eavesdropper
def perform_privacy_amplification(alice_raw_key, bob_raw_key, bits_to_discard, accuracy):
    sequence_length = len(alice_raw_key)
    random_indexes = sample(range(sequence_length), bits_to_discard)
    matching_values = 0

    random_indexes.sort()
    print(f"Positions of bits checked: {random_indexes}")

    for i in random_indexes:
        if alice_raw_key[i] == bob_raw_key[i]:
            matching_values += 1

    if matching_values * 100 / bits_to_discard >= accuracy:
        print("Result: No eavesdropper detected\n")

        alice_sifted_key = ''
        bob_sifted_key = ''
        for i in range(sequence_length):
            if not i in random_indexes:
                alice_sifted_key += alice_raw_key[i]
                bob_sifted_key += bob_raw_key[i]

        print(f"Alice's sifted key: {alice_sifted_key}\n")
        print(f"Bob's sifted key: {bob_sifted_key}\n")
    else:
        print("Result: Eavesdropper detected. Abort protocol.")
        sys.exit(0)

def encrypt_message(message):
    encryption_key = input("Enter encryption key: ")
    encrypted_message = encrypt(message, encryption_key)
    return encrypted_message
    

def descrypt_message(encrypted_message):
    decryption_key = input("Enter decryption key: ")
    decrypted_message = decrypt(encrypted_message, decryption_key)
    return decrypted_message