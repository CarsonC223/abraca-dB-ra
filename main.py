from database import setup_database, store_song
import matplotlib.pyplot as plt
from FFT import fingerprint_song


# def main():
#     setup_database()
#     store_song("songs/audio.wav")

# if __name__ == "__main__":
#     main()

points = fingerprint_song(r"songs\Shake-Back.wav")

print(f"Total peaks detected: {len(points)}")
print(points[:20])

if points:
    times, frequencies = zip(*points)

    plt.figure(figsize=(12, 6))
    plt.scatter(times, frequencies, s=2)

    plt.title("Audio Fingerprint Constellation Map")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Frequency (Hz)")
    plt.ylim(0, 5000)
    plt.grid(True)

    plt.show()
