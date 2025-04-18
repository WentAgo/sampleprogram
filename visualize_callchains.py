import json
import re
from collections import defaultdict, deque

import networkx as nx
import plotly.graph_objects as go

def get_levels(G, root_nodes):
    levels = defaultdict(list)
    visited = set()
    queue = deque([(node, 0) for node in root_nodes])

    while queue:
        node, level = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        levels[level].append(node)
        for child in G.successors(node):
            if child not in visited:
                queue.append((child, level + 1))
    return levels

def create_top_down_layout(G):
    roots = [node for node in G.nodes if G.in_degree(node) == 0]
    levels = get_levels(G, roots)
    pos = {}
    y_gap = -1.5
    x_gap = 2.5

    for level, nodes in levels.items():
        for i, node in enumerate(nodes):
            pos[node] = (i * x_gap, level * y_gap)

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
        line=dict(width=1, color='#888'),
        hoverinfo='none',
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
        textposition="bottom center",
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
                        margin=dict(b=20, l=20, r=20, t=60),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False),
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
            src = chain[i]
            dst = chain[i + 1]
            G.add_edge(src, dst, test=test_name)

pos = create_top_down_layout(G)
create_figure(G, pos, 'Call Chain Graph', 'html/callchains.html')

for test_name, chains in callchains.items():
    G_test = nx.DiGraph()

    for chain in chains:
        src = test_name
        dst = chain[0]
        G_test.add_edge(src, dst, test=test_name)
        for i in range(len(chain) - 1):
            src = chain[i]
            dst = chain[i + 1]
            G_test.add_edge(src, dst, test=test_name)

    pos_test = create_top_down_layout(G_test)
    create_figure(G_test, pos_test, f"{test_name} Call Chain", f"html/tests/{test_name}_call_chain.html")

def convert_method_name(method: str) -> str:
    return re.sub(r'\.(\w+)\[(\w+)\]', lambda m: f'.{m.group(2)}_{m.group(1)}', method)

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
            src = chain[i]
            dst = chain[i + 1]
            G_method.add_edge(src, dst, test=test_name)

    if len(G_method) == 0:
        continue

    pos_method = create_top_down_layout(G_method)
    create_figure(G_method, pos_method, f"{method} Call Chains", f"html/methods/{convert_method_name(method)}_call_chain.html")
