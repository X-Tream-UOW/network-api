import argparse
import math
import struct


def analyze_bin_file(filepath, verbose=False):
    try:
        with open(filepath, 'rb') as f:
            record_size = 6  # 4 bytes index (uint32) + 2 bytes sample (uint16)

            indices = []
            samples = []

            while True:
                chunk = f.read(record_size)
                if len(chunk) < record_size:
                    break
                index, sample = struct.unpack('IH', chunk)
                indices.append(index)
                samples.append(sample)

                if verbose:
                    print(f"{index}: {sample}")

        count = len(samples)
        if count == 0:
            print("[!] File is empty or corrupt.")
            return

        # Check integrity (all indices are continuous from 0 to N-1)
        expected_indices = list(range(count))
        integrity_ok = indices == expected_indices

        # Compute stats
        mean = sum(samples) / count
        variance = sum((x - mean) ** 2 for x in samples) / count
        stddev = math.sqrt(variance)

        print("\nAnalysis Result:")
        print(f"  Samples:   {count}")
        print(f"  Mean:      {mean:.2f}")
        print(f"  Std Dev:   {stddev:.2f}")
        print(f"  Integrity: {'OK' if integrity_ok else 'MISMATCHED INDICES'}")

    except FileNotFoundError:
        print(f"[!] File not found: {filepath}")
    except Exception as e:
        print(f"[!] Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inspect a binary sample file.")
    parser.add_argument("file", help="Path to .bin file")
    parser.add_argument("--print", action="store_true", help="Print index:sample values")

    args = parser.parse_args()
    analyze_bin_file(args.file, verbose=args.print)
