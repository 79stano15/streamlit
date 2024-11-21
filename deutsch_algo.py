import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info.operators import Operator
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Nastavenie stránky Streamlit
st.title("Deutschov Algoritmus s Qiskit 🚀")
st.header("Kvantový obvod")

# Vytvorenie Oracle operátorov
constant_zero = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]  # Vždy vráti 0
constant_one = [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]  # Vždy vráti 1
balanced_not = [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]  # Vyvážená: NOT
identity_matrix = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]  # Totožnosť (Identity)

# Vytvorenie Operator objektov
const_0 = Operator(constant_zero)
const_1 = Operator(constant_one)
balanced_op = Operator(balanced_not)
identity_op = Operator(identity_matrix)

# Funkcia na vytvorenie kvantového obvodu s Oracle
def create_quantum_circuit(op, label):
    qc = QuantumCircuit(2, 1)  # 2 qubity, 1 klasický register
    qc.x(1)
    qc.h([0, 1])               # Aplikuj Hadamard na oba qubity
    qc.unitary(op, [1, 0], label=label)  # Aplikuj Oracle
    qc.h(0)                    # Aplikuj Hadamard na prvý qubit
    qc.measure(0, 0)           # Meraj prvý qubit
    return qc

# Vytvorenie obvodov pre rôzne Oracle operátory
qc_const_0 = create_quantum_circuit(const_0, 'Const_0')
qc_const_1 = create_quantum_circuit(const_1, 'Const_1')
qc_balanced = create_quantum_circuit(balanced_op, 'Balanced')
qc_identity = create_quantum_circuit(identity_op, 'Identity')

# Výber Oracle z rozhrania Streamlit
st.sidebar.header("Vyber Oracle")
oracle_choice = st.sidebar.selectbox(
    "Zvoľ Oracle:", ["Constant Zero", "Constant One", "Balanced (NOT)", "Identity"]
)

# Vyber kvantový obvod na základe výberu
if oracle_choice == "Constant Zero":
    qc = qc_const_0
elif oracle_choice == "Constant One":
    qc = qc_const_1
elif oracle_choice == "Balanced (NOT)":
    qc = qc_balanced
else:
    qc = qc_identity

# Zobrazenie vybraného obvodu
st.subheader(f"Vybraný Oracle: {oracle_choice}")
st.pyplot(qc.draw(output='mpl'))

# Simulácia výsledkov pomocou AerSimulator
simulator = AerSimulator()
compiled_circuit = transpile(qc, simulator)
job = simulator.run(compiled_circuit, shots=1024)
result = job.result()
counts = result.get_counts()

# Zobrazenie histogramu výsledkov
st.header("Výsledky simulácie")
fig, ax = plt.subplots()
plot_histogram(counts, ax=ax)
st.pyplot(fig)

# Zobrazenie výstupov v texte
st.subheader("Pozorované výstupy")
for outcome in counts:
    st.write(f"{outcome} bolo pozorované {counts[outcome]} krát")
