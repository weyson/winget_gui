"""图形用户界面"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
from threading import Thread
from models import SoftwarePackage, PackageManager
from winget_handler import WingetHandler
from i18n import I18n


class WingetGUI:
    """主应用程序界面"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Winget 软件更新管理器")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        
        self.i18n = I18n()
        self.package_manager = PackageManager()
        self.winget_handler = WingetHandler(i18n=self.i18n)
        
        self._setup_ui()
        self._apply_language()
        self._check_winget()
        
    def _setup_ui(self):
        """设置用户界面"""
        toolbar = ttk.Frame(self.root, padding="5")
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        self.refresh_btn = ttk.Button(
            toolbar,
            text="🔄 刷新",
            command=self._on_refresh
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        self.select_all_var = tk.BooleanVar(value=False)
        self.select_all_cb = ttk.Checkbutton(
            toolbar,
            text="全选",
            variable=self.select_all_var,
            command=self._on_select_all
        )
        self.select_all_cb.pack(side=tk.LEFT, padx=5)
        
        self.deselect_all_btn = ttk.Button(
            toolbar,
            text="取消全选",
            command=self._on_deselect_all
        )
        self.deselect_all_btn.pack(side=tk.LEFT, padx=5)
        
        self.upgrade_btn = ttk.Button(
            toolbar,
            text="⬆️ 更新所选",
            command=self._on_upgrade
        )
        self.upgrade_btn.pack(side=tk.LEFT, padx=5)
        
        self._create_language_selector(toolbar)
        
        self.status_label = ttk.Label(
            toolbar,
            text="就绪",
            padding="5"
        )
        self.status_label.pack(side=tk.RIGHT, padx=5)
        
        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        content_frame = ttk.Frame(self.root, padding="5")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        self._create_log_area()
        
        columns = ('select', 'name', 'id', 'current', 'available', 'source')
        self.tree = ttk.Treeview(
            content_frame,
            columns=columns,
            show='headings',
            selectmode='none'
        )
        
        self.tree.heading('select', text='')
        self.tree.heading('name', text='软件名称')
        self.tree.heading('id', text='软件ID')
        self.tree.heading('current', text='当前版本')
        self.tree.heading('available', text='可用版本')
        self.tree.heading('source', text='来源')
        
        self.tree.column('select', width=40, minwidth=40, anchor='center')
        self.tree.column('name', width=230)
        self.tree.column('id', width=180)
        self.tree.column('current', width=90)
        self.tree.column('available', width=90)
        self.tree.column('source', width=90)
        
        scrollbar = ttk.Scrollbar(
            content_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind('<Button-1>', self._on_tree_click)
    
    def _create_language_selector(self, parent):
        """创建语言选择器"""
        languages = self.i18n.get_supported_languages()
        self.lang_options = [(code, lang['name']) for code, lang in languages.items()]
        
        self.lang_var = tk.StringVar(value=self.i18n.get_language())
        
        self.lang_combobox = ttk.Combobox(
            parent,
            textvariable=self.lang_var,
            values=[name for _, name in self.lang_options],
            state='readonly',
            width=12
        )
        self.lang_combobox.pack(side=tk.RIGHT, padx=5)
        self.lang_combobox.bind('<<ComboboxSelected>>', self._on_language_change)
        
        self.lang_label = ttk.Label(parent, text=self.i18n.t('language') + ':')
        self.lang_label.pack(side=tk.RIGHT, padx=(5, 0))
    
    def _on_language_change(self, event):
        """语言切换事件"""
        selected_name = self.lang_var.get()
        for code, name in self.lang_options:
            if name == selected_name:
                self.i18n.set_language(code)
                self._apply_language()
                break
    
    def _apply_language(self):
        """应用语言设置（实时刷新所有界面文本）"""
        self.root.title(self.i18n.t('app_title'))
        
        self.refresh_btn.config(text=f"🔄 {self.i18n.t('refresh')}")
        self.select_all_cb.config(text=self.i18n.t('select_all'))
        self.deselect_all_btn.config(text=self.i18n.t('deselect_all'))
        self.upgrade_btn.config(text=self.i18n.t('upgrade_selected'))
        
        self.tree.heading('name', text=self.i18n.t('column_name'))
        self.tree.heading('id', text=self.i18n.t('column_id'))
        self.tree.heading('current', text=self.i18n.t('column_current_version'))
        self.tree.heading('available', text=self.i18n.t('column_available_version'))
        self.tree.heading('source', text=self.i18n.t('column_source'))
        
        self.log_label.config(text=self.i18n.t('log_label'))
        
        self.lang_label.config(text=self.i18n.t('language') + ':')
        
        self._update_selected_count()
    
    def _create_log_area(self):
        """创建日志区域（显示更新进度）"""
        log_frame = ttk.Frame(self.root, padding="5")
        log_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.log_label = ttk.Label(log_frame, text="更新进度：")
        self.log_label.pack(side=tk.LEFT, padx=5)
        
        self.log_text = tk.Text(log_frame, height=4, state=tk.DISABLED, font=('Consolas', 9))
        self.log_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.HORIZONTAL, command=self.log_text.xview)
        log_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.log_text.configure(xscrollcommand=log_scrollbar.set)
        
    def _check_winget(self):
        """检查 winget 是否可用"""
        available, message = self.winget_handler.check_winget_available()
        if not available:
            messagebox.showerror(self.i18n.t('error'), message)
            self._set_buttons_state(False)
        else:
            self._on_refresh()
    
    def _set_buttons_state(self, enabled: bool):
        """设置按钮状态"""
        state = 'normal' if enabled else 'disabled'
        self.refresh_btn.config(state=state)
        self.upgrade_btn.config(state=state)
        self.deselect_all_btn.config(state=state)
        self.lang_combobox.config(state='readonly' if enabled else 'disabled')
    
    def _set_status(self, message: str):
        """设置状态信息"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def _add_log(self, message: str):
        """添加日志信息"""
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def _clear_log(self):
        """清空日志"""
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state=tk.DISABLED)
    
    def _on_refresh(self):
        """刷新按钮点击事件"""
        self._set_buttons_state(False)
        self._set_status(self.i18n.t('status_refreshing'))
        
        thread = Thread(target=self._refresh_packages, daemon=True)
        thread.start()
    
    def _refresh_packages(self):
        """刷新软件包列表（在后台线程中运行）"""
        try:
            packages, error = self.winget_handler.get_upgradeable_packages()
            self.root.after(0, lambda: self._update_package_list(packages, error))
        except Exception as e:
            self.root.after(0, lambda: self._handle_refresh_error(str(e)))
    
    def _update_package_list(self, packages: List[SoftwarePackage], error: str):
        """更新软件包列表显示"""
        if error:
            messagebox.showerror(self.i18n.t('error'), f"{self.i18n.t('status_refreshing').replace('...', '')}{self.i18n.t('error')}:\n{error}")
            self._set_buttons_state(True)
            self._set_status(self.i18n.t('error'))
            return
        
        self.tree.delete(*self.tree.get_children())
        self.package_manager.clear_packages()
        
        for pkg in packages:
            self.package_manager.add_package(pkg)
            self.tree.insert('', 'end', values=(
                '☐',
                pkg.name,
                pkg.package_id,
                pkg.current_version,
                pkg.available_version,
                pkg.source
            ))
        
        self._update_selected_count()
        self._set_buttons_state(True)
        self.select_all_var.set(False)
    
    def _handle_refresh_error(self, error: str):
        """处理刷新错误"""
        messagebox.showerror(self.i18n.t('error'), f"{self.i18n.t('status_refreshing').replace('...', '')}{self.i18n.t('error')}:\n{error}")
        self._set_buttons_state(True)
        self._set_status(self.i18n.t('error'))
    
    def _on_select_all(self):
        """全选复选框点击事件"""
        if self.select_all_var.get():
            self.package_manager.select_all()
        else:
            self.package_manager.deselect_all()
        self._update_tree_selection()
    
    def _on_deselect_all(self):
        """取消全选按钮点击事件"""
        self.package_manager.deselect_all()
        self.select_all_var.set(False)
        self._update_tree_selection()
    
    def _update_tree_selection(self):
        """更新树形视图的选中状态（更新复选框显示）"""
        items = self.tree.get_children()
        for i, item in enumerate(items):
            if i < len(self.package_manager.packages):
                pkg = self.package_manager.packages[i]
                checkbox = '☑' if pkg.selected else '☐'
                values = list(self.tree.item(item, 'values'))
                values[0] = checkbox
                self.tree.item(item, values=values)
                tags = ('selected',) if pkg.selected else ()
                self.tree.item(item, tags=tags)
        self._update_selected_count()
    
    def _update_selected_count(self):
        """更新选中数量显示"""
        total = len(self.package_manager.packages)
        selected = len(self.package_manager.get_selected_packages())
        if total > 0:
            self.status_label.config(text=self.i18n.t('status_found_packages', count=total, selected=selected))
        else:
            self.status_label.config(text=self.i18n.t('status_no_packages'))
    
    def _on_tree_click(self, event):
        """树形视图点击事件（点击任意列切换复选框）"""
        region = self.tree.identify('region', event.x, event.y)
        if region == 'cell':
            item = self.tree.identify_row(event.y)
            
            if item:
                index = self.tree.index(item)
                if index < len(self.package_manager.packages):
                    pkg = self.package_manager.packages[index]
                    pkg.selected = not pkg.selected
                    
                    self.select_all_var.set(self.package_manager.is_all_selected())
                    self._update_item_display(item, pkg.selected)
                    self._update_selected_count()
    
    def _update_item_display(self, item: str, selected: bool):
        """更新项目的显示状态（包括复选框）"""
        checkbox = '☑' if selected else '☐'
        values = list(self.tree.item(item, 'values'))
        values[0] = checkbox
        self.tree.item(item, values=values)
        
        tags = ('selected',) if selected else ()
        self.tree.item(item, tags=tags)
        
        self.tree.tag_configure('selected', background='#e3f2fd')
    
    def _on_upgrade(self):
        """更新按钮点击事件"""
        selected = self.package_manager.get_selected_packages()
        
        if not selected:
            messagebox.showwarning(self.i18n.t('warning'), self.i18n.t('warning_no_selection'))
            return
        
        packages_text = "\n".join([f"• {pkg.name}" for pkg in selected[:5]])
        remaining = len(selected) - 5
        
        if remaining > 0:
            message = self.i18n.t('confirm_upgrade_message', count=len(selected), packages=packages_text)
            message += "\n" + self.i18n.t('confirm_upgrade_more', remaining=remaining)
        else:
            message = self.i18n.t('confirm_upgrade_message', count=len(selected), packages=packages_text)
        
        if not messagebox.askyesno(self.i18n.t('confirm_upgrade_title'), message):
            return
        
        self._set_buttons_state(False)
        thread = Thread(target=self._upgrade_packages, args=(selected,), daemon=True)
        thread.start()
    
    def _upgrade_packages(self, packages: List[SoftwarePackage]):
        """更新选中的软件包（在后台线程中执行）"""
        total = len(packages)
        results = []
        
        self.root.after(0, self._clear_log)
        
        for i, pkg in enumerate(packages, 1):
            pkg_name = pkg.name
            
            self.root.after(0, lambda name=pkg_name, idx=i, total=total: 
                           self._set_status(self.i18n.t('status_upgrading', name=name, index=idx, total=total)))
            self.root.after(0, lambda name=pkg_name: 
                           self._add_log(self.i18n.t('log_start', name=name)))
            
            def progress_callback(line, name=pkg_name):
                self.root.after(0, lambda msg=line, n=name: self._add_log(f"[{n}] {msg}"))
            
            result = self.winget_handler.upgrade_package(pkg.package_id, progress_callback)
            results.append((pkg, result))
            
            status_key = 'log_success' if result.success else 'log_failure'
            self.root.after(0, lambda name=pkg_name, key=status_key: 
                           self._add_log(self.i18n.t(key, name=name)))
        
        self.root.after(0, lambda: self._show_upgrade_results(results))
    
    def _show_upgrade_results(self, results):
        """显示更新结果汇总（在主线程中运行）"""
        success_count = sum(1 for _, r in results if r.success)
        fail_count = len(results) - success_count
        
        message = f"{self.i18n.t('result_complete')}\n\n{self.i18n.t('result_success', success=success_count)}\n{self.i18n.t('result_failure', failure=fail_count)}\n\n"
        
        if success_count > 0:
            message += self.i18n.t('result_success_list') + "\n"
            for pkg, result in results:
                if result.success:
                    message += f"✓ {pkg.name}\n"
        
        if fail_count > 0:
            message += "\n" + self.i18n.t('result_failure_list') + "\n"
            for pkg, result in results:
                if not result.success:
                    message += f"✗ {pkg.name}: {result.message}\n"
        
        messagebox.showinfo(self.i18n.t('result_title'), message)
        
        self._set_status(self.i18n.t('status_upgrade_complete'))
        self._set_buttons_state(True)
        
        self._on_refresh()
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()


def main():
    """主函数"""
    app = WingetGUI()
    app.run()


if __name__ == '__main__':
    main()