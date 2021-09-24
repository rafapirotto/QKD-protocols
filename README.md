# Quantum key distribution protocols implementations
This repository includes the implementations of three QKD protocols: BB84, B92, E91. All protocols can be ran using qiskit's "QasmSimulator" or the real quantum machine "ibmq_manila". Additionally, the BB84 and B92 were implemented with eavesdropping. Finally, this repository includes the code used to analyze the impact of eavesdropping in the BB84 protocol in a real quantum computer provided by IBM. All the code contained in this repository was done using python.

Executing a protocol is done using the "main.py" file contained inside each protocol's folder. Bear in mind that in order to run the implementations, IBM's SDK "qiskit" should be installed. The instructions are linked in the following section.

## Pre-requisites
* [python](https://www.python.org/downloads/)
* [qiskit](https://qiskit.org/documentation/getting_started.html)