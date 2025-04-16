
# Memory Allocator Simulator

This is a simple command-line based memory management simulator written in Python. It simulates dynamic memory allocation and deallocation using **First Fit**, **Best Fit**, and **Worst Fit** strategies. It also supports memory compaction and provides status reports.

## Features

- Allocate memory using:
  - **First Fit (F)**
  - **Best Fit (B)**
  - **Worst Fit (W)**
- Release memory blocks by process name
- Compact memory to reduce fragmentation
- View current memory allocation status
- Interactive command-line interface

## How It Works

The simulator maintains a list of memory blocks, each with:
- `start` and `end` address
- `status`: `'Free'` or `'Allocated'`
- `process`: name of the process (if allocated)

## Getting Started

### Requirements

- Python 3.x

### Running the Program

1. Clone the repository or copy the script.
2. Run the script:

```bash
python memory_allocator.py
```

3. Enter the total memory size in bytes when prompted.
4. Use the following commands in the prompt:

### Commands

- `RQ <process_name> <size> <strategy>`  
  Request memory for a process.  
  Example: `RQ P1 100 F`

- `RL <process_name>`  
  Release memory allocated to a process.  
  Example: `RL P1`

- `C`  
  Compact memory to remove fragmentation.

- `STAT`  
  Print the current memory layout.

- `X`  
  Exit the program.

### Allocation Strategies

| Strategy | Description             |
|----------|-------------------------|
| F        | First Fit               |
| B        | Best Fit                |
| W        | Worst Fit               |

## Example

```text
Enter memory size in bytes: 1024
allocator > RQ P1 200 F
allocator > RQ P2 300 B
allocator > STAT
Addresses [0:199] Process P1
Addresses [200:499] Process P2
Addresses [500:1023] Unused
allocator > RL P1
allocator > C
allocator > STAT
Addresses [0:299] Process P2
Addresses [300:1023] Unused
allocator > X
```

## Notes

- This simulator does not support paging or segmentation.
- External fragmentation may occur based on the allocation strategy used.
- Memory is compacted manually using the `C` command.

## License

This project is open-source and free to use for educational or personal purposes.
