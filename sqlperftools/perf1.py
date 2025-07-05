import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue
import threading
import time
import random


class SQLPerformanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL性能检测客户端")

        # 初始化线程池（4个工作线程）
        self.executor = ThreadPoolExecutor(max_workers=4)

        # 任务队列和状态变量
        self.task_queue = queue.Queue()
        self.running_tasks = 0
        self.max_tasks = 10  # 最大同时运行任务数

        # 创建UI组件
        self.create_widgets()

        # 启动后台任务检查器
        self.check_tasks()

        # 窗口关闭时的清理
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

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
            command=self.start_sql_tasks,
            state=tk.NORMAL
        )
        self.execute_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ttk.Button(
            button_frame,
            text="取消所有任务",
            command=self.cancel_all_tasks,
            state=tk.DISABLED
        )
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        # 进度显示
        self.progress = ttk.Progressbar(
            main_frame,
            mode='determinate',
            maximum=100
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

    def start_sql_tasks(self):
        """开始执行SQL任务"""
        sql = self.sql_entry.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("警告", "请输入SQL语句！")
            return

        # 分割多条SQL语句（简单实现）
        sql_list = [s.strip() for s in sql.split(';') if s.strip()]

        if not sql_list:
            return

        # 更新UI状态
        self.execute_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        self.status_var.set(f"正在执行 {len(sql_list)} 条SQL语句...")
        self.progress["maximum"] = len(sql_list)
        self.progress["value"] = 0

        # 为每条SQL创建任务
        for i, sql in enumerate(sql_list, 1):
            if len(sql) > 100:
                sql_short = sql[:100] + "..."
            else:
                sql_short = sql

            # 在结果树中添加占位项
            item_id = self.result_tree.insert(
                "", tk.END,
                values=(i, sql_short, "运行中", "排队中"),
                tags=("pending",)
            )

            # 提交任务到线程池
            future = self.executor.submit(
                self.execute_sql_task,
                sql,
                item_id
            )

            # 将future和item_id关联存储
            self.task_queue.put((future, item_id))
            self.running_tasks += 1

    def execute_sql_task(self, sql, item_id):
        """执行SQL任务的线程函数"""
        try:
            # 模拟SQL执行时间（5-30秒随机）
            duration = random.randint(5, 30)

            # 更新状态为"运行中"
            self.update_item_status(item_id, "运行中", duration="运行中")

            # 模拟SQL执行过程
            for i in range(duration):
                if self.should_cancel:
                    self.update_item_status(item_id, "已取消", duration=i)
                    return None

                time.sleep(1)

                # 更新进度
                progress = (i + 1) / duration * 100
                self.update_item_progress(item_id, progress)

            # 随机决定成功或失败（模拟）
            if random.random() < 0.2:  # 20%概率失败
                raise Exception("模拟执行错误: 超时或语法错误")

            # 返回模拟结果
            return {
                "item_id": item_id,
                "sql": sql,
                "duration": duration,
                "plan": f"模拟执行计划\n索引使用: 是\n扫描行数: {random.randint(100, 10000)}",
                "status": "成功"
            }
        except Exception as e:
            return {
                "item_id": item_id,
                "sql": sql,
                "duration": duration if 'duration' in locals() else 0,
                "error": str(e),
                "status": "失败"
            }

    def check_tasks(self):
        """定期检查任务完成状态"""
        try:
            # 检查已完成的任务
            for future, item_id in list(self.task_queue.queue):
                if future.done():
                    try:
                        result = future.result()
                        self.handle_task_result(result)
                    except Exception as e:
                        self.handle_task_error(item_id, str(e))

                    self.task_queue.queue.remove((future, item_id))
                    self.running_tasks -= 1

            # 更新UI状态
            completed = self.progress["value"]
            total = self.progress["maximum"]

            if self.running_tasks > 0:
                self.status_var.set(f"运行中: {self.running_tasks}/{total} 任务")
            else:
                self.status_var.set("所有任务完成")
                self.execute_button.config(state=tk.NORMAL)
                self.cancel_button.config(state=tk.DISABLED)

        except Exception as e:
            print(f"任务检查错误: {e}")

        # 每100毫秒检查一次
        self.root.after(100, self.check_tasks)

    def handle_task_result(self, result):
        """处理任务完成结果"""
        if result["status"] == "成功":
            self.update_item_status(
                result["item_id"],
                "完成",
                duration=result["duration"],
                tag="success"
            )
        else:
            self.update_item_status(
                result["item_id"],
                "失败",
                duration=result["duration"],
                tag="error"
            )

        # 存储完整结果
        item = self.result_tree.item(result["item_id"])
        item["values"] = (
            item["values"][0],  # ID
            item["values"][1],  # SQL摘要
            result["duration"],
            result["status"]
        )

        # 更新进度条
        self.progress.step(1)

        # 存储额外数据
        self.result_tree.set(result["item_id"], "data", result)

    def handle_task_error(self, item_id, error):
        """处理任务错误"""
        self.update_item_status(
            item_id,
            "错误",
            duration="错误",
            tag="error"
        )

        item = self.result_tree.item(item_id)
        item["values"] = (
            item["values"][0],  # ID
            item["values"][1],  # SQL摘要
            "N/A",
            f"错误: {error}"
        )

        # 更新进度条
        self.progress.step(1)

        # 存储错误信息
        self.result_tree.set(item_id, "data", {"error": error})

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

        # 确保UI更新在主线程执行
        self.root.after(0, _update)

    def update_item_progress(self, item_id, progress):
        """更新单个项目的进度"""

        def _update():
            item = self.result_tree.item(item_id)
            values = list(item["values"])
            values[2] = f"{progress:.1f}%"
            self.result_tree.item(item_id, values=values)

        self.root.after(0, _update)

    def cancel_all_tasks(self):
        """取消所有运行中的任务"""
        if messagebox.askyesno("确认", "确定要取消所有运行中的任务吗？"):
            self.should_cancel = True
            for future, _ in list(self.task_queue.queue):
                future.cancel()

            self.status_var.set("正在取消任务...")

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
                f"状态: {item_data['status']}\n\n"
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
        if self.running_tasks > 0 and messagebox.askyesno(
                "确认",
                "有任务正在运行，确定要退出吗？"
        ):
            self.executor.shutdown(wait=False)
            self.root.destroy()
        elif self.running_tasks == 0:
            self.executor.shutdown()
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SQLPerformanceApp(root)
    root.mainloop()