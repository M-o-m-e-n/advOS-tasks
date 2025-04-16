class MemoryBlock:
    def __init__(self, start, end, status='Free', process=None):
        self.start = start
        self.end = end
        self.status = status  # 'Free' or 'Allocated'
        self.process = process

    def size(self):
        return self.end - self.start + 1

    def __repr__(self):
        return f"Addresses [{self.start}:{self.end}] {'Unused' if self.status == 'Free' else 'Process ' + self.process}"


class MemoryAllocator:
    def __init__(self, size):
        self.memory = [MemoryBlock(0, size - 1)]
        self.size = size

    def _merge_free_blocks(self):
        merged = []
        self.memory.sort(key=lambda b: b.start)
        for block in self.memory:
            if merged and merged[-1].status == 'Free' and block.status == 'Free':
                merged[-1].end = block.end
            else:
                merged.append(block)
        self.memory = merged

    def _find_block(self, size, strategy):
        if strategy not in ('F', 'B', 'W'):
            raise ValueError(f"Invalid allocation strategy '{strategy}'. Use 'F', 'B', or 'W'.")

        free_blocks = [b for b in self.memory if b.status == 'Free' and b.size() >= size]
        if not free_blocks:
            return None
        if strategy == 'F':
            return min(free_blocks, key=lambda b: b.start)
        elif strategy == 'B':
            return min(free_blocks, key=lambda b: b.size())
        elif strategy == 'W':
            return max(free_blocks, key=lambda b: b.size())


    def request(self, process_name, size, strategy):
        # Check if process name already exists
        for block in self.memory:
            if block.status == 'Allocated' and block.process == process_name:
                print(f"Error: Process '{process_name}' already exists.")
                return

        try:
            block = self._find_block(size, strategy)
        except ValueError as e:
            print("Error:", e)
            return

        if not block:
            print("Error: Not enough memory for the process (external fragmentation).")
            return

        idx = self.memory.index(block)
        allocated = MemoryBlock(block.start, block.start + size - 1, 'Allocated', process_name)
        remaining_size = block.size() - size
        if remaining_size > 0:
            new_free = MemoryBlock(block.start + size, block.end)
            self.memory[idx:idx+1] = [allocated, new_free]
        else:
            self.memory[idx] = allocated

    def release(self, process_name):
        for i, block in enumerate(self.memory):
            if block.status == 'Allocated' and block.process == process_name:
                self.memory[i] = MemoryBlock(block.start, block.end)
                self._merge_free_blocks()
                return
        print("Error: Process not found.")

    def compact(self):
        new_memory = []
        current_start = 0
        for block in self.memory:
            if block.status == 'Allocated':
                size = block.size()
                new_block = MemoryBlock(current_start, current_start + size - 1, 'Allocated', block.process)
                new_memory.append(new_block)
                current_start += size
        if current_start < self.size:
            new_memory.append(MemoryBlock(current_start, self.size - 1))
        self.memory = new_memory

    def stat(self):
        for block in self.memory:
            print(block)

    def run(self):
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


if __name__ == "__main__":
    while True:
        try:
            mem_size = int(input("Enter memory size in bytes: "))
            if mem_size <= 0:
                print("Memory size must be a positive number.")
                continue
            break
        except ValueError:
            print("Invalid number, please try again.")

    allocator = MemoryAllocator(mem_size)
    allocator.run()
