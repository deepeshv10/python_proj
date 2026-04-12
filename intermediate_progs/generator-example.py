# A generator example to read a large file and yiled it line by line until 'ERROR' is found in it.


def stream_large_file(file_path):
    """Reads a file line by line without loading the whole thing into RAM."""
    with open(file_path, "r") as file:
        for line in file:
            # You can clean or transform the data here
            yield line.strip()

# Usage
log_gen = stream_large_file("intermediate_progs/sample-log.txt")

# Process only what you need, when you need it
for log in log_gen:
    if "ERROR" in log:
        print(f"Found issue: {log}")
        break  # We stop here; the rest of the file is never even read!