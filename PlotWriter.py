#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Galgame 剧情可视化批量生成器
author : kimi
"""

import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


# ------------------ 工具函数 ------------------
def is_narrator_or_player(speaker: str) -> bool:
    """旁白 / player 没有 character 字段"""
    return speaker in ("旁白", "player")


def new_dialogue():
    """返回一条空 dialogue 模板"""
    return {
        "type": "dialogue",
        "speaker": "",
        "text": "",
        "photo": None,
        "character": {
            "emotion": "neutral",
            "position": "center",
            "voice": ""
        }
    }


def new_choice():
    """返回一条空 choice 模板"""
    return {
        "type": "choice",
        "photo": None,
        "speaker": "",
        "character": {
            "emotion": "neutral",
            "position": "center"
        },
        "choices": []
    }


# ------------------ 主窗口 ------------------
class GalEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Galgame 剧情批量生成器")
        self.geometry("1000x700")
        self.scenes = {}          # 所有场景数据
        self.cur_scene_id = None  # 当前正在编辑的场景
        self.cur_item_idx = None  # 当前正在编辑的条目索引
        self.filepath = None      # 当前打开的文件

        # ---- 顶部菜单 ----
        menubar = tk.Menu(self)
        menu_file = tk.Menu(menubar, tearoff=0)
        menu_file.add_command(label="新建", command=self.file_new)
        menu_file.add_command(label="打开", command=self.file_open)
        menu_file.add_command(label="保存", command=self.file_save)
        menu_file.add_command(label="另存为", command=self.file_saveas)
        menubar.add_cascade(label="文件", menu=menu_file)
        self.config(menu=menubar)

        # ---- 左：场景列表 ----
        left = ttk.Frame(self, width=200)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        ttk.Label(left, text="场景列表").pack(anchor=tk.W)
        self.scene_listbox = tk.Listbox(left)
        self.scene_listbox.pack(fill=tk.BOTH, expand=True)
        self.scene_listbox.bind("<<ListboxSelect>>", self.on_scene_select)

        ttk.Button(left, text="新增场景", command=self.add_scene).pack(fill=tk.X, pady=2)
        ttk.Button(left, text="删除场景", command=self.del_scene).pack(fill=tk.X)

        # ---- 中：条目列表 ----
        mid = ttk.Frame(self, width=250)
        mid.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        ttk.Label(mid, text="条目列表").pack(anchor=tk.W)
        self.item_listbox = tk.Listbox(mid)
        self.item_listbox.pack(fill=tk.BOTH, expand=True)
        self.item_listbox.bind("<<ListboxSelect>>", self.on_item_select)

        ttk.Button(mid, text="添加对话", command=lambda: self.add_item("dialogue")).pack(fill=tk.X, pady=2)
        ttk.Button(mid, text="添加分支", command=lambda: self.add_item("choice")).pack(fill=tk.X)

        # ---- 右：编辑区 ----
        right = ttk.Frame(self)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        ttk.Label(right, text="编辑区").pack(anchor=tk.W)
        self.editor = EditorPanel(right, self.on_data_changed)
        self.editor.pack(fill=tk.BOTH, expand=True)

        # ---- 底部：导出 ----
        bottom = ttk.Frame(self)
        bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        ttk.Button(bottom, text="导出 JSON（合并）", command=self.export_json).pack(side=tk.RIGHT, padx=5)

        self.file_new()

    # ---------- 文件相关 ----------
    def file_new(self):
        self.scenes = {}
        self.cur_scene_id = None
        self.cur_item_idx = None
        self.filepath = None
        self.refresh_all()

    def file_open(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            messagebox.showerror("打开失败", str(e))
            return
        self.scenes = data
        self.filepath = path
        self.refresh_all()

    def file_save(self):
        if not self.filepath:
            self.file_saveas()
            return
        self.save_to_path(self.filepath)

    def file_saveas(self):
        path = filedialog.asksaveasfilename(defaultextension=".json",
                                          filetypes=[("JSON files", "*.json")])
        if path:
            self.save_to_path(path)
            self.filepath = path

    def save_to_path(self, path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.scenes, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("保存成功", f"已保存到 {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("保存失败", str(e))

    # ---------- 场景管理 ----------
    def add_scene(self):
        """新增场景：先让用户输入场景 ID"""
        dlg = SceneNameDialog(self)
        self.wait_window(dlg)
        if not dlg.ok or not dlg.scene_id.strip():
            return
        sid = dlg.scene_id.strip()
        if sid in self.scenes:
            messagebox.showwarning("提示", f"场景 {sid} 已存在！")
            return
        self.scenes[sid] = {
            "bg": "library",
            "bgm": "normal",
            "end_with": "dialogue",
            "next_scene": None,
            "last_scene": None,
            "dialogues": []
        }
        self.refresh_scene_list()
        # 自动选中新场景
        idx = list(sorted(self.scenes.keys())).index(sid)
        self.scene_listbox.selection_clear(0, tk.END)
        self.scene_listbox.selection_set(idx)
        self.scene_listbox.see(idx)
        self.on_scene_select()

    def del_scene(self):
        if not self.cur_scene_id:
            return
        if messagebox.askyesno("确认", f"删除场景 {self.cur_scene_id}？"):
            del self.scenes[self.cur_scene_id]
            self.cur_scene_id = None
            self.refresh_all()

    def on_scene_select(self, event=None):
        sel = self.scene_listbox.curselection()
        if not sel:
            return
        self.cur_scene_id = self.scene_listbox.get(sel[0])
        self.refresh_item_list()
        self.item_listbox.selection_clear(0, tk.END)
        self.cur_item_idx = None
        self.editor.clear()

    # ---------- 条目管理 ----------
    def add_item(self, typ: str):
        if not self.cur_scene_id:
            messagebox.showwarning("提示", "请先选择或创建一个场景")
            return
        dia = new_dialogue() if typ == "dialogue" else new_choice()
        self.scenes[self.cur_scene_id]["dialogues"].append(dia)
        self.refresh_item_list()
        self.item_listbox.selection_clear(0, tk.END)
        self.item_listbox.selection_set(tk.END)
        self.on_item_select()

    def on_item_select(self, event=None):
        sel = self.item_listbox.curselection()
        if not sel:
            return
        self.cur_item_idx = int(sel[0])
        item = self.scenes[self.cur_scene_id]["dialogues"][self.cur_item_idx]
        self.editor.load(item)

    def on_data_changed(self, new_item):
        """编辑器回调：数据被修改"""
        if self.cur_scene_id is None or self.cur_item_idx is None:
            return
        self.scenes[self.cur_scene_id]["dialogues"][self.cur_item_idx] = new_item
        # 刷新 item 列表的文字
        self.refresh_item_list()

    # ---------- 导出 ----------
    def export_json(self):
        """把当前所有场景合并导出为一个 JSON"""
        if not self.scenes:
            messagebox.showwarning("提示", "没有可导出的场景")
            return
        path = filedialog.asksaveasfilename(defaultextension=".json",
                                          filetypes=[("JSON files", "*.json")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.scenes, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("导出成功", f"已导出到 {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("导出失败", str(e))

    # ---------- 刷新界面 ----------
    def refresh_all(self):
        self.refresh_scene_list()
        self.refresh_item_list()
        self.editor.clear()

    def refresh_scene_list(self):
        self.scene_listbox.delete(0, tk.END)
        for sid in sorted(self.scenes.keys()):
            self.scene_listbox.insert(tk.END, sid)

    def refresh_item_list(self):
        self.item_listbox.delete(0, tk.END)
        if not self.cur_scene_id:
            return
        for i, dia in enumerate(self.scenes[self.cur_scene_id]["dialogues"]):
            t = dia.get("type", "dialogue")
            sp = dia.get("speaker", "")
            txt = (dia.get("text", "")[:30] + "…") if len(dia.get("text", "")) > 30 else dia.get("text", "")
            self.item_listbox.insert(tk.END, f"{i+1}.[{t}]{sp}: {txt}")


# ------------------ 右侧编辑器 ------------------
class EditorPanel(ttk.Frame):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback  # 数据被修改后回调
        self.build_ui()

    def build_ui(self):
        # ---- 通用字段 ----
        frm = ttk.LabelFrame(self, text="基本信息")
        frm.pack(fill=tk.X, pady=5)
        ttk.Label(frm, text="type").grid(row=0, column=0, sticky=tk.W)
        self.type_var = tk.StringVar()
        self.type_cb = ttk.Combobox(frm, textvariable=self.type_var, state="readonly", width=10)
        self.type_cb["values"] = ("dialogue", "choice")
        self.type_cb.bind("<<ComboboxSelected>>", self.on_type_change)
        self.type_cb.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(frm, text="speaker").grid(row=0, column=2, sticky=tk.W, padx=10)
        self.speaker_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.speaker_var, width=15).grid(row=0, column=3, sticky=tk.W)

        ttk.Label(frm, text="text").grid(row=1, column=0, sticky=tk.W)
        self.text_txt = tk.Text(frm, height=4, width=60)
        self.text_txt.grid(row=1, column=1, columnspan=3, sticky=tk.W)

        # ---- character 区 ----
        self.frm_char = ttk.LabelFrame(self, text="character（旁白/player 无需填写）")
        self.frm_char.pack(fill=tk.X, pady=5)
        ttk.Label(self.frm_char, text="emotion").grid(row=0, column=0, sticky=tk.W)
        self.emotion_var = tk.StringVar()
        ttk.Entry(self.frm_char, textvariable=self.emotion_var, width=10).grid(row=0, column=1, sticky=tk.W)
        ttk.Label(self.frm_char, text="position").grid(row=0, column=2, sticky=tk.W, padx=10)
        self.position_var = tk.StringVar()
        ttk.Entry(self.frm_char, textvariable=self.position_var, width=10).grid(row=0, column=3, sticky=tk.W)
        ttk.Label(self.frm_char, text="voice").grid(row=1, column=0, sticky=tk.W)
        self.voice_var = tk.StringVar()
        ttk.Entry(self.frm_char, textvariable=self.voice_var, width=10).grid(row=1, column=1, sticky=tk.W)

        # ---- choice 区 ----
        self.frm_choice = ttk.LabelFrame(self, text="choices（仅当 type=choice 时生效）")
        self.frm_choice.pack(fill=tk.BOTH, expand=True, pady=5)
        self.choice_tree = ttk.Treeview(self.frm_choice, columns=("text", "next"), height=6)
        self.choice_tree.heading("#0", text="ID")
        self.choice_tree.heading("text", text="选项文字")
        self.choice_tree.heading("next", text="跳转场景")
        self.choice_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Button(self.frm_choice, text="添加选项", command=self.add_choice).pack(side=tk.TOP, padx=5)
        ttk.Button(self.frm_choice, text="删除选项", command=self.del_choice).pack(side=tk.TOP, padx=5, pady=2)

        # ---- 保存按钮 ----
        ttk.Button(self, text="应用修改", command=self.apply).pack(pady=5)

    # ---------- 加载 ----------
    def clear(self):
        self.type_var.set("")
        self.speaker_var.set("")
        self.text_txt.delete("1.0", tk.END)
        self.emotion_var.set("")
        self.position_var.set("")
        self.voice_var.set("")
        for i in self.choice_tree.get_children():
            self.choice_tree.delete(i)
        self.on_type_change()

    def load(self, item: dict):
        self.clear()
        self.type_var.set(item.get("type", "dialogue"))
        self.speaker_var.set(item.get("speaker", ""))
        self.text_txt.insert("1.0", item.get("text", ""))
        if "character" in item:
            c = item["character"]
            self.emotion_var.set(c.get("emotion", ""))
            self.position_var.set(c.get("position", ""))
            self.voice_var.set(c.get("voice", ""))
        if item.get("type") == "choice":
            for ch in item.get("choices", []):
                self.choice_tree.insert("", tk.END, text=ch.get("choiceId", ""),
                                      values=(ch.get("text", ""), ch.get("nextScene", "")))
        self.on_type_change()

    # ---------- 事件 ----------
    def on_type_change(self, *_):
        typ = self.type_var.get()
        # 旁白/player 不显示 character
        speaker = self.speaker_var.get()
        if is_narrator_or_player(speaker):
            self.frm_char.pack_forget()
        else:
            self.frm_char.pack(fill=tk.X, pady=5)
        # choice 区
        if typ == "choice":
            self.frm_choice.pack(fill=tk.BOTH, expand=True, pady=5)
        else:
            self.frm_choice.pack_forget()

    def add_choice(self):
        dlg = ChoiceDialog(self)
        self.wait_window(dlg)
        if dlg.ok:
            self.choice_tree.insert("", tk.END, text=dlg.choice_id,
                                  values=(dlg.text, dlg.next_scene))

    def del_choice(self):
        sel = self.choice_tree.selection()
        if sel:
            self.choice_tree.delete(sel)

    def apply(self):
        """把当前界面数据打包成 dict 并回调"""
        typ = self.type_var.get()
        speaker = self.speaker_var.get()
        item = {
            "type": typ,
            "speaker": speaker,
            "text": self.text_txt.get("1.0", tk.END).rstrip("\n"),
            "photo": None
        }
        # character
        if not is_narrator_or_player(speaker):
            item["character"] = {
                "emotion": self.emotion_var.get() or "neutral",
                "position": self.position_var.get() or "center",
                "voice": self.voice_var.get()
            }
        # choice
        if typ == "choice":
            choices = []
            for row in self.choice_tree.get_children():
                ch_id = self.choice_tree.item(row, "text")
                val = self.choice_tree.item(row, "values")
                choices.append({
                    "choiceId": ch_id,
                    "text": val[0],
                    "nextScene": val[1]
                })
            item["choices"] = choices
        self.callback(item)


# ------------------ 新增场景命名弹窗 ------------------
class SceneNameDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("新建场景")
        self.ok = False
        self.scene_id = ""

        ttk.Label(self, text="请输入新场景 ID：").pack(padx=10, pady=5)
        self.ent = ttk.Entry(self, width=30)
        self.ent.pack(padx=10, pady=5)
        self.ent.focus()

        frm = ttk.Frame(self)
        frm.pack(pady=8)
        ttk.Button(frm, text="确定", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(frm, text="取消", command=self.destroy).pack(side=tk.LEFT, padx=5)

        self.transient(parent)
        self.grab_set()

    def on_ok(self):
        sid = self.ent.get().strip()
        if not sid:
            messagebox.showwarning("提示", "场景 ID 不能为空！")
            return
        self.scene_id = sid
        self.ok = True
        self.destroy()


# ------------------ 添加选项弹窗 ------------------
class ChoiceDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("添加选项")
        self.ok = False
        self.choice_id = ""
        self.text = ""
        self.next_scene = ""

        ttk.Label(self, text="choiceId").grid(row=0, column=0, sticky=tk.W)
        self.id_ent = ttk.Entry(self, width=20)
        self.id_ent.grid(row=0, column=1)

        ttk.Label(self, text="选项文字").grid(row=1, column=0, sticky=tk.W)
        self.txt_ent = ttk.Entry(self, width=40)
        self.txt_ent.grid(row=1, column=1)

        ttk.Label(self, text="跳转场景").grid(row=2, column=0, sticky=tk.W)
        self.next_ent = ttk.Entry(self, width=20)
        self.next_ent.grid(row=2, column=1)

        ttk.Button(self, text="确定", command=self.on_ok).grid(row=3, column=0, pady=10)
        ttk.Button(self, text="取消", command=self.destroy).grid(row=3, column=1)

        self.transient(parent)
        self.grab_set()

    def on_ok(self):
        self.choice_id = self.id_ent.get().strip()
        self.text = self.txt_ent.get().strip()
        self.next_scene = self.next_ent.get().strip()
        if not self.choice_id:
            messagebox.showwarning("提示", "choiceId 不能为空")
            return
        self.ok = True
        self.destroy()


# ------------------ main ------------------
if __name__ == "__main__":
    GalEditor().mainloop()