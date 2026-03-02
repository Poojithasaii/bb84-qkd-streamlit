import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# BB84 Simulation Function
def bb84_simulation(n, eve_present=False):
    alice_bits = np.random.randint(2, size=n)
    alice_bases = np.random.randint(2, size=n)
    bob_bases = np.random.randint(2, size=n)

    eve_bits = np.zeros(n)

    # Eve intercept-resend
    if eve_present:
        eve_bases = np.random.randint(2, size=n)
        for i in range(n):
            if eve_bases[i] == alice_bases[i]:
                eve_bits[i] = alice_bits[i]
            else:
                eve_bits[i] = np.random.randint(2)
    else:
        eve_bits = alice_bits.copy()

    # Bob measurement
    bob_results = np.zeros(n)
    for i in range(n):
        if bob_bases[i] == alice_bases[i]:
            bob_results[i] = eve_bits[i]
        else:
            bob_results[i] = np.random.randint(2)

    # Basis reconciliation
    sifted_key_alice = []
    sifted_key_bob = []

    for i in range(n):
        if alice_bases[i] == bob_bases[i]:
            sifted_key_alice.append(alice_bits[i])
            sifted_key_bob.append(bob_results[i])

    if len(sifted_key_alice) == 0:
        return 0

    sifted_key_alice = np.array(sifted_key_alice)
    sifted_key_bob = np.array(sifted_key_bob)

    errors = np.sum(sifted_key_alice != sifted_key_bob)
    qber = errors / len(sifted_key_alice)

    return qber


def security_check(qber):
    if qber > 0.11:
        return "⚠ Communication Compromised! Eve Detected."
    else:
        return "✅ Communication Secure. Key Accepted."


# Streamlit UI
st.title("Quantum Key Distribution - BB84 Simulation")

n = st.slider("Number of Bits", min_value=10, max_value=1000, value=100, step=10)
eve = st.checkbox("Simulate Eve (Eavesdropper)")

if st.button("Run Simulation"):
    qber = bb84_simulation(n, eve)
    st.subheader(f"QBER: {round(qber, 3)}")
    st.write(security_check(qber))

    # Graph Comparison
    n_values = [20, 50, 100, 200]
    qber_without = [bb84_simulation(x, False) for x in n_values]
    qber_with = [bb84_simulation(x, True) for x in n_values]

    fig, ax = plt.subplots()
    ax.plot(n_values, qber_without, marker='o')
    ax.plot(n_values, qber_with, marker='o')
    ax.set_xlabel("Number of Bits")
    ax.set_ylabel("QBER")
    ax.set_title("QBER Comparison")
    ax.legend(["Without Eve", "With Eve"])

    st.pyplot(fig)