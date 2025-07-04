import tkinter as tk
from tkinter import font, scrolledtext, ttk
import re
import sqlparse
import time


class SQLHighlighter:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.base_font = font.Font(family="Consolas", size=11)
        self.setup_tags()
        self.last_highlight_time = 0

    def setup_tags(self):
        # 创建所有标签的字体对象
        self.keyword_font = font.Font(font=self.base_font)
        self.keyword_font.configure(weight="bold")

        self.comment_font = font.Font(font=self.base_font)
        self.comment_font.configure(slant="italic")

        self.function_font = font.Font(font=self.base_font)
        self.string_font = font.Font(font=self.base_font)
        self.number_font = font.Font(font=self.base_font)
        self.operator_font = font.Font(font=self.base_font)
        self.datatype_font = font.Font(font=self.base_font)

        # 配置标签样式
        self.text_widget.tag_configure("keyword", foreground="#FF00CC", font=self.keyword_font)
        self.text_widget.tag_configure("function", foreground="#AA00AA", font=self.function_font)
        self.text_widget.tag_configure("string", foreground="#00AA00", font=self.string_font)
        self.text_widget.tag_configure("comment", foreground="#888888", font=self.comment_font)
        self.text_widget.tag_configure("number", foreground="#FF5500", font=self.number_font)
        self.text_widget.tag_configure("operator", foreground="#CC5500", font=self.operator_font)
        self.text_widget.tag_configure("datatype", foreground="#009999", font=self.datatype_font)

    def update_font_size(self, new_size):
        """更新所有字体大小"""
        self.base_font.configure(size=new_size)
        self.keyword_font.configure(size=new_size)
        self.comment_font.configure(size=new_size)
        self.function_font.configure(size=new_size)
        self.string_font.configure(size=new_size)
        self.number_font.configure(size=new_size)
        self.operator_font.configure(size=new_size)
        self.datatype_font.configure(size=new_size)

    def highlight_sql(self):
        """高亮SQL代码中的所有元素 - 使用更可靠的方法"""
        current_time = time.time()
        if current_time - self.last_highlight_time < 0.1:  # 防止过于频繁的高亮
            return
        self.last_highlight_time = current_time

        # 清除所有旧标签
        for tag in ["keyword", "function", "string", "comment", "number", "operator", "datatype"]:
            self.text_widget.tag_remove(tag, "1.0", "end")

        # 获取整个文本内容
        content = self.text_widget.get("1.0", "end-1c")
        if not content:
            return

        # 高亮不同类型的元素（注意顺序很重要）
        self.highlight_comments(content)
        self.highlight_strings(content)
        self.highlight_numbers(content)
        self.highlight_operators(content)
        self.highlight_keywords(content)
        self.highlight_functions(content)
        self.highlight_datatypes(content)

    def highlight_keywords(self, content):
        """高亮SQL关键字 - 使用更可靠的方法"""
        keywords = [
            "SELECT", "FROM", "WHERE", "INSERT", "UPDATE", "DELETE", "JOIN",
            "AND", "OR", "NOT", "GROUP BY", "ORDER BY", "HAVING", "LIMIT",
            "AS", "ON", "INTO", "VALUES", "SET", "CREATE", "TABLE", "INDEX",
            "DROP", "ALTER", "PRIMARY", "KEY", "FOREIGN", "REFERENCES", "UNIQUE",
            "DISTINCT", "CASE", "WHEN", "THEN", "ELSE", "END", "IS", "NULL",
            "BETWEEN", "LIKE", "IN", "EXISTS", "ALL", "ANY", "SOME", "ASC", "DESC"
        ]

        # 转换为小写用于不区分大小写的匹配
        content_lower = content.lower()

        for word in keywords:
            # 转换为小写用于匹配
            word_lower = word.lower()

            # 使用正则表达式匹配整个单词
            pattern = r'\b' + re.escape(word) + r'\b'

            # 在内容中查找所有匹配项
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                start_idx = f"1.0+{match.start()}c"
                end_idx = f"1.0+{match.end()}c"
                self.text_widget.tag_add("keyword", start_idx, end_idx)

    def highlight_functions(self, content):
        """高亮SQL函数 - 使用更可靠的方法"""
        functions = ["COUNT", "SUM", "AVG", "MAX", "MIN", "CONCAT", "NOW",
                     "DATE_FORMAT", "COALESCE", "CAST", "CONVERT", "LENGTH",
                     "UPPER", "LOWER", "SUBSTRING", "TRIM", "ROUND", "DATE_ADD"]

        for func in functions:
            pattern = r'\b' + re.escape(func) + r'\s*\('
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                start_idx = f"1.0+{match.start()}c"
                end_idx = f"1.0+{match.end()}c"
                self.text_widget.tag_add("function", start_idx, end_idx)

    def highlight_strings(self, content):
        """高亮字符串 - 使用更可靠的方法"""
        # 单引号字符串
        matches = re.finditer(r"'(.*?)'", content)
        for match in matches:
            start_idx = f"1.0+{match.start()}c"
            end_idx = f"1.0+{match.end()}c"
            self.text_widget.tag_add("string", start_idx, end_idx)

        # 双引号字符串
        matches = re.finditer(r'"(.*?)"', content)
        for match in matches:
            start_idx = f"1.0+{match.start()}c"
            end_idx = f"1.0+{match.end()}c"
            self.text_widget.tag_add("string", start_idx, end_idx)

    def highlight_comments(self, content):
        """高亮注释 - 使用更可靠的方法"""
        # 高亮单行注释 (-- 注释)
        matches = re.finditer(r'--.*?$', content, re.MULTILINE)
        for match in matches:
            start_idx = f"1.0+{match.start()}c"
            end_idx = f"1.0+{match.end()}c"
            self.text_widget.tag_add("comment", start_idx, end_idx)

        # 高亮多行注释 (/* 注释 */)
        matches = re.finditer(r'/\*.*?\*/', content, re.DOTALL)
        for match in matches:
            start_idx = f"1.0+{match.start()}c"
            end_idx = f"1.0+{match.end()}c"
            self.text_widget.tag_add("comment", start_idx, end_idx)

    def highlight_numbers(self, content):
        """高亮数字 - 使用更可靠的方法"""
        # 整数和小数
        matches = re.finditer(r'\b\d+\b', content)
        for match in matches:
            start_idx = f"1.0+{match.start()}c"
            end_idx = f"1.0+{match.end()}c"
            self.text_widget.tag_add("number", start_idx, end_idx)

        matches = re.finditer(r'\b\d+\.\d+\b', content)
        for match in matches:
            start_idx = f"1.0+{match.start()}c"
            end_idx = f"1.0+{match.end()}c"
            self.text_widget.tag_add("number", start_idx, end_idx)

    def highlight_operators(self, content):
        """高亮操作符 - 使用更可靠的方法"""
        operators = [
            "=", "<", ">", "<=", ">=", "<>", "!=",
            r"\+", "-", r"\*", "/", "%", r"\|\|"
        ]

        for op in operators:
            # 使用转义的操作符
            pattern = re.escape(op)
            matches = re.finditer(pattern, content)
            for match in matches:
                start_idx = f"1.0+{match.start()}c"
                end_idx = f"1.0+{match.end()}c"
                self.text_widget.tag_add("operator", start_idx, end_idx)

    def highlight_datatypes(self, content):
        """高亮数据类型 - 使用更可靠的方法"""
        datatypes = ["INT", "VARCHAR", "CHAR", "TEXT", "DATE", "DATETIME",
                     "TIMESTAMP", "DECIMAL", "FLOAT", "BOOLEAN", "BLOB"]

        for dtype in datatypes:
            pattern = r'\b' + re.escape(dtype) + r'\b'
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                start_idx = f"1.0+{match.start()}c"
                end_idx = f"1.0+{match.end()}c"
                self.text_widget.tag_add("datatype", start_idx, end_idx)


class SQLFormatterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL 编辑器")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")

        # 创建样式
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, font=("Arial", 10))
        self.style.configure("TFrame", background="#f0f0f0")

        # 创建主框架
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill="both", expand=True)

        # 创建工具栏
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill="x", pady=(0, 10))

        # 格式化按钮
        format_btn = ttk.Button(toolbar, text="美化 SQL", command=self.format_sql)
        format_btn.pack(side="left", padx=(0, 10))

        # 高亮按钮
        highlight_btn = ttk.Button(toolbar, text="应用高亮", command=self.apply_highlight)
        highlight_btn.pack(side="left", padx=(0, 10))

        # 字体大小控制
        font_frame = ttk.Frame(toolbar)
        font_frame.pack(side="right", padx=10)

        ttk.Label(font_frame, text="字体大小:").pack(side="left")
        self.font_size = tk.IntVar(value=12)
        font_spin = ttk.Spinbox(font_frame, from_=8, to=24, width=3,
                                textvariable=self.font_size, command=self.update_font)
        font_spin.pack(side="left", padx=5)

        # 主题选择
        theme_frame = ttk.Frame(toolbar)
        theme_frame.pack(side="right", padx=10)

        ttk.Label(theme_frame, text="主题:").pack(side="left")
        self.theme_var = tk.StringVar(value="default")
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, width=12)
        theme_combo["values"] = ("default", "dark", "blue", "green")
        theme_combo.pack(side="left", padx=5)
        theme_combo.bind("<<ComboboxSelected>>", self.change_theme)

        # 创建文本区域
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill="both", expand=True)

        # 创建滚动文本框
        self.text_widget = scrolledtext.ScrolledText(
            text_frame, wrap="none", font=("Consolas", 12), undo=True,
            padx=10, pady=10, bg="white", fg="black", insertbackground="black"
        )
        self.text_widget.pack(fill="both", expand=True)

        # 初始化高亮器
        self.highlighter = SQLHighlighter(self.text_widget)

        # 设置初始SQL
        self.set_initial_sql()

        # 绑定事件
        self.text_widget.bind("<Control-f>", lambda e: self.format_sql())
        self.text_widget.bind("<Control-h>", lambda e: self.apply_highlight())
        self.text_widget.bind("<KeyRelease>", self.on_key_release)  # 实时高亮

        # 初始高亮
        self.apply_highlight()

    def set_initial_sql(self):
        """设置初始SQL示例"""
        initial_sql = """/* 示例SQL查询 */
SELECT orders.id AS order_id, 
       customers.name, 
       SUM(order_items.quantity * products.price) AS total,
       COUNT(DISTINCT order_items.product_id) AS unique_products
FROM orders
JOIN customers ON orders.customer_id = customers.id
JOIN order_items ON orders.id = order_items.order_id
JOIN products ON order_items.product_id = products.id
WHERE orders.status = 'completed'
  AND orders.order_date BETWEEN '2023-01-01' AND '2023-12-31'
  AND total_price > 100.50
GROUP BY orders.id, customers.name
HAVING SUM(order_items.quantity * products.price) > 1000
ORDER BY total DESC
LIMIT 10;"""

        self.text_widget.insert("1.0", initial_sql)

    def format_sql(self):
        """格式化SQL代码 - 修复注释位置问题"""
        raw_sql = self.text_widget.get("1.0", "end-1c")

        try:
            # 使用sqlparse格式化SQL - 使用更兼容的设置
            formatted_sql = sqlparse.format(
                raw_sql,
                reindent=True,  # 重新缩进
                keyword_case="upper",  # 关键词大写
                identifier_case="lower",  # 标识符小写
                strip_comments=False,  # 保留注释
                use_space_around_operators=True,
                indent_width=2,  # 减少缩进宽度
                indent_after_first=False,
                comma_first=False
            )

            # 替换文本
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", formatted_sql)

            # 重新应用高亮
            self.apply_highlight()

        except Exception as e:
            error_message = f"\n\n/* SQL格式化错误: {str(e)} */"
            self.text_widget.insert("end", error_message)
            self.text_widget.tag_add("comment", "end-2l", "end")

    def apply_highlight(self):
        """应用语法高亮"""
        self.highlighter.highlight_sql()

    def on_key_release(self, event=None):
        """按键释放时触发高亮"""
        self.apply_highlight()

    def update_font(self):
        """更新字体大小"""
        new_size = self.font_size.get()
        # 更新文本组件字体
        self.text_widget.configure(font=("Consolas", new_size))

        # 更新高亮器的所有字体
        self.highlighter.update_font_size(new_size)

        # 重新应用高亮
        self.apply_highlight()

    def change_theme(self, event=None):
        """更改编辑器主题"""
        theme = self.theme_var.get()

        if theme == "dark":
            self.text_widget.configure(bg="#2d2d2d", fg="#f0f0f0", insertbackground="white")
        elif theme == "blue":
            self.text_widget.configure(bg="#e6f2ff", fg="#003366", insertbackground="#003366")
        elif theme == "green":
            self.text_widget.configure(bg="#e6ffe6", fg="#006600", insertbackground="#006600")
        else:  # default
            self.text_widget.configure(bg="white", fg="black", insertbackground="black")

        # 重新应用高亮
        self.apply_highlight()


if __name__ == "__main__":
    root = tk.Tk()
    app = SQLFormatterApp(root)
    root.mainloop()