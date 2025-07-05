import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import asyncio
import sqlite3
import threading
import time
import random
from datetime import datetime
import os


class SQLPerformanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL性能检测工具 (SQLite3)")
        self.root.geometry("1000x700")

        # 创建 asyncio 事件循环
        self.loop = asyncio.new_event_loop()

        # 数据库连接
        self.conn = None
        self.db_path = "performance_test.db"

        # 当前运行的任务
        self.running_tasks = {}
        self.task_counter = 0
        self.completed_tasks = {}  # 存储已完成任务的结果

        # 创建UI组件
        self.create_widgets()

        # 初始化数据库
        self.initialize_database()

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

    def initialize_database(self):
        """初始化SQLite数据库并创建测试数据（兼容版本）"""
        try:
            # 如果数据库已存在，删除它
            if os.path.exists(self.db_path):
                os.remove(self.db_path)

            # 创建新数据库
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()

            # 创建测试表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS large_table (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                email TEXT,
                salary REAL,
                join_date TEXT
            )
            """)

            # 创建大表（用于模拟耗时查询）
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS huge_table (
                id INTEGER PRIMARY KEY,
                value1 REAL,
                value2 REAL,
                value3 REAL,
                description TEXT
            )
            """)

            # 插入大量测试数据 - 使用循环替代 generate_series
            # 小表：1000条记录
            for i in range(1, 1001):
                name = f"User{random.randint(1, 1000000)}"
                age = random.randint(20, 60)
                email = f"user{random.randint(1, 1000000)}@example.com"
                salary = round(3000.0 + random.random() * 7000, 2)
                days_ago = random.randint(0, 365)
                join_date = datetime.now().replace(microsecond=0) - timedelta(days=days_ago)

                cursor.execute("""
                INSERT INTO large_table (name, age, email, salary, join_date)
                VALUES (?, ?, ?, ?, ?)
                """, (name, age, email, salary, join_date.strftime("%Y-%m-%d")))

            # 大表：100,000条记录 - 用于模拟耗时查询
            # 批量插入以提高性能
            batch_size = 1000
            for batch in range(100):  # 100 batches of 1000 = 100,000
                values = []
                for i in range(batch_size):
                    value1 = round(random.random() * 1000, 2)
                    value2 = round(random.random() * 1000, 2)
                    value3 = round(random.random() * 1000, 2)
                    description = f"Description {random.randint(1, 1000000)}"
                    values.append((value1, value2, value3, description))

                cursor.executemany("""
                INSERT INTO huge_table (value1, value2, value3, description)
                VALUES (?, ?, ?, ?)
                """, values)

            # 创建复杂视图（用于模拟复杂查询）
            cursor.execute("""
            CREATE VIEW IF NOT EXISTS complex_view AS
            SELECT 
                l.id, 
                l.name, 
                l.age, 
                h.value1, 
                h.value2,
                (h.value1 + h.value2) AS total,
                CASE 
                    WHEN (h.value1 + h.value2) > 1500 THEN 'High'
                    WHEN (h.value1 + h.value2) > 1000 THEN 'Medium'
                    ELSE 'Low'
                END AS category
            FROM large_table l
            JOIN huge_table h ON l.id = h.id % 1000
            """)

            self.conn.commit()
            self.update_status("数据库初始化完成! 已创建测试数据.")
        except Exception as e:
            self.update_status(f"数据库初始化失败: {str(e)}")
            messagebox.showerror("错误", f"数据库初始化失败: {str(e)}")

    def create_widgets(self):
        """创建所有GUI组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # SQL输入区域
        sql_frame = ttk.LabelFrame(main_frame, text="SQL输入", padding=10)
        sql_frame.pack(fill=tk.X, pady=5)

        self.sql_entry = scrolledtext.ScrolledText(sql_frame, height=10, wrap=tk.WORD)
        self.sql_entry.pack(fill=tk.BOTH, expand=True)

        # 预置查询按钮
        preset_frame = ttk.Frame(sql_frame)
        preset_frame.pack(fill=tk.X, pady=5)

        ttk.Label(preset_frame, text="预置查询:").pack(side=tk.LEFT, padx=5)

        self.preset_var = tk.StringVar()
        presets = [
            ("简单查询", "SELECT * FROM large_table LIMIT 10"),
            ("中等复杂度", "SELECT * FROM complex_view WHERE category = 'High'"),
            ("耗时查询1", "SELECT AVG(value1), AVG(value2), AVG(value3) FROM huge_table"),
            ("耗时查询2", "SELECT category, COUNT(*), AVG(total) FROM complex_view GROUP BY category"),
            ("复杂连接", """
            SELECT 
                l.name, 
                l.age, 
                h.value1, 
                h.value2,
                h.value3,
                (h.value1 + h.value2 + h.value3) AS total
            FROM large_table l
            JOIN huge_table h ON l.id = h.id % 1000
            WHERE total > 1500
            ORDER BY total DESC
            """),
            ("最大复杂度", """
            WITH RECURSIVE fibonacci(n, a, b) AS (
                SELECT 1, 0, 1
                UNION ALL
                SELECT n+1, b, a+b FROM fibonacci WHERE n < 40
            )
            SELECT f.a, f.b, l.name, h.value1
            FROM fibonacci f
            JOIN large_table l ON f.n = l.id % 10
            JOIN huge_table h ON f.n = h.id % 10
            """)
        ]

        for text, query in presets:
            btn = ttk.Button(
                preset_frame,
                text=text,
                width=15,
                command=lambda q=query: self.set_query(q)
            )
            btn.pack(side=tk.LEFT, padx=2)

        # 控制按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        self.execute_btn = ttk.Button(
            button_frame,
            text="执行SQL",
            command=self.execute_sql
        )
        self.execute_btn.pack(side=tk.LEFT, padx=5)

        self.cancel_btn = ttk.Button(
            button_frame,
            text="取消所有任务",
            command=self.cancel_all_tasks,
            state=tk.DISABLED
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=5)

        # 添加延迟选项
        delay_frame = ttk.Frame(button_frame)
        delay_frame.pack(side=tk.LEFT, padx=20)

        ttk.Label(delay_frame, text="模拟延迟:").pack(side=tk.LEFT)
        self.delay_var = tk.DoubleVar(value=0.0)
        delay_spin = ttk.Spinbox(
            delay_frame,
            from_=0,
            to=10,
            increment=0.5,
            textvariable=self.delay_var,
            width=5
        )
        delay_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(delay_frame, text="秒").pack(side=tk.LEFT)

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

        # 为结果树添加滚动条容器
        result_container = ttk.Frame(result_frame)
        result_container.pack(fill=tk.BOTH, expand=True)

        # 创建结果树
        self.result_tree = ttk.Treeview(result_container)
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(
            result_container,
            orient=tk.VERTICAL,
            command=self.result_tree.yview
        )
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

        # 为任务树添加滚动条容器
        task_container = ttk.Frame(task_frame)
        task_container.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "sql", "status", "start_time", "duration")
        self.task_tree = ttk.Treeview(
            task_container,
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

        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 任务树滚动条
        task_scrollbar = ttk.Scrollbar(
            task_container,
            orient=tk.VERTICAL,
            command=self.task_tree.yview
        )
        self.task_tree.configure(yscrollcommand=task_scrollbar.set)
        task_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 绑定任务树选择事件
        self.task_tree.bind("<<TreeviewSelect>>", self.on_task_select)

        # 添加标签样式
        self.task_tree.tag_configure("running", background="#e6f7ff")
        self.task_tree.tag_configure("success", background="#e6ffe6")
        self.task_tree.tag_configure("error", background="#ffe6e6")
        self.task_tree.tag_configure("cancelled", background="#f0f0f0")

    def set_query(self, query):
        """设置预置查询"""
        self.sql_entry.delete("1.0", tk.END)
        self.sql_entry.insert("1.0", query)

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

            # 获取模拟延迟时间
            delay = self.delay_var.get()

            # 在asyncio线程中执行SQL
            future = asyncio.run_coroutine_threadsafe(
                self.execute_sql_task(task_id, sql, delay),
                self.loop
            )

            # 存储任务引用
            self.running_tasks[task_id] = {
                "future": future,
                "start_time": time.time(),
                "sql": sql,
                "delay": delay
            }

            # 添加完成回调
            future.add_done_callback(
                lambda f, tid=task_id: self.on_sql_task_done(f, tid)
            )

    async def execute_sql_task(self, task_id, sql, delay):
        """执行SQL任务的协程 - 使用线程池执行同步SQLite操作"""
        try:
            # 在单独的线程中执行数据库操作
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                None,  # 使用默认线程池执行器
                self.run_sqlite_query,  # 同步函数
                task_id,
                sql,
                delay
            )
            return result
        except Exception as e:
            return {
                "task_id": task_id,
                "error": str(e),
                "status": "失败"
            }

    def run_sqlite_query(self, task_id, sql, delay):
        """执行SQLite查询的同步函数"""
        try:
            start_time = time.time()

            # 创建新的数据库连接（每个任务独立连接）
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 模拟查询延迟
            if delay > 0:
                time.sleep(delay)

            # 执行SQL并获取结果
            cursor.execute(sql)
            result = cursor.fetchall()

            # 获取执行计划
            try:
                cursor.execute(f"EXPLAIN QUERY PLAN {sql}")
                plan_rows = cursor.fetchall()

                # 解析执行计划为可读格式
                plan_text = self.format_query_plan(plan_rows)
            except Exception as e:
                plan_text = f"无法获取执行计划: {str(e)}"

            # 计算执行时间
            duration = time.time() - start_time

            # 获取列名
            col_names = []
            if cursor.description:
                col_names = [desc[0] for desc in cursor.description]

            # 关闭连接
            conn.close()

            return {
                "task_id": task_id,
                "result": result,
                "columns": col_names,
                "plan": plan_text,
                "duration": duration,
                "status": "成功",
                "sql": sql
            }
        except Exception as e:
            return {
                "task_id": task_id,
                "error": str(e),
                "duration": time.time() - start_time,
                "status": "失败",
                "sql": sql
            }

    def format_query_plan(self, plan_rows):
        """格式化SQLite查询计划为可读文本"""
        plan_text = "SQLite 执行计划:\n"
        plan_text += "=" * 50 + "\n"

        for row in plan_rows:
            # row结构: (selectid, order, from, detail)
            plan_text += f"步骤 {row[1]}: {row[3]}\n"

        plan_text += "=" * 50 + "\n"
        plan_text += "说明:\n"
        plan_text += "- 'SCAN TABLE' 表示全表扫描\n"
        plan_text += "- 'SEARCH TABLE' 表示使用索引查找\n"
        plan_text += "- 'USE TEMP B-TREE' 表示使用了临时表\n"

        return plan_text

    def on_sql_task_done(self, future, task_id):
        """SQL任务完成回调"""
        try:
            result = future.result()
            # 在主线程中更新UI
            self.root.after(0, self.update_task_result, task_id, result)

            # 从运行任务中移除并存储结果
            if task_id in self.running_tasks:
                self.completed_tasks[task_id] = result
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
            duration = result.get("duration", 0)
            self.task_tree.set(str(task_id), "status", result["status"])
            self.task_tree.set(str(task_id), "duration", f"{duration:.2f}")

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
        elif task_id in self.completed_tasks:
            # 任务已完成，显示结果
            self.show_task_details(task_id, self.completed_tasks[task_id])
        else:
            # 未知状态
            self.plan_text.config(state=tk.NORMAL)
            self.plan_text.delete(1.0, tk.END)
            self.plan_text.insert(tk.END, "无法找到任务结果")
            self.plan_text.config(state=tk.DISABLED)

            # 清空结果树
            for item in self.result_tree.get_children():
                self.result_tree.delete(item)

    def show_running_task(self, task_id):
        """显示运行中任务的详情"""
        task_info = self.running_tasks[task_id]
        self.plan_text.config(state=tk.NORMAL)
        self.plan_text.delete(1.0, tk.END)
        self.plan_text.insert(tk.END, f"任务运行中...\n\nSQL:\n{task_info['sql']}\n\n模拟延迟: {task_info['delay']}秒")
        self.plan_text.config(state=tk.DISABLED)

        # 清空结果树
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        # 显示加载中的提示
        self.result_tree["columns"] = ["状态"]
        self.result_tree.heading("#0", text="信息")
        self.result_tree.heading("状态", text="值")
        self.result_tree.column("#0", width=200)
        self.result_tree.column("状态", width=300)

        self.result_tree.insert("", "end", text="任务状态", values=("运行中...",))
        self.result_tree.insert("", "end", text="开始时间", values=(self.task_tree.item(str(task_id), "values")[3],))
        self.result_tree.insert("", "end", text="已运行时间",
                                values=(f"{time.time() - task_info['start_time']:.2f}秒",))

    def show_task_details(self, task_id, result):
        """显示任务详情 - 修复执行结果和执行计划显示"""
        # 更新执行计划标签页
        self.plan_text.config(state=tk.NORMAL)
        self.plan_text.delete(1.0, tk.END)

        if "plan" in result:
            self.plan_text.insert(tk.END, f"执行计划:\n{'=' * 50}\n")
            self.plan_text.insert(tk.END, result["plan"])
            self.plan_text.insert(tk.END, f"\n{'=' * 50}\n")
        elif "error" in result:
            self.plan_text.insert(tk.END, f"错误信息:\n{'=' * 50}\n")
            self.plan_text.insert(tk.END, result["error"])
            self.plan_text.insert(tk.END, f"\n{'=' * 50}\n")

        self.plan_text.insert(tk.END, f"\n原始SQL:\n{result.get('sql', '')}")
        self.plan_text.config(state=tk.DISABLED)

        # 更新执行结果标签页
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        # 清空列配置
        self.result_tree["columns"] = []

        if "result" in result and result["result"]:
            # 创建结果树的列
            columns = result.get("columns", [])
            if not columns:
                # 如果没有列名，使用默认列名
                if result["result"]:
                    columns = [f"列 {i + 1}" for i in range(len(result["result"][0]))]
                else:
                    columns = ["结果"]

            # 配置列
            self.result_tree["columns"] = columns
            for col in columns:
                self.result_tree.heading(col, text=col)
                self.result_tree.column(col, width=100, anchor=tk.W)

            # 填充数据
            for row_idx, row in enumerate(result["result"]):
                # 确保行数据长度与列数匹配
                if len(row) < len(columns):
                    # 如果数据不足，填充空值
                    row = list(row) + [""] * (len(columns) - len(row))
                elif len(row) > len(columns):
                    # 如果数据过多，截断
                    row = row[:len(columns)]

                self.result_tree.insert("", tk.END, values=row)

                # 限制最多显示1000行
                if row_idx >= 1000:
                    self.result_tree.insert("", tk.END, values=("...",) * len(columns))
                    self.result_tree.insert("", tk.END,
                                            values=(f"只显示前1000行，共{len(result['result'])}行",) * len(columns))
                    break
        elif "error" in result:
            # 显示错误信息
            self.result_tree["columns"] = ["错误信息"]
            self.result_tree.heading("错误信息", text="错误详情")
            self.result_tree.column("错误信息", width=800)
            self.result_tree.insert("", tk.END, values=(result["error"],))
        else:
            # 显示无结果信息
            self.result_tree["columns"] = ["状态"]
            self.result_tree.heading("状态", text="执行结果")
            self.result_tree.column("状态", width=800)
            self.result_tree.insert("", tk.END, values=("查询成功，但无结果返回",))

    def cancel_all_tasks(self):
        """取消所有任务"""
        if messagebox.askyesno("确认", "确定要取消所有运行中的任务吗？"):
            for task_id, task_info in list(self.running_tasks.items()):
                # 取消任务
                task_info["future"].cancel()

                # 更新任务状态
                self.task_tree.set(str(task_id), "status", "已取消")
                self.task_tree.item(str(task_id), tags=("cancelled",))

                # 存储取消状态
                self.completed_tasks[task_id] = {
                    "task_id": task_id,
                    "status": "已取消",
                    "sql": task_info["sql"]
                }

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

        # 停止事件循环
        self.loop.call_soon_threadsafe(self.loop.stop)

        # 等待线程结束
        self.asyncio_thread.join(timeout=1.0)

        # 关闭数据库连接
        if self.conn:
            self.conn.close()
            try:
                os.remove(self.db_path)
            except:
                pass

        self.root.destroy()


if __name__ == "__main__":
    import sys

    if sys.version_info < (3, 7):
        print("需要 Python 3.7 或更高版本")
        sys.exit(1)

    from datetime import timedelta

    root = tk.Tk()
    app = SQLPerformanceApp(root)
    root.mainloop()