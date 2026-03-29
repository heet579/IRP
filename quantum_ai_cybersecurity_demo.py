#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=======================================================================
  AI & Quantum Computing in Cybersecurity — Demonstration Suite
  COMP 5800: Industry Research Project  |  Group M261M-1303
  Mentor: Dr. David Dzakpasu           |  Host: Industry Research Hub
=======================================================================

DEMONSTRATIONS
--------------
  [1]  Shor's Algorithm        — How quantum computers break RSA
  [2]  Grover's Algorithm      — How quantum computers weaken AES
  [3]  Kyber-512 KEM           — NIST post-quantum key exchange
  [4]  LSTM Anomaly Detector   — AI-powered network intrusion detection
  [5]  Security Dashboard      — Comparative analysis & visualisations

REQUIREMENTS
------------
  pip install numpy matplotlib scikit-learn tensorflow

REFERENCES
----------
  • Shor, P.W. (1994). Algorithms for quantum computation.  FOCS '94.
  • Grover, L.K. (1996). A fast quantum mechanical algorithm.  STOC '96.
  • Bos et al. (2018). CRYSTALS-Kyber. IEEE EuroS&P.
  • NIST FIPS 203 (ML-KEM, 2024).
  • Malhotra et al. (2015). Long Short Term Memory Networks for Anomaly
    Detection in Time Series.  ESANN.
=======================================================================
"""

import io
import sys
import time
import math
import random
import hashlib
import warnings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

# Force UTF-8 on Windows consoles (cp1252 can't display box-drawing chars)
if hasattr(sys.stdout, "buffer") and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                  errors="replace", line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8",
                                  errors="replace", line_buffering=True)

warnings.filterwarnings("ignore")

# ── ANSI colour helpers ───────────────────────────────────────────────
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

def banner(title, color=CYAN):
    w = 70
    print(f"\n{color}{BOLD}{'═' * w}{RESET}")
    print(f"{color}{BOLD}  {title}{RESET}")
    print(f"{color}{BOLD}{'═' * w}{RESET}\n")

def step(msg):    print(f"  {CYAN}▶{RESET}  {msg}")
def ok(msg):      print(f"  {GREEN}✔{RESET}  {msg}")
def warn(msg):    print(f"  {YELLOW}⚠{RESET}  {msg}")
def info(msg):    print(f"  {DIM}{msg}{RESET}")


# =======================================================================
#  SECTION 1 — SHOR'S ALGORITHM: Quantum Threat to RSA
# =======================================================================

def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def _order_finding(a: int, N: int) -> int | None:
    """
    Simulate the quantum period-finding subroutine of Shor's algorithm.

    On a real quantum computer this subroutine uses the Quantum Fourier
    Transform and runs in O((log N)^3).  Here we perform it classically
    to illustrate the algorithm's logic — the classical version is
    exponentially slower, which is precisely why a quantum computer
    gives an exponential speed-up.
    """
    for r in range(1, N * 4):
        if pow(a, r, N) == 1:
            return r
    return None

def shors_factor(N: int) -> tuple[int, int] | tuple[None, None]:
    """
    Shor's algorithm: factor N into two non-trivial prime factors.

    Steps
    -----
    1.  Pick random a ∈ [2, N-1].
    2.  If gcd(a, N) > 1 we got lucky — that gcd is a factor.
    3.  (Quantum step) Find the period r of f(x) = aˣ mod N.
    4.  If r is even, compute gcd(a^(r/2) ± 1, N).
    5.  Return the non-trivial factor pair.
    """
    if N % 2 == 0:
        return 2, N // 2

    for _ in range(40):
        a = random.randint(2, N - 1)
        g = _gcd(a, N)
        if g > 1:
            return g, N // g

        r = _order_finding(a, N)
        if r is None or r % 2 != 0:
            continue

        x = pow(a, r // 2, N)
        p = _gcd(x - 1, N)
        q = _gcd(x + 1, N)

        if 1 < p < N:
            return p, N // p
        if 1 < q < N:
            return q, N // q

    return None, None

def demo_shors() -> tuple:
    banner("SECTION 1 — Shor's Algorithm: Quantum Threat to RSA", CYAN)

    print(
        "  RSA encryption is secured by the MATHEMATICAL HARDNESS of\n"
        "  factoring a large semiprime  N = p × q.\n\n"
        f"  {'Algorithm':<35} {'Complexity':<28} {'RSA-2048 estimate'}\n"
        f"  {'─'*35} {'─'*28} {'─'*22}\n"
        f"  {'Classical (GNFS)':<35} {'O(exp(n^(1/3)·(log n)^(2/3)))':<28} {'~10¹⁷ years'}\n"
        f"  {'Quantum  (Shor)':<35} {'O((log n)³)  [polynomial]':<28} {'~minutes'}\n"
    )

    test_cases = [
        (15,  "p= 3, q= 5"),
        (21,  "p= 3, q= 7"),
        (35,  "p= 5, q= 7"),
        (77,  "p= 7, q=11"),
        (143, "p=11, q=13"),
        (323, "p=17, q=19"),
        (667, "p=23, q=29"),
    ]

    print(f"  {'N':>6}  {'Factors':>14}  {'Verify':>8}  {'Time (ms)':>10}  {'Label'}")
    print(f"  {'─'*6}  {'─'*14}  {'─'*8}  {'─'*10}  {'─'*20}")

    for N, label in test_cases:
        t0 = time.perf_counter()
        p, q = shors_factor(N)
        ms = (time.perf_counter() - t0) * 1000
        if p and q:
            verify = "✔" if p * q == N else "✗"
            print(f"  {N:>6}  {p:>6} × {q:<6}  {verify:>8}  {ms:>9.3f}  {label}")
        else:
            warn(f"  N={N} — factoring failed (retry)")

    print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  REAL-WORLD IMPACT                                               │
  │  • RSA-2048 secures TLS, SSH, banking, HTTPS (all major infra)  │
  │  • A 4,096-logical-qubit computer breaks RSA-2048 in minutes     │
  │  • IBM / Google roadmap: fault-tolerant qubits by ~2030–2035     │
  │  • "Harvest Now, Decrypt Later" attacks ARE happening today      │
  └──────────────────────────────────────────────────────────────────┘
    """)

    # Data for plot ── log₁₀(operations) vs key size
    bit_sizes = np.arange(512, 4097, 64)
    # GNFS: exp(1.923 · n^(1/3) · (ln n)^(2/3))
    classical = np.array([
        1.923 * (b ** (1/3)) * (math.log(b) ** (2/3)) / math.log(10)
        for b in bit_sizes
    ])
    # Shor: O((log n)^3) — polynomial
    quantum = np.array([3 * math.log10(b) for b in bit_sizes])

    return bit_sizes, classical, quantum


