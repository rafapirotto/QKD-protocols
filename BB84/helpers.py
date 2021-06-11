from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import QasmSimulator
from qiskit.tools.monitor import job_monitor
from qiskit.tools.visualization import circuit_drawer
from random import randint
from constants import *


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


def make_measurements(bases, circuit):
    for i in range(len(bases)):
        base = bases[i]

        if base == Z_BASE:
            measure_in_z(circuit, i)
        elif base == X_BASE:
            measure_in_x(circuit, i)


def get_same_bases_positions(first_bases, second_bases):
    positions = []
    bases_length = len(first_bases)

    for i in range(bases_length):
        first_base = first_bases[i]
        second_base = second_bases[i]

        if first_base == second_base:
            positions.append(i)

    return positions


def get_measurements(counts, shots, accuracy, size):
    measurements = []
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
        elif zeros > ones:
            if zeros * 100 / shots >= accuracy:
                measurements.append(BIT_0)
            else:
                random_number = str(randint(0, 1))
                measurements.append(random_number)

    measurements.reverse()
    return measurements


def save_circuit_image(circuit, file_name):
    print("Saving circuit image")
    diagram = circuit_drawer(
        circuit, output="mpl", style={"backgroundcolor": "#EEEEEE"}
    )
    diagram.savefig(f"{file_name}.png", format="png")


def get_counts(circuit, backend, shots):
    compiled_circuit = transpile(circuit, backend)
    job = backend.run(compiled_circuit, shots=shots)
    job_monitor(job)
    result = job.result()
    counts = result.get_counts(circuit)

    return counts


def discard_different_positions(arr, correct_positions):
    corrected_array = []

    for i in correct_positions:
        corrected_array.append(arr[i])

    return corrected_array


def privacy_amplification():
    return None
