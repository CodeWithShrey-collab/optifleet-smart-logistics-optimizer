def hamiltonian_cycle(graph):
    n = len(graph)
    if n == 0:
        return []
    if n == 1:
        return [0, 0]

    path = [-1] * n
    path[0] = 0

    def is_safe(vertex, position):
        if graph[path[position - 1]][vertex] == 0:
            return False
        if vertex in path:
            return False
        return True

    def solve(position):
        if position == n:
            return graph[path[position - 1]][path[0]] == 1

        for vertex in range(1, n):
            if is_safe(vertex, position):
                path[position] = vertex
                if solve(position + 1):
                    return True
                path[position] = -1

        return False

    if solve(1):
        return path + [path[0]]
    return []
