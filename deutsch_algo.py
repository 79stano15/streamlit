import streamlit as st
from qiskit import QuantumCircuit, Aer, transpile
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Nastavenie stránky Streamlit
st.title("Deutschov Algoritmus s Qiskit 🚀")
st.header("Kvantový obvod")

# Funkcia na vytvorenie Oracle operátorov
def constant_oracle(is_one):
    """Konštantný Oracle"""
    qc = QuantumCircuit(2)
    if is_one:
        qc.x(1)  # Ak je konštantná 1, invertuj druhý qubit
    return qc.to_gate(label="Const")

def balanced_oracle():
    """Vyvážený Oracle"""
    qc = QuantumCircuit(2)
    qc.cx(0, 1)  # CNOT brána: Vyvážené správanie
    return qc.to_gate(label="Balanced")

# Funkcia na vytvorenie Deutschovho algoritmu
def deutsch_algorithm(oracle):
    qc = QuantumCircuit(2, 1)  # 2 qubity, 1 klasický register
    qc.x(1)                    # Inicializuj druhý qubit do stavu |1⟩
    qc.h([0, 1])               # Hadamard na oba qubity
    qc.append(oracle, [0, 1])  # Aplikuj Oracle
    qc.h(0)                    # Hadamard na prvý qubit
    qc.measure(0, 0)           # Meraj prvý qubit
    return qc

# Výber Oracle z Streamlit rozhrania
st.sidebar.header("Vyber Oracle")
oracle_choice = st.sidebar.selectbox(
    "Zvoľ Oracle:", ["Constant Zero", "Constant One", "Balanced"]
)

# Vyber správny Oracle na základe voľby používateľa
if oracle_choice == "Constant Zero":
    oracle = constant_oracle(is_one=False)
elif oracle_choice == "Constant One":
    oracle = constant_oracle(is_one=True)
else:
    oracle = balanced_oracle()

# Vytvor Deutschov algoritmus s vybraným Oracle
qc = deutsch_algorithm(oracle)

# Zobrazenie kvantového obvodu
st.subheader(f"Vybraný Oracle: {oracle_choice}")
st.pyplot(qc.draw(output='mpl'))

# Simulácia výsledkov pomocou AerSimulator
simulator = Aer.get_backend('aer_simulator')
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
