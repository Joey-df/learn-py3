import tkinter as tk
from tkinter import ttk
import webbrowser

def create_hyperlink(text_widget, url, text):
    # 插入文本并添加标签
    text_widget.insert(tk.END, text, ("hyperlink", url))
    # 配置超链接样式
    text_widget.tag_configure("hyperlink", foreground="blue", underline=1)

def on_link_click(event):
    # 获取点击位置的标签
    tags = event.widget.tag_names(tk.CURRENT)
    # 检查是否有超链接标签
    for tag in tags:
        if tag.startswith("http"):
            webbrowser.open(tag)  # 使用默认浏览器打开
            return "break"  # 阻止事件继续传播

root = tk.Tk()
text = tk.Text(root, wrap="word", cursor="arrow")
text.pack(fill="both", expand=True)

# 创建超链接（注意：标签名直接使用URL）
create_hyperlink(text, "https://www.python.org", "访问Python官网\n")
create_hyperlink(text, "https://github.com", "访问GitHub\n")

# 绑定点击事件
text.tag_bind("hyperlink", "<Button-1>", on_link_click)
text.tag_bind("hyperlink", "<Enter>", lambda e: text.config(cursor="hand2"))
text.tag_bind("hyperlink", "<Leave>", lambda e: text.config(cursor="arrow"))

root.mainloop()