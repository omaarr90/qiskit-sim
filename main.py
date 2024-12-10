# This is a sample Python script.
from alice import Alice
from bob import Bob
from eve import Eve
from qiskit import QuantumCircuit

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

global_numb_qubits = 100

def simulate_bb84_without_eve(num_qubits):
    qc = QuantumCircuit(global_numb_qubits)
    alice = Alice(global_numb_qubits, qc)
    bob = Bob(global_numb_qubits, qc)
    # Call prepare_qubits explicitly
    alice.prepare_qubits()

    bob.measure_qubits()

    alice_sifted_bits, alice_matching_indices = alice.sift_key(bob.bases)
    print(alice_matching_indices)
    bob_sifted_bits = bob.sift_key(alice_matching_indices)

    print(alice_sifted_bits)
    print(bob_sifted_bits)
    print("Alice's sifted key count is:" + str(len(alice_sifted_bits)))
    print("Bob's sifted key count is:" + str(len(bob_sifted_bits)))

    if alice_sifted_bits == bob_sifted_bits:
        print("Key exchange was successful.")
    else:
        print("Key exchange failed.")

    qc.draw("mpl")

def simulate_bb84_with_eve(num_qubits):
    qc = QuantumCircuit(global_numb_qubits)
    alice = Alice(global_numb_qubits, qc)
    bob = Bob(global_numb_qubits, qc)
    eve = Eve(global_numb_qubits, qc)
    # Call prepare_qubits explicitly
    alice.prepare_qubits()
    qc.barrier(label="Alice - End")

    eve.measure_qubits()
    qc.barrier(label="Eve - End")

    bob.measure_qubits()

    alice_sifted_bits, alice_matching_indices = alice.sift_key(bob.bases)
    print(alice_matching_indices)
    bob_sifted_bits = bob.sift_key(alice_matching_indices)

    print(alice_sifted_bits)
    print(bob_sifted_bits)
    print("Alice's sifted key count is:" + str(len(alice_sifted_bits)))
    print("Bob's sifted key count is:" + str(len(bob_sifted_bits)))

    if alice_sifted_bits == bob_sifted_bits:
        print("Key exchange was successful.")
    else:
        print("Key exchange failed.")

    qc.draw("mpl")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    simulate_bb84_without_eve(100)