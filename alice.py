import random
from qiskit import QuantumCircuit
from util import Basis
from hkdf import convert
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class Alice:
    def __init__(self, num_qubits: int, qc: QuantumCircuit):
        self.qc = qc
        self.num_qubits = num_qubits
        self.bases = [random.choice([Basis.Z, Basis.X]) for _ in range(num_qubits)]
        self.bits = [random.choice([0, 1]) for _ in range(num_qubits)]
        self.key = None
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
        self.key = convert(sifted_bits,48)
        print("Alice key is:")
        print(self.key)
        return sifted_bits, matching_indices
    
    def encrypt(self, plaintext: bytes) -> bytes:
        iv = self.key[:16]
        aes_key = self.key[16:]
        cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        iv = self.key[:16]
        aes_key = self.key[16:]
        cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext