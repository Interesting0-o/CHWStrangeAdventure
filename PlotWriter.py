# galgame_editor.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os


class GalgameScriptEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Galgame 剧情编辑器")
        self.root.geometry("1100x750")

        # 数据
        self.script_data = {"scenes": {}}
        self.current_scene = None
        self.current_dialogue_index = None
        # 实时 speaker 值
        self._real_speaker = ""

        # 预设列表
        self.characters = ["旁白", "player", "角色"]
        self.emotions = ["neutral", "happy", "sad", "angry", "surprised"]
        self.positions = ["left", "center", "right"]

        self.build_ui()
        self.update_scene_list()
        self.on_speaker_change()

    # --------------------------- 界面构建 ---------------------------
    def build_ui(self):
        main = ttk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ---- 左：场景列表 ----
        left = ttk.Frame(main, width=200)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        ttk.Label(left, text="场景列表").pack()
        self.scene_listbox = tk.Listbox(left, height=25)
        self.scene_listbox.pack(fill=tk.BOTH, expand=True)
        self.scene_listbox.bind("<<ListboxSelect>>", self.on_scene_select)
        btn = ttk.Frame(left)
        btn.pack(fill=tk.X, pady=5)
        ttk.Button(btn, text="新建场景", command=self.new_scene).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn, text="删除场景", command=self.delete_scene).pack(side=tk.LEFT, padx=2)

        # ---- 中：编辑区 ----
        center = ttk.Frame(main)
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Label(center, text="对话列表").pack(anchor=tk.W)
        self.dlg_listbox = tk.Listbox(center, height=10)
        self.dlg_listbox.pack(fill=tk.X, pady=5)
        self.dlg_listbox.bind("<<ListboxSelect>>", self.on_dialogue_select)

        btn2 = ttk.Frame(center)
        btn2.pack(fill=tk.X, pady=5)
        ttk.Button(btn2, text="添加对话", command=self.add_dialogue).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn2, text="删除对话", command=self.delete_dialogue).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn2, text="添加分支选项", command=self.add_choice).pack(side=tk.LEFT, padx=2)

        # ---- 对话编辑表单 ----
        form = ttk.LabelFrame(center, text="编辑对话")
        form.pack(fill=tk.BOTH, expand=True, pady=10)

        # 说话人
        sp_frame = ttk.Frame(form)
        sp_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(sp_frame, text="说话人:").pack(side=tk.LEFT)
        self.speaker_var = tk.StringVar()
        self.speaker_combo = ttk.Combobox(sp_frame, textvariable=self.speaker_var,
                                         values=self.characters, state="readonly", width=12)
        self.speaker_combo.pack(side=tk.LEFT, padx=5)
        self.speaker_combo.bind("<<ComboboxSelected>>", self.on_speaker_change)

        # 自定义角色名
        cus_frame = ttk.Frame(form)
        cus_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(cus_frame, text="自定义角色名:").pack(side=tk.LEFT)
        self.custom_name_var = tk.StringVar()
        self.custom_entry = ttk.Entry(cus_frame, textvariable=self.custom_name_var, width=15)
        self.custom_entry.pack(side=tk.LEFT, padx=5)
        self.custom_entry.bind("<KeyRelease>", lambda e: self._sync_speaker())

        # 角色设置
        self.char_frame = ttk.LabelFrame(form, text="角色设置")
        self.char_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(self.char_frame, text="表情:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.emotion_var = tk.StringVar()
        ttk.Combobox(self.char_frame, textvariable=self.emotion_var,
                    values=self.emotions, state="readonly", width=10).grid(row=0, column=1, padx=5)
        ttk.Label(self.char_frame, text="位置:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.pos_var = tk.StringVar()
        ttk.Combobox(self.char_frame, textvariable=self.pos_var,
                    values=self.positions, state="readonly", width=10).grid(row=1, column=1, padx=5)
        ttk.Label(self.char_frame, text="语音:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.voice_var = tk.StringVar()
        ttk.Entry(self.char_frame, textvariable=self.voice_var, width=12).grid(row=2, column=1, padx=5)

        # 文本
        txt_frame = ttk.Frame(form)
        txt_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        ttk.Label(txt_frame, text="文本内容:").pack(anchor=tk.W)
        self.text_w = tk.Text(txt_frame, height=6)
        self.text_w.pack(fill=tk.BOTH, expand=True)

        # 场景设置
        set_frame = ttk.LabelFrame(center, text="场景设置")
        set_frame.pack(fill=tk.X, padx=5, pady=5)
        labels = ["背景:", "BGM:", "结束方式:", "下一场景:"]
        vars = [tk.StringVar() for _ in labels]
        self.bg_var, self.bgm_var, self.end_var, self.next_var = vars
        widgets = [
            ttk.Entry(set_frame, textvariable=vars[0]),
            ttk.Entry(set_frame, textvariable=vars[1]),
            ttk.Combobox(set_frame, textvariable=vars[2], values=["dialogue", "choice"], state="readonly"),
            ttk.Entry(set_frame, textvariable=vars[3])
        ]
        for i, (lab, w) in enumerate(zip(labels, widgets)):
            ttk.Label(set_frame, text=lab).grid(row=i, column=0, sticky=tk.W, padx=5)
            w.grid(row=i, column=1, sticky=tk.EW, padx=5)
        set_frame.columnconfigure(1, weight=1)

        ttk.Button(center, text="保存当前对话", command=self.save_current_dialogue).pack(pady=5)

        # ---- 右：JSON 预览 ----
        right = ttk.Frame(main, width=350)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        ttk.Label(right, text="JSON 预览").pack()
        self.pre = tk.Text(right, width=45, height=35)
        self.pre.pack(fill=tk.BOTH, expand=True)

        # ---- 底部全局按钮 ----
        bot = ttk.Frame(self.root)
        bot.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(bot, text="新建项目", command=self.new_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(bot, text="打开项目", command=self.open_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(bot, text="保存项目", command=self.save_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(bot, text="导出 JSON", command=self.export_json).pack(side=tk.LEFT, padx=5)

    # --------------------------- 逻辑 ---------------------------
    def on_speaker_change(self, _evt=None):
        sp = self.speaker_var.get()
        if sp == "角色":
            self.custom_entry.config(state='normal')
            self.char_frame.pack(fill=tk.X, padx=5, pady=5)
        else:
            self.custom_name_var.set("")
            self.custom_entry.config(state='disabled')
            self.char_frame.pack_forget()
        self._sync_speaker()

    def _sync_speaker(self):
        if self.speaker_var.get() == "角色":
            name = self.custom_name_var.get().strip()
            self._real_speaker = name if name else "DemoCharacter"
        else:
            self._real_speaker = self.speaker_var.get()

    # ---------- 场景管理 ----------
    def update_scene_list(self):
        self.scene_listbox.delete(0, tk.END)
        for sid in self.script_data["scenes"]:
            self.scene_listbox.insert(tk.END, sid)

    def new_scene(self):
        d = tk.Toplevel(self.root)
        d.title("新建场景")
        d.geometry("300x120")
        d.transient(self.root)
        ttk.Label(d, text="场景 ID:").pack(pady=5)
        v = tk.StringVar()
        ttk.Entry(d, textvariable=v).pack()

        def ok():
            sid = v.get().strip()
            if sid and sid not in self.script_data["scenes"]:
                self.script_data["scenes"][sid] = {"bg": "library", "bgm": "normal",
                                                  "end_with": "dialogue", "dialogues": []}
                self.update_scene_list()
                self.scene_listbox.selection_clear(0, tk.END)
                self.scene_listbox.selection_set(tk.END)
                self.on_scene_select()
                d.destroy()
            else:
                messagebox.showwarning("警告", "ID 不能为空或已存在", parent=d)

        ttk.Button(d, text="创建", command=ok).pack(pady=10)

    def delete_scene(self):
        idx = self.scene_listbox.curselection()
        if not idx:
            messagebox.showwarning("警告", "请先选择场景")
            return
        sid = self.scene_listbox.get(idx[0])
        if messagebox.askyesno("确认", f"删除场景 '{sid}'？"):
            del self.script_data["scenes"][sid]
            self.update_scene_list()
            self.dlg_listbox.delete(0, tk.END)

    def on_scene_select(self, _evt=None):
        idx = self.scene_listbox.curselection()
        if not idx:
            return
        sid = self.scene_listbox.get(idx[0])
        self.current_scene = sid
        sc = self.script_data["scenes"][sid]
        self.bg_var.set(sc.get("bg", ""))
        self.bgm_var.set(sc.get("bgm", ""))
        self.end_var.set(sc.get("end_with", "dialogue"))
        self.next_var.set(sc.get("next_scene", ""))
        self.update_dialogue_list()

    # ---------- 对话管理 ----------
    def update_dialogue_list(self):
        self.dlg_listbox.delete(0, tk.END)
        if not self.current_scene:
            return
        dlgs = self.script_data["scenes"][self.current_scene]["dialogues"]
        for i, d in enumerate(dlgs):
            sp = d.get("speaker", "")
            txt = d.get("text", "")
            if len(txt) > 40:
                txt = txt[:38] + "…"
            self.dlg_listbox.insert(tk.END, f"{i+1}. {sp}: {txt}")

    def add_dialogue(self):
        if not self.current_scene:
            messagebox.showwarning("警告", "请先选择场景")
            return
        dlgs = self.script_data["scenes"][self.current_scene]["dialogues"]
        dlgs.append({"type": "dialogue", "speaker": "旁白", "text": "新对话"})
        self.update_dialogue_list()
        self.dlg_listbox.selection_clear(0, tk.END)
        self.dlg_listbox.selection_set(tk.END)
        self.on_dialogue_select()

    def delete_dialogue(self):
        idx = self.dlg_listbox.curselection()
        if not idx:
            messagebox.showwarning("警告", "请选择对话")
            return
        del self.script_data["scenes"][self.current_scene]["dialogues"][idx[0]]
        self.update_dialogue_list()

    def add_choice(self):
        if not self.current_scene:
            messagebox.showwarning("警告", "请先选择场景")
            return
        dlgs = self.script_data["scenes"][self.current_scene]["dialogues"]
        dlgs.append({"type": "choice", "speaker": "DemoCharacter",
                    "choices": [{"choiceId": "choice_1", "text": "选项1", "nextScene": "scene_1"},
                               {"choiceId": "choice_2", "text": "选项2", "nextScene": "scene_2"}]})
        self.update_dialogue_list()

    def on_dialogue_select(self, _evt=None):
        idx = self.dlg_listbox.curselection()
        if not idx or not self.current_scene:
            return
        self.current_dialogue_index = idx[0]
        d = self.script_data["scenes"][self.current_scene]["dialogues"][idx[0]]
        self.speaker_var.set(d.get("speaker", ""))
        self.text_w.delete(1.0, tk.END)
        self.text_w.insert(1.0, d.get("text", ""))
        c = d.get("character", {})
        self.emotion_var.set(c.get("emotion", ""))
        self.pos_var.set(c.get("position", ""))
        self.voice_var.set(c.get("voice", ""))
        self.on_speaker_change()

    # ---------- 保存 ----------
    def save_current_dialogue(self):
        if self.current_dialogue_index is None or not self.current_scene:
            messagebox.showwarning("警告", "未选择对话")
            return
        self._sync_speaker()
        d = self.script_data["scenes"][self.current_scene]["dialogues"][self.current_dialogue_index]
        d["speaker"] = self._real_speaker
        d["text"] = self.text_w.get(1.0, tk.END).strip()
        if self.speaker_var.get() == "角色":
            if "character" not in d:
                d["character"] = {}
            d["character"]["emotion"] = self.emotion_var.get()
            d["character"]["position"] = self.pos_var.get()
            d["character"]["voice"] = self.voice_var.get()
        else:
            d.pop("character", None)
        sc = self.script_data["scenes"][self.current_scene]
        sc["bg"] = self.bg_var.get()
        sc["bgm"] = self.bgm_var.get()
        sc["end_with"] = self.end_var.get()
        sc["next_scene"] = self.next_var.get()
        self.update_dialogue_list()
        self.update_preview()
        messagebox.showinfo("成功", "已保存")

    def update_preview(self):
        self.pre.delete(1.0, tk.END)
        if self.current_scene:
            self.pre.insert(1.0, json.dumps({self.current_scene: self.script_data["scenes"][self.current_scene]},
                                           ensure_ascii=False, indent=2))

    # ---------- 项目 IO ----------
    def new_project(self):
        if messagebox.askyesno("确认", "新建将清空当前内容，继续？"):
            self.script_data = {"scenes": {}}
            self.current_scene = None
            self.update_scene_list()
            self.dlg_listbox.delete(0, tk.END)
            self.pre.delete(1.0, tk.END)

    def open_project(self):
        f = filedialog.askopenfilename(title="打开项目", filetypes=[("JSON", "*.json"), ("All", "*.*")])
        if f:
            try:
                with open(f, 'r', encoding='utf-8') as fd:
                    self.script_data = json.load(fd)
                self.update_scene_list()
                self.dlg_listbox.delete(0, tk.END)
                self.pre.delete(1.0, tk.END)
            except Exception as e:
                messagebox.showerror("错误", f"打开失败：{e}")

    def save_project(self):
        f = filedialog.asksaveasfilename(title="保存项目", defaultextension=".json",
                                        filetypes=[("JSON", "*.json"), ("All", "*.*")])
        if f:
            try:
                with open(f, 'w', encoding='utf-8') as fd:
                    json.dump(self.script_data, fd, ensure_ascii=False, indent=2)
                messagebox.showinfo("成功", "已保存")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败：{e}")

    def export_json(self):
        self.update_preview()
        self.save_project()


# --------------------------- main ---------------------------
def main():
    root = tk.Tk()
    GalgameScriptEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()