from math import asin, cos, radians, sin, sqrt


def compute_mst(nodes, edges):
    parent = {}
    rank = {}

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(left, right):
        root_left = find(left)
        root_right = find(right)
        if root_left == root_right:
            return

        if rank[root_left] < rank[root_right]:
            parent[root_left] = root_right
        elif rank[root_left] > rank[root_right]:
            parent[root_right] = root_left
        else:
            parent[root_right] = root_left
            rank[root_left] += 1

    for node in nodes:
        parent[node] = node
        rank[node] = 0

    ordered_edges = sorted(edges, key=lambda edge: edge["weight"])
    mst_edges = []
    total_cost = 0.0

    for edge in ordered_edges:
        source = edge["u"]
        target = edge["v"]
        weight = edge["weight"]

        if find(source) != find(target):
            union(source, target)
            mst_edges.append(edge)
            total_cost += weight

    return mst_edges, round(total_cost, 2)


def build_warehouse_edges(warehouses):
    edges = []
    for index, source in enumerate(warehouses):
        for target in warehouses[index + 1:]:
            edges.append(
                {
                    "u": source.id,
                    "v": target.id,
                    "weight": round(
                        haversine_distance(
                            source.latitude,
                            source.longitude,
                            target.latitude,
                            target.longitude,
                        ),
                        2,
                    ),
                }
            )
    return edges


def haversine_distance(lat1, lon1, lat2, lon2):
    earth_radius_km = 6371
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return earth_radius_km * c
