"""Run 12, the Geometer (round 1). Notes-side measures on a Hooktheory clip melody; no fitted settings; deterministic.

Fourier on Z12 (Amiot; Parseval). p = duration-weighted melody pitch-class distribution (sums to 1);
f_k = sum_j p_j exp(-2 pi i j k / 12). Parseval: sum_{k=0..11} |f_k|^2 = 12 sum_j p_j^2, f_0 = 1, |f_k| = |f_{12-k}|, so
    C = 12 sum p^2 - 1 = 2(|f1|^2 + ... + |f5|^2) + |f6|^2       (the Renyi-2 twin of pitch-class entropy, split by axis).
G_C    : C (total Fourier energy; high = concentrated on few pitch classes).
G_E5   : 2|f5|^2 (energy on the fifths axis: diatonic / pentatonic shape). Transposition- and inversion-invariant, needs no tonic.
G_REST : C - 2|f5|^2 (concentration on the other axes: chromatic clusters, thirds, whole tones, tritones).
G_S5   : 2|f5|^2 / C (share of the concentration that is fifths-shaped).
G_PI   : Gaussian predictive information of the per-note pitch series (Ibragimov-Rozanov / partial-autocorrelation form):
         I = -1/2 sum_{k=1..K} k ln(1 - a_k^2) - K(K+1)/(4n), a_k from Levinson-Durbin on the biased autocovariances,
         K = 4 notes (clips are short), the last term the white-noise bias. Reading only on clips."""
import numpy as np

KEYS = ["G_C", "G_E5", "G_REST", "G_S5", "G_PI"]
_W = np.exp(-2j * np.pi * np.outer(np.arange(12), np.arange(12)) / 12)


def fourier(pcd):
    p = np.asarray(pcd, float); p = p / p.sum()
    f = _W @ p
    C = 12 * float((p * p).sum()) - 1.0
    e5 = 2 * abs(f[5]) ** 2
    return C, e5


def pacf(x, K):
    x = np.asarray(x, float) - np.mean(x); n = len(x)
    g = np.array([np.dot(x[:n - k], x[k:]) / n for k in range(K + 1)])
    if g[0] <= 0: return None
    a = np.zeros(K + 1); phi = np.zeros(K + 1); v = g[0]
    for k in range(1, K + 1):
        acc = g[k] - np.dot(phi[1:k], g[1:k][::-1])
        ak = acc / v; a[k] = ak
        new = phi.copy(); new[k] = ak
        new[1:k] = phi[1:k] - ak * phi[1:k][::-1]
        phi = new; v = v * (1 - ak * ak)
        if v <= 0: return None
    return a[1:]


def pred_info(x, K):
    a = pacf(x, K)
    if a is None: return None
    a = np.clip(a, -0.999999, 0.999999)
    k = np.arange(1, K + 1)
    return float(-0.5 * np.sum(k * np.log(1 - a * a)) - K * (K + 1) / (4.0 * len(x)))


def clip_measure(mel, a):
    pcd = np.zeros(12)
    for pi, di in zip(mel["pitch"], mel["dur"]): pcd[pi % 12] += di
    C, e5 = fourier(pcd)
    pi4 = pred_info(mel["pitch"], 4) if len(mel["pitch"]) >= 24 and np.std(mel["pitch"]) > 0 else None
    return dict(G_C=C, G_E5=e5, G_REST=C - e5, G_S5=(e5 / C) if C > 1e-9 else None, G_PI=pi4)
