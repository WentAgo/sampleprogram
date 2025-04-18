import json
import re
import networkx as nx
import plotly.graph_objects as go

with open("callchains.json") as f:
    callchains = json.load(f)

def convert_method_name(method: str) -> str:
    return re.sub(r'\.(\w+)\[(\w+)\]', lambda m: f'.{m.group(2)}_{m.group(1)}', method)

def create_figure(G, title_text, filename):
    pos = nx.spring_layout(G, seed=42)

    edge_x, edge_y = [], []
    for src, dst in G.edges():
        x0, y0 = pos[src]
        x1, y1 = pos[dst]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color='#888'), hoverinfo='none', mode='lines')

    node_x, node_y, node_text = [], [], []
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
        marker=dict(showscale=False, color='lightblue', size=20, line_width=2)
    )

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

G_all = nx.DiGraph()
for test_name, chains in callchains.items():
    for chain in chains:
        if not chain:
            continue
        G_all.add_edge(test_name, chain[0])
        for i in range(len(chain) - 1):
            G_all.add_edge(chain[i], chain[i + 1])
create_figure(G_all, "Call Chain Graph", "html/callchains.html")

for test_name, chains in callchains.items():
    G_test = nx.DiGraph()
    for chain in chains:
        if not chain:
            continue
        G_test.add_edge(test_name, chain[0])
        for i in range(len(chain) - 1):
            G_test.add_edge(chain[i], chain[i + 1])
    create_figure(G_test, f"{test_name} Call Chain", f"html/tests/{test_name}_call_chain.html")

all_methods = {method for chains in callchains.values() for chain in chains for method in chain}
for method in all_methods:
    G_method = nx.DiGraph()
    for test_name, chains in callchains.items():
        for chain in chains:
            if method in chain:
                G_method.add_edge(test_name, chain[0])
                for i in range(len(chain) - 1):
                    G_method.add_edge(chain[i], chain[i + 1])
    if G_method.number_of_nodes() > 0:
        filename = f"html/methods/{convert_method_name(method)}_call_chain.html"
        create_figure(G_method, f"{method} Call Chains", filename)
