Solutions Considered
To efficiently extract logs for a specific date from a large log file (~1 TB), we explored and implemented the following three approaches. Each approach aimed to find a balance between memory efficiency, execution time, and scalability.

1. Naive Approach: Read Entire File into Memory
Description:

This approach involves reading the entire log file into memory at once using Python’s readlines() or read() function. After loading the file, the script processes and filters the logs that match the desired date. The results are written to an output file.

Pros:
Very simple and easy to implement.
Minimal overhead for smaller files (files that can fully fit in memory).

Cons:
Memory-intensive: Requires the entire file to be loaded into memory, making it infeasible for very large files (e.g., 1 TB). This causes crashes or performance bottlenecks.
Scalability limited to the size of physical memory (RAM).
Final Decision:

This approach was not chosen as it cannot handle large files and is impractical in real-world scenarios for this task.

2. Line-by-Line Streaming (Improved Memory Management)
Description:

This approach involves streaming the file line-by-line using Python’s file handling (for line in file:). At any given time, only one line is stored in memory. Each line is checked to see if it matches the date, and if so, it is written to the output file.

Pros:
Memory-efficient: Only processes one line at a time, regardless of the total file size.
Handles very large files effortlessly (even files larger than available RAM).
Simple to implement and provides a straightforward solution.

Cons:
Lower performance: This approach is limited by the speed of disk I/O since the file is read and processed sequentially.
For very large files (e.g., 1 TB), the runtime can be significant.
Final Decision:

This approach provides a simple and practical solution for environments with limited memory or single-threaded systems. While not the fastest solution, it was included as a baseline implementation due to its reliability and simplicity.

3. Buffered I/O + Parallel Processing (Final Solution)
Description:

In this approach, the file is first split into smaller chunks (e.g., 10 GB chunks) using a tool like split. Each chunk is then processed independently in parallel using Python’s multiprocessing module. A buffer is used to process chunks incrementally (e.g., 10 MB at a time), ensuring both memory and disk I/O efficiency. The filtered results from all chunks are merged into a single output file.

Pros:
Highly scalable: Can handle extremely large files efficiently by processing chunks in parallel.
Improved runtime: Takes full advantage of multi-core systems, reducing the overall processing time.
Memory-efficient: Each process only handles a specific chunk of the file, and within each chunk, only a 10 MB buffer is loaded in memory at any given time.
Ideal for large-scale file processing tasks.
Cons:

Slightly more complex implementation due to chunking and parallel processing.
Requires additional tools (e.g., split command) for optimal chunking.
Final Decision:

This approach was chosen as the final solution. It strikes the right balance between execution time, memory efficiency, and scalability, making it the best approach for large files such as a 1 TB log file. The use of parallel processing ensures significant speedup, while buffered I/O minimizes memory usage and improves disk performance.

Final Solution Summary
The Buffered I/O + Parallel Processing approach was selected as the final solution due to its scalability, efficiency, and ability to handle very large files effectively. By splitting the file into smaller chunks, processing them in parallel, and merging the results, this approach provides the best performance for both single-use extractions and larger-scale repetitive tasks.

The other approaches—Naive Approach and Line-by-Line Streaming—serve as important baselines, demonstrating the incremental improvements in terms of memory usage and runtime efficiency.

Steps to Run
Prerequisites:

Python 3 installed.
The script assumes the tool split is available for breaking the file into chunks (default on Linux/macOS, installable via Git Bash or WSL on Windows).
Prepare the Log File:

Place the log file (logs_2024.log) in the same directory as the script.
Run the Script:

Provide the target date as a command-line argument:
bash
Copy code
python extract_logs.py <YYYY-MM-DD>
Example:
bash
Copy code
python extract_logs.py 2024-12-01
Output:

The filtered logs for the specified date will be saved in the output directory with the filename output_<YYYY-MM-DD>.txt (e.g., output_2024-12-01.txt).
Intermediate Files:

Intermediate chunks and filtered chunk files (e.g., chunk_aa_filtered.txt) will also be temporarily created and cleaned up.
Conclusion
Using Buffered I/O + Parallel Processing, the final implementation allows efficient processing of massive log files (e.g., 1 TB or more) while balancing memory efficiency and runtime performance. The solution leverages the scalability of parallel processing and the simplicity of buffered file handling, making it both practical and highly effective in real-world scenarios.
