# import argparse
# from pycfg.pycfg import PyCFG, CFGNode, slurp

# def extract_features(pythonfile):
#     """ 指定した Python ファイルの制御フローグラフ（CFG）を解析し、特徴量を取得する """

#     # 制御フローグラフの生成
#     cfg = PyCFG()
#     cfg.gen_cfg(slurp(pythonfile).strip())

#     # ユニークなノード数をカウント
#     nodes = set(CFGNode.cache.keys())
#     node_count = len(nodes)

#     # ユニークなエッジを取得（親 → 子 の関係）
#     edge_set = set()
#     for node in CFGNode.cache.values():
#         for child in node.children:
#             edge_set.add((node.rid, child.rid))
#     edge_count = len(edge_set)

#     # McCabe’s Cyclomatic Complexity（循環的複雑度）
#     complexity = edge_count - node_count + 2

#     # ループ数（for / while）
#     loop_count = sum(1 for node in CFGNode.cache.values() if "_for:" in node.source() or "_while:" in node.source())

#     # 条件分岐（if / elif）
#     conditional_count = sum(1 for node in CFGNode.cache.values() if "_if:" in node.source())

#     # サイクル数（再帰的なエッジ）
#     cycle_count = sum(1 for node in CFGNode.cache.values() if any(child.rid == node.rid for child in node.children))

#     # 連結成分数（Connected Components）
#     visited = set()
#     def dfs(node):
#         if node.rid in visited:
#             return
#         visited.add(node.rid)
#         for child in node.children:
#             dfs(child)

#     component_count = 0
#     for node in CFGNode.cache.values():
#         if node.rid not in visited:
#             dfs(node)
#             component_count += 1

#     # 特徴量を辞書で返す
#     return {
#         "nodes": node_count,
#         "edges": edge_count,
#         "cyclomatic_complexity": complexity,
#         "loop_statements": loop_count,
#         "conditional_statements": conditional_count,
#         "cycles": cycle_count,
#         "connected_components": component_count
#     }

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("pythonfile", help="解析する Python ファイル")
#     args = parser.parse_args()

#     features = extract_features(args.pythonfile)

#     # 結果を表示
#     print("=== 制御フローグラフ（CFG）特徴量 ===")
#     for key, value in features.items():
#         print(f"{key}: {value}")

import argparse
from pycfg.pycfg import PyCFG, CFGNode, slurp
from collections import deque

def count_all_paths_dfs(start_node, end_node):
    """ DFS を用いて、開始ノードから終了ノードまでのすべてのパスをカウント """
    def dfs(node, visited):
        if node == end_node:
            return 1  # ゴールに到達した場合、1つのパス
        count = 0
        for child in node.children:
            if child.rid not in visited:  # 無限ループを防ぐ
                count += dfs(child, visited | {child.rid})
        return count
    
    return dfs(start_node, {start_node.rid})

def count_paths_topological(cfg):
    """ トポロジカルソートを用いて、各ノードへのパス数を計算 """
    in_degree = {node.rid: 0 for node in cfg.values()}
    path_count = {node.rid: 0 for node in cfg.values()}
    
    # 入次数を計算
    for node in cfg.values():
        for child in node.children:
            in_degree[child.rid] += 1
    
    # トポロジカルソート
    queue = [node for node in cfg.values() if in_degree[node.rid] == 0]
    
    # 開始ノードにパスを 1 つ設定
    start_node = queue[0]
    path_count[start_node.rid] = 1  

    while queue:
        node = queue.pop(0)
        for child in node.children:
            path_count[child.rid] += path_count[node.rid]
            in_degree[child.rid] -= 1
            if in_degree[child.rid] == 0:
                queue.append(child)
    
    # 最後のノードのパス数を返す
    end_node = max(cfg.values(), key=lambda x: x.rid)
    return path_count[end_node.rid]

def extract_features(pythonfile):
    """ 指定した Python ファイルの制御フローグラフ（CFG）を解析し、特徴量を取得する """

    # 制御フローグラフの生成
    cfg = PyCFG()
    cfg.gen_cfg(slurp(pythonfile).strip())

    # ユニークなノード数をカウント
    nodes = set(CFGNode.cache.keys())
    node_count = len(nodes)

    # ユニークなエッジを取得
    edge_set = set()
    for node in CFGNode.cache.values():
        for child in node.children:
            edge_set.add((node.rid, child.rid))
    edge_count = len(edge_set)

    # Cyclomatic Complexity（循環的複雑度）
    complexity = edge_count - node_count + 2

    # ループ数（for / while）
    loop_count = sum(1 for node in CFGNode.cache.values() if "_for:" in node.source() or "_while:" in node.source())

    # 条件分岐数（if / elif）
    conditional_count = sum(1 for node in CFGNode.cache.values() if "_if:" in node.source())

    # サイクル数
    cycle_count = sum(1 for node in CFGNode.cache.values() if any(child.rid == node.rid for child in node.children))

    # 連結成分数
    visited = set()
    def dfs(node):
        if node.rid in visited:
            return
        visited.add(node.rid)
        for child in node.children:
            dfs(child)

    component_count = 0
    for node in CFGNode.cache.values():
        if node.rid not in visited:
            dfs(node)
            component_count += 1

    # **開始ノードと終了ノードを取得**
    start_node = next(iter(CFGNode.cache.values()))
    end_node = next(reversed(list(CFGNode.cache.values())))

    # **DFS でパス数をカウント**
    path_count_dfs = count_all_paths_dfs(start_node, end_node)

    # **トポロジカルソートでパス数を計算**
    path_count_topological = count_paths_topological(CFGNode.cache)

    # 特徴量の辞書を作成
    features = {
        "Nodes (ノード数)": node_count,
        "Edges (エッジ数)": edge_count,
        "Cyclomatic Complexity (循環的複雑度)": complexity,
        "Loop Statements (ループ数)": loop_count,
        "Conditional Statements (条件分岐数)": conditional_count,
        "Cycles (サイクル数)": cycle_count,
        "Connected Components (連結成分数)": component_count,
        "Paths (DFS 計測)": path_count_dfs,
        "Paths (Topological 計測)": path_count_topological
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
