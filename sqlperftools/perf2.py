import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import asyncio
from threading import Thread
import random
import time


class AsyncSQLPerformanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL性能检测客户端(Async)")

        # 创建asyncio事件循环
        self.loop = asyncio.new_event_loop()
        self.tasks = set()
        self.running = False

        # 创建UI组件
        self.create_widgets()

        # 启动asyncio事件循环线程
        self.thread = Thread(target=self.run_async_loop, daemon=True)
        self.thread.start()

        # 窗口关闭时的清理
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def run_async_loop(self):
        """在新线程中运行asyncio事件循环"""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def create_widgets(self):
        """创建所有GUI组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # SQL输入区域
        sql_frame = ttk.LabelFrame(main_frame, text="SQL输入", padding="5")
        sql_frame.pack(fill=tk.X, pady=5)

        self.sql_entry = scrolledtext.ScrolledText(sql_frame, height=10, wrap=tk.WORD)
        self.sql_entry.pack(fill=tk.BOTH, expand=True)

        # 控制按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        self.execute_button = ttk.Button(
            button_frame,
            text="执行SQL",
            command=self.start_async_tasks
        )
        self.execute_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ttk.Button(
            button_frame,
            text="取消所有任务",
            command=self.cancel_async_tasks,
            state=tk.DISABLED
        )
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        # 进度显示
        self.progress = ttk.Progressbar(
            main_frame,
            mode='determinate'
        )
        self.progress.pack(fill=tk.X, pady=5)

        self.status_var = tk.StringVar(value="准备就绪")
        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_label.pack(fill=tk.X, pady=5)

        # 结果展示区域
        result_frame = ttk.LabelFrame(main_frame, text="执行结果", padding="5")
        result_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "sql", "time", "status")
        self.result_tree = ttk.Treeview(
            result_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        # 设置列宽和标题
        self.result_tree.heading("id", text="ID")
        self.result_tree.column("id", width=50, anchor=tk.CENTER)

        self.result_tree.heading("sql", text="SQL摘要")
        self.result_tree.column("sql", width=200)

        self.result_tree.heading("time", text="耗时(秒)")
        self.result_tree.column("time", width=80, anchor=tk.CENTER)

        self.result_tree.heading("status", text="状态")
        self.result_tree.column("status", width=100, anchor=tk.CENTER)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_tree.pack(fill=tk.BOTH, expand=True)

        # 右键菜单
        self.setup_context_menu()

    def setup_context_menu(self):
        """设置结果树的右键菜单"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="查看详情", command=self.show_details)
        self.context_menu.add_command(label="复制SQL", command=self.copy_sql)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="删除记录", command=self.delete_record)

        def show_menu(event):
            item = self.result_tree.identify_row(event.y)
            if item:
                self.result_tree.selection_set(item)
                self.context_menu.post(event.x_root, event.y_root)

        self.result_tree.bind("<Button-3>", show_menu)

    def start_async_tasks(self):
        """开始执行异步SQL任务"""
        sql = self.sql_entry.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("警告", "请输入SQL语句！")
            return

        # 分割多条SQL语句
        sql_list = [s.strip() for s in sql.split(';') if s.strip()]

        if not sql_list:
            return

        # 更新UI状态
        self.execute_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        self.status_var.set(f"正在执行 {len(sql_list)} 条SQL语句...")
        self.progress["maximum"] = len(sql_list)
        self.progress["value"] = 0
        self.running = True

        # 为每条SQL创建异步任务
        for i, sql in enumerate(sql_list, 1):
            if len(sql) > 100:
                sql_short = sql[:100] + "..."
            else:
                sql_short = sql

            # 在结果树中添加占位项
            item_id = self.result_tree.insert(
                "", tk.END,
                values=(i, sql_short, "0", "排队中"),
                tags=("pending",)
            )

            # 创建异步任务
            task = asyncio.run_coroutine_threadsafe(
                self.async_execute_sql(sql, item_id),
                self.loop
            )

            # 存储任务引用
            self.tasks.add(task)
            task.add_done_callback(
                lambda t, item_id=item_id: self.on_async_task_done(t, item_id)
            )

    async def async_execute_sql(self, sql, item_id):
        """异步执行SQL任务"""
        try:
            # 模拟SQL执行时间（5-30秒随机）
            duration = random.randint(5, 30)

            # 更新状态为"运行中"
            self.update_item_status(item_id, "运行中", "0")

            # 模拟SQL执行过程
            for i in range(duration):
                if not self.running:
                    self.update_item_status(item_id, "已取消", str(i))
                    return {"status": "cancelled"}

                await asyncio.sleep(1)

                # 更新进度
                progress = (i + 1) / duration * 100
                self.update_item_progress(item_id, f"{progress:.1f}%")

            # 随机决定成功或失败（模拟）
            if random.random() < 0.2:  # 20%概率失败
                raise Exception("模拟执行错误: 超时或语法错误")

            # 返回模拟结果
            return {
                "item_id": item_id,
                "sql": sql,
                "duration": duration,
                "plan": f"模拟执行计划\n索引使用: 是\n扫描行数: {random.randint(100, 10000)}",
                "status": "success"
            }
        except Exception as e:
            return {
                "item_id": item_id,
                "sql": sql,
                "duration": i if 'i' in locals() else 0,
                "error": str(e),
                "status": "error"
            }

    def on_async_task_done(self, task, item_id):
        """异步任务完成时的回调"""
        try:
            result = task.result()
            self.tasks.discard(task)

            if result["status"] == "success":
                self.handle_async_success(result)
            elif result["status"] == "error":
                self.handle_async_error(result)
            elif result["status"] == "cancelled":
                self.handle_async_cancelled(item_id)

            # 更新进度条
            self.progress.step(1)

            # 检查是否所有任务完成
            if all(t.done() for t in self.tasks):
                self.running = False
                self.status_var.set("所有任务完成")
                self.execute_button.config(state=tk.NORMAL)
                self.cancel_button.config(state=tk.DISABLED)

        except Exception as e:
            print(f"任务处理错误: {e}")

    def handle_async_success(self, result):
        """处理异步任务成功"""
        self.update_item_status(
            result["item_id"],
            "完成",
            str(result["duration"]),
            "success"
        )

        # 存储完整结果
        item = self.result_tree.item(result["item_id"])
        item["values"] = (
            item["values"][0],  # ID
            item["values"][1],  # SQL摘要
            result["duration"],
            "成功"
        )

        self.result_tree.set(result["item_id"], "data", result)

    def handle_async_error(self, result):
        """处理异步任务错误"""
        self.update_item_status(
            result["item_id"],
            "失败",
            str(result["duration"]),
            "error"
        )

        item = self.result_tree.item(result["item_id"])
        item["values"] = (
            item["values"][0],  # ID
            item["values"][1],  # SQL摘要
            result["duration"],
            f"错误: {result['error']}"
        )

        self.result_tree.set(result["item_id"], "data", result)

    def handle_async_cancelled(self, item_id):
        """处理异步任务取消"""
        self.update_item_status(
            item_id,
            "已取消",
            "N/A",
            "cancelled"
        )

        item = self.result_tree.item(item_id)
        item["values"] = (
            item["values"][0],  # ID
            item["values"][1],  # SQL摘要
            "N/A",
            "已取消"
        )

    def update_item_status(self, item_id, status, duration=None, tag=None):
        """更新结果树中项目的状态"""

        def _update():
            item = self.result_tree.item(item_id)
            values = list(item["values"])

            if duration is not None:
                values[2] = duration
            values[3] = status

            self.result_tree.item(item_id, values=values)
            if tag:
                self.result_tree.item(item_id, tags=(tag,))

        self.root.after(0, _update)

    def update_item_progress(self, item_id, progress):
        """更新单个项目的进度"""

        def _update():
            item = self.result_tree.item(item_id)
            values = list(item["values"])
            values[2] = progress
            self.result_tree.item(item_id, values=values)

        self.root.after(0, _update)

    def cancel_async_tasks(self):
        """取消所有异步任务"""
        if messagebox.askyesno("确认", "确定要取消所有运行中的任务吗？"):
            self.running = False
            self.status_var.set("正在取消任务...")

            for task in self.tasks:
                if not task.done():
                    task.cancel()

    def show_details(self):
        """显示选中SQL的详细信息"""
        selected = self.result_tree.selection()
        if not selected:
            return

        item_id = selected[0]
        item_data = self.result_tree.set(item_id, "data")

        detail_win = tk.Toplevel(self.root)
        detail_win.title("SQL执行详情")

        text = scrolledtext.ScrolledText(detail_win, width=80, height=20)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if "error" in item_data:
            content = f"错误信息:\n{item_data['error']}\n\nSQL:\n{item_data['sql']}"
        else:
            content = (
                f"SQL:\n{item_data['sql']}\n\n"
                f"执行时间: {item_data['duration']}秒\n"
                f"状态: 成功\n\n"
                f"执行计划:\n{item_data['plan']}"
            )

        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)

    def copy_sql(self):
        """复制选中的SQL到剪贴板"""
        selected = self.result_tree.selection()
        if not selected:
            return

        item_id = selected[0]
        item_data = self.result_tree.set(item_id, "data")
        self.root.clipboard_clear()
        self.root.clipboard_append(item_data.get("sql", ""))

    def delete_record(self):
        """删除选中的记录"""
        selected = self.result_tree.selection()
        if not selected:
            return

        item_id = selected[0]
        self.result_tree.delete(item_id)

    def on_close(self):
        """窗口关闭时的清理工作"""
        if self.running and messagebox.askyesno(
                "确认",
                "有任务正在运行，确定要退出吗？"
        ):
            self.running = False
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.root.destroy()
        elif not self.running:
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AsyncSQLPerformanceApp(root)
    root.mainloop()