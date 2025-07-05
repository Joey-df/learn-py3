import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import asyncio
import asyncpg  # 使用异步 PostgreSQL 驱动
import threading
import time
from datetime import datetime


class SQLPerformanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL性能检测工具")
        self.root.geometry("1000x700")

        # 创建 asyncio 事件循环
        self.loop = asyncio.new_event_loop()

        # 数据库连接池
        self.pool = None

        # 当前运行的任务
        self.running_tasks = {}
        self.task_counter = 0

        # 创建UI组件
        self.create_widgets()

        # 启动 asyncio 事件循环线程
        self.asyncio_thread = threading.Thread(
            target=self.run_asyncio_loop,
            daemon=True
        )
        self.asyncio_thread.start()

        # 窗口关闭时的清理
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def run_asyncio_loop(self):
        """在新线程中运行 asyncio 事件循环"""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def create_widgets(self):
        """创建所有GUI组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 连接设置区域
        conn_frame = ttk.LabelFrame(main_frame, text="数据库连接设置", padding=10)
        conn_frame.pack(fill=tk.X, pady=5)

        # 连接参数输入
        ttk.Label(conn_frame, text="主机:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.host_entry = ttk.Entry(conn_frame, width=20)
        self.host_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        self.host_entry.insert(0, "localhost")

        ttk.Label(conn_frame, text="端口:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.port_entry = ttk.Entry(conn_frame, width=10)
        self.port_entry.grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        self.port_entry.insert(0, "5432")

        ttk.Label(conn_frame, text="数据库:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.db_entry = ttk.Entry(conn_frame, width=20)
        self.db_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        self.db_entry.insert(0, "testdb")

        ttk.Label(conn_frame, text="用户名:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.user_entry = ttk.Entry(conn_frame, width=15)
        self.user_entry.grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)
        self.user_entry.insert(0, "postgres")

        ttk.Label(conn_frame, text="密码:").grid(row=1, column=4, sticky=tk.W, padx=5, pady=2)
        self.password_entry = ttk.Entry(conn_frame, width=15, show="*")
        self.password_entry.grid(row=1, column=5, sticky=tk.W, padx=5, pady=2)
        self.password_entry.insert(0, "password")

        # 连接按钮
        self.connect_btn = ttk.Button(
            conn_frame,
            text="连接数据库",
            command=self.connect_to_db
        )
        self.connect_btn.grid(row=0, column=6, rowspan=2, padx=10)

        # SQL输入区域
        sql_frame = ttk.LabelFrame(main_frame, text="SQL输入", padding=10)
        sql_frame.pack(fill=tk.X, pady=5)

        self.sql_entry = scrolledtext.ScrolledText(sql_frame, height=10, wrap=tk.WORD)
        self.sql_entry.pack(fill=tk.BOTH, expand=True)

        # 控制按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        self.execute_btn = ttk.Button(
            button_frame,
            text="执行SQL",
            command=self.execute_sql,
            state=tk.DISABLED
        )
        self.execute_btn.pack(side=tk.LEFT, padx=5)

        self.cancel_btn = ttk.Button(
            button_frame,
            text="取消所有任务",
            command=self.cancel_all_tasks,
            state=tk.DISABLED
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=5)

        # 状态栏
        self.status_var = tk.StringVar(value="准备就绪")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(fill=tk.X, pady=5)

        # 结果展示区域 - 使用Notebook切换不同结果
        self.result_notebook = ttk.Notebook(main_frame)
        self.result_notebook.pack(fill=tk.BOTH, expand=True)

        # 执行结果标签页
        result_frame = ttk.Frame(self.result_notebook, padding=5)
        self.result_notebook.add(result_frame, text="执行结果")

        self.result_tree = ttk.Treeview(result_frame)
        self.result_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 执行计划标签页
        plan_frame = ttk.Frame(self.result_notebook, padding=5)
        self.result_notebook.add(plan_frame, text="执行计划")

        self.plan_text = scrolledtext.ScrolledText(
            plan_frame,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.plan_text.pack(fill=tk.BOTH, expand=True)

        # 任务列表标签页
        task_frame = ttk.Frame(self.result_notebook, padding=5)
        self.result_notebook.add(task_frame, text="任务列表")

        columns = ("id", "sql", "status", "start_time", "duration")
        self.task_tree = ttk.Treeview(
            task_frame,
            columns=columns,
            show="headings"
        )

        # 设置列标题
        self.task_tree.heading("id", text="ID")
        self.task_tree.heading("sql", text="SQL摘要")
        self.task_tree.heading("status", text="状态")
        self.task_tree.heading("start_time", text="开始时间")
        self.task_tree.heading("duration", text="耗时(秒)")

        # 设置列宽
        self.task_tree.column("id", width=50, anchor=tk.CENTER)
        self.task_tree.column("sql", width=300)
        self.task_tree.column("status", width=100, anchor=tk.CENTER)
        self.task_tree.column("start_time", width=150)
        self.task_tree.column("duration", width=80, anchor=tk.CENTER)

        self.task_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # 任务树滚动条
        task_scrollbar = ttk.Scrollbar(task_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=task_scrollbar.set)
        task_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 绑定任务树选择事件
        self.task_tree.bind("<<TreeviewSelect>>", self.on_task_select)

    async def create_db_pool(self):
        """创建数据库连接池"""
        host = self.host_entry.get()
        port = self.port_entry.get()
        database = self.db_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()

        try:
            self.pool = await asyncpg.create_pool(
                host=host,
                port=int(port),
                database=database,
                user=user,
                password=password,
                min_size=1,
                max_size=5
            )
            return True
        except Exception as e:
            self.update_status(f"连接失败: {str(e)}")
            return False

    def connect_to_db(self):
        """连接数据库按钮事件"""
        self.connect_btn.config(state=tk.DISABLED)
        self.update_status("正在连接数据库...")

        # 在asyncio线程中执行连接操作
        future = asyncio.run_coroutine_threadsafe(
            self.create_db_pool(),
            self.loop
        )

        # 添加连接完成的回调
        future.add_done_callback(self.on_db_connected)

    def on_db_connected(self, future):
        """数据库连接完成回调"""
        try:
            connected = future.result()
            if connected:
                self.update_status("数据库连接成功!")
                self.execute_btn.config(state=tk.NORMAL)
            else:
                self.connect_btn.config(state=tk.NORMAL)
        except Exception as e:
            self.update_status(f"连接错误: {str(e)}")
            self.connect_btn.config(state=tk.NORMAL)

    def execute_sql(self):
        """执行SQL按钮事件"""
        sql = self.sql_entry.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("警告", "请输入SQL语句!")
            return

        # 分割多条SQL语句
        sql_list = [s.strip() for s in sql.split(';') if s.strip()]

        if not sql_list:
            return

        # 禁用执行按钮，启用取消按钮
        self.execute_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.update_status(f"正在执行 {len(sql_list)} 条SQL语句...")

        # 为每条SQL创建任务
        for sql in sql_list:
            # 生成任务ID
            task_id = self.task_counter
            self.task_counter += 1

            # 在任务树中添加任务
            start_time = datetime.now().strftime("%H:%M:%S")
            sql_short = sql[:50] + "..." if len(sql) > 50 else sql
            self.task_tree.insert(
                "", tk.END,
                iid=str(task_id),
                values=(task_id, sql_short, "运行中", start_time, "0.0"),
                tags=("running",)
            )

            # 在asyncio线程中执行SQL
            future = asyncio.run_coroutine_threadsafe(
                self.execute_sql_task(task_id, sql),
                self.loop
            )

            # 存储任务引用
            self.running_tasks[task_id] = {
                "future": future,
                "start_time": time.time(),
                "sql": sql
            }

            # 添加完成回调
            future.add_done_callback(
                lambda f, tid=task_id: self.on_sql_task_done(f, tid)
            )

    async def execute_sql_task(self, task_id, sql):
        """执行SQL任务的协程"""
        try:
            async with self.pool.acquire() as conn:
                # 执行SQL并获取结果
                start_time = time.time()
                result = await conn.fetch(sql)
                duration = time.time() - start_time

                # 获取执行计划
                plan = await conn.fetch(f"EXPLAIN ANALYZE {sql}")
                plan_text = "\n".join(str(row) for row in plan)

                return {
                    "task_id": task_id,
                    "result": result,
                    "plan": plan_text,
                    "duration": duration,
                    "status": "成功"
                }
        except Exception as e:
            return {
                "task_id": task_id,
                "error": str(e),
                "duration": time.time() - start_time,
                "status": "失败"
            }

    def on_sql_task_done(self, future, task_id):
        """SQL任务完成回调"""
        try:
            result = future.result()
            # 在主线程中更新UI
            self.root.after(0, self.update_task_result, task_id, result)

            # 从运行任务中移除
            if task_id in self.running_tasks:
                del self.running_tasks[task_id]

            # 检查是否所有任务完成
            if not self.running_tasks:
                self.execute_btn.config(state=tk.NORMAL)
                self.cancel_btn.config(state=tk.DISABLED)
                self.update_status("所有任务完成!")
        except Exception as e:
            self.update_status(f"任务处理错误: {str(e)}")

    def update_task_result(self, task_id, result):
        """更新任务结果到UI"""
        # 更新任务树中的状态
        if "status" in result:
            self.task_tree.set(str(task_id), "status", result["status"])
            self.task_tree.set(str(task_id), "duration", f"{result['duration']:.2f}")

            # 根据状态更新标签
            if result["status"] == "成功":
                self.task_tree.item(str(task_id), tags=("success",))
            else:
                self.task_tree.item(str(task_id), tags=("error",))

        # 如果当前选择的是这个任务，显示详细信息
        selected = self.task_tree.selection()
        if selected and int(selected[0]) == task_id:
            self.show_task_details(task_id, result)

    def on_task_select(self, event):
        """任务树选择事件"""
        selected = self.task_tree.selection()
        if not selected:
            return

        task_id = int(selected[0])

        # 查找任务结果
        if task_id in self.running_tasks:
            # 任务还在运行中
            self.show_running_task(task_id)
        else:
            # 任务已完成，尝试显示结果
            # 在实际应用中，您可能需要存储已完成任务的结果
            # 这里简化处理，只显示状态
            status = self.task_tree.item(selected[0], "values")[2]
            self.plan_text.config(state=tk.NORMAL)
            self.plan_text.delete(1.0, tk.END)
            self.plan_text.insert(tk.END, f"任务状态: {status}")
            self.plan_text.config(state=tk.DISABLED)

            # 清空结果树
            for item in self.result_tree.get_children():
                self.result_tree.delete(item)

    def show_running_task(self, task_id):
        """显示运行中任务的详情"""
        task_info = self.running_tasks[task_id]
        self.plan_text.config(state=tk.NORMAL)
        self.plan_text.delete(1.0, tk.END)
        self.plan_text.insert(tk.END, f"任务运行中...\nSQL: {task_info['sql']}")
        self.plan_text.config(state=tk.DISABLED)

        # 清空结果树
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

    def show_task_details(self, task_id, result):
        """显示任务详情"""
        # 更新执行计划标签页
        self.plan_text.config(state=tk.NORMAL)
        self.plan_text.delete(1.0, tk.END)

        if "plan" in result:
            self.plan_text.insert(tk.END, result["plan"])
        elif "error" in result:
            self.plan_text.insert(tk.END, f"错误信息:\n{result['error']}")
        self.plan_text.config(state=tk.DISABLED)

        # 更新执行结果标签页
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        if "result" in result and result["result"]:
            # 动态创建结果树的列
            columns = list(result["result"][0].keys())
            self.result_tree["columns"] = columns

            # 配置列标题
            for col in columns:
                self.result_tree.heading(col, text=col)
                self.result_tree.column(col, width=100)

            # 填充数据
            for row in result["result"]:
                values = [row[col] for col in columns]
                self.result_tree.insert("", tk.END, values=values)

    def cancel_all_tasks(self):
        """取消所有任务"""
        if messagebox.askyesno("确认", "确定要取消所有运行中的任务吗？"):
            for task_id, task_info in list(self.running_tasks.items()):
                # 取消任务
                task_info["future"].cancel()

                # 更新任务状态
                self.task_tree.set(str(task_id), "status", "已取消")
                self.task_tree.item(str(task_id), tags=("cancelled",))

            # 清空运行中任务
            self.running_tasks = {}

            # 更新按钮状态
            self.execute_btn.config(state=tk.NORMAL)
            self.cancel_btn.config(state=tk.DISABLED)
            self.update_status("所有任务已取消")

    def update_status(self, message):
        """更新状态栏"""
        self.status_var.set(message)

    def on_close(self):
        """窗口关闭时的清理工作"""
        if self.running_tasks:
            if messagebox.askyesno(
                    "确认",
                    "有任务正在运行，确定要退出吗？"
            ):
                self.cancel_all_tasks()

        # 关闭数据库连接池
        if self.pool:
            asyncio.run_coroutine_threadsafe(self.pool.close(), self.loop).result()

        # 停止事件循环
        self.loop.call_soon_threadsafe(self.loop.stop)

        # 等待线程结束
        self.asyncio_thread.join(timeout=1.0)

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SQLPerformanceApp(root)
    root.mainloop()