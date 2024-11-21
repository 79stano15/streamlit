import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info.operators import Operator
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Nastavenie stránky Streamlit
st.title("Deutschov Algoritmus s Qiskit 🚀")
st.header("Kvantový obvod")

# Vytvorenie matic operatorov
constant_zero = [[1,0,0,0], [0,1,0,0], [0,0,0,1], [0,0,1,0]]
constant_one = [[0,1,0,0], [1,0,0,0], [0,0,0,1], [0,0,1,0]]
identity_matrix = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]
not_matrix = [[0,1,0,0], [1,0,0,0], [0,0,1,0], [0,0,0,1]]

# Vytvorenie operatorov
const_0 = Operator(constant_zero)
const_1 = Operator(constant_one)
identity = Operator(identity_matrix)
not_op = Operator(not_matrix)

# Funkcia na vytvorenie kvantového obvodu s operátorom
def create_quantum_circuit(op, label):
    qc = QuantumCircuit(2)
    qc.x(1)
    qc.h([0,1])
    qc.unitary(op, [0, 1], label=label)  # Aplikuj Oracle
    qc.h(0)
    qc.measure_all()  # Meranie všetkých qubitov
    return qc

# Vytvorenie obvodov pre rôzne operátory
qc_const_0 = create_quantum_circuit(const_0, 'Const_0')
qc_const_1 = create_quantum_circuit(const_1, 'Const_1')
qc_identity = create_quantum_circuit(identity, 'Identity')
qc_not = create_quantum_circuit(not_op, 'NOT')

# Výber Oracle z Streamlit rozhrania
st.sidebar.header("Vyber Oracle")
oracle_choice = st.sidebar.selectbox(
    "Zvoľ Oracle:", ["Constant Zero", "Constant One", "Identity", "NOT"]
)

# Výber kvantového obvodu na základe výberu používateľa
if oracle_choice == "Constant Zero":
    qc = qc_const_0
elif oracle_choice == "Constant One":
    qc = qc_const_1
elif oracle_choice == "Identity":
    qc = qc_identity
else:
    qc = qc_not

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
