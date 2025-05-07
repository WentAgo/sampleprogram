import json
import re
import networkx as nx
import plotly.graph_objects as go
from collections import deque, defaultdict

def convert_method_name(method: str) -> str:
    return re.sub(r'\.(\w+)\[(\w+)\]', lambda m: f'.{m.group(2)}_{m.group(1)}', method)

def compute_top_down_positions(G):
    levels = defaultdict(list)
    indegree = {node: 0 for node in G.nodes()}
    for u, v in G.edges():
        indegree[v] += 1

    queue = deque()
    for node, deg in indegree.items():
        if deg == 0:
            queue.append((node, 0))

    visited = set()
    while queue:
        node, level = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        levels[level].append(node)
        for neighbor in G.successors(node):
            queue.append((neighbor, level + 1.8))

    pos = {}
    max_width = max(len(nodes) for nodes in levels.values())
    for level, nodes in levels.items():
        count = len(nodes)
        spacing = 1.0 / (count + 1)
        for i, node in enumerate(nodes):
            x = (i + 1) * spacing
            y = -level * 0.5
            if i % 2 == 1:
                y -= 0.15
            pos[node] = (x, y)
    return pos

def create_figure(G, pos, title_text, filename):
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.2, color='#888'),
        hoverinfo='text',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color='lightblue',
            size=20,
            line_width=2))

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=dict(text=title_text, font=dict(size=20)),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)
                    ))

    fig.write_html(filename)

with open("callchains.json") as f:
    callchains = json.load(f)

G = nx.DiGraph()
for test_name, chains in callchains.items():
    for chain in chains:
        src = test_name
        dst = chain[0]
        G.add_edge(src, dst, test=test_name)
        for i in range(len(chain) - 1):
            G.add_edge(chain[i], chain[i + 1], test=test_name)

pos = compute_top_down_positions(G)
create_figure(G, pos, "Call chains", "html/callchains.html")

for test_name, chains in callchains.items():
    G_test = nx.DiGraph()
    for chain in chains:
        src = test_name
        dst = chain[0]
        G_test.add_edge(src, dst, test=test_name)
        for i in range(len(chain) - 1):
            G_test.add_edge(chain[i], chain[i + 1], test=test_name)

    pos_test = compute_top_down_positions(G_test)
    filename = f"html/tests/{test_name}_call_chain.html"
    create_figure(G_test, pos_test, f"{test_name} Call Chain", filename)

all_methods = set()
for chains in callchains.values():
    for chain in chains:
        all_methods.update(chain)

for method in all_methods:
    relevant_chains = []
    for test_name, chains in callchains.items():
        for chain in chains:
            if method in chain:
                relevant_chains.append((test_name, chain))

    G_method = nx.DiGraph()
    for test_name, chain in relevant_chains:
        if not chain:
            continue
        G_method.add_edge(test_name, chain[0], test=test_name)
        for i in range(len(chain) - 1):
            G_method.add_edge(chain[i], chain[i + 1], test=test_name)

    if len(G_method) == 0:
        continue

    pos_method = compute_top_down_positions(G_method)
    filename = f"html/methods/{convert_method_name(method)}_call_chain.html"
    create_figure(G_method, pos_method, f"{method} Call Chain", filename)
