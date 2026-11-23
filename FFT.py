import cmath
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import find_peaks

# ---------------------------------
# 1. Recursive FFT algorithm
# ---------------------------------

def FFT(P):
    n = len(P)

    if n == 1:
        return P

    omega = cmath.exp(-2j * cmath.pi / n)

    Pe = P[::2]
    Po = P[1::2]

    ye = FFT(Pe)
    yo = FFT(Po)

    y = [0j] * n

    for j in range(n // 2):
        t = omega**j * yo[j]

        y[j] = ye[j] + t
        y[j + n // 2] = ye[j] - t

    return y

# ---------------------------------
# 2. Prepare Samples
# ---------------------------------
def prepare_samples(audio, start, N):
    # Extract segment
    samples = audio[start:start + N].astype(float)

    # Pad with zeros if too short
    if len(samples) < N:
        samples = np.pad(samples, (0, N - len(samples)))

    # Apply Hann window
    window = np.hanning(N)
    samples = samples * window

    return samples, window

# ---------------------------------
# 3. Find FFT peaks
# ---------------------------------
def find_fft_peaks(magnitudes, max_peaks=5, prominence=0.05, distance=5):
    # Handle empty or silent segments
    if len(magnitudes) == 0 or np.max(magnitudes) <= 0:
        return []

    # Detect local maxima
    peaks, _ = find_peaks(
        magnitudes,
        prominence=prominence * np.max(magnitudes),
        distance=distance
    )

    # Sort peaks by amplitude (strongest first)
    peaks = sorted(
        peaks,
        key=lambda i: magnitudes[i],
        reverse=True
    )

    # Return only the strongest peaks
    return peaks[:max_peaks]

#---------------------------------
# 4. Fingerprint Song
#---------------------------------
def fingerprint_song(filename):

    fs, audio = wavfile.read(filename)

    # Convert stereo to mono
    if audio.ndim == 2:
        audio = audio.mean(axis=1)

    N = 4096
    hop_size = 2048

    fingerprint_points = []

    for start in range(0, len(audio) - N + 1, hop_size):
        samples, window = prepare_samples(audio, start, N)

        # Run FFT on this segment
        result = FFT(samples.tolist())

        positive_fft = np.array(result[:N // 2 + 1])

        # Calculate one-sided amplitude spectrum
        magnitudes = np.abs(positive_fft) / np.sum(window)
        magnitudes[1:-1] *= 2

        # Find peaks
        peaks = find_fft_peaks(magnitudes)

        # Calculate timestamp
        time = start / fs

        # Convert peak indices to frequencies and store
        for k in peaks:
            frequency = k * fs / N
            fingerprint_points.append((time, frequency))

    return fingerprint_points

# points = fingerprint_song("audio.wav")

# print(f"Total peaks detected: {len(points)}")
# print(points[:20])