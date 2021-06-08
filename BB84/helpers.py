from qiskit import QuantumCircuit, transpile, IBMQ
from qiskit.providers.aer import QasmSimulator
from qiskit.tools.monitor import job_monitor
from qiskit.tools.visualization import circuit_drawer


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
    bases = ['Z' if bit == '0' else 'X' for bit in bit_sequence]

    return bases


def get_state(bit, base):
    if bit == '0':
        if base == 'Z':
            return '|0>'
        elif base == 'X':
            return '|+>'
    if bit == '1':
        if base == 'Z':
            return '|1>'
        elif base == 'X':
            return '|->'


def get_states(bits, bases):
    states = []

    for i in range(len(bits)):
        state = get_state(bits[i], bases[i])
        states.append(state)

    return states


def insert_states_in_circuit(circuit, states):
    for i in range(len(states)):
        state = states[i]

        if state == '|0>':
            pass
        elif state == '|1>':
            circuit.x([i])
        elif state == '|+>':
            circuit.h([i])
        elif state == '|->':
            circuit.x([i])
            circuit.h([i])


def measure_in_z(circuit, i):
    circuit.measure([i], [i])


def measure_in_x(circuit, i):
    circuit.h([i])
    measure_in_z(circuit, i)


def make_measurements(bases, circuit):
    for i in range(len(bases)):
        base = bases[i]

        if base == 'Z':
            measure_in_z(circuit, i)
        elif base == 'X':
            measure_in_x(circuit, i)


def get_same_bases_positions(first_bases, second_bases):
    positions = []
    bases_length = len(first_bases)

    for i in range(bases_length):
        first_base = first_bases[i]
        second_base = second_bases[i]

        if first_base == second_base:
            positions.append(bases_length - 1 - i)

    positions.reverse()

    return positions


def get_key(counts, shots, accuracy, valid_positions):
    final_key = ''
    value_list = counts.items()

    for i in valid_positions:
        zeros = 0
        ones = 0

        for (key, value) in value_list:
            if key[i] == '1':
                ones += value
            elif key[i] == '0':
                zeros += value

        if ones > zeros:
            if ones * 100 / shots >= accuracy:
                final_key += '1'
        elif zeros > ones:
            if zeros * 100 / shots >= accuracy:
                final_key += '0'

    return final_key


def save_circuit_image(circuit, file_name):
    diagram = circuit_drawer(circuit, output='mpl', style={'backgroundcolor': '#EEEEEE'})
    diagram.savefig(f"{file_name}.png", format="png")


def get_counts(circuit, backend, shots):
    compiled_circuit = transpile(circuit, backend)
    job = backend.run(compiled_circuit, shots=shots)
    job_monitor(job)
    result = job.result()
    counts = result.get_counts(circuit)

    return counts


def privacy_amplification():
    return None
