# import argparse
# from pycfg.pycfg import PyCFG, CFGNode, slurp
# from collections import deque

# def count_all_paths_dfs(start_node, end_node):
#     """ DFS を用いて、開始ノードから終了ノードまでのすべてのパスをカウント """
#     def dfs(node, visited):
#         if node == end_node:
#             return 1  # ゴールに到達した場合、1つのパス
#         count = 0
#         for child in node.children:
#             if child.rid not in visited:  # 無限ループを防ぐ
#                 count += dfs(child, visited | {child.rid})
#         return count

#     return dfs(start_node, {start_node.rid})

# def count_paths_topological(cfg):
#     """ トポロジカルソートを用いて、各ノードへのパス数を計算 """
#     in_degree = {node.rid: 0 for node in cfg.values()}
#     path_count = {node.rid: 0 for node in cfg.values()}

#     # 入次数を計算
#     for node in cfg.values():
#         for child in node.children:
#             in_degree[child.rid] += 1

#     # トポロジカルソート
#     queue = [node for node in cfg.values() if in_degree[node.rid] == 0]

#     # 開始ノードにパスを 1 つ設定
#     start_node = queue[0]
#     path_count[start_node.rid] = 1

#     while queue:
#         node = queue.pop(0)
#         for child in node.children:
#             path_count[child.rid] += path_count[node.rid]
#             in_degree[child.rid] -= 1
#             if in_degree[child.rid] == 0:
#                 queue.append(child)

#     # 最後のノードのパス数を返す
#     end_node = max(cfg.values(), key=lambda x: x.rid)
#     return path_count[end_node.rid]

# def extract_features(pythonfile):
#     """ 指定した Python ファイルの制御フローグラフ（CFG）を解析し、特徴量を取得する """

#     # 制御フローグラフの生成
#     cfg = PyCFG()
#     cfg.gen_cfg(slurp(pythonfile).strip())

#     # ユニークなノード数をカウント
#     nodes = set(CFGNode.cache.keys())
#     node_count = len(nodes)

#     # ユニークなエッジを取得
#     edge_set = set()
#     for node in CFGNode.cache.values():
#         for child in node.children:
#             edge_set.add((node.rid, child.rid))
#     edge_count = len(edge_set)

#     # Cyclomatic Complexity（循環的複雑度）
#     complexity = edge_count - node_count + 2

#     # ループ数（for / while）
#     loop_count = sum(1 for node in CFGNode.cache.values() if "_for:" in node.source() or "_while:" in node.source())

#     # 条件分岐数（if / elif）
#     conditional_count = sum(1 for node in CFGNode.cache.values() if "_if:" in node.source())

#     # サイクル数
#     cycle_count = sum(1 for node in CFGNode.cache.values() if any(child.rid == node.rid for child in node.children))

#     # 連結成分数
#     # visited = set()
#     # def dfs(node):
#     #     if node.rid in visited:
#     #         return
#     #     visited.add(node.rid)
#     #     for child in node.children:
#     #         dfs(child)

#     # component_count = 0
#     # for node in CFGNode.cache.values():
#     #     if node.rid not in visited:
#     #         dfs(node)
#     #         component_count += 1
#     visited = set()
#     def dfs(node):
#       if node.rid in visited:
#         return
#       visited.add(node.rid)
#       for child in node.children:
#         dfs(child)

#     component_count = 0
#     for node in CFGNode.cache.values():
#     # ⭐️ ダミーノード（start, stop）を無視
#       if node.rid not in visited and node.source() != "start" and node.source() != "stop":
#         dfs(node)
#         component_count += 1


#     # **開始ノードと終了ノードを取得**
#     start_node = next(iter(CFGNode.cache.values()))
#     end_node = next(reversed(list(CFGNode.cache.values())))

#     # **DFS でパス数をカウント**
#     path_count_dfs = count_all_paths_dfs(start_node, end_node)

#     # **トポロジカルソートでパス数を計算**
#     path_count_topological = count_paths_topological(CFGNode.cache)

