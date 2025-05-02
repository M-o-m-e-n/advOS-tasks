# Represents a block of memory with a start and end address, status (Free or Allocated), and optional process name
class MemoryBlock:
    def __init__(self, start, end, status='Free', process=None):
        self.start = start
        self.end = end
        self.status = status  # 'Free' or 'Allocated'
        self.process = process

    def size(self):
        # Returns the size of the memory block
        return self.end - self.start + 1

    def __repr__(self):
        # String representation for printing block details
        return f"Addresses [{self.start}:{self.end}] {'Unused' if self.status == 'Free' else 'Process ' + self.process}"


# Manages memory allocation, deallocation, compaction, and status reporting
class MemoryAllocator:
    def __init__(self, size):
        # Initialize the memory with one large free block
        self.memory = [MemoryBlock(0, size - 1)]
        self.size = size

    def _merge_free_blocks(self):
        # Merge adjacent free memory blocks into one to reduce fragmentation
        merged = []
        self.memory.sort(key=lambda b: b.start)
        for block in self.memory:
            if merged and merged[-1].status == 'Free' and block.status == 'Free':
                merged[-1].end = block.end  # Merge with previous
            else:
                merged.append(block)
        self.memory = merged

    def _find_block(self, size, strategy):
        # Find a free block of at least 'size' using the given strategy:
        # F = First Fit, B = Best Fit, W = Worst Fit
        if strategy not in ('F', 'B', 'W'):
            raise ValueError(f"Invalid allocation strategy '{strategy}'. Use 'F', 'B', or 'W'.")

        free_blocks = [b for b in self.memory if b.status == 'Free' and b.size() >= size]
        if not free_blocks:
            return None

        if strategy == 'F':
            return min(free_blocks, key=lambda b: b.start)  # First Fit
        elif strategy == 'B':
            return min(free_blocks, key=lambda b: b.size())  # Best Fit
        elif strategy == 'W':
            return max(free_blocks, key=lambda b: b.size())  # Worst Fit

    def request(self, process_name, size, strategy):
        # Handle memory allocation request for a process

        # Check for duplicate process name
        for block in self.memory:
            if block.status == 'Allocated' and block.process == process_name:
                print(f"Error: Process '{process_name}' already exists.")
                return

        # Try to find a suitable block using the strategy
        try:
            block = self._find_block(size, strategy)
        except ValueError as e:
            print("Error:", e)
            return

        # If no block is found, external fragmentation might be the issue
        if not block:
            print("Error: Not enough memory for the process (external fragmentation).")
            return

        # Allocate memory
        idx = self.memory.index(block)
        allocated = MemoryBlock(block.start, block.start + size - 1, 'Allocated', process_name)
        remaining_size = block.size() - size

        # Split the block if there's leftover space
        if remaining_size > 0:
            new_free = MemoryBlock(block.start + size, block.end)
            self.memory[idx:idx+1] = [allocated, new_free]
        else:
            self.memory[idx] = allocated

    def release(self, process_name):
        # Free the memory occupied by a specific process
        for i, block in enumerate(self.memory):
            if block.status == 'Allocated' and block.process == process_name:
                self.memory[i] = MemoryBlock(block.start, block.end)  # Mark as Free
                self._merge_free_blocks()  # Merge any adjacent free blocks
                return
        print("Error: Process not found.")

    def compact(self):
        # Compact memory by shifting allocated blocks to the start
        new_memory = []
        current_start = 0
        for block in self.memory:
            if block.status == 'Allocated':
                size = block.size()
                new_block = MemoryBlock(current_start, current_start + size - 1, 'Allocated', block.process)
                new_memory.append(new_block)
                current_start += size

        # Add remaining space as a single free block
        if current_start < self.size:
            new_memory.append(MemoryBlock(current_start, self.size - 1))
        self.memory = new_memory

    def stat(self):
        # Display the current memory allocation status
        for block in self.memory:
            print(block)

    def run(self):
        # Interactive loop for processing user commands
        while True:
            cmd = input("allocator > ").strip()
            if cmd.startswith("RQ"):
                _, name, size, strategy = cmd.split()
                self.request(name, int(size), strategy)
            elif cmd.startswith("RL"):
                _, name = cmd.split()
                self.release(name)
            elif cmd == "C":
                self.compact()
            elif cmd == "STAT":
                self.stat()
            elif cmd == "X":
                break
            else:
                print("Invalid command.")


# Entry point of the program
if __name__ == "__main__":
    # Ask the user for memory size and ensure it's valid
    while True:
        try:
            mem_size = int(input("Enter memory size in bytes: "))
            if mem_size <= 0:
                print("Memory size must be a positive number.")
                continue
            break
        except ValueError:
            print("Invalid number, please try again.")

    # Initialize and start the allocator
    allocator = MemoryAllocator(mem_size)
    allocator.run()
