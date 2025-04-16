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