#     # 特徴量の辞書を作成
#     features = {
#         "Nodes (ノード数)": node_count,
#         "Edges (エッジ数)": edge_count,
#         "Cyclomatic Complexity (循環的複雑度)": complexity,
#         "Loop Statements (ループ数)": loop_count,
#         "Conditional Statements (条件分岐数)": conditional_count,
#         "Cycles (サイクル数)": cycle_count,
#         "Connected Components (連結成分数)": component_count,
#         "Paths (DFS 計測)": path_count_dfs,
#         "Paths (Topological 計測)": path_count_topological
#     }

#     return features

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("pythonfile", help="解析する Python ファイル")
#     args = parser.parse_args()

#     features = extract_features(args.pythonfile)

#     # === 結果を表示 ===
#     print("\n=== 制御フローグラフ（CFG）特徴量 ===")
#     for key, value in features.items():
#         print(f"{key}: {value}")

# import argparse
# import ast
# import tkinter as tk
# from PIL import Image, ImageTk
# from pycfg.pycfg import PyCFG, CFGNode, slurp
# from collections import deque

# def extract_function_arguments(pythonfile, function_name):
#     """ Python ファイルを AST 解析して、指定された関数の引数を取得 """
#     with open(pythonfile, "r") as f:
#         source = f.read()
#     tree = ast.parse(source)

#     for node in ast.walk(tree):
#         if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == function_name:
#             if len(node.args) > 0 and isinstance(node.args[0], ast.Constant):
#                 return node.args[0].value  # `example(5)` の `5` を取得
#     return None  # 取得できない場合は `None`

# def estimate_loop_iterations(node, execution_value):
#     """ for / while ループの最大繰り返し回数を推定 """
#     try:
#         source = node.source()
#         if "_for:" in source:
#             return execution_value if execution_value is not None else 0
#         elif "_while:" in source:
#             return execution_value if execution_value is not None else 0
#     except Exception:
#         return 0  # 解析できない場合はデフォルト
#     return 0

# def count_loop_statements(cfg):
#     """ プログラムに書かれたループ（for, while）の数をカウント """
#     return sum(1 for node in cfg.values() if "_for:" in node.source() or "_while:" in node.source())

# def count_cycles(cfg, execution_value):
#     """ ループの実行回数（ループごとの最大実行回数）と再帰呼び出しの回数を考慮したサイクル数 """
#     cycle_count = 0

#     for node in cfg.values():
#         cycle_count += estimate_loop_iterations(node, execution_value)

#         # 再帰呼び出しのカウント
#         if node.source().startswith("call:"):
#             called_function = node.source().split(":")[1].strip()
#             if called_function in cfg and any(called_function in c.source() for c in cfg.values()):
#                 cycle_count += 1  # 再帰関数のサイクル
#     return cycle_count

# def count_paths(cfg, start_node, end_node):
#     """ DFS（深さ優先探索）を用いて、CFG のすべての実行経路（Paths）の数をカウント """
#     def dfs(node, visited):
#         if node == end_node:
#             return 1
#         visited.add(node)
#         path_count = 0
#         for child in node.children:
#             if child not in visited:
#                 path_count += dfs(child, visited.copy())
#         return path_count

#     return dfs(start_node, set())

# def extract_features(pythonfile):
#     """ 指定した Python ファイルの制御フローグラフ（CFG）を解析し、特徴量を取得する """

#     # 実行回数の取得 (`example(5)` の `5` を取得)
#     execution_value = extract_function_arguments(pythonfile, "example")

#     # 制御フローグラフの生成
#     cfg = PyCFG()
#     cfg.gen_cfg(slurp(pythonfile).strip())

#     # `pygraphviz` を使ってエッジ数を取得
#     arcs = []
#     g = CFGNode.to_graph(arcs)
#     g.draw(pythonfile + ".png", prog="dot")

#     # 正しいエッジ数・ノード数を取得
#     node_count = g.number_of_nodes()
#     edge_count = g.number_of_edges()

