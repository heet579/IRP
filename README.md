# AI & Quantum Computing in Cybersecurity
### COMP 5800 — Industry Research Project | Group M261M-1303
**Mentor:** Dr. David Dzakpasu &nbsp;|&nbsp; **Host:** Industry Research Hub

---

## Overview

This project explores how **Artificial Intelligence** and **Quantum Computing** present both threats and opportunities to modern Cybersecurity. The demonstration suite provides working Python implementations of the key algorithms discussed in the research report.

---

## Demonstration Suite

`quantum_ai_cybersecurity_demo.py` covers four algorithms:

| # | Algorithm | What it shows |
|---|-----------|---------------|
| 1 | **Shor's Algorithm** | How quantum computers can break RSA encryption by factoring semiprime integers exponentially faster than any classical algorithm |
| 2 | **Grover's Algorithm** | How quantum computers reduce AES brute-force key search from O(2ⁿ) to O(2^(n/2)), breaking AES-128 and motivating a move to AES-256 |
| 3 | **Kyber-512 KEM** | Full post-quantum key exchange (NIST FIPS 203 / ML-KEM) based on Module-LWE — KeyGen, Encapsulate, Decapsulate |
| 4 | **LSTM Anomaly Detector** | Unsupervised LSTM Autoencoder trained on normal network traffic to detect DDoS, port scans, data exfiltration, and brute-force attacks without signatures |

A **6-panel matplotlib dashboard** is generated at the end comparing all algorithms visually.

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/heet579/quantum-ai-cybersecurity.git
cd quantum-ai-cybersecurity
```

### 2. Install dependencies

```bash
pip install numpy matplotlib scikit-learn tensorflow
```

> **Python 3.10+** recommended. TensorFlow 2.x is required for the LSTM section.
> If TensorFlow is unavailable, the script automatically falls back to scikit-learn's Isolation Forest.

### 3. Run the demo

```bash
python quantum_ai_cybersecurity_demo.py
```

The script runs all four sections sequentially and opens the dashboard plot.
A PNG of the dashboard is also saved to the current directory as:
```
quantum_ai_cybersecurity_dashboard.png
```

---

## Expected Output

```
SECTION 1 — Shor's Algorithm: Quantum Threat to RSA
  N=  15 -> 3 x 5   [OK]   0.014ms
  N= 143 -> 11 x 13 [OK]   0.005ms
  N= 667 -> 23 x 29 [OK]   0.079ms

SECTION 2 — Grover's Algorithm: Quantum Threat to AES
  AES-128   Classical: 2^128   Quantum: 2^64   [BROKEN]
  AES-256   Classical: 2^256   Quantum: 2^128  [SAFE]

SECTION 3 — Kyber-512 KEM: Post-Quantum Key Exchange
  KEY AGREEMENT SUCCESS — both parties hold the same 256-bit key.

SECTION 4 — LSTM Anomaly Detector
  Accuracy: 99.6% | Precision: 98.9% | Recall: 100.0% | F1: 99.4%
```

---

## Project Structure

```
.
├── quantum_ai_cybersecurity_demo.py   # Main demo script
├── quantum_ai_cybersecurity_dashboard.png  # Generated dashboard (after running)
├── README.md
└── research/                          # Research papers (not tracked by git)
```

---

## Algorithm Details

### Shor's Algorithm (1994)
Factors an integer N in **O((log N)³)** using the Quantum Fourier Transform to find the period of f(x) = aˣ mod N. Classical general number field sieve (GNFS) requires sub-exponential time, making RSA-2048 practically unbreakable classically — but trivial for a large enough quantum computer.

### Grover's Algorithm (1996)
Provides a **quadratic speedup** over classical brute-force search. For AES with an n-bit key, Grover reduces the search from 2ⁿ to 2^(n/2) operations. AES-128 is therefore reduced to 2⁶⁴ — feasible with quantum hardware — while AES-256 remains secure at 2¹²⁸.

### CRYSTALS-Kyber / ML-KEM (NIST FIPS 203, 2024)
A **Key Encapsulation Mechanism** based on the hardness of **Module Learning With Errors (Module-LWE)**. Given a public matrix A and t = A·s + e (where s is small), it is computationally infeasible to recover s — even with a quantum computer. The demo implements exact polynomial arithmetic in Z₃₃₂₉[X]/(X²⁵⁶+1).

### LSTM Autoencoder (Anomaly Detection)
An **encoder-decoder LSTM** trained exclusively on normal network traffic. The reconstruction error of unseen traffic is compared against a threshold (μ + 3σ of normal errors). Traffic exceeding the threshold is flagged as an anomaly — no attack signatures required, enabling zero-day detection.

---

## References

- Shor, P.W. (1994). *Algorithms for quantum computation*. FOCS '94.
- Grover, L.K. (1996). *A fast quantum mechanical algorithm for database search*. STOC '96.
- Bos et al. (2018). *CRYSTALS-Kyber: a CCA-secure module-lattice-based KEM*. IEEE EuroS&P.
- NIST FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (2024).
- Malhotra et al. (2015). *Long Short Term Memory Networks for Anomaly Detection in Time Series*. ESANN.
- Khan et al. *Quantum Computing and Its Implications for Cybersecurity*. Nanotechnology Perceptions.
- Singh & Kumar (2024). *Enhancing Cyber Security Using Quantum Computing and AI: A Review*. IJARSCT.
- Dash & Ullah (2024). *Quantum-safe: Cybersecurity in the age of Quantum-Powered AI*. WJARR.

---

## Research Context

This work is part of **COMP 5800: Industry Research Project** examining:
- How quantum computers threaten current RSA/ECC public-key infrastructure
- The "Harvest Now, Decrypt Later" threat model
- NIST Post-Quantum Cryptography standardisation (Kyber, Dilithium, SPHINCS+)
- AI/ML techniques for proactive threat detection in a post-quantum world

---

*Group M261M-1303 | COMP 5800 | Mentor: Dr. David Dzakpasu*
