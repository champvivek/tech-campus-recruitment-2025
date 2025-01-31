import os
from multiprocessing import Pool

def extract_logs(input_file, date, output_file, buffer_size=10 * 1024 * 1024):
    """
    Extract logs for a specific date from the provided file.
    Reads file line-by-line (or with buffering) to minimize memory usage.
    """
    try:
        with open(input_file, "r", buffering=buffer_size) as infile, open(output_file, "w", buffering=buffer_size) as outfile:
            for line in infile:
                # Match only lines starting with the specified date
                if line[:10] == date:
                    outfile.write(line)

        print(f"Logs for {date} have been written to {output_file}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except PermissionError:
        print(f"Error: Insufficient permissions to access '{input_file}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def parallel_process_logs(log_file, date, output_dir="output", chunk_size_gb=10, num_processes=4):
    """
    Split a large log file into smaller chunks and process them in parallel.
    Each process filters lines by the target date and writes results into separate files.
    """
    # Split input file into smaller chunks
    print(f"Splitting {log_file} into smaller chunks...")
    chunk_prefix = os.path.join(output_dir, "chunk_")
    os.makedirs(output_dir, exist_ok=True)

    split_command = f"split -b {chunk_size_gb}G {log_file} {chunk_prefix}"
    os.system(split_command)  # Works on Linux, macOS

    # Get the list of chunks
    chunk_files = [os.path.join(output_dir, file) for file in os.listdir(output_dir) if file.startswith("chunk_")]
    if not chunk_files:
        print("Error: No chunk files created. Ensure 'split' command is available.")
        return

    print(f"File successfully split into {len(chunk_files)} chunks.")

    # Process each chunk in parallel
    print(f"Processing {len(chunk_files)} chunks in parallel using {num_processes} processes...")
    with Pool(num_processes) as pool:
        tasks = [(chunk_file, date, f"{chunk_file}_filtered.txt") for chunk_file in chunk_files]
        pool.starmap(process_single_chunk, tasks)

    # Merge all outputs
    final_output_file = os.path.join(output_dir, f"output_{date}.txt")
    merge_files([task[2] for task in tasks], final_output_file)

    print(f"All filtered logs for {date} have been saved to {final_output_file}")


def process_single_chunk(chunk_file, date, output_file):
    """
    Helper function to process a single chunk, filtering logs by date.
    """
    print(f"Processing chunk {chunk_file}...")
    extract_logs(chunk_file, date, output_file)


def merge_files(file_list, output_file):
    """
    Merge multiple filtered chunk output files into a single file.
    """
    print(f"Merging chunk outputs into {output_file}...")
    with open(output_file, "w", buffering=10 * 1024 * 1024) as outfile:
        for file in file_list:
            with open(file, "r", buffering=10 * 1024 * 1024) as infile:
                for line in infile:
                    outfile.write(line)


# Main Execution
if __name__ == "__main__":
    # Hardcoded parameters
    log_file = "logs_2024.log"  # Path to your 1 TB log file
    date_to_filter = "2024-12-01"  # Date you want to filter logs for
    output_directory = "output"  # Output directory for filtered results and temporary chunks

    # Check if the log file exists
    if not os.path.exists(log_file):
        print(f"Error: File '{log_file}' not found.")
        exit(1)

    # Process the log file
    parallel_process_logs(log_file, date_to_filter, output_directory, chunk_size_gb=10, num_processes=4)