#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书文件上传工具 GUI版
"""

import os
import sys
import threading
import queue
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
from dotenv import load_dotenv, set_key

# 导入原始逻辑
from feishu_uploader import FeishuUploader

class TextRedirector:
    """将 stdout 重定向到 Tkinter Text 组件"""
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.after(0, self._insert, str)

    def _insert(self, str):
        self.widget.configure(state='normal')
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)
        self.widget.configure(state='disabled')

    def flush(self):
        pass

class FeishuUploaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("飞书文件上传工具 v1.0")
        self.root.geometry("800x600")
        
        # 加载环境变量
        load_dotenv()
        self.env_path = Path(".env")
        if not self.env_path.exists():
            with open(self.env_path, "w") as f:
                f.write("")

        self.setup_ui()
        self.load_settings()
        
        # 重定向输出
        sys.stdout = TextRedirector(self.log_area)
        sys.stderr = TextRedirector(self.log_area)

    def setup_ui(self):
        # 配置容器
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 设置区域
        settings_frame = ttk.LabelFrame(main_frame, text="配置参数", padding="10")
        settings_frame.pack(fill=tk.X, pady=5)

        # APP ID
        ttk.Label(settings_frame, text="APP ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.app_id_var = tk.StringVar()
        ttk.Entry(settings_frame, textvariable=self.app_id_var, width=50).grid(row=0, column=1, sticky=tk.W, padx=5)

        # APP SECRET
        ttk.Label(settings_frame, text="APP SECRET:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.app_secret_var = tk.StringVar()
        ttk.Entry(settings_frame, textvariable=self.app_secret_var, width=50, show="*").grid(row=1, column=1, sticky=tk.W, padx=5)

        # PARENT NODE
        ttk.Label(settings_frame, text="父节点 Token:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.parent_node_var = tk.StringVar()
        ttk.Entry(settings_frame, textvariable=self.parent_node_var, width=50).grid(row=2, column=1, sticky=tk.W, padx=5)

        # PROXY URL
        ttk.Label(settings_frame, text="代理 URL:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.proxy_url_var = tk.StringVar()
        ttk.Entry(settings_frame, textvariable=self.proxy_url_var, width=50).grid(row=3, column=1, sticky=tk.W, padx=5)
        ttk.Label(settings_frame, text="(例如 http://127.0.0.1:3128)", foreground="gray").grid(row=3, column=2, sticky=tk.W)

        # 目录选择
        path_frame = ttk.LabelFrame(main_frame, text="上传目标", padding="10")
        path_frame.pack(fill=tk.X, pady=5)

        ttk.Label(path_frame, text="根目录:").grid(row=0, column=0, sticky=tk.W)
        self.root_dir_var = tk.StringVar()
        ttk.Entry(path_frame, textvariable=self.root_dir_var, width=60).grid(row=0, column=1, padx=5)
        ttk.Button(path_frame, text="浏览", command=self.browse_directory).grid(row=0, column=2)

        # 选项
        options_frame = ttk.Frame(main_frame, padding="5")
        options_frame.pack(fill=tk.X)

        self.dry_run_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="演练模式 (Dry Run)", variable=self.dry_run_var).pack(side=tk.LEFT, padx=10)

        self.force_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="强制上传", variable=self.force_var).pack(side=tk.LEFT, padx=10)

        self.concurrent_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="并发上传 (5)", variable=self.concurrent_var).pack(side=tk.LEFT, padx=10)

        self.skip_proxy_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="禁用系统代理 (解决407错误)", variable=self.skip_proxy_var).pack(side=tk.LEFT, padx=10)

        self.retry_var = tk.BooleanVar(value=False)
        self.retry_cb = ttk.Checkbutton(options_frame, text="重试失败项", variable=self.retry_var)
        self.retry_cb.pack(side=tk.LEFT, padx=10)

        # 控制按钮
        control_frame = ttk.Frame(main_frame, padding="10")
        control_frame.pack(fill=tk.X)
        self.start_btn = ttk.Button(control_frame, text="开始上传", command=self.start_upload)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="停止上传", command=self.stop_upload, state='disabled')
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.uploader = None

        # 日志区域
        log_frame = ttk.LabelFrame(main_frame, text="运行日志", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True)
        self.log_area = scrolledtext.ScrolledText(log_frame, state='disabled', height=15)
        self.log_area.pack(fill=tk.BOTH, expand=True)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.root_dir_var.set(directory)

    def load_settings(self):
        self.app_id_var.set(os.getenv("FEISHU_APP_ID", ""))
        self.app_secret_var.set(os.getenv("FEISHU_APP_SECRET", ""))
        self.parent_node_var.set(os.getenv("FEISHU_PARENT_NODE", ""))
        self.proxy_url_var.set(os.getenv("PROXY_URL", ""))
        self.skip_proxy_var.set(os.getenv("SKIP_PROXY", "False") == "True")

    def save_settings(self):
        set_key(str(self.env_path), "FEISHU_APP_ID", self.app_id_var.get())
        set_key(str(self.env_path), "FEISHU_APP_SECRET", self.app_secret_var.get())
        set_key(str(self.env_path), "FEISHU_PARENT_NODE", self.parent_node_var.get())
        set_key(str(self.env_path), "PROXY_URL", self.proxy_url_var.get())
        set_key(str(self.env_path), "SKIP_PROXY", str(self.skip_proxy_var.get()))

    def start_upload(self):
        # 验证输入
        if not all([self.app_id_var.get(), self.app_secret_var.get(), self.parent_node_var.get(), self.root_dir_var.get()]):
            messagebox.showerror("错误", "请填写所有必填字段")
            return

        self.save_settings()
        self.start_btn.configure(state='disabled')
        self.stop_btn.configure(state='normal')
        
        # 开启线程执行任务
        thread = threading.Thread(target=self.run_uploader_task)
        thread.daemon = True
        thread.start()

    def stop_upload(self):
        if self.uploader:
            self.uploader.stop()
            print("\n[!] 正在发送停止信号...")
            self.stop_btn.configure(state='disabled')

    def run_uploader_task(self):
        # 初始化结果变量
        success_count = 0
        failed_count = 0
        failed_files = []
        
        try:
            proxy_url = self.proxy_url_var.get()
            proxy_port = os.getenv("PROXY_PORT", "")
            if not proxy_url and proxy_port:
                proxy_url = f"http://127.0.0.1:{proxy_port}"

            self.uploader = FeishuUploader(
                self.app_id_var.get(),
                self.app_secret_var.get(),
                self.parent_node_var.get(),
                skip_proxy=self.skip_proxy_var.get(),
                proxy_url=proxy_url
            )
            uploader = self.uploader
            
            root_dir = self.root_dir_var.get()
            dry_run = self.dry_run_var.get()
            force = self.force_var.get()
            concurrent = self.concurrent_var.get()
            retry = self.retry_var.get()
            
            failed_json = Path("failed_uploads.json")
            retry_files = None
            
            # 如果选择了重试模式
            if retry:
                if not failed_json.exists():
                    self.root.after(0, lambda: messagebox.showwarning("提示", "找不到 failed_uploads.json 文件，无法重试"))
                    self.root.after(0, lambda: self.retry_var.set(False))
                    return
                
                with open(failed_json, 'r', encoding='utf-8') as f:
                    retry_files = json.load(f)
                    for f_info in retry_files:
                        f_info["local_path"] = Path(f_info["local_path"])
                print(f"模式: 重试模式 (共 {len(retry_files)} 个之前失败的任务)")

            if concurrent:
                success_count, failed_count, failed_files = uploader.upload_all_concurrent(root_dir, dry_run, force, files_override=retry_files)
            else:
                success_count, failed_count, failed_files = uploader.upload_all(root_dir, dry_run, force, files_override=retry_files)
            
            print(f"\n任务结束: 成功 {success_count}, 失败 {failed_count}")
            
            failed_json = Path("failed_uploads.json")
            if failed_count > 0:
                # 将 Path 对象转换为字符串以便 JSON 序列化
                serializable_failed = []
                for f_info in failed_files:
                    f_copy = f_info.copy()
                    f_copy["local_path"] = str(f_copy["local_path"])
                    serializable_failed.append(f_copy)
                    
                with open(failed_json, 'w', encoding='utf-8') as f:
                    json.dump(serializable_failed, f, indent=4, ensure_ascii=False)
                print(f"✓ 失败清单已保存至: {failed_json}")
                print("请检查该文件以获取详细信息。")
            else:
                if failed_json.exists():
                    try:
                        failed_json.unlink()
                    except:
                        pass
                # 任务成功完成后，自动取消“重试项”勾选
                self.root.after(0, lambda: self.retry_var.set(False))

            self.root.after(0, lambda: messagebox.showinfo("完成", f"上传完成!\n成功: {success_count}\n失败: {failed_count}"))
            
        except Exception as e:
            err_msg = str(e)
            print(f"\n发生严重错误: {err_msg}")
            self.root.after(0, lambda m=err_msg: messagebox.showerror("错误", m))
        finally:
            self.root.after(0, lambda: self.start_btn.configure(state='normal'))
            self.root.after(0, lambda: self.stop_btn.configure(state='disabled'))
            self.uploader = None

if __name__ == "__main__":
    root = tk.Tk()
    app = FeishuUploaderGUI(root)
    root.mainloop()
