import os
import tkinter as tk
from tkinter import filedialog
#窗口
root = tk.Tk()
root.geometry('600x300')
root.title('洛谷爬虫')
#难度或者题解
diff = ["入门","普及-","普及","普及+","提高+","省选","NOI","题解","暂无评定"]

search_frame = tk.Frame(root)
search_frame.pack()

#难度选择
diff_Label = tk.Label(root, text="难度:")
diff_Label.pack(padx=0, pady=0)
selected_diff = tk.StringVar()
diff_menu = tk.OptionMenu(root, selected_diff, *diff)
diff_menu.pack(padx=0, pady=0)

tk.Label(search_frame, text='关键字:').pack(side=tk.LEFT, padx=0, pady=10)
key_entry = tk.Entry(search_frame) # 创建一个输入框
key_entry.pack(side=tk.LEFT, padx=5, pady=10) # 将输入框显示到界面
tk.Label(search_frame, text='选择文件夹:').pack(side=tk.LEFT, padx=0, pady=10)
type_entry = tk.Entry(search_frame)
type_entry.pack(side=tk.LEFT, padx=5, pady=10)
button = tk.Button(search_frame, text='搜索')
button.pack(side=tk.LEFT, padx=5, pady=10)

list_box = tk.Listbox(root)
list_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 点击按钮搜索文件
def search():
    # 1. 获取关键字、难度
    key = key_entry.get()
    diff =selected_diff.get()
    print(key, diff)

    # 2. 读取windows 系统的文件
    dir_path = filedialog.askdirectory()
    if dir_path:
        if diff in diff:
           file_list.delete(0, tk.END)
    # print(dir_path)   # 遍历文件，实现搜索功能
    file_list = os.walk(dir_path)
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file_path)
            if key in file_name and file_name.endswith(diff + '.md'):
                file_list.insert(tk.END, file_name)



# 创建滚动窗口并布局到页面上
sb = tk.Scrollbar(root)
sb.pack(side=tk.RIGHT, fill=tk.Y)
sb.config(command=list_box.yview)
list_box.config(yscrollcommand=sb.set)

button.config(command=search)

def list_click(event):
    # 1. 获取到选中的内容
    index = list_box.curselection()[0]
    path = list_box.get(index)
    print(path)
    # 2. 读取选中的路径内容
    content = open(path, mode='r', encoding='utf-8').read()
    # 3. 将内容显示到新的窗口
    top = tk.Toplevel(root)
    filename = path.split('/')[-1]
    top.title(filename)
    text = tk.Text(top)
    text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    text.insert(tk.END, content)


# 绑定点击事件
list_box.bind('<Double-Button-1>', list_click)

root.mainloop()
