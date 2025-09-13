#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Upload Manager for QB Academy
Handles file upload UI and integration with database
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sqlite3
from datetime import datetime

class FileUploadManager:
    def __init__(self, parent, database_manager, current_user):
        self.parent = parent
        self.db_manager = database_manager
        self.current_user = current_user
        
    def create_file_upload_dialog(self, category='general', related_table=None, related_id=None):
        """إنشاء نافذة رفع الملفات"""
        upload_window = tk.Toplevel(self.parent)
        upload_window.title("رفع ملف جديد")
        upload_window.geometry("700x600")  # زيادة الارتفاع
        upload_window.configure(bg="#2D0A4D")
        upload_window.resizable(True, True)  # السماح بتغيير الحجم
        upload_window.grab_set()  # جعل النافذة modal
        upload_window.transient(self.parent)  # ربط النافذة بالنافذة الرئيسية
        
        # توسيط النافذة
        upload_window.update_idletasks()
        x = (upload_window.winfo_screenwidth() // 2) - (700 // 2)
        y = (upload_window.winfo_screenheight() // 2) - (600 // 2)
        upload_window.geometry(f"700x600+{x}+{y}")
        
        # التأكد من ظهور النافذة في المقدمة
        upload_window.lift()
        upload_window.focus_force()
        
        # عنوان النافذة
        title_label = tk.Label(upload_window,
                             text="رفع ملف جديد",
                             font=("Arial", 18, "bold"),
                             fg="#FFD700",
                             bg="#2D0A4D")
        title_label.pack(pady=20)
        
        # إطار رئيسي مع تمرير
        main_container = tk.Frame(upload_window, bg="#2D0A4D")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # إطار قابل للتمرير للمحتوى
        canvas = tk.Canvas(main_container, bg="#2D0A4D", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#2D0A4D")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # إطار المحتوى داخل الإطار القابل للتمرير
        content_frame = tk.Frame(scrollable_frame, bg="#3C1361", padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # متغيرات
        selected_file = tk.StringVar()
        file_category = tk.StringVar(value=category)
        file_description = tk.StringVar()
        
        # اختيار الملف
        file_frame = tk.Frame(content_frame, bg="#3C1361")
        file_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(file_frame,
                text="اختيار الملف:",
                font=("Arial", 12, "bold"),
                fg="#FFD700",
                bg="#3C1361").pack(anchor=tk.E, pady=5)
        
        file_path_frame = tk.Frame(file_frame, bg="#3C1361")
        file_path_frame.pack(fill=tk.X, pady=5)
        
        file_entry = tk.Entry(file_path_frame,
                            textvariable=selected_file,
                            font=("Arial", 10),
                            state='readonly',
                            width=40)
        file_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(file_path_frame,
                             text="📁 تصفح",
                             font=("Arial", 11, "bold"),
                             fg="white",
                             bg="#5A2A9C",
                             relief=tk.RAISED,
                             bd=2,
                             command=lambda: self.browse_file(selected_file))
        browse_btn.pack(side=tk.RIGHT, padx=5)
        
        # فئة الملف
        category_frame = tk.Frame(content_frame, bg="#3C1361")
        category_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(category_frame,
                text="فئة الملف:",
                font=("Arial", 12, "bold"),
                fg="#FFD700",
                bg="#3C1361").pack(anchor=tk.E, pady=5)
        
        category_combo = ttk.Combobox(category_frame,
                                    textvariable=file_category,
                                    values=['documents', 'procedures', 'forms', 'certificates', 'reports', 'general'],
                                    state='readonly',
                                    font=("Arial", 10))
        category_combo.pack(anchor=tk.E, pady=5)
        
        # وصف الملف
        desc_frame = tk.Frame(content_frame, bg="#3C1361")
        desc_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(desc_frame,
                text="وصف الملف:",
                font=("Arial", 12, "bold"),
                fg="#FFD700",
                bg="#3C1361").pack(anchor=tk.E, pady=5)
        
        desc_entry = tk.Entry(desc_frame,
                            textvariable=file_description,
                            font=("Arial", 10))
        desc_entry.pack(fill=tk.X, pady=5)
        
        # معلومات إضافية
        info_frame = tk.Frame(content_frame, bg="#3C1361")
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = tk.Text(info_frame,
                          height=3,
                          font=("Arial", 9),
                          bg="#2D0A4D",
                          fg="white",
                          wrap=tk.WORD)
        info_text.pack(fill=tk.X, pady=5)
        info_text.insert(tk.END, "ملاحظة: سيتم حفظ الملف بشكل آمن في نظام إدارة الملفات.\nأنواع الملفات المدعومة: PDF, DOC, DOCX, XLS, XLSX, TXT, JPG, PNG")
        info_text.config(state=tk.DISABLED)
        
        # إضافة تعليمات واضحة
        instruction_frame = tk.Frame(content_frame, bg="#3C1361")
        instruction_frame.pack(fill=tk.X, pady=10)
        
        instruction_label = tk.Label(instruction_frame,
                                   text="⚠️ تعليمات: اختر الملف أولاً، ثم اضغط على زر 'رفع الملف' أسفل النافذة",
                                   font=("Arial", 11, "bold"),
                                   fg="#FFD700",
                                   bg="#3C1361",
                                   wraplength=450,
                                   justify=tk.CENTER)
        instruction_label.pack(pady=5)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # أزرار التحكم - خارج المنطقة القابلة للتمرير (ثابتة في الأسفل)
        btn_frame = tk.Frame(upload_window, bg="#2D0A4D")
        btn_frame.pack(fill=tk.X, padx=20, pady=(10, 20), side=tk.BOTTOM)
        
        # إطار الأزرار مع ارتفاع ثابت وحدود واضحة
        buttons_container = tk.Frame(btn_frame, bg="#3C1361", height=100, relief=tk.RAISED, bd=3)
        buttons_container.pack(fill=tk.X, pady=10)
        buttons_container.pack_propagate(False)  # منع تقليص الحجم
        
        # إضافة تسمية للأزرار
        btn_label = tk.Label(buttons_container, text="🔽 خيارات الرفع 🔽", 
                           font=("Arial", 14, "bold"), fg="#FFD700", bg="#3C1361")
        btn_label.pack(pady=(8, 5))
        
        # إطار داخلي للأزرار
        inner_btn_frame = tk.Frame(buttons_container, bg="#3C1361")
        inner_btn_frame.pack(fill=tk.X, padx=20)
        
        # زر الرفع
        upload_btn = tk.Button(inner_btn_frame,
                             text="📤 اختر ملف أولاً",
                             font=("Arial", 16, "bold"),
                             fg="white",
                             bg="#CCCCCC",  # رمادي في البداية
                             width=20,
                             height=2,
                             relief=tk.RAISED,
                             bd=4,
                             state=tk.DISABLED,  # البداية معطل
                             command=lambda: self.upload_file(
                                 selected_file.get(),
                                 file_category.get(),
                                 file_description.get(),
                                 related_table,
                                 related_id,
                                 upload_window
                             ))
        upload_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        # زر الإلغاء
        cancel_btn = tk.Button(inner_btn_frame,
                             text="❌ إلغاء",
                             font=("Arial", 16, "bold"),
                             fg="white",
                             bg="#DC3545",
                             width=20,
                             height=2,
                             relief=tk.RAISED,
                             bd=4,
                             command=upload_window.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # تحديث دالة تتبع تغيير الملف
        def on_file_change(*args):
            if selected_file.get().strip():
                upload_btn.config(state=tk.NORMAL, bg="#4CAF50", text="📤 رفع الملف المحدد")
            else:
                upload_btn.config(state=tk.DISABLED, bg="#CCCCCC", text="📤 اختر ملف أولاً")
        
        # ربط التتبع
        selected_file.trace('w', on_file_change)
        
        # ربط عجلة الماوس بالتمرير
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        return upload_window
    
    def browse_file(self, file_var):
        """تصفح واختيار ملف"""
        file_path = filedialog.askopenfilename(
            title="اختيار ملف",
            filetypes=[
                ("جميع الملفات المدعومة", "*.pdf;*.doc;*.docx;*.xls;*.xlsx;*.txt;*.jpg;*.jpeg;*.png"),
                ("ملفات PDF", "*.pdf"),
                ("ملفات Word", "*.doc;*.docx"),
                ("ملفات Excel", "*.xls;*.xlsx"),
                ("ملفات نصية", "*.txt"),
                ("ملفات الصور", "*.jpg;*.jpeg;*.png"),
                ("جميع الملفات", "*.*")
            ]
        )
        
        if file_path:
            file_var.set(file_path)
    
    def upload_file(self, file_path, category, description, related_table, related_id, window):
        """رفع الملف وحفظه"""
        if not file_path:
            messagebox.showwarning("تحذير", "الرجاء اختيار ملف أولاً")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("خطأ", "الملف المحدد غير موجود")
            return
        
        try:
            # التحقق من حجم الملف (أقصى حد 50 ميجا)
            file_size = os.path.getsize(file_path)
            if file_size > 50 * 1024 * 1024:  # 50 MB
                messagebox.showerror("خطأ", "حجم الملف كبير جداً. الحد الأقصى 50 ميجابايت")
                return
            
            # رفع الملف
            result = self.db_manager.save_file(
                file_path=file_path,
                category=category,
                related_table=related_table,
                related_id=related_id,
                user_id=self.current_user['id'] if self.current_user else None,
                description=description
            )
            
            if result:
                # تسجيل النشاط
                self.db_manager.log_activity(
                    user_id=self.current_user['id'] if self.current_user else None,
                    action=f"رفع ملف: {result['original_name']}",
                    table_name="uploaded_files",
                    record_id=result['file_id']
                )
                
                messagebox.showinfo("نجح الرفع", 
                                  f"تم رفع الملف بنجاح!\n"
                                  f"اسم الملف: {result['original_name']}\n"
                                  f"الحجم: {self.format_file_size(result['file_size'])}\n"
                                  f"الفئة: {category}")
                window.destroy()
            else:
                messagebox.showerror("خطأ", "فشل في رفع الملف")
                
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء رفع الملف:\n{str(e)}")
    
    def create_file_manager_window(self):
        """إنشاء نافذة إدارة الملفات"""
        manager_window = tk.Toplevel(self.parent)
        manager_window.title("إدارة الملفات")
        manager_window.geometry("900x700")
        manager_window.configure(bg="#2D0A4D")
        manager_window.grab_set()  # جعل النافذة modal
        manager_window.transient(self.parent)  # ربط النافذة بالنافذة الرئيسية
        
        # توسيط النافذة
        manager_window.update_idletasks()
        x = (manager_window.winfo_screenwidth() // 2) - (900 // 2)
        y = (manager_window.winfo_screenheight() // 2) - (700 // 2)
        manager_window.geometry(f"900x700+{x}+{y}")
        
        # عنوان النافذة
        title_label = tk.Label(manager_window,
                             text="📂 إدارة الملفات والمستندات",
                             font=("Arial", 20, "bold"),
                             fg="#FFD700",
                             bg="#2D0A4D")
        title_label.pack(pady=15)
        
        # إطار التحكم
        control_frame = tk.Frame(manager_window, bg="#3C1361")
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # فلترة حسب الفئة
        filter_frame = tk.Frame(control_frame, bg="#3C1361")
        filter_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(filter_frame,
                text="فلترة حسب الفئة:",
                font=("Arial", 10, "bold"),
                fg="#FFD700",
                bg="#3C1361").pack(side=tk.LEFT, padx=5)
        
        category_var = tk.StringVar(value="الكل")
        category_filter = ttk.Combobox(filter_frame,
                                     textvariable=category_var,
                                     values=['الكل', 'documents', 'procedures', 'forms', 'certificates', 'reports', 'general'],
                                     state='readonly',
                                     width=15)
        category_filter.pack(side=tk.LEFT, padx=5)
        
        # زر رفع ملف جديد
        upload_btn = tk.Button(control_frame,
                             text="رفع ملف جديد",
                             font=("Arial", 10, "bold"),
                             fg="white",
                             bg="#4CAF50",
                             command=lambda: self.create_file_upload_dialog())
        upload_btn.pack(side=tk.RIGHT, padx=10)
        
        # جدول الملفات
        files_frame = tk.Frame(manager_window, bg="#3C1361")
        files_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # إنشاء Treeview للملفات
        columns = ("الرقم", "اسم الملف", "الفئة", "الحجم", "تاريخ الرفع", "الوصف")
        files_tree = ttk.Treeview(files_frame, columns=columns, show="headings", height=15)
        
        # تنسيق الأعمدة
        files_tree.heading("الرقم", text="الرقم")
        files_tree.heading("اسم الملف", text="اسم الملف")
        files_tree.heading("الفئة", text="الفئة")
        files_tree.heading("الحجم", text="الحجم")
        files_tree.heading("تاريخ الرفع", text="تاريخ الرفع")
        files_tree.heading("الوصف", text="الوصف")
        
        files_tree.column("الرقم", width=50)
        files_tree.column("اسم الملف", width=200)
        files_tree.column("الفئة", width=100)
        files_tree.column("الحجم", width=80)
        files_tree.column("تاريخ الرفع", width=120)
        files_tree.column("الوصف", width=200)
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(files_frame, orient="vertical", command=files_tree.yview)
        files_tree.configure(yscrollcommand=scrollbar.set)
        
        files_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # أزرار الإجراءات
        actions_frame = tk.Frame(manager_window, bg="#2D0A4D")
        actions_frame.pack(fill=tk.X, padx=20, pady=10)
        
        download_btn = tk.Button(actions_frame,
                               text="تحميل الملف",
                               font=("Arial", 10, "bold"),
                               fg="white",
                               bg="#5A2A9C",
                               command=lambda: self.download_selected_file(files_tree))
        download_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(actions_frame,
                             text="حذف الملف",
                             font=("Arial", 10, "bold"),
                             fg="white",
                             bg="#8B0000",
                             command=lambda: self.delete_selected_file(files_tree))
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(actions_frame,
                              text="تحديث القائمة",
                              font=("Arial", 10, "bold"),
                              fg="white",
                              bg="#5A2A9C",
                              command=lambda: self.refresh_files_list(files_tree, category_var.get()))
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # ربط تغيير الفئة بتحديث القائمة
        category_filter.bind('<<ComboboxSelected>>', 
                           lambda e: self.refresh_files_list(files_tree, category_var.get()))
        
        # تحميل الملفات الأولي
        self.refresh_files_list(files_tree, "الكل")
        
        return manager_window
    
    def refresh_files_list(self, tree, category):
        """تحديث قائمة الملفات"""
        # مسح الجدول
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            # جلب الملفات من قاعدة البيانات
            if category == "الكل":
                conn = sqlite3.connect(self.db_manager.db_path)
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, original_name, category, file_size, upload_date, description
                    FROM uploaded_files
                    ORDER BY upload_date DESC
                ''')
                files = cursor.fetchall()
                conn.close()
            else:
                files_data = self.db_manager.get_files_by_category(category)
                if files_data:
                    files = [(f['id'], f['original_name'], f.get('category', category), f['file_size'], 
                             f['upload_date'], f.get('description', '')) for f in files_data]
                else:
                    files = []
            
            # إضافة الملفات للجدول
            for file_info in files:
                tree.insert("", tk.END, values=(
                    file_info[0],  # ID
                    file_info[1],  # اسم الملف
                    file_info[2],  # الفئة
                    self.format_file_size(file_info[3]),  # الحجم
                    file_info[4][:19] if file_info[4] else "",  # التاريخ
                    file_info[5] if file_info[5] else ""  # الوصف
                ))
                
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحميل قائمة الملفات:\n{str(e)}")
    
    def download_selected_file(self, tree):
        """تحميل الملف المحدد"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "الرجاء تحديد ملف أولاً")
            return
        
        try:
            # الحصول على معرف الملف من العنصر المحدد
            file_id = tree.item(selected[0])['values'][0]
            print(f"DEBUG: Selected file ID: {file_id}")  # Debug info
            
            # جلب معلومات الملف من قاعدة البيانات
            file_info = self.db_manager.get_file_info(file_id)
            
            if not file_info:
                messagebox.showerror("خطأ", "معلومات الملف غير موجودة")
                return
            
            print(f"DEBUG: File info: {file_info}")  # Debug info
            
            # التحقق من وجود الملف
            source_file_path = file_info['file_path']
            if not os.path.exists(source_file_path):
                error_msg = f"الملف المصدر غير موجود:\n{source_file_path}"
                print(f"DEBUG: {error_msg}")  # Debug info
                messagebox.showerror("خطأ", error_msg)
                return
            
            print(f"DEBUG: Source file exists: {source_file_path}")  # Debug info
            
            # اختيار مكان الحفظ
            file_extension = file_info.get('file_type', '')
            save_path = filedialog.asksaveasfilename(
                title="حفظ الملف",
                initialfile=file_info['original_name'],
                defaultextension=file_extension if file_extension.startswith('.') else f".{file_extension}",
                filetypes=[
                    ("جميع الملفات", "*.*"),
                    ("ملفات PDF", "*.pdf"),
                    ("ملفات Word", "*.docx;*.doc"),
                    ("ملفات Excel", "*.xlsx;*.xls"),
                    ("ملفات النصوص", "*.txt"),
                    ("ملفات الصور", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")
                ]
            )
            
            if save_path:
                print(f"DEBUG: Saving to: {save_path}")  # Debug info
                try:
                    import shutil
                    # نسخ الملف مع الحفاظ على البيانات الوصفية
                    shutil.copy2(source_file_path, save_path)
                    print(f"DEBUG: File copied successfully")  # Debug info
                    messagebox.showinfo("نجح التحميل", f"تم حفظ الملف بنجاح في:\n{save_path}")
                except PermissionError:
                    messagebox.showerror("خطأ", "ليس لديك صلاحية للكتابة في المجلد المحدد")
                except FileNotFoundError as e:
                    messagebox.showerror("خطأ", f"لم يتم العثور على الملف:\n{str(e)}")
                except Exception as e:
                    messagebox.showerror("خطأ", f"فشل في تحميل الملف:\n{str(e)}\n\nمسار الملف المصدر: {source_file_path}")
            else:
                print("DEBUG: User cancelled save dialog")  # Debug info
                
        except Exception as e:
            print(f"DEBUG: Exception in download_selected_file: {e}")  # Debug info
            messagebox.showerror("خطأ", f"حدث خطأ غير متوقع:\n{str(e)}")
    
    def delete_selected_file(self, tree):
        """حذف الملف المحدد"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "الرجاء تحديد ملف أولاً")
            return
        
        if not messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من رغبتك في حذف هذا الملف؟"):
            return
        
        file_id = tree.item(selected[0])['values'][0]
        
        if self.db_manager.delete_file(file_id):
            tree.delete(selected[0])
            messagebox.showinfo("تم الحذف", "تم حذف الملف بنجاح")
        else:
            messagebox.showerror("خطأ", "فشل في حذف الملف")
    
    def format_file_size(self, size_bytes):
        """تنسيق حجم الملف"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
