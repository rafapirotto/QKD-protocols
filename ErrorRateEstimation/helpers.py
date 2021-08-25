from qiskit import transpile
from qiskit.tools.monitor import job_monitor
from qiskit.tools.visualization import circuit_drawer
from constants import *

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

def getStadistic(backend, circuit, shots, expected_values):
    # this reverse is done because IBM notation is different
    # also, this only causes a difference if the expected_values array is not symmetric
    expected_values.reverse()
    counts = get_counts(circuit, backend, shots)
    value_list = counts.items()
    errors = []
    for i in range(len(expected_values)):
        zeros = 0
        ones = 0

        for (key, value) in value_list:
            if key[i] == BIT_1:
                ones += value
            elif key[i] == BIT_0:
                zeros += value
        if expected_values[i] == BIT_1:
            errors.append(ones / shots)
        else:
            errors.append(zeros / shots)

    return errors


def save_circuit_image(circuit, file_name):
    diagram = circuit_drawer(
        circuit, output="mpl", style={"backgroundcolor": "#EEEEEE"}
    )
    diagram.savefig(f"{file_name}.png", format="png")


def initialize_circuit_with_zeros(circuit):
    for i in range(circuit.num_qubits):
        circuit.reset(i)