#     # Cyclomatic Complexity（循環的複雑度）
#     complexity = edge_count - node_count + 2

#     # ループ文（for / while）の数
#     loop_statements = count_loop_statements(CFGNode.cache)

#     # サイクル数（ループの実行回数＋再帰の回数）
#     cycles = count_cycles(CFGNode.cache, execution_value)

#     # 条件分岐数（if / elif）
#     conditional_count = sum(1 for node in CFGNode.cache.values() if "_if:" in node.source())

#     # 連結成分数
#     visited = set()
#     def dfs_component(node):
#         if node.rid in visited:
#             return
#         visited.add(node.rid)
#         for child in node.children:
#             dfs_component(child)

#     component_count = 0
#     for node in CFGNode.cache.values():
#         if node.rid not in visited and node.source() != "start" and node.source() != "stop":
#             dfs_component(node)
#             component_count += 1

#     # パス数の計算（開始ノード → 終了ノード）
#     start_node = CFGNode.cache[0]  # `start` ノード
#     end_node = max(CFGNode.cache.values(), key=lambda n: n.rid)  # `stop` に最も近いノード
#     paths = count_paths(CFGNode.cache, start_node, end_node)

#     # **特徴量の辞書を作成**
#     features = {
#         "Nodes (ノード数)": node_count,
#         "Edges (エッジ数)": edge_count,
#         "Cyclomatic Complexity (循環的複雑度)": complexity,
#         "Loop Statements (ループの数)": loop_statements,
#         "Cycles (ループの実行回数 + 再帰回数)": cycles,
#         "Conditional Statements (条件分岐数)": conditional_count,
#         "Connected Components (連結成分数)": component_count,
#         "Paths (実行パス数)": paths,
#     }

#     return features

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("pythonfile", help="解析する Python ファイル")
#     args = parser.parse_args()

#     features = extract_features(args.pythonfile)

#     # === 結果を表示 ===
#     print("\n=== 制御フローグラフ（CFG）特徴量 ===")
#     for key, value in features.items():
#         print(f"{key}: {value}")


import argparse
import ast
import tkinter as tk
from PIL import Image, ImageTk
from pycfg.pycfg import PyCFG, CFGNode, slurp
from collections import deque

def extract_function_arguments(pythonfile, function_name):
    """PythonファイルをAST解析して、指定された関数の引数を取得"""
    with open(pythonfile, "r") as f:
        source = f.read()
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == function_name:
            if len(node.args) > 0 and isinstance(node.args[0], ast.Constant):
                return node.args[0].value  # `example(5)` の `5` を取得
    return None  # 取得できない場合は `None`

def estimate_loop_iterations(node, execution_value):
    """for / while ループの最大繰り返し回数を推定"""
    try:
        source = node.source()
        if "_for:" in source:
            return execution_value if execution_value is not None else 0
        elif "_while:" in source:
            return execution_value if execution_value is not None else 0
    except Exception:
        return 0  # 解析できない場合はデフォルト
    return 0

def count_loop_statements(cfg):
    """プログラムに書かれたループ（for, while）の数をカウント"""
    return sum(1 for node in cfg.values() if "_for:" in node.source() or "_while:" in node.source())

def count_cycles(cfg, execution_value):
    """ループの実行回数（ループごとの最大実行回数）と再帰呼び出しの回数を考慮したサイクル数"""
    cycle_count = 0

    for node in cfg.values():
        cycle_count += estimate_loop_iterations(node, execution_value)

        # 再帰呼び出しのカウント
        if node.source().startswith("call:"):
            called_function = node.source().split(":")[1].strip()
            if called_function in cfg and any(called_function in c.source() for c in cfg.values()):
                cycle_count += 1  # 再帰関数のサイクル
    return cycle_count

