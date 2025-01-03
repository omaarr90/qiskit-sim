# This is a sample Python script.
from alice import Alice
from bob import Bob
from eve import Eve
from qiskit import QuantumCircuit
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def simulate_bb84_without_eve(qc, num_qubits):
    alice = Alice(num_qubits, qc)
    bob = Bob(num_qubits, qc)

    # 1 Alice Prepare her qubits
    qc.barrier(label="Alice - Start")
    alice.prepare_qubits()
    qc.barrier(label="Alice - End")

    # 2 Bob Measure qubits
    qc.barrier(label="Bob - Start")
    bob.measure_qubits()
    qc.barrier(label="Bob - End")

    # 3 Bob shares his bases with Alice, and Alice only select the bits with matching bases.
    alice_sifted_bits, alice_matching_indices = alice.sift_key(bob.bases)
    # 4 Alice share her matching indices with Bob and bob select the qubits with matching indices.
    bob_sifted_bits = bob.sift_key(alice_matching_indices)

    print("Alice sifted bits: " + str(alice_sifted_bits))
    print("Bob sifted bits: " + str(bob_sifted_bits))

    if alice_sifted_bits == bob_sifted_bits:
        print("Key exchange was successful.")
    else:
        print("Key exchange failed.")
    
    alice_message = "Hello, Bob!".encode('utf-8')
    alice_ciphertext = alice.encrypt(alice_message)
    print(f"Alice's ciphertext: {alice_ciphertext}")
    bob_plaintext = bob.decrypt(alice_ciphertext)
    print(f"Bob's plaintext: {bob_plaintext}")

    bob_message = "Hello, Alice!".encode('utf-8')
    bob_ciphertext = bob.encrypt(bob_message)
    print(f"Bob's ciphertext: {bob_ciphertext}")
    alice_plaintext = alice.decrypt(bob_ciphertext)
    print(f"Alice's plaintext: {alice_plaintext}")

def simulate_bb84_with_eve(qc, num_qubits):
    alice = Alice(num_qubits, qc)
    bob = Bob(num_qubits, qc)
    eve = Eve(num_qubits, qc)

    # 1 Alice Prepare her qubits
    qc.barrier(label="Alice - Start")
    alice.prepare_qubits()
    qc.barrier(label="Alice - End")

    # 2 Eve tries to guess Alice bases and measure in same bases as Alice
    qc.barrier(label="Eve - Start")
    eve.measure_qubits()
    qc.barrier(label="Eve - End")

    # 3 Bob Measure qubits
    qc.barrier(label="Bob - Start")
    bob.measure_qubits()
    qc.barrier(label="Bob - End")
    
    # 4 Bob shares his bases with Alice, and Alice only select the bits with matching bases.
    alice_sifted_bits, alice_matching_indices = alice.sift_key(bob.bases)
    # 5 Alice share her matching indices with Bob and bob select the qubits with matching indices.
    bob_sifted_bits = bob.sift_key(alice_matching_indices)

    print("Alice sifted bits: " + str(alice_sifted_bits))
    print("Bob sifted bits: " + str(bob_sifted_bits))
    print("Alice's sifted key count is:" + str(len(alice_sifted_bits)))
    print("Bob's sifted key count is:" + str(len(bob_sifted_bits)))

    if alice_sifted_bits == bob_sifted_bits:
        print("Key exchange was successful.")
    else:
        print("Key exchange failed.")

    qc.draw("mpl")
