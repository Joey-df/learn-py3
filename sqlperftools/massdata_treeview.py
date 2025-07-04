import tkinter as tk
from tkinter import ttk, messagebox
import random
import time


class VirtualTreeview(ttk.Frame):
    def __init__(self, parent, total_rows, page_size=100, buffer_size=20):
        super().__init__(parent)
        self.total_rows = total_rows
        self.page_size = page_size
        self.buffer_size = buffer_size
        self.current_page = 0
        self.visible_data = []

        # 创建UI组件
        self.create_widgets()

        # 初始化数据
        self.load_data()

        # 绑定滚动事件
        self.tree.bind("<MouseWheel>", self.on_mousewheel)
        self.tree.bind("<Configure>", self.on_resize)

    def create_widgets(self):
        # 创建顶部控制面板
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        # 分页控制
        ttk.Label(control_frame, text="分页大小:").pack(side=tk.LEFT, padx=(0, 5))
        self.page_size_var = tk.StringVar(value=str(self.page_size))
        page_size_combo = ttk.Combobox(control_frame, textvariable=self.page_size_var,
                                       values=["50", "100", "200", "500"], width=8)
        page_size_combo.pack(side=tk.LEFT, padx=(0, 10))
        page_size_combo.bind("<<ComboboxSelected>>", self.update_page_size)

        # 跳转页面
        ttk.Label(control_frame, text="跳转到:").pack(side=tk.LEFT, padx=(10, 5))
        self.goto_var = tk.StringVar()
        goto_entry = ttk.Entry(control_frame, textvariable=self.goto_var, width=8)
        goto_entry.pack(side=tk.LEFT)
        goto_entry.bind("<Return>", self.goto_page)

        # 页面信息
        self.page_info = ttk.Label(control_frame, text="")
        self.page_info.pack(side=tk.LEFT, padx=10)

        # 搜索框
        ttk.Label(control_frame, text="搜索:").pack(side=tk.LEFT, padx=(20, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(control_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT)
        search_entry.bind("<Return>", self.perform_search)

        # 创建Treeview和滚动条
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,
                                 selectmode="extended", height=20)
        self.tree.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.tree.yview)

        # 设置列
        self.tree["columns"] = ("id", "name", "value", "category", "status")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("id", width=60, anchor=tk.CENTER)
        self.tree.column("name", width=150, anchor=tk.W)
        self.tree.column("value", width=100, anchor=tk.E)
        self.tree.column("category", width=120, anchor=tk.W)
        self.tree.column("status", width=100, anchor=tk.CENTER)

        # 设置表头
        self.tree.heading("id", text="ID", anchor=tk.CENTER)
        self.tree.heading("name", text="名称", anchor=tk.W)
        self.tree.heading("value", text="数值", anchor=tk.E)
        self.tree.heading("category", text="类别", anchor=tk.W)
        self.tree.heading("status", text="状态", anchor=tk.CENTER)

        # 状态栏
        self.status_var = tk.StringVar(value="就绪 | 总数据: {:,} 行".format(self.total_rows))
        status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 5))

    def load_data(self, start_index=None):
        """加载当前页的数据"""
        # 清空当前显示的数据
        self.tree.delete(*self.tree.get_children())

        # 计算当前页的开始和结束索引
        if start_index is None:
            start_index = self.current_page * self.page_size
        end_index = min(start_index + self.page_size, self.total_rows)

        # 记录加载时间
        start_time = time.time()

        # 生成模拟数据（实际应用中从内存数据结构中获取）
        self.visible_data = []
        for i in range(start_index, end_index):
            # 模拟不同类别的数据
            category = random.choice(["电子产品", "家居用品", "服装", "食品", "书籍"])
            status = random.choice(["正常", "警告", "错误"])

            item = (
                i + 1,  # ID
                f"项目 {i + 1}",  # 名称
                f"${random.randint(10, 1000):,}",  # 数值
                category,
                status
            )
            self.visible_data.append(item)

            # 插入到Treeview（带颜色标记）
            tags = ("evenrow" if i % 2 == 0 else "oddrow",)
            if status == "警告":
                tags = tags + ("warning",)
            elif status == "错误":
                tags = tags + ("error",)

            self.tree.insert("", tk.END, values=item, tags=tags)

        # 配置标签样式
        self.tree.tag_configure("evenrow", background="#f0f0f0")
        self.tree.tag_configure("oddrow", background="#ffffff")
        self.tree.tag_configure("warning", foreground="orange")
        self.tree.tag_configure("error", foreground="red")

        # 更新页面信息
        total_pages = (self.total_rows + self.page_size - 1) // self.page_size
        current_page = start_index // self.page_size + 1
        self.page_info.config(text=f"第 {current_page}/{total_pages} 页 | 显示 {start_index + 1}-{end_index} 行")

        # 更新状态栏
        elapsed = (time.time() - start_time) * 1000
        self.status_var.set(
            f"已加载 {len(self.visible_data)} 行 | 耗时 {elapsed:.2f}ms | 总数据: {self.total_rows:,} 行")

    def update_page_size(self, event=None):
        """更新分页大小"""
        try:
            new_size = int(self.page_size_var.get())
            if new_size != self.page_size and 10 <= new_size <= 1000:
                self.page_size = new_size
                self.current_page = 0
                self.load_data()
        except ValueError:
            pass

    def goto_page(self, event=None):
        """跳转到指定页面"""
        try:
            page_num = int(self.goto_var.get()) - 1
            total_pages = (self.total_rows + self.page_size - 1) // self.page_size
            if 0 <= page_num < total_pages:
                self.current_page = page_num
                self.load_data()
            else:
                messagebox.showerror("错误", f"页码必须在 1 到 {total_pages} 之间")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的页码数字")

    def perform_search(self, event=None):
        """执行搜索操作（简化版）"""
        search_term = self.search_var.get().lower()
        if not search_term:
            return

        # 在实际应用中，这里应该搜索整个数据集
        # 这里简化为在当前页搜索
        found = False
        for i, item in enumerate(self.visible_data):
            if search_term in str(item).lower():
                # 滚动到匹配行
                self.tree.selection_set(self.tree.get_children()[i])
                self.tree.see(self.tree.get_children()[i])
                found = True
                break

        if not found:
            messagebox.showinfo("搜索", f"未找到包含 '{search_term}' 的项目")

    def on_mousewheel(self, event):
        """处理鼠标滚轮事件实现滚动加载"""
        if event.delta < 0:  # 向下滚动
            if self.tree.yview()[1] >= 0.95:  # 滚动到底部附近
                self.load_next_page()
        elif event.delta > 0:  # 向上滚动
            if self.tree.yview()[0] <= 0.05:  # 滚动到顶部附近
                self.load_prev_page()

    def on_resize(self, event):
        """窗口大小改变时调整显示行数"""
        # 根据Treeview高度计算可显示的行数
        tree_height = self.tree.winfo_height()
        row_height = 25  # 每行高度
        visible_rows = max(10, tree_height // row_height)

        # 如果可显示行数变化超过10%，更新分页大小
        if abs(visible_rows - self.page_size) / self.page_size > 0.1:
            self.page_size = visible_rows
            self.page_size_var.set(str(self.page_size))
            self.load_data()

    def load_next_page(self):
        """加载下一页"""
        next_page_start = (self.current_page + 1) * self.page_size
        if next_page_start < self.total_rows:
            self.current_page += 1
            self.load_data()

    def load_prev_page(self):
        """加载上一页"""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_data()


class LargeDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("大数据量展示优化方案")
        self.root.geometry("1000x700")

        # 创建Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 添加Treeview标签页
        self.tree_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tree_frame, text="Treeview 展示")

        # 创建虚拟Treeview
        self.virtual_tree = VirtualTreeview(self.tree_frame, total_rows=500000)
        self.virtual_tree.pack(fill=tk.BOTH, expand=True)

        # 添加Text标签页
        self.text_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.text_frame, text="Text 展示")

        # 创建Text组件和滚动条
        text_scroll = ttk.Scrollbar(self.text_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_widget = tk.Text(self.text_frame, yscrollcommand=text_scroll.set,
                                   wrap=tk.NONE, font=("Courier New", 10))
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text_scroll.config(command=self.text_widget.yview)

        # 添加数据到Text
        self.add_text_data()

        # 添加说明标签页
        self.info_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.info_frame, text="优化说明")
        self.create_info_tab()

    def add_text_data(self):
        """添加数据到Text组件（带分页）"""
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, "大数据量Text组件优化示例\n\n")
        self.text_widget.insert(tk.END, "当前显示前1000行数据（实际数据量：500,000行）\n\n")

        # 只加载部分数据
        for i in range(1000):
            value = random.randint(1000, 9999)
            self.text_widget.insert(tk.END, f"行 {i + 1}: 随机数值 = {value}\n")

        self.text_widget.insert(tk.END, "\n... 更多数据未显示 ...\n")

    def create_info_tab(self):
        """创建说明标签页"""
        info_text = """大数据量展示优化方案说明

1. 分页加载
   - 只加载当前页的数据（默认100行）
   - 通过分页控件可调整每页显示行数
   - 支持页面跳转功能

2. 虚拟滚动
   - 滚动到列表底部自动加载下一页
   - 滚动到列表顶部自动加载上一页
   - 响应式设计：窗口大小改变时自动调整显示行数

3. 内存优化
   - 所有数据存储在内存中（500,000行）
   - 但只渲染当前可见区域的数据
   - 减少界面元素数量提高性能

4. 搜索功能
   - 支持在当前页搜索内容
   - 定位并高亮显示匹配项

5. 性能监控
   - 显示数据加载耗时
   - 显示当前加载行数

6. 样式优化
   - 交替行背景色提高可读性
   - 状态标记使用颜色区分

针对Text组件的优化：
   - 只显示部分数据（前1000行）
   - 实际应用中应使用类似Treeview的分页机制
   - 或使用只读模式并限制显示行数

注意事项：
   - 实际应用应结合数据库分页查询
   - 考虑使用线程防止界面冻结
   - 对于极大数据集（>100万行），考虑使用专业数据网格控件
"""
        text_widget = tk.Text(self.info_frame, wrap=tk.WORD, font=("微软雅黑", 11))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, info_text)
        text_widget.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = LargeDataApp(root)
    root.mainloop()