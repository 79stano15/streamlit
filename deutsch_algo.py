import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info.operators import Operator
from qiskit_aer.backends import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Nastavenie stránky Streamlit
st.title("Deutschov Algoritmus s Qiskit 🚀")
st.header("Kvantový obvod a Matica Oracle")

# Definícia Oracle operátorov ako matíc
constant_zero = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]  # Konštantná 0
constant_one = [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]  # Konštantná 1
balanced_not = [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]  # Vyvážený Oracle: NOT
identity_matrix = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]  # Totožnosť

# Vytvorenie Operator objektov
const_0 = Operator(constant_zero)
const_1 = Operator(constant_one)
balanced_op = Operator(balanced_not)
identity_op = Operator(identity_matrix)

# Funkcia na vytvorenie Deutschovho algoritmu
def deutsch_algorithm(oracle, label):
    qc = QuantumCircuit(2, 1)  # 2 qubity, 1 klasický register
    qc.x(1)                    # Inicializuj druhý qubit do stavu |1⟩
    qc.h([0, 1])               # Hadamard na oba qubity
    qc.append(oracle, [1, 0])  # Aplikuj Oracle (ako matica)
    qc.h(0)                    # Hadamard na prvý qubit
    qc.measure(0, 0)           # Meraj prvý qubit
    return qc

# Výber Oracle z Streamlit rozhrania
st.sidebar.header("Vyber Oracle")
oracle_choice = st.sidebar.selectbox(
    "Zvoľ Oracle:", ["Constant Zero", "Constant One", "Balanced NOT", "Identity"]
)

# Výber správneho Oracle a jeho matice
if oracle_choice == "Constant Zero":
    oracle, matrix, label = const_0, constant_zero, "Const_0"
elif oracle_choice == "Constant One":
    oracle, matrix, label = const_1, constant_one, "Const_1"
elif oracle_choice == "Balanced NOT":
    oracle, matrix, label = balanced_op, balanced_not, "Balanced"
else:
    oracle, matrix, label = identity_op, identity_matrix, "Identity"

# Vytvor Deutschov algoritmus s vybraným Oracle
qc = deutsch_algorithm(oracle, label)

# Zobrazenie matice Oracle
st.subheader(f"Matica Oracle pre: {oracle_choice}")
st.write(matrix)

# Zobrazenie vybraného obvodu
st.subheader(f"Kvantový obvod pre: {oracle_choice}")
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
