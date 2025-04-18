import networkx as nx
import gast
from python_graphs import control_flow
import inspect
import matplotlib.pyplot as plt

# 解析対象の関数を定義
def example(x):
    if x > 0:
        for i in range(x):
            print(i)
    else:
        while x < 0:
            x += 1
    return x

# 制御フローグラフを生成
cfg = control_flow.get_control_flow_graph(example)

# # ノードの属性を確認
# for node in cfg.nodes:
#     print(f"Node: {node}")
#     print(f"Attributes: {dir(node)}")
#     break  # 最初のノードだけ確認

# # ノードの instruction 属性を確認
# for node in cfg.nodes:
#     print(f"Node: {node}")
#     print(f"Instruction: {node.instruction}")
#     if node.instruction:
#         print(f"Instruction Node: {node.instruction.node}")
#         print(f"Instruction Node Type: {type(node.instruction.node)}")
#     break  # 最初のノードだけ確認

# # ノードの instruction.node を確認
# for node in cfg.nodes:
#     if node.instruction and node.instruction.node:
#         print(f"Instruction Node: {node.instruction.node}")
#         print(f"Instruction Node Type: {type(node.instruction.node)}")

# 制御フローグラフのノードを確認
for node in cfg.nodes:
    print(f"Node: {node}")
    print(f"Instruction: {node.instruction}")
    if node.instruction:
        print(f"Instruction Node: {node.instruction.node}")
        print(f"Instruction Node Type: {type(node.instruction.node)}")
    # ラベルを取得する場合、適切なラベル名を指定
    if hasattr(node, 'get_label'):
        try:
            print(f"Labels: {node.get_label('example_label')}")  # 'example_label' を適切なラベル名に置き換え
        except KeyError:
            print("Labels: No label with the specified name")
    else:
        print("Labels: No label method available")
    print("-" * 50)

# # NetworkX のグラフを作成
# G = nx.DiGraph()
# for node in cfg.nodes:
#     G.add_node(node)  # ノードを追加
#     for next_node in node.next:  # 後続ノードを取得
#         G.add_edge(node.uuid, next_node.uuid)  # エッジもUUIDを使用

# # 特徴量の計算
# num_nodes = G.number_of_nodes()
# num_edges = G.number_of_edges()
# num_connected_components = nx.number_weakly_connected_components(G)
# num_cycles = len(list(nx.simple_cycles(G)))
# cyclomatic_complexity = num_edges - num_nodes + 2 * num_connected_components

# ループ文と条件文の数を計算
# num_loops = sum(1 for node in cfg.nodes if isinstance(node.instruction.node, (ast.For, ast.While)))
# num_conditionals = sum(1 for node in cfg.nodes if isinstance(node.instruction.node, ast.If))
# num_loops = 0
# num_conditionals = 0

# for node in cfg.nodes:
#     if node.instruction and node.instruction.node:
#         ast_node = node.instruction.node
#         # ループ文を検出
#         if isinstance(ast_node, (gast.For, gast.While)):
#             num_loops += 1
#         # 条件文を検出
#         elif isinstance(ast_node, gast.If):
#             num_conditionals += 1


# ノード数を計算
num_nodes = len(cfg.nodes)

# エッジ数を計算
num_edges = sum(len(node.next) for node in cfg.nodes)

# 連結成分数を計算
def calculate_connected_components(cfg):
    visited = set()
    components = 0

    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        for next_node in node.next:
            dfs(next_node)

    for node in cfg.nodes:
        if node not in visited:
            components += 1
            dfs(node)

    return components

num_connected_components = calculate_connected_components(cfg)

# サイクル数を計算
def detect_cycles(cfg):
    visited = set()
    stack = set()
    cycles = 0

    def dfs(node):
        nonlocal cycles
        if node in stack:
            cycles += 1
            return
        if node in visited:
            return
        visited.add(node)
        stack.add(node)
        for next_node in node.next:
            dfs(next_node)
        stack.remove(node)

    for node in cfg.nodes:
        if node not in visited:
            dfs(node)

    return cycles

num_cycles = detect_cycles(cfg)

# サイクロマティック複雑度を計算
cyclomatic_complexity = num_edges - num_nodes + 2 * num_connected_components

# 出力
print(f"ノード数: {num_nodes}")
print(f"エッジ数: {num_edges}")
print(f"連結成分数: {num_connected_components}")
print(f"サイクル数: {num_cycles}")
print(f"サイクロマティック複雑度: {cyclomatic_complexity}")
# print(f"ループ文の数: {num_loops}")
# print(f"条件文の数: {num_conditionals}")


# ループ文と条件文をカウントするクラス
class ASTVisitor(gast.NodeVisitor):
    def __init__(self):
        self.num_loops = 0
        self.num_conditionals = 0

    def visit_For(self, node):
        self.num_loops += 1
        self.generic_visit(node)  # 子ノードも訪問

    def visit_While(self, node):
        self.num_loops += 1
        self.generic_visit(node)  # 子ノードも訪問

    def visit_If(self, node):
        self.num_conditionals += 1
        self.generic_visit(node)  # 子ノードも訪問

# 関数のソースコードを取得
source_code = inspect.getsource(example)

# AST を解析
source_ast = gast.parse(source_code)  # 関数を AST に変換
visitor = ASTVisitor()
visitor.visit(source_ast)

# 結果を取得
num_loops = visitor.num_loops
num_conditionals = visitor.num_conditionals

# 出力
print(f"ループ文の数 (AST): {num_loops}")
print(f"条件文の数 (AST): {num_conditionals}")



# # グラフを可視化
# def visualize_graph(G, entry_node=None, exit_nodes=None):
#     pos = nx.spring_layout(G)  # ノードの配置を決定
#     plt.figure(figsize=(10, 8))

#     # ノードの色を設定
#     node_colors = []
#     for node in G.nodes:
#         if node == entry_node:
#             node_colors.append('green')  # 開始ノードは緑
#         elif exit_nodes and node in exit_nodes:
#             node_colors.append('red')  # 終了ノードは赤
#         else:
#             node_colors.append('lightblue')  # その他のノードは青

#     # グラフを描画
#     nx.draw(
#         G, pos, with_labels=True, node_color=node_colors, edge_color='gray',
#         node_size=2000, font_size=10
#     )
#     plt.title("Control Flow Graph")
#     plt.show()

# # 開始ノードと終了ノードを特定
# entry_node = list(G.nodes)[0]  # 最初のノードを開始ノードと仮定
# exit_nodes = [node for node in G.nodes if G.out_degree(node) == 0]  # 出次数が0のノードを終了ノードと仮定

# # 可視化関数を呼び出し
# visualize_graph(G, entry_node=entry_node, exit_nodes=exit_nodes)