def count_paths(cfg, start_node, end_node):
    """DFS（深さ優先探索）を用いて、CFG のすべての実行経路（Paths）の数をカウント"""
    def dfs(node, visited):
        if node.rid == end_node.rid:
            return 1  # 終了ノードに到達したらパスが 1 つ成立
        visited.add(node.rid)  # `CFGNode` ではなく `rid`（一意の ID）を保存
        path_count = 0
        for child in node.children:
            if child.rid not in visited:  # `CFGNode` ではなく `rid` を比較
                path_count += dfs(child, visited.copy())  # 新しい `set()` を渡す
        return path_count

    return dfs(start_node, set())  # 訪問済みノードを記録する `set()` を渡す

def extract_features(pythonfile):
    """指定した Python ファイルの制御フローグラフ（CFG）を解析し、特徴量を取得する"""

    # 実行回数の取得 (`example(5)` の `5` を取得)
    execution_value = extract_function_arguments(pythonfile, "example")

    # 制御フローグラフの生成
    cfg = PyCFG()
    cfg.gen_cfg(slurp(pythonfile).strip())

    # `pygraphviz` を使ってエッジ数を取得
    arcs = []
    g = CFGNode.to_graph(arcs)
    g.draw(pythonfile + ".png", prog="dot")

    # 正しいエッジ数・ノード数を取得
    node_count = g.number_of_nodes()
    edge_count = g.number_of_edges()

    # Cyclomatic Complexity（循環的複雑度）
    complexity = edge_count - node_count + 2

    # ループ文（for / while）の数
    loop_statements = count_loop_statements(CFGNode.cache)

    # サイクル数（ループの実行回数＋再帰の回数）
    cycles = count_cycles(CFGNode.cache, execution_value)

    # 条件分岐数（if / elif）
    conditional_count = sum(1 for node in CFGNode.cache.values() if "_if:" in node.source())

    # 連結成分数
    visited = set()
    def dfs_component(node):
        if node.rid in visited:
            return
        visited.add(node.rid)
        for child in node.children:
            dfs_component(child)

    component_count = 0
    for node in CFGNode.cache.values():
        if node.rid not in visited and node.source() != "start" and node.source() != "stop":
            dfs_component(node)
            component_count += 1

    # パス数の計算（開始ノード → 終了ノード）
    start_node = CFGNode.cache[0]  # `start` ノード
    end_node = max(CFGNode.cache.values(), key=lambda n: n.rid)  # `stop` に最も近いノード
    paths = count_paths(CFGNode.cache, start_node, end_node)

    # **特徴量の辞書を作成**
    features = {
        "Nodes (ノード数)": node_count,
        "Edges (エッジ数)": edge_count,
        "Cyclomatic Complexity (循環的複雑度)": complexity,
        "Loop Statements (ループの数)": loop_statements,
        "Cycles (ループの実行回数 + 再帰回数)": cycles,
        "Conditional Statements (条件分岐数)": conditional_count,
        "Connected Components (連結成分数)": component_count,
        "Paths (実行パス数)": paths,
    }

    return features

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pythonfile", help="解析する Python ファイル")
    args = parser.parse_args()

    features = extract_features(args.pythonfile)

    # === 結果を表示 ===
    print("\n=== 制御フローグラフ（CFG）特徴量 ===")
    for key, value in features.items():
        print(f"{key}: {value}")

    # GUI で表示
    root = tk.Tk()
    root.title("制御フローグラフ")
    img1 = Image.open(args.pythonfile + ".png")
    img1 = img1.resize((800, 600), Image.LANCZOS)
    img = ImageTk.PhotoImage(img1)

    panel = tk.Label(root, height=600, image=img)
    panel.pack(side="top", fill="both", expand="yes")

    background = "gray"
    frame = tk.Frame(root, bg=background)
    frame.pack(side="bottom", fill="both", expand="yes")

    tk.Label(frame, text="ノード数\t\t" + str(features["Nodes (ノード数)"]), bg=background).pack()
    tk.Label(frame, text="エッジ数\t\t" + str(features["Edges (エッジ数)"]), bg=background).pack()
    tk.Label(frame, text="循環的複雑度\t" + str(features["Cyclomatic Complexity (循環的複雑度)"]), bg=background).pack()

    root.mainloop()
