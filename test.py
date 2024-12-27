from pycfg.pycfg import PyCFG, CFGNode, slurp 
import argparse
import tkinter as tk
from PIL import Image, ImageTk

parser = argparse.ArgumentParser()

parser.add_argument('pythonfile', help='解析するPythonファイル')
args = parser.parse_args()
arcs = []

cfg = PyCFG()
cfg.gen_cfg(slurp(args.pythonfile).strip())
g = CFGNode.to_graph(arcs)
g.draw(args.pythonfile + '.png', prog='dot')

# tkinterを使用して描画
root = tk.Tk()
root.title("制御フローグラフ")
img1 = Image.open(str(args.pythonfile) + ".png")  # PILソリューション
img1 = img1.resize((800, 600), Image.LANCZOS)
img = ImageTk.PhotoImage(img1)

background = "gray"

panel = tk.Label(root, height=600, image=img)
panel.pack(side="top", fill="both", expand="yes")
nodes = g.number_of_nodes()  # ノード数
edges = g.number_of_edges()  # エッジ数
complexity = edges - nodes + 2  # 循環的複雑度

frame = tk.Frame(root, bg=background)
frame.pack(side="bottom", fill="both", expand="yes")

tk.Label(frame, text="ノード数\t\t" + str(nodes), bg=background).pack()
tk.Label(frame, text="エッジ数\t\t" + str(edges), bg=background).pack()
tk.Label(frame, text="循環的複雑度\t" + str(complexity), bg=background).pack()

root.mainloop()