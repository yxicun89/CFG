import ast
import networkx as nx
import matplotlib.pyplot as plt

class CFGBuilder(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.current_node = None
        self.counter = 0
        self.parent_stack = []  # 親ノードを追跡するためのスタック

    def add_node(self, name):
        self.counter += 1
        node_name = f"{name}_{self.counter}"
        self.graph.add_node(node_name)
        return node_name

    def add_edge(self, from_node, to_node, label=""):
        self.graph.add_edge(from_node, to_node, label=label)

    def visit_FunctionDef(self, node):
        func_node = self.add_node(f"Function: {node.name}")
        if self.current_node:
            self.add_edge(self.current_node, func_node)
        self.current_node = func_node
        self.parent_stack.append(func_node)

        # Visit children nodes
        for stmt in node.body:
            self.visit(stmt)

        self.parent_stack.pop()

    def visit_If(self, node):
        if_node = self.add_node("If")
        self.add_edge(self.current_node, if_node)
        self.current_node = if_node

        # True branch
        true_node = self.add_node("True")
        self.add_edge(if_node, true_node, label="True")
        self.parent_stack.append(self.current_node)
        self.current_node = true_node
        for stmt in node.body:
            self.visit(stmt)
        self.current_node = self.parent_stack.pop()

        # False branch
        if node.orelse:
            false_node = self.add_node("False")
            self.add_edge(if_node, false_node, label="False")
            self.parent_stack.append(self.current_node)
            self.current_node = false_node
            for stmt in node.orelse:
                self.visit(stmt)
            self.current_node = self.parent_stack.pop()

    def visit_For(self, node):
        for_node = self.add_node("For")
        self.add_edge(self.current_node, for_node)
        self.current_node = for_node
        self.parent_stack.append(self.current_node)
        for stmt in node.body:
            self.visit(stmt)
        self.add_edge(self.current_node, for_node, label="Loop Back")
        self.current_node = self.parent_stack.pop()

    def visit_While(self, node):
        while_node = self.add_node("While")
        self.add_edge(self.current_node, while_node)
        self.current_node = while_node
        self.parent_stack.append(self.current_node)
        for stmt in node.body:
            self.visit(stmt)
        self.add_edge(self.current_node, while_node, label="Loop Back")
        self.current_node = self.parent_stack.pop()

    def build(self, source_code):
        tree = ast.parse(source_code)
        self.visit(tree)
        return self.graph


# CFGの可視化
def visualize_cfg(graph):
    plt.figure(figsize=(14, 10))  # 図のサイズを調整
    pos = nx.spring_layout(graph, seed=42, k=0.5)  # レイアウトを調整
    edge_labels = nx.get_edge_attributes(graph, "label")

    # ノードの描画
    nx.draw(
        graph, 
        pos, 
        with_labels=True, 
        node_color='skyblue', 
        node_size=3000, 
        font_size=10, 
        font_color='black', 
        font_weight='bold', 
        edge_color='gray', 
        alpha=0.9, 
        linewidths=1.5
        )

    # エッジラベルの描画（ラベル位置調整）
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color="red", label_pos=0.5)

    plt.title("Control Flow Graph (CFG)", fontsize=16)
    plt.axis('off')  # 軸を非表示にする
    plt.show()

# サンプルコード解析
source_code = """
def example(x):
    if x > 0:
        for i in range(x):
            if i % 2 == 0:
                print(f"Even: {i}")
            else:
                print(f"Odd: {i}")
    else:
        while x < 0:
            print(f"Negative: {x}")
            x += 1

    if x > 10:
        print("Done")
    else:
        print("Not Done")
"""

builder = CFGBuilder()
cfg = builder.build(source_code)

# CFGを可視化
visualize_cfg(cfg)



