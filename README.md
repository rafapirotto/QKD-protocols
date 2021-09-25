# Quantum key distribution protocols implementations
This repository contains the implementations of three QKD protocols: BB84, B92, E91. All protocols can be ran using qiskit's "QasmSimulator" or the real quantum machine "ibmq_manila". Additionally, the BB84 and B92 were implemented with eavesdropping. Finally, this repository includes the code used to analyze the impact of eavesdropping in the BB84 protocol in a real quantum computer provided by IBM. All the code contained in this repository was done using python.

Running a protocol is done executing the "main.py" file contained inside each protocol's folder. Bear in mind that in order to run the implementations, IBM's SDK "qiskit" should be installed. A link to the instructions of qiskit's installation is provided in the next section.

## Pre-requisites
* [python](https://www.python.org/downloads/)
* [qiskit](https://qiskit.org/documentation/getting_started.html)
