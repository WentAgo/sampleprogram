import json
import re

import networkx as nx
import plotly.graph_objects as go

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

pos = nx.spring_layout(G, seed=42)

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
    textposition="top center",
    hoverinfo='text',
    marker=dict(
        showscale=False,
        color='lightblue',
        size=20,
        line_width=2))

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title=dict(text='Call Chain Graph', font=dict(size=20)),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False)
                ))

fig.write_html("html/callchains.html")

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

    pos_test = nx.spring_layout(G_test, seed=42)

    edge_x_test = []
    edge_y_test = []
    for edge in G_test.edges():
        x0, y0 = pos_test[edge[0]]
        x1, y1 = pos_test[edge[1]]
        edge_x_test += [x0, x1, None]
        edge_y_test += [y0, y1, None]

    edge_trace_test = go.Scatter(
        x=edge_x_test, y=edge_y_test,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x_test = []
    node_y_test = []
    node_text_test = []
    for node in G_test.nodes():
        x, y = pos_test[node]
        node_x_test.append(x)
        node_y_test.append(y)
        node_text_test.append(node)

    node_trace_test = go.Scatter(
        x=node_x_test, y=node_y_test,
        mode='markers+text',
        text=node_text_test,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color='lightblue',
            size=20,
            line_width=2))

    fig_test = go.Figure(data=[edge_trace_test, node_trace_test],
                         layout=go.Layout(
                             title=dict(text=f'{test_name} Call Chain', font=dict(size=20)),
                             showlegend=False,
                             hovermode='closest',
                             margin=dict(b=20, l=5, r=5, t=40),
                             xaxis=dict(showgrid=False, zeroline=False),
                             yaxis=dict(showgrid=False, zeroline=False)
                         ))

    filename = f"html/tests/{test_name}_call_chain.html"
    fig_test.write_html(filename)

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

    pos_method = nx.spring_layout(G_method, seed=42)

    def convert_method_name(method: str) -> str:
        return re.sub(r'\.(\w+)\[(\w+)\]', lambda m: f'.{m.group(2)}_{m.group(1)}', method)

    create_figure(G_method, pos_method, f"{method} Call Chains", f"html/methods/{convert_method_name(method)}_call_chain.html")
