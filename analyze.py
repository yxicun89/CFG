# import ast
# import networkx as nx

# class CFGBuilder(ast.NodeVisitor):
#     def __init__(self):
#         self.graph = nx.DiGraph()
#         self.current_node = None
#         self.counter = 0

#     def add_node(self, name):
#         self.counter += 1
#         node_name = f"{name}_{self.counter}"
#         self.graph.add_node(node_name)
#         return node_name

#     def visit_FunctionDef(self, node):
#         func_node = self.add_node(f"Function: {node.name}")
#         if self.current_node:
#             self.graph.add_edge(self.current_node, func_node)
#         self.current_node = func_node
#         self.generic_visit(node)

#     def visit_If(self, node):
#         if_node = self.add_node("If")
#         self.graph.add_edge(self.current_node, if_node)
#         self.current_node = if_node
#         self.generic_visit(node)

#     def visit_For(self, node):
#         for_node = self.add_node("For")
#         self.graph.add_edge(self.current_node, for_node)
#         self.current_node = for_node
#         self.generic_visit(node)

#     def visit_While(self, node):
#         while_node = self.add_node("While")
#         self.graph.add_edge(self.current_node, while_node)
#         self.current_node = while_node
#         self.generic_visit(node)

#     def build(self, source_code):
#         tree = ast.parse(source_code)
#         print(ast.dump(tree))
#         self.visit(tree)
#         print(self.graph.nodes)
#         return self.graph

# # Pythonコードを解析
# source_code = """
# def example():
#     for i in range(10):
#         if i % 2 == 0:
#             print(i)
# """
# builder = CFGBuilder()
# cfg = builder.build(source_code)

# # サイクル数を計算
# cycles = list(nx.simple_cycles(cfg))
# print(f"サイクル数: {len(cycles)}")


# import ast
# import networkx as nx

# class CFGBuilder(ast.NodeVisitor):
#     def __init__(self):
#         self.graph = nx.DiGraph()
#         self.current_node = None
#         self.counter = 0

#     def add_node(self, name):
#         """ノードを追加して名前を返す"""
#         self.counter += 1
#         node_name = f"{name}_{self.counter}"
#         self.graph.add_node(node_name)
#         print(f"ノード追加: {node_name}")
#         return node_name

#     def visit_FunctionDef(self, node):
#         print(f"訪問: FunctionDef ({node.name})")
#         func_node = self.add_node(f"Function: {node.name}")
#         if self.current_node:
#             self.graph.add_edge(self.current_node, func_node)
#             print(f"エッジ追加: {self.current_node} -> {func_node}")
#         self.current_node = func_node
#         self.generic_visit(node)

#     def visit_If(self, node):
#         print("訪問: If 文")
#         if_node = self.add_node("If")
#         self.graph.add_edge(self.current_node, if_node)
#         print(f"エッジ追加: {self.current_node} -> {if_node}")
#         self.current_node = if_node
#         self.generic_visit(node)

#     def visit_For(self, node):
#         print("訪問: For 文")
#         for_node = self.add_node("For")
#         self.graph.add_edge(self.current_node, for_node)
#         print(f"エッジ追加: {self.current_node} -> {for_node}")
#         self.current_node = for_node
#         self.generic_visit(node)

#     def visit_While(self, node):
#         print("訪問: While 文")
#         while_node = self.add_node("While")
#         self.graph.add_edge(self.current_node, while_node)
#         print(f"エッジ追加: {self.current_node} -> {while_node}")
#         self.current_node = while_node
#         self.generic_visit(node)

#     def build(self, source_code):
#         print("構文木を構築中...")
#         tree = ast.parse(source_code)
#         print(ast.dump(tree, indent=4))  # 構文木全体の出力（デバッグ用）
#         self.visit(tree)
#         return self.graph

# # Pythonコードを解析
# source_code = """
# def example():
#     for i in range(10):
#         if i % 2 == 0:
#             print(i)
# """

# builder = CFGBuilder()
# cfg = builder.build(source_code)

# # サイクル数を計算
# print("\n--- サイクル数を計算 ---")
# cycles = list(nx.simple_cycles(cfg))
# print(f"サイクル数: {len(cycles)}")
# print("\n--- ノード一覧 ---")
# print(cfg.nodes())
# print("\n--- エッジ一覧 ---")
# print(cfg.edges())




import ast
import networkx as nx
import matplotlib.pyplot as plt

class CFGBuilder(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.current_node = None
        self.counter = 0

    def add_node(self, name):
        self.counter += 1
        node_name = f"{name}_{self.counter}"
        self.graph.add_node(node_name)
        return node_name

    def visit_FunctionDef(self, node):
        func_node = self.add_node(f"Function: {node.name}")
        if self.current_node:
            self.graph.add_edge(self.current_node, func_node)
        self.current_node = func_node
        self.generic_visit(node)

    def visit_If(self, node):
        if_node = self.add_node("If")
        self.graph.add_edge(self.current_node, if_node)
        self.current_node = if_node
        self.generic_visit(node)

    def visit_For(self, node):
        for_node = self.add_node("For")
        self.graph.add_edge(self.current_node, for_node)
        self.current_node = for_node
        self.generic_visit(node)

    def visit_While(self, node):
        while_node = self.add_node("While")
        self.graph.add_edge(self.current_node, while_node)
        self.current_node = while_node
        self.generic_visit(node)

    def build(self, source_code):
        tree = ast.parse(source_code)
        self.visit(tree)
        return self.graph

# # 特徴量計算関数
# def analyze_cfg(graph):
#     # Connected Components
#     connected_components = list(nx.weakly_connected_components(graph))
#     num_connected_components = len(connected_components)
    
#     # Loop Statements (For, While ノード数)
#     loop_statements = sum(1 for node in graph.nodes if "For" in node or "While" in node)
    
#     # Conditional Statements (If ノード数)
#     conditional_statements = sum(1 for node in graph.nodes if "If" in node)
    
#     # Cycles
#     cycles = list(nx.simple_cycles(graph))
#     num_cycles = len(cycles)
    
#     # Paths
#     paths = list(nx.all_simple_paths(graph, source=min(graph.nodes), target=max(graph.nodes)))
#     num_paths = len(paths)
    
#     # Cyclomatic Complexity (E - N + 2 * P)
#     edges = graph.number_of_edges()
#     nodes = graph.number_of_nodes()
#     cyclomatic_complexity = edges - nodes + 2 * num_connected_components
    
#     return {
#         "connected_components": num_connected_components,
#         "loop_statements": loop_statements,
#         "conditional_statements": conditional_statements,
#         "cycles": num_cycles,
#         "paths": num_paths,
#         "cyclomatic_complexity": cyclomatic_complexity,
#     }

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
    print("Done")
"""


builder = CFGBuilder()
cfg = builder.build(source_code)
# analysis = analyze_cfg(cfg)

# 結果表示
# print("\n--- 制御フローグラフ解析結果 ---")
# for feature, value in analysis.items():
#     print(f"{feature}: {value}")
# グラフの視覚化
def visualize_cfg(graph):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)  # レイアウト設定
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=3000, font_size=10, font_color='black', font_weight='bold', edge_color='gray')
    plt.title("Control Flow Graph (CFG)")
    plt.show()

visualize_cfg(cfg)