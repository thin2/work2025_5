import math
from collections import Counter, defaultdict

# Provided float vertices
pieces = [
    # Small triangle 1
    [(2 - 1.5*math.sqrt(2), 2 + 2.5*math.sqrt(2)),
     (2 - math.sqrt(2),    2 + 2*math.sqrt(2)),
     (2 - 0.5*math.sqrt(2),2 + 1.5*math.sqrt(2))],
    # Small triangle 2
    [(2 - 0.5*math.sqrt(2),2 + 2.5*math.sqrt(2)),
     (2 - 0.5*math.sqrt(2),2 + 1.5*math.sqrt(2)),
     (2 - math.sqrt(2),    2 + 2*math.sqrt(2))],
    # Square
    [(2 - math.sqrt(2),    2 + 2*math.sqrt(2)),
     (2 - 0.5*math.sqrt(2),2 + 1.5*math.sqrt(2)),
     (2 - math.sqrt(2),    2 + math.sqrt(2)),
     (2 - 1.5*math.sqrt(2),2 + 1.5*math.sqrt(2))],
    # Large triangle 1
    [(2 - math.sqrt(2),    2 + math.sqrt(2)),
     (2,                   2),
     (2 - math.sqrt(2),    2 + math.sqrt(2))],
    # Medium triangle
    [(2 - math.sqrt(2),    2 + math.sqrt(2)),
     (2 - math.sqrt(2),    math.sqrt(2)),
     (1 - math.sqrt(2),    1 + math.sqrt(2))],
    # Large triangle 2
    [(2, 2), (2, 0), (0, 0)],
    # Parallelogram
    [(3,1), (4,1), (3,0), (2,0)]
]

def trace_boundary(all_vertices_lists):
    edges = Counter()
    for verts in all_vertices_lists:
        for i in range(len(verts)):
            e = tuple(sorted((verts[i], verts[(i+1)%len(verts)])))
            edges[e] += 1
    boundary_edges = [e for e,c in edges.items() if c==1]
    adj = defaultdict(list)
    for a,b in boundary_edges:
        adj[a].append(b)
        adj[b].append(a)
    start = max(adj.keys(), key=lambda v:(v[1], -v[0]))
    path = [start]
    prev=None; curr=start
    while True:
        nbrs=adj[curr]
        if prev is None:
            def angle0(v):
                dx,dy=v[0]-curr[0], v[1]-curr[1]
                return (math.atan2(dy,dx)+2*math.pi)%(2*math.pi)
            nxt=min(nbrs, key=angle0)
        else:
            ux,uy=curr[0]-prev[0], curr[1]-prev[1]
            def rel_ang(v):
                vx,vy=v[0]-curr[0], v[1]-curr[1]
                return (math.atan2(vy,vx)-math.atan2(uy,ux))%(2*math.pi)
            nxt=min(nbrs, key=rel_ang)
        if nxt==start:
            break
        path.append(nxt)
        prev, curr=curr, nxt
    return path

boundary_path = trace_boundary(pieces)
print(boundary_path)