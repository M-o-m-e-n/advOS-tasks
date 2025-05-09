import matplotlib.pyplot as plt

def get_user_input():
    try:
        num_cylinders = int(input("Enter total number of cylinders (e.g., 5000): "))
        queue_size = int(input("Enter the number of requests in the queue: "))
        queue = list(map(int, input(f"Enter {queue_size} cylinder requests separated by spaces: ").split()))
        if len(queue) != queue_size or any(r < 0 or r >= num_cylinders for r in queue):
            raise ValueError("Invalid request values.")
        head = int(input(f"Enter initial head position (0 to {num_cylinders - 1}): "))
        if not 0 <= head < num_cylinders:
            raise ValueError("Invalid head position.")
        algo = input("Enter algorithm to use (FCFS / SCAN / C-SCAN): ").strip().upper()
        if algo not in ("FCFS", "SCAN", "C-SCAN"):
            raise ValueError("Invalid algorithm choice.")

        direction = None
        if algo in ("SCAN", "C-SCAN"):
            dir_input = input("Enter head movement direction (I for Inner to Outer, O for Outer to Inner): ").strip().upper()
            if dir_input not in ("I", "O"):
                raise ValueError("Invalid direction. Use 'I' or 'O'.")
            direction = "up" if dir_input == "I" else "down"

        return num_cylinders, queue, head, algo, direction
    except ValueError as e:
        print("Error:", e)
        exit(1)

def fcfs(queue, head):
    total_seek = 0
    order = [head]
    for r in queue:
        total_seek += abs(head - r)
        head = r
        order.append(r)
    return total_seek, order

def scan(queue, head, max_cylinder, direction):
    queue = sorted(queue)
    total_seek = 0
    order = [head]
    below = [r for r in queue if r < head]
    above = [r for r in queue if r >= head]

    if direction == "up":
        for r in above:
            total_seek += abs(head - r)
            head = r
            order.append(r)

        if head != max_cylinder - 1:
            total_seek += abs(head - (max_cylinder - 1))
            head = max_cylinder - 1
            order.append(head)

        for r in reversed(below):
            total_seek += abs(head - r)
            head = r
            order.append(r)

    else:  # direction == "down"
        for r in reversed(below):
            total_seek += abs(head - r)
            head = r
            order.append(r)

        if head != 0:
            total_seek += abs(head - 0)
            head = 0
            order.append(head)

        for r in above:
            total_seek += abs(head - r)
            head = r
            order.append(r)

    return total_seek, order

def c_scan(queue, head, max_cylinder, direction):
    queue = sorted(queue)
    total_seek = 0
    order = [head]
    below = [r for r in queue if r < head]
    above = [r for r in queue if r >= head]

    if direction == "up":
        for r in above:
            total_seek += abs(head - r)
            head = r
            order.append(r)

        if head != max_cylinder - 1:
            total_seek += abs(head - (max_cylinder - 1))
            head = max_cylinder - 1
            order.append(head)

        # Jump from end to start
        total_seek += head
        head = 0
        order.append(head)

        for r in below:
            total_seek += abs(head - r)
            head = r
            order.append(r)

    else:  # direction == "down"
        for r in reversed(below):
            total_seek += abs(head - r)
            head = r
            order.append(r)

        if head != 0:
            total_seek += abs(head - 0)
            head = 0
            order.append(head)

        # Jump from start to end
        total_seek += max_cylinder - 1
        head = max_cylinder - 1
        order.append(head)

        for r in reversed(above):
            total_seek += abs(head - r)
            head = r
            order.append(r)

    return total_seek, order

def plot_head_movement(order, algo):
    steps = list(range(len(order)))
    plt.figure(figsize=(10, 5))
    plt.plot(order, steps, marker='o', linestyle='-', color='green', label=algo)
    plt.scatter(order[0], steps[0], color='black', label='Initial Head')
    plt.text(order[0], steps[0] + 0.5, 'Initial Head', ha='center', color='black')
    plt.xlabel("Cylinder Position")
    plt.ylabel("Time / Step")
    plt.title("Disk Head Movement Visualization")
    plt.grid(True)
    plt.legend()
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

def main():
    num_cylinders, queue, head, algo, direction = get_user_input()

    if algo == "FCFS":
        total_seek, order = fcfs(queue, head)
    elif algo == "SCAN":
        total_seek, order = scan(queue, head, num_cylinders, direction)
    elif algo == "C-SCAN":
        total_seek, order = c_scan(queue, head, num_cylinders, direction)

    print("\n--- Disk Scheduling Result ---")
    print("Algorithm Used:", algo)
    print("Total Seek Time:", total_seek)
    print("Order of Head Movement:")
    print(" -> ".join(map(str, order)))

    plot_head_movement(order, algo)

if __name__ == "__main__":
    main()
