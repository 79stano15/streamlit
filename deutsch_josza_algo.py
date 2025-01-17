import streamlit as st
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info.operators import Operator
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import random
import itertools

def generate_balanced_truth_table(n):
    size = 2 ** n
    half_size = size // 2
    truth_table = [1] * half_size + [0] * half_size  # Polovica 1, polovica 0
    random.shuffle(truth_table)  # Náhodné premiešanie

    # Kontrola
    if truth_table.count(1) != half_size or truth_table.count(0) != half_size:
        raise ValueError("Truth table is not balanced!")

    return truth_table


# Funkcia na reverznú analýzu: zistenie kombinácie AND a NOT
def reverse_engineer_logic(n, truth_table):
    inputs = list(itertools.product([0, 1], repeat=n))  # Všetky vstupné kombinácie
    logic_expressions = []

    for idx, output in enumerate(truth_table):
        if output == 1:
            expression = []
            for bit_idx, bit in enumerate(inputs[idx]):
                var_name = chr(65 + bit_idx)  # Používaj veľké písmená A, B, C...
                if bit == 1:
                    expression.append(f"{var_name}")
                else:
                    expression.append(f"¬{var_name}")
            logic_expressions.append(" ∧ ".join(expression))

    final_expression = " ∨ ".join(f"({expr})" for expr in logic_expressions)
    return final_expression

def generate_oracle_matrix(n, truth_table):
    size = 2 ** (n + 1)  # Rozmery matice (n qubitov + 1 pomocný)
    matrix = np.eye(size, dtype=int)  # Začneme s jednotkovou maticou (identity)

    for i in range(size):
        input_index = i % (2 ** n)  # Index v pravdivostnej tabuľke

        if truth_table[input_index] == 1:
            matrix[i, i] = 0  # Nulujeme diagonálny prvok
            target_index = i ^ (1 << n)  # Invertujeme pomocný qubit
            matrix[i, target_index] = 1  # Nastavíme prepnutý index

    # Log matice pre overenie
    print("Generovaná Oracle matica:")
    print(matrix)
    return matrix


# Funkcia na vytvorenie kvantového obvodu s operátorom
def create_quantum_circuit(op, label, n):
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(range(n + 1))
    qc.unitary(op, list(range(n + 1)), label=label)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc

# Nastavenie stránky Streamlit
st.title("Deutsch-Joszov Algoritmus s Qiskit 🚀")
st.header("Kvantový obvod")

# Výber počtu qubitov
n = st.slider("Vyber počet qubitov:", min_value=2, max_value=6, value=3)

# Výber Oracle z Streamlit rozhrania
st.sidebar.header("Vyber Oracle")
oracle_choice = st.sidebar.selectbox(
    "Zvoľ Oracle:", ["Constant (Identity)", "Random Balanced"]
)

# Inicializácia Oracle matice a popisu
selected_matrix = None
logic_expression = None

if oracle_choice == "Constant (Identity)":
    # Identita ako Oracle
    size = 2 ** (n + 1)
    selected_matrix = np.eye(size, dtype=int)
    logic_expression = "f(x) = x (Identity Function)"
else:
    # Náhodná balancovaná funkcia
    truth_table = generate_balanced_truth_table(n)
    selected_matrix = generate_oracle_matrix(n, truth_table)
    logic_expression = reverse_engineer_logic(n, truth_table)

# Vytvorenie Oracle operátora
oracle_operator = Operator(selected_matrix)

# Zobrazenie vybraného Oracle
st.subheader(f"Vybraný Oracle: {oracle_choice}")
st.text(f"Logická kombinácia: {logic_expression}")

# Vytvorenie kvantového obvodu
qc = create_quantum_circuit(oracle_operator, "Oracle", n)

# Zobrazenie kvantového obvodu
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

# Zobrazenie matice Oracle
st.header("Matica Oracle")
fig, ax = plt.subplots()
ax.matshow(np.zeros_like(selected_matrix), cmap="binary")  # Vizualizácia matice

# Pridanie hodnôt priamo do matice
for (i, j), val in np.ndenumerate(selected_matrix):
    ax.text(j, i, f"{val}", ha='center', va='center', fontsize=8)

ax.set_xticks([])  # Skrytie číslovania stĺpcov
ax.set_yticks([])  # Skrytie číslovania riadkov
st.pyplot(fig)
