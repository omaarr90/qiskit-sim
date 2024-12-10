import random
from qiskit import ClassicalRegister, QuantumCircuit
from util import Basis
from qiskit_aer import AerSimulator

class Bob:
    def __init__(self, num_qubits: int, qc: QuantumCircuit):
        self.qc = qc
        self.num_qubits = num_qubits
        self.bases = [random.choice([Basis.Z, Basis.X]) for _ in range(num_qubits)]
        self.measurements = None  # Will store the measurement results

    def measure_qubits(self):
        # Add a classical register if not present
        if len(self.qc.cregs) == 0:
            self.qc.add_register(ClassicalRegister(self.num_qubits))

        for i in range(self.num_qubits):
            if self.bases[i] == Basis.X:
                self.qc.h(i)  # Rotate to measure in X basis by applying H before measurement
        self.qc.barrier()

        for i in range(self.num_qubits):
            self.qc.measure(i, i)

        # Execute the circuit on a simulator
        simulator = AerSimulator()
        job = simulator.run(self.qc, shots=1)
        result = job.result()
        counts = result.get_counts()

        # counts is a dictionary like {'010101...': 1}, we extract the key
        measured_string = list(counts.keys())[0]
        # Convert measured_string into a list of ints (0/1)
        self.measurements = [int(bit) for bit in measured_string[::-1]]
        print("Bob Measurments is:")
        print(self.measurements)

    def sift_key(self, matching_indices):
        # Return the bits that correspond to the matching bases
        if self.measurements is None:
            raise ValueError("No measurements available. Please measure first.")
        sifted_bits = [self.measurements[i] for i in matching_indices]
        return sifted_bits
