import random
from qiskit import QuantumCircuit
from util import Basis

class Alice:
    def __init__(self, num_qubits: int, qc: QuantumCircuit):
        self.qc = qc
        self.num_qubits = num_qubits
        self.bases = [random.choice([Basis.Z, Basis.X]) for _ in range(num_qubits)]
        self.bits = [random.choice([0, 1]) for _ in range(num_qubits)]
        print("Alice original bits")
        print(self.bits)

    def prepare_qubits(self):
        for i in range(self.num_qubits):
            if self.bases[i] == Basis.Z:
                # Z basis
                if self.bits[i] == 1:
                    self.qc.x(i)  # Prepare |1>
            else:
                # X basis
                self.qc.h(i)    # |0> -> |+>
                if self.bits[i] == 1:
                    self.qc.z(i) # |+> -> |->

    def sift_key(self, bob_bases):
        # Find indices where Alice’s and Bob’s bases match
        matching_indices = [i for i in range(self.num_qubits) if self.bases[i] == bob_bases[i]]
        # Extract the bits that correspond to matching bases
        sifted_bits = [self.bits[i] for i in matching_indices]
        return sifted_bits, matching_indices
