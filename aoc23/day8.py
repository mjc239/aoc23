def compute_visited(start_node, instructions, maps):
    # Computes the list of (node, instruction_index) states, starting from start_node,
    # as well as the the first repeated element of the list (defining the start
    # of the cycle)
    visited = []
    state = (start_node, 0)
    instruction_idx = 0
    while state not in visited:
        visited.append(state)
        instruction_idx = (instruction_idx + 1) % len(instructions)
        state = (maps[state[0]][instructions[state[1]]], instruction_idx)
    return visited, state


def num_steps(node, instructions, maps):
    # Computes the number of steps taken to reach the first destination node
    steps = 0
    while node[2] != "Z":
        for instr in instructions:
            steps += 1
            node = maps[node][instr]
            if node[2] == "Z":
                break
    return steps