# =======================================================================
#  SECTION 2 — GROVER'S ALGORITHM: Quantum Threat to AES
# =======================================================================

def demo_grovers() -> None:
    banner("SECTION 2 — Grover's Algorithm: Quantum Threat to AES", CYAN)

    print(
        "  AES symmetric encryption is secured by BRUTE-FORCE hardness:\n"
        "  an attacker must try up to 2ⁿ keys to break an n-bit key.\n\n"
        "  Grover's algorithm provides a QUADRATIC speedup via amplitude\n"
        "  amplification, reducing the key search from O(2ⁿ) → O(2^(n/2)).\n"
    )

    print(
        f"  {'Scheme':<12} {'Classical (bits)':<20} {'After Grover':<20} {'Status'}\n"
        f"  {'─'*12} {'─'*20} {'─'*20} {'─'*28}"
    )

    rows = [
        ("AES-128",  128, 64,  f"{RED}BROKEN   — 2^64 is feasible{RESET}"),
        ("AES-192",  192, 96,  f"{YELLOW}MARGINAL — borderline safe{RESET}"),
        ("AES-256",  256, 128, f"{GREEN}SAFE     — 2^128 still secure{RESET}"),
    ]
    for name, c, q, status in rows:
        print(f"  {name:<12} 2^{c:<18} 2^{q:<18} {status}")

    # Simulate Grover's search on a mini key-space
    TARGET       = 137
    SPACE        = 1024   # tiny "key space" for demo
    grover_iters = int(math.pi / 4 * math.sqrt(SPACE))

    print(f"\n  Live simulation on a {SPACE}-element search space (target = {TARGET}):\n")

    step("Classical brute-force:")
    classic_steps = next(i + 1 for i in range(SPACE) if i == TARGET)
    ok(f"Found in {classic_steps} steps  (linear scan, worst case {SPACE})")

    step("Grover's quantum search:")
    ok(f"Expected convergence in ~{grover_iters} iterations  (√{SPACE} speedup)")
    ok(f"Speed-up factor: {classic_steps / grover_iters:.1f}×  "
       f"(for AES-128: 2^128 → 2^64 = 18 billion billion ops)")

    print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  NIST RECOMMENDATION (post-quantum era)                          │
  │  • Migrate from AES-128  →  AES-256                              │
  │  • AES-256 maintains 128-bit quantum security  (acceptable)      │
  │  • This is a symmetric-key upgrade — relatively low-cost fix     │
  └──────────────────────────────────────────────────────────────────┘
    """)


# =======================================================================
#  SECTION 3 — CRYSTALS-KYBER KEM: Post-Quantum Defence
# =======================================================================

class Kyber512:
    """
    Simplified CRYSTALS-Kyber (ML-KEM) Key Encapsulation Mechanism.

    Security foundation
    -------------------
    The hardness of the Module Learning With Errors (Module-LWE) problem:
    given (A, t = A·s + e) it is computationally infeasible to recover
    the small secret vector s — even with a quantum computer.

    Parameter set  (matching NIST FIPS 203 Kyber-512)
    --------------------------------------------------
    n  = 256    polynomial degree
    q  = 3329   prime modulus
    k  = 2      module rank (number of polynomial components)
    η₁ = 3      noise distribution for key generation
    η₂ = 2      noise distribution for encryption

    Security level: ~128-bit classical, ~128-bit quantum (NIST Level 1)

    NOTE: Production Kyber uses the Number Theoretic Transform (NTT)
    for O(n log n) polynomial multiplication over Z_3329.  This demo
    uses exact convolution arithmetic (O(n²)) which is slower but
    produces identical, mathematically correct results.
    """

    N  = 256    # polynomial degree
    Q  = 3329   # prime modulus
    K  = 2      # module dimension
    E1 = 3      # η₁: noise for keygen
    E2 = 2      # η₂: noise for encapsulation

    # ── Low-level polynomial arithmetic ──────────────────────────────

    def _cbd(self, eta: int, n: int) -> np.ndarray:
        """Sample n coefficients from the Centred Binomial Distribution CBD(η)."""
        a = np.random.randint(0, 2, (n, eta)).sum(axis=1)
        b = np.random.randint(0, 2, (n, eta)).sum(axis=1)
        return (a - b).astype(np.int64) % self.Q

    def _poly_mul(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Multiply two degree-(n-1) polynomials in  Z_q[X] / (X^n + 1).

        The ring identity X^n ≡ -1 means coefficients that "wrap around"
        past degree n-1 are subtracted from the lower-degree position.
        """
        n, q = self.N, self.Q
        conv = np.convolve(a, b)          # length 2n-1 integer convolution
        result = conv[:n].copy()
        result[:len(conv) - n] -= conv[n:]   # X^n ≡ -1 reduction
        return result % q

    def _poly_add(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return (a + b) % self.Q

    def _mat_vec(self, M, v) -> list:
        """Multiply k×k polynomial matrix M by polynomial vector v."""
        out = []
        for row in M:
            acc = np.zeros(self.N, dtype=np.int64)
            for mij, vj in zip(row, v):
                acc = self._poly_add(acc, self._poly_mul(mij, vj))
            out.append(acc)
        return out

    def _uniform_poly(self) -> np.ndarray:
        """Sample a polynomial with coefficients uniform in [0, q)."""
        return np.random.randint(0, self.Q, self.N, dtype=np.int64)

    # ── KEM operations ────────────────────────────────────────────────

    def keygen(self):
        """
        Key Generation
        --------------
        Private key:  s  — small coefficient vector (from CBD)
        Public key:   (A, t)  where  t = A·s + e  (Module-LWE instance)

        An attacker who sees (A, t) cannot recover s without solving
        Module-LWE — believed hard even for quantum adversaries.
        """
        A  = [[self._uniform_poly() for _ in range(self.K)] for _ in range(self.K)]
        s  = [self._cbd(self.E1, self.N) for _ in range(self.K)]
        e  = [self._cbd(self.E1, self.N) for _ in range(self.K)]
        As = self._mat_vec(A, s)
        t  = [self._poly_add(As[i], e[i]) for i in range(self.K)]
        return (A, t), s   # (public_key, secret_key)

    def encapsulate(self, pk):
        """
        Encapsulation  (Bob → Alice)
        ----------------------------
        Given Alice's public key (A, t):
          1. Sample a random message m ∈ {0,1}^n
          2. Choose ephemeral randomness r, e₁, e₂
          3. Compute ciphertext  (u, v):
               u = Aᵀ·r + e₁
               v = tᵀ·r + e₂ + ⌊q/2⌋·m
          4. Shared secret = SHA-256(m)
        """
        A, t = pk
        m  = np.random.randint(0, 2, self.N, dtype=np.int64)
        r  = [self._cbd(self.E1, self.N) for _ in range(self.K)]
        e1 = [self._cbd(self.E2, self.N) for _ in range(self.K)]
        e2 = self._cbd(self.E2, self.N)

        AT  = [[A[j][i] for j in range(self.K)] for i in range(self.K)]
        ATr = self._mat_vec(AT, r)
        u   = [self._poly_add(ATr[i], e1[i]) for i in range(self.K)]

        # tᵀ · r
        tr = np.zeros(self.N, dtype=np.int64)
        for i in range(self.K):
            tr = self._poly_add(tr, self._poly_mul(t[i], r[i]))

        # v = tᵀ·r + e₂ + ⌊q/2⌋·m
        m_enc = (m * (self.Q // 2)) % self.Q
        v     = self._poly_add(self._poly_add(tr, e2), m_enc)

        shared_secret = hashlib.sha3_256(m.tobytes()).hexdigest()
        return shared_secret, (u, v)

    def decapsulate(self, sk, ciphertext):
        """
        Decapsulation  (Alice)
        ----------------------
        Using secret key s and ciphertext (u, v):
          1.  w = v - sᵀ·u  ≈  ⌊q/2⌋·m  +  small_noise
          2.  Decode: round each coefficient to 0 or ⌊q/2⌋
          3.  Shared secret = SHA-256(m̂)

        Correctness holds because the noise terms e, e₁, e₂ are small:
          v - sᵀ·u = ⌊q/2⌋·m + e₂ + eᵀ·r  (where eᵀ·r is small)
        """
        s = sk
        u, v = ciphertext

        su = np.zeros(self.N, dtype=np.int64)
        for i in range(self.K):
            su = self._poly_add(su, self._poly_mul(s[i], u[i]))

        w       = (v - su) % self.Q
        half_q  = self.Q // 2
        quarter = half_q // 2
        m_hat   = np.where(np.minimum(w, self.Q - w) < quarter, 0, 1).astype(np.int64)

        return hashlib.sha3_256(m_hat.tobytes()).hexdigest()


def demo_kyber() -> tuple:
    banner("SECTION 3 — Kyber-512 KEM: Post-Quantum Key Exchange", GREEN)

    print(
        "  CRYSTALS-Kyber (standardised as NIST FIPS 203 ML-KEM, 2024)\n"
        "  is the world's leading post-quantum Key Encapsulation Mechanism.\n\n"
        "  Security basis: Module Learning With Errors (Module-LWE)\n"
        "  Resistant to:   Shor's algorithm, quantum Fourier sampling,\n"
        "                  and all known classical + quantum attacks.\n"
    )

    kyber = Kyber512()

    # ── Key Generation ────────────────────────────────────────────────
    step("Alice  →  KeyGen()  ─ generating public/private key pair …")
    t0 = time.perf_counter()
    pk, sk = kyber.keygen()
    kg_ms  = (time.perf_counter() - t0) * 1000
    ok(f"Key pair generated in {kg_ms:.1f} ms")
    ok(f"Public key  : matrix A  ({kyber.K}×{kyber.K} polynomials in Z_{kyber.Q}[X]/(X^{kyber.N}+1))")
    ok(f"              + vector t ({kyber.K} polynomials  =  A·s + e)")
    ok(f"Secret key  : s ({kyber.K} polynomials, coefficients ∈ CBD(η={kyber.E1}))")
    info(f"  Max |secret coeff|: {max(abs(int(c) if int(c) < kyber.Q//2 else int(c) - kyber.Q) for poly in sk for c in poly)}")

    # ── Encapsulation ─────────────────────────────────────────────────
    print()
    step("Bob    →  Encapsulate(pk)  ─ deriving shared secret …")
    t0 = time.perf_counter()
    ss_bob, ct = kyber.encapsulate(pk)
    enc_ms = (time.perf_counter() - t0) * 1000
    ok(f"Encapsulated in {enc_ms:.1f} ms")
    ok(f"Shared secret (Bob):   {ss_bob[:48]}…")
    ok(f"Ciphertext:  u ({kyber.K} polynomials) + v (1 polynomial)")

    # ── Decapsulation ─────────────────────────────────────────────────
    print()
    step("Alice  →  Decapsulate(sk, ct)  ─ recovering shared secret …")
    t0 = time.perf_counter()
    ss_alice = kyber.decapsulate(sk, ct)
    dec_ms   = (time.perf_counter() - t0) * 1000
    ok(f"Decapsulated in {dec_ms:.1f} ms")
    ok(f"Shared secret (Alice): {ss_alice[:48]}…")

    # ── Verify key agreement ──────────────────────────────────────────
    print()
    if ss_alice == ss_bob:
        print(f"  {GREEN}{BOLD}✔  KEY AGREEMENT SUCCESS — both parties hold the same 256-bit key.{RESET}")
    else:
        print(f"  {RED}✗  Decryption error (noise was too large in this trial — retry).{RESET}")
        info("  Production Kyber uses exact NTT arithmetic to guarantee correctness.")

    print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  KEY SIZE COMPARISON (bytes)                                     │
  │                       Public Key   Private Key   Quantum-safe?  │
  │  RSA-2048             256 B        1,193 B        ✗  No         │
  │  ECC-256              64 B           32 B         ✗  No         │
  │  Kyber-512 (Level 1)  800 B        1,632 B        ✔  Yes        │
  │  Kyber-768 (Level 3)  1,184 B      2,400 B        ✔  Yes        │
  │  Kyber-1024 (Level 5) 1,568 B      3,168 B        ✔  Yes        │
  └──────────────────────────────────────────────────────────────────┘
    """)

    return kg_ms, enc_ms, dec_ms


# =======================================================================
#  SECTION 4 — LSTM ANOMALY DETECTOR: AI-Powered IDS
# =======================================================================

def _generate_traffic(n_normal: int = 900, n_attack: int = 100, seed: int = 42):
    """
    Generate synthetic network-flow feature data.

    Feature vector (6 normalised columns)
    --------------------------------------
    0  packet_rate       packets / second  (normalised)
    1  byte_rate         bytes / second    (normalised)
    2  connection_count  active TCP conns  (normalised)
    3  port_entropy      Shannon H of dst ports
    4  duration_mean     mean flow length  (normalised)
    5  tcp_error_rate    retransmits / RST ratio
    """
    rng = np.random.default_rng(seed)
    n   = n_attack // 4

    # Normal traffic — correlated, moderate values
    normal = np.clip(rng.normal(0.30, 0.07, (n_normal, 6)), 0.05, 0.65)

    # ── Attack patterns ───────────────────────────────────────────────
    def _base(size):
        return np.clip(rng.normal(0.30, 0.07, (size, 6)), 0.05, 0.65)

    # DDoS: extreme packet & byte spike, many connections
    ddos         = _base(n)
    ddos[:, 0]   = rng.uniform(0.88, 1.00, n)  # packet_rate ↑↑
    ddos[:, 1]   = rng.uniform(0.82, 1.00, n)  # byte_rate   ↑↑
    ddos[:, 2]   = rng.uniform(0.78, 0.98, n)  # conns       ↑↑

    # Port scan: high port entropy, many short connections
    scan         = _base(n)
    scan[:, 2]   = rng.uniform(0.72, 0.95, n)  # conns        ↑
    scan[:, 3]   = rng.uniform(0.88, 1.00, n)  # port_entropy ↑↑
    scan[:, 4]   = rng.uniform(0.01, 0.08, n)  # duration     ↓↓

    # Data exfiltration: high bytes, very few connections (stealthy)
    exfil        = _base(n)
    exfil[:, 1]  = rng.uniform(0.78, 1.00, n)  # byte_rate ↑↑
    exfil[:, 2]  = rng.uniform(0.01, 0.12, n)  # conns     ↓↓

    # Brute-force: high TCP errors, many connections
    remainder    = n_attack - 3 * n
    brute        = _base(remainder)
    brute[:, 5]  = rng.uniform(0.82, 1.00, remainder)  # error_rate ↑↑
    brute[:, 2]  = rng.uniform(0.72, 0.92, remainder)  # conns      ↑

    attacks = np.vstack([ddos, scan, exfil, brute])
    attacks = np.clip(attacks, 0.0, 1.0)

    attack_labels = (
        ["DDoS"]        * n +
        ["Port Scan"]   * n +
        ["Exfiltration"]* n +
        ["Brute Force"] * remainder
    )
    return normal, attacks, attack_labels

def _make_sequences(data: np.ndarray, seq_len: int = 12) -> np.ndarray:
    return np.array([data[i:i+seq_len] for i in range(len(data) - seq_len + 1)])


def demo_lstm() -> tuple:
    banner("SECTION 4 — LSTM Anomaly Detector: AI-Powered IDS", GREEN)

    print(
        "  An LSTM Autoencoder learns the NORMAL temporal patterns of\n"
        "  network traffic from unlabelled data.  At inference time,\n"
        "  traffic that cannot be reconstructed accurately triggers an\n"
        "  alert — without needing a single attack signature.\n\n"
        "  Architecture:  Input → LSTM Encoder → Bottleneck →\n"
        "                 LSTM Decoder → Reconstruction\n"
        "  Threshold:     μ(normal error) + 3σ  →  ALERT\n"
    )

    SEQ = 12
    F   = 6    # features
    ATTACK_TYPES = ["DDoS", "Port Scan", "Exfiltration", "Brute Force"]

    step("Generating synthetic network traffic …")
    normal, attacks, atk_labels = _generate_traffic(n_normal=900, n_attack=100)
    ok(f"Normal flows:  {len(normal):,}")
    ok(f"Attack flows:  {len(attacks):,}  ({', '.join(ATTACK_TYPES)})")

    TRAIN_N = 700
    X_train = _make_sequences(normal[:TRAIN_N], SEQ)
    X_val   = _make_sequences(normal[TRAIN_N:], SEQ)
    X_atk   = _make_sequences(attacks, SEQ)

    try:
        import tensorflow as tf
        from tensorflow.keras import Model
        from tensorflow.keras.layers import (Input, LSTM, Dense,
                                              RepeatVector, TimeDistributed)
        from tensorflow.keras.callbacks import EarlyStopping
        tf.get_logger().setLevel("ERROR")

        step(f"TensorFlow {tf.__version__} — building LSTM Autoencoder …")

        inp     = Input(shape=(SEQ, F))
        encoded = LSTM(48, activation="tanh", return_sequences=False)(inp)
        rep     = RepeatVector(SEQ)(encoded)
        decoded = LSTM(48, activation="tanh", return_sequences=True)(rep)
        out     = TimeDistributed(Dense(F))(decoded)
        model   = Model(inp, out)
        model.compile(optimizer="adam", loss="mse")

        param_count = model.count_params()
        ok(f"Model:  Input({SEQ}×{F}) → LSTM(48) → RepeatVector → LSTM(48) → Output({SEQ}×{F})")
        ok(f"Trainable parameters: {param_count:,}")

        step("Training on normal traffic only  (early stopping, patience=8) …")
        history = model.fit(
            X_train, X_train,
            validation_data=(X_val, X_val),
            epochs=80,
            batch_size=32,
            callbacks=[EarlyStopping(monitor="val_loss", patience=8,
                                     restore_best_weights=True, verbose=0)],
            verbose=0
        )
        epochs_done = len(history.history["loss"])
        ok(f"Training complete — {epochs_done} epochs  |  "
           f"val_loss = {history.history['val_loss'][-1]:.6f}")

        err_norm = np.mean((X_val  - model.predict(X_val,  verbose=0))**2, axis=(1,2))
        err_atk  = np.mean((X_atk  - model.predict(X_atk,  verbose=0))**2, axis=(1,2))
        train_loss = history.history["loss"]
        val_loss   = history.history["val_loss"]

    except ImportError:
        warn("TensorFlow not found — falling back to Isolation Forest (sklearn)")
        from sklearn.ensemble import IsolationForest

        step("Training Isolation Forest on normal traffic …")
        clf = IsolationForest(n_estimators=300, contamination=0.05, random_state=42)
        clf.fit(normal[:TRAIN_N])
        ok("Isolation Forest trained (300 estimators)")

        err_norm = -clf.score_samples(normal[TRAIN_N:])
        err_atk  = -clf.score_samples(attacks)
        train_loss = val_loss = None

    # ── Evaluation ────────────────────────────────────────────────────
    threshold = err_norm.mean() + 3 * err_norm.std()

    tp = int((err_atk  > threshold).sum())
    fp = int((err_norm > threshold).sum())
    tn = int((err_norm <= threshold).sum())
    fn = int((err_atk  <= threshold).sum())

    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec  = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1   = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    acc  = (tp + tn) / (tp + tn + fp + fn)
    fpr  = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    print()
    ok(f"Threshold (μ + 3σ)    :  {threshold:.5f}")
    ok(f"Attacks detected (TP) :  {tp} / {len(err_atk)}")
    ok(f"False alarms    (FP)  :  {fp} / {len(err_norm)}")
    print()
    ok(f"Accuracy   :  {acc:.1%}   |  Precision : {prec:.1%}")
    ok(f"Recall     :  {rec:.1%}   |  F1-Score  : {f1:.1%}")
    ok(f"False Positive Rate:  {fpr:.1%}")

    print(f"""
  ┌──────────────────────────────────────────────────────────────────┐
  │  WHY AI OVER SIGNATURE-BASED IDS?                                │
  │  • Detects zero-day attacks  (no prior signature needed)         │
  │  • Learns evolving baselines  (adaptive, not static rules)       │
  │  • Works on encrypted traffic  (behaviour, not payload)          │
  │  • Complements post-quantum crypto at the network layer          │
  └──────────────────────────────────────────────────────────────────┘
    """)

    return err_norm, err_atk, threshold, atk_labels, train_loss, val_loss


# =======================================================================
#  SECTION 5 — SECURITY DASHBOARD: Matplotlib Visualisation
# =======================================================================

def _style(ax, title, xlabel="", ylabel=""):
    """Apply a consistent dark-mode style to an axes."""
    BG, FG, GRID = "#161b22", "#e6edf3", "#30363d"
    ax.set_facecolor(BG)
    ax.set_title(title, color=FG, fontsize=10, fontweight="bold", pad=7)
    ax.set_xlabel(xlabel, color="#8b949e", fontsize=8)
    ax.set_ylabel(ylabel, color="#8b949e", fontsize=8)
    ax.tick_params(colors=FG, labelsize=7)
    for sp in ax.spines.values():
        sp.set_edgecolor(GRID)
    ax.grid(True, color=GRID, alpha=0.45, linestyle="--", linewidth=0.8)


def plot_dashboard(
    bit_sizes, cls_ops, qnt_ops,
    kyber_times,
    err_norm, err_atk, threshold,
    atk_labels, train_loss, val_loss
):
    banner("SECTION 5 — Security Dashboard", YELLOW)
    step("Rendering visualisation …")

    fig = plt.figure(figsize=(20, 15))
    fig.patch.set_facecolor("#0d1117")
    gs  = GridSpec(3, 3, figure=fig, hspace=0.50, wspace=0.38)

    R, G, O, B = "#f85149", "#3fb950", "#f0883e", "#58a6ff"
    FG = "#e6edf3"

    # ── 1. RSA: Classical vs Quantum complexity ───────────────────────
    ax1 = fig.add_subplot(gs[0, :2])
    ax1.plot(bit_sizes, cls_ops, color=R, lw=2.5,
             label="Classical (GNFS) — sub-exponential")
    ax1.plot(bit_sizes, qnt_ops, color=G, lw=2.5,
             label="Quantum (Shor's)  — polynomial O((log n)³)")
    ax1.axvline(2048, color=O,   lw=1.5, ls="--", alpha=0.85,
                label="RSA-2048  (TLS / banking standard)")
    ax1.axvline(4096, color=B,   lw=1.5, ls="--", alpha=0.85,
                label="RSA-4096  (high-security infra)")
    ax1.fill_between(bit_sizes, cls_ops, qnt_ops, alpha=0.08, color=G)
    _style(ax1, "Shor's Algorithm — RSA Factoring Complexity (log₁₀ ops)",
           "RSA Key Size (bits)", "log₁₀(Operations Required)")
    ax1.legend(framealpha=0.15, labelcolor=FG, fontsize=8)

    # ── 2. Grover's speedup bar chart ─────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 2])
    keys = [64, 80, 96, 112, 128, 192, 256]
    cls_g, qnt_g = keys, [k // 2 for k in keys]
    x = np.arange(len(keys))
    w = 0.36
    ax2.bar(x - w/2, cls_g, w, color=R, alpha=0.82, label="Classical")
    ax2.bar(x + w/2, qnt_g, w, color=G, alpha=0.82, label="Grover")
    ax2.axhline(128, color=O, lw=1.8, ls="--", label="128-bit floor")
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"AES-{k}" for k in keys], rotation=38,
                        ha="right", fontsize=7)
    _style(ax2, "Grover's Algorithm — AES Security Reduction",
           "", "Effective Security (bits)")
    ax2.legend(framealpha=0.15, labelcolor=FG, fontsize=7)

    # ── 3. Key size comparison ────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 0])
    schemes   = ["RSA\n2048", "ECC\n256", "Kyber\n512", "Kyber\n768", "Kyber\n1024"]
    pub_kb    = [256,  64,  800,  1184, 1568]
    priv_kb   = [1193,  32, 1632, 2400, 3168]
    col_bar   = [R, R, G, G, G]
    x3 = np.arange(len(schemes))
    ax3.bar(x3 - 0.2, pub_kb,  0.36, color=col_bar, alpha=0.85, label="Public key (B)")
    ax3.bar(x3 + 0.2, priv_kb, 0.36, color=col_bar, alpha=0.50, label="Private key (B)")
    ax3.set_xticks(x3)
    ax3.set_xticklabels(schemes, fontsize=7.5)
    _style(ax3, "Key Sizes: Classical vs Kyber (bytes)", "", "Bytes")
    ax3.legend(
        handles=[mpatches.Patch(color=R, label="Quantum-vulnerable"),
                 mpatches.Patch(color=G, label="Quantum-safe (PQC)")],
        framealpha=0.15, labelcolor=FG, fontsize=8
    )

    # ── 4. Kyber operation timings ────────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 1])
    ops   = ["KeyGen", "Encapsulate", "Decapsulate"]
    times = list(kyber_times)
    bars  = ax4.bar(ops, times, color=[B, G, O], alpha=0.85, edgecolor="none")
    for bar, t in zip(bars, times):
        ax4.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + max(times) * 0.02,
                 f"{t:.1f} ms", ha="center",
                 color=FG, fontsize=9, fontweight="bold")
    _style(ax4, "Kyber-512 KEM Operation Latency", "", "Time (ms)")

    # ── 5. Error distribution histogram ──────────────────────────────
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.hist(err_norm, bins=35, color=G, alpha=0.72,
             label=f"Normal  (n={len(err_norm)})", density=True)
    ax5.hist(err_atk,  bins=35, color=R, alpha=0.72,
             label=f"Attacks (n={len(err_atk)})",  density=True)
    ax5.axvline(threshold, color=O, lw=2.2, ls="--",
                label=f"Threshold = {threshold:.4f}")
    _style(ax5, "LSTM — Reconstruction Error Distribution",
           "MSE Reconstruction Error", "Density")
    ax5.legend(framealpha=0.15, labelcolor=FG, fontsize=8)

    # ── 6. Timeline — anomaly detection ──────────────────────────────
    ax6 = fig.add_subplot(gs[2, :])
    n_show = min(150, len(err_norm))
    a_show = min(len(err_atk), 100)

    timeline = np.concatenate([err_norm[:n_show], err_atk[:a_show]])
    labels   = np.concatenate([np.zeros(n_show),  np.ones(a_show)])
    idx      = np.arange(len(timeline))

    ax6.scatter(idx[labels == 0], timeline[labels == 0],
                color=G, s=18, alpha=0.65, label="Normal traffic", zorder=3)
    ax6.scatter(idx[labels == 1], timeline[labels == 1],
                color=R, s=40, alpha=0.90, marker="^",
                label="Attack traffic (DDoS / Scan / Exfil / BruteForce)", zorder=4)
    ax6.axhline(threshold, color=O, lw=2, ls="--",
                label=f"Detection threshold  μ+3σ = {threshold:.4f}", zorder=5)
    ax6.fill_between(idx, threshold, timeline.max() * 1.05,
                     where=(timeline > threshold),
                     color=R, alpha=0.08, label="Alert zone")
    _style(ax6,
           "LSTM Autoencoder — Network Traffic Anomaly Detection Timeline (unsupervised)",
           "Sample Index", "Reconstruction Error (MSE)")
    ax6.legend(framealpha=0.15, labelcolor=FG, fontsize=8, loc="upper left",
               ncol=2)

    # ── Main title ────────────────────────────────────────────────────
    fig.suptitle(
        "AI & Quantum Computing in Cybersecurity  ·  COMP 5800  ·  Group M261M-1303",
        color=FG, fontsize=13, fontweight="bold", y=0.99
    )

    out_path = "quantum_ai_cybersecurity_dashboard.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    ok(f"Dashboard saved →  {out_path}")
    plt.show()


# =======================================================================
#  MAIN ENTRY POINT
# =======================================================================

if __name__ == "__main__":

    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════════════════════╗
║   AI & Quantum Computing in Cybersecurity — Demonstration Suite      ║
║   COMP 5800: Industry Research Project  |  Group M261M-1303          ║
║   Mentor: Dr. David Dzakpasu           |  Host: Industry Research Hub║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")

    # Section 1 — Shor's Algorithm
    bit_sizes, cls_ops, qnt_ops = demo_shors()

    # Section 2 — Grover's Algorithm
    demo_grovers()

    # Section 3 — Kyber-512 KEM
    kyber_times = demo_kyber()

    # Section 4 — LSTM Anomaly Detector
    err_norm, err_atk, threshold, atk_labels, tl, vl = demo_lstm()

    # Section 5 — Dashboard
    plot_dashboard(
        bit_sizes, cls_ops, qnt_ops,
        kyber_times,
        err_norm, err_atk, threshold,
        atk_labels, tl, vl
    )

    print(f"""
{GREEN}{BOLD}{'═' * 70}
  DEMONSTRATION COMPLETE
{'═' * 70}{RESET}

  Algorithms covered
  ──────────────────
  [1]  Shor's Algorithm    — factored RSA semiprime targets classically,
                             illustrating the quantum exponential speed-up
  [2]  Grover's Algorithm  — showed AES-128 key-space reduced to 2^64;
                             AES-256 still safe at 2^128 quantum security
  [3]  Kyber-512 KEM       — full keygen / encapsulate / decapsulate cycle
                             over Z_3329[X]/(X^256+1)  (NIST FIPS 203)
  [4]  LSTM Autoencoder    — unsupervised anomaly detection on synthetic
                             network flows  (DDoS / scan / exfil / brute)

  Output
  ──────
  quantum_ai_cybersecurity_dashboard.png  — 6-panel comparative dashboard

  References
  ──────────
  Shor, P.W.  (1994). FOCS. | Grover, L.K. (1996). STOC.
  Bos et al.  (2018). CRYSTALS-Kyber. IEEE EuroS&P.
  NIST FIPS 203 ML-KEM (2024). | Malhotra et al. (2015). ESANN.

{GREEN}{BOLD}{'═' * 70}{RESET}
""")
