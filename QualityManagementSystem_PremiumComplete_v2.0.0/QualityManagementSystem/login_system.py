#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Login System for QB Academy
Handles user authentication and session management
"""

import tkinter as tk
from tkinter import messagebox
import hashlib

class LoginSystem:
    def __init__(self, database_manager, on_login_success):
        self.db_manager = database_manager
        self.on_login_success = on_login_success
        self.current_user = None
        self.login_window = None
    
    def show_login_window(self):
        """عرض نافذة تسجيل الدخول"""
        self.login_window = tk.Tk()
        self.login_window.title("تسجيل الدخول - QB Academy")
        self.login_window.geometry("500x450")
        self.login_window.configure(bg="#2D0A4D")
        self.login_window.resizable(False, False)
        
        # توسيط النافذة
        self.center_window(self.login_window, 500, 450)
        
        # إطار الرئيسي
        main_frame = tk.Frame(self.login_window, bg="#3C1361", padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # شعار وعنوان
        title_label = tk.Label(main_frame,
                             text="QB Academy",
                             font=("Arial", 24, "bold"),
                             fg="#FFD700",
                             bg="#3C1361")
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(main_frame,
                                text="نظام إدارة الجودة",
                                font=("Arial", 14),
                                fg="white",
                                bg="#3C1361")
        subtitle_label.pack(pady=(0, 20))
        
        # متغيرات النموذج
        username_var = tk.StringVar()
        password_var = tk.StringVar()
        
        # حقل اسم المستخدم
        username_frame = tk.Frame(main_frame, bg="#3C1361")
        username_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(username_frame,
                text="اسم المستخدم:",
                font=("Arial", 12, "bold"),
                fg="#FFD700",
                bg="#3C1361").pack(anchor=tk.W, pady=(0, 5))
        
        self.username_entry = tk.Entry(username_frame,
                                textvariable=username_var,
                                font=("Arial", 12),
                                width=30)
        self.username_entry.pack(fill=tk.X, pady=(0, 10))
        self.username_entry.focus()
        
        # حقل كلمة المرور
        password_frame = tk.Frame(main_frame, bg="#3C1361")
        password_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(password_frame,
                text="كلمة المرور:",
                font=("Arial", 12, "bold"),
                fg="#FFD700",
                bg="#3C1361").pack(anchor=tk.W, pady=(0, 5))
        
        self.password_entry = tk.Entry(password_frame,
                                textvariable=password_var,
                                font=("Arial", 12),
                                width=30,
                                show="*")
        self.password_entry.pack(fill=tk.X, pady=(0, 10))
        
        # زر تسجيل الدخول
        login_btn = tk.Button(main_frame,
                            text="تسجيل الدخول",
                            font=("Arial", 14, "bold"),
                            fg="white",
                            bg="#4CAF50",
                            width=20,
                            height=2,
                            command=lambda: self.attempt_login(self.username_entry.get(), self.password_entry.get()))
        login_btn.pack(pady=20)
        login_btn.pack(pady=20)
        
        # معلومات الحساب الافتراضي
        info_frame = tk.Frame(main_frame, bg="#3C1361")
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        info_label = tk.Label(info_frame,
                             text="الحساب الافتراضي:",
                             font=("Arial", 10, "bold"),
                             fg="#FFD700",
                             bg="#3C1361")
        info_label.pack(pady=(0, 5))
        
        info_details = tk.Label(info_frame,
                              text="اسم المستخدم: admin\nكلمة المرور: admin123",
                              font=("Arial", 9),
                              fg="#AAAAAA",
                              bg="#3C1361",
                              justify=tk.CENTER)
        info_details.pack()
        
        # ربط Enter بتسجيل الدخول
        self.password_entry.bind('<Return>', lambda e: self.attempt_login(self.username_entry.get(), self.password_entry.get()))
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        
        self.login_window.protocol("WM_DELETE_WINDOW", self.on_login_window_close)
        self.login_window.mainloop()
    
    def center_window(self, window, width, height):
        """توسيط النافذة على الشاشة"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def attempt_login(self, username, password):
        """محاولة تسجيل الدخول"""
        # تنظيف النصوص من المسافات الزائدة
        username = username.strip() if username else ""
        password = password.strip() if password else ""
        
        print(f"Username input: '{username}' (length: {len(username)})")
        print(f"Password input: '{password}' (length: {len(password)})")
        
        if len(username) == 0 or len(password) == 0:
            messagebox.showwarning("تحذير", f"الرجاء إدخال اسم المستخدم وكلمة المرور\nUsername: '{username}'\nPassword: {'*' * len(password)}")
            return
        
        try:
            # إضافة رسالة تشخيص للتحقق من البيانات
            print(f"محاولة تسجيل الدخول باستخدام: '{username}' / '{password[:3]}...'")
            
            user = self.db_manager.authenticate_user(username, password)
            
            if user:
                self.current_user = user
                
                # تسجيل النشاط
                self.db_manager.log_activity(
                    user_id=user['id'],
                    action="تسجيل دخول",
                    table_name="users",
                    record_id=user['id']
                )
                
                messagebox.showinfo("نجح تسجيل الدخول", f"مرحباً {user['full_name']}")
                
                # إغلاق نافذة تسجيل الدخول
                self.login_window.destroy()
                
                # استدعاء وظيفة النجاح
                self.on_login_success(user)
                
            else:
                messagebox.showerror("خطأ في تسجيل الدخول", f"اسم المستخدم أو كلمة المرور غير صحيحة\nUsername: '{username}'\nPassword length: {len(password)}")
                
        except Exception as e:
            print(f"خطأ في تسجيل الدخول: {str(e)}")
            messagebox.showerror("خطأ", f"حدث خطأ أثناء تسجيل الدخول:\n{str(e)}")
    
    def on_login_window_close(self):
        """عند إغلاق نافذة تسجيل الدخول"""
        if messagebox.askquestion("تأكيد الخروج", "هل تريد إغلاق التطبيق؟") == 'yes':
            self.login_window.destroy()
            import sys
            sys.exit()
    
    def logout(self):
        """تسجيل الخروج"""
        if self.current_user:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.current_user['id'],
                action="تسجيل خروج",
                table_name="users",
                record_id=self.current_user['id']
            )
            
            self.current_user = None
        
        # إعادة عرض نافذة تسجيل الدخول
        self.show_login_window()
    
    def create_user_management_window(self, parent):
        """نافذة إدارة المستخدمين (للمديرين فقط)"""
        if not self.current_user or self.current_user['role'] != 'admin':
            messagebox.showerror("غير مسموح", "هذه الصفحة متاحة للمديرين فقط")
            return
        
        user_window = tk.Toplevel(parent)
        user_window.title("إدارة المستخدمين")
        user_window.geometry("700x500")
        user_window.configure(bg="#2D0A4D")
        
        # عنوان النافذة
        title_label = tk.Label(user_window,
                             text="إدارة المستخدمين",
                             font=("Arial", 18, "bold"),
                             fg="#FFD700",
                             bg="#2D0A4D")
        title_label.pack(pady=10)
        
        # إطار الأزرار
        btn_frame = tk.Frame(user_window, bg="#2D0A4D")
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        add_user_btn = tk.Button(btn_frame,
                               text="إضافة مستخدم جديد",
                               font=("Arial", 10, "bold"),
                               fg="white",
                               bg="#4CAF50",
                               command=lambda: self.create_new_user_dialog(user_window))
        add_user_btn.pack(side=tk.LEFT, padx=5)
        
        # جدول المستخدمين
        users_frame = tk.Frame(user_window, bg="#3C1361")
        users_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        from tkinter import ttk
        columns = ("الرقم", "اسم المستخدم", "الاسم الكامل", "البريد الإلكتروني", "الدور", "النشاط", "آخر دخول")
        users_tree = ttk.Treeview(users_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            users_tree.heading(col, text=col)
            users_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(users_frame, orient="vertical", command=users_tree.yview)
        users_tree.configure(yscrollcommand=scrollbar.set)
        
        users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # تحميل المستخدمين
        self.load_users_list(users_tree)
        
        return user_window
    
    def load_users_list(self, tree):
        """تحميل قائمة المستخدمين"""
        # مسح الجدول
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            import sqlite3
            with sqlite3.connect(self.db_manager.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, username, full_name, email, role, is_active, last_login
                    FROM users
                    ORDER BY created_at DESC
                ''')
                
                for user in cursor.fetchall():
                    status = "نشط" if user[5] else "غير نشط"
                    last_login = user[6][:19] if user[6] else "لم يسجل دخول"
                    
                    tree.insert("", tk.END, values=(
                        user[0], user[1], user[2], user[3] or "", user[4], status, last_login
                    ))
                    
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحميل قائمة المستخدمين:\n{str(e)}")
    
    def create_new_user_dialog(self, parent):
        """نافذة إضافة مستخدم جديد"""
        new_user_window = tk.Toplevel(parent)
        new_user_window.title("إضافة مستخدم جديد")
        new_user_window.geometry("500x600")
        new_user_window.configure(bg="#2D0A4D")
        new_user_window.resizable(True, True)
        new_user_window.grab_set()  # Make it modal
        new_user_window.transient(parent)  # Keep it on top of parent
        
        # توسيط النافذة
        self.center_window(new_user_window, 500, 600)
        
        # إطار رئيسي مع شريط تمرير
        main_frame = tk.Frame(new_user_window, bg="#2D0A4D")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(main_frame, bg="#2D0A4D", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#2D0A4D")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        # Title
        title_label = tk.Label(scrollable_frame,
                             text="إضافة مستخدم جديد",
                             font=("Arial", 18, "bold"),
                             fg="#FFD700",
                             bg="#2D0A4D")
        title_label.pack(pady=(20, 30))
        
        # إطار المحتوى
        content_frame = tk.Frame(scrollable_frame, bg="#3C1361", padx=30, pady=30)
        content_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # متغيرات النموذج
        username_var = tk.StringVar()
        password_var = tk.StringVar()
        full_name_var = tk.StringVar()
        email_var = tk.StringVar()
        role_var = tk.StringVar(value="user")
        
        # الحقول
        fields = [
            ("اسم المستخدم:", username_var),
            ("كلمة المرور:", password_var),
            ("الاسم الكامل:", full_name_var),
            ("البريد الإلكتروني:", email_var)
        ]
        
        entries = {}
        for i, (label, var) in enumerate(fields):
            field_frame = tk.Frame(content_frame, bg="#3C1361")
            field_frame.pack(fill=tk.X, pady=10)
            
            tk.Label(field_frame, text=label, font=("Arial", 12, "bold"),
                    fg="#FFD700", bg="#3C1361").pack(anchor=tk.E, pady=(0, 5))
            
            entry = tk.Entry(field_frame, textvariable=var, font=("Arial", 12), width=30)
            if "كلمة المرور" in label:
                entry.config(show="*")
            entry.pack(fill=tk.X, pady=(0, 5), ipady=5)
            entries[label] = entry
        
        # دور المستخدم
        role_frame = tk.Frame(content_frame, bg="#3C1361")
        role_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(role_frame, text="الدور:", font=("Arial", 12, "bold"),
                fg="#FFD700", bg="#3C1361").pack(anchor=tk.E, pady=(0, 5))
        
        from tkinter import ttk
        role_combo = ttk.Combobox(role_frame, textvariable=role_var,
                                values=['user', 'admin', 'manager', 'auditor'],
                                state='readonly', font=("Arial", 12), width=27)
        role_combo.pack(fill=tk.X, pady=(0, 5), ipady=5)
        
        # إضافة وصف للأدوار
        role_desc_frame = tk.Frame(content_frame, bg="#3C1361")
        role_desc_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(role_desc_frame, text="وصف الأدوار:", font=("Arial", 10, "bold"),
                fg="#ADD8E6", bg="#3C1361").pack(anchor=tk.E, pady=(0, 5))
        
        roles_description = """
• user: مستخدم عادي - الوصول الأساسي للنظام
• admin: مدير النظام - جميع الصلاحيات
• manager: مدير القسم - صلاحيات إدارية محدودة  
• auditor: مراجع - صلاحيات القراءة والمراجعة
        """
        
        tk.Label(role_desc_frame, text=roles_description, font=("Arial", 9),
                fg="#D3D3D3", bg="#3C1361", justify=tk.RIGHT, anchor="e").pack(fill=tk.X)
        
        # أزرار التحكم
        btn_frame = tk.Frame(scrollable_frame, bg="#2D0A4D")
        btn_frame.pack(fill=tk.X, padx=40, pady=30)
        
        create_btn = tk.Button(btn_frame,
                             text="✅ إنشاء المستخدم",
                             font=("Arial", 12, "bold"),
                             fg="white",
                             bg="#4CAF50",
                             padx=20, pady=10,
                             command=lambda: self.create_new_user(
                                 username_var.get(),
                                 password_var.get(),
                                 full_name_var.get(),
                                 email_var.get(),
                                 role_var.get(),
                                 new_user_window
                             ))
        create_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(btn_frame,
                             text="❌ إلغاء",
                             font=("Arial", 12, "bold"),
                             fg="white",
                             bg="#8B0000",
                             padx=20, pady=10,
                             command=new_user_window.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=10)
        
        # Focus on first field
        entries["اسم المستخدم:"].focus_set()
        
        # Ensure proper sizing
        new_user_window.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def create_new_user(self, username, password, full_name, email, role, window):
        """إنشاء مستخدم جديد"""
        # التحقق من البيانات
        if not all([username, password, full_name]):
            messagebox.showwarning("تحذير", "الرجاء ملء جميع الحقول المطلوبة")
            return
        
        if len(password) < 6:
            messagebox.showwarning("تحذير", "كلمة المرور يجب أن تكون 6 أحرف على الأقل")
            return
        
        try:
            # تشفير كلمة المرور
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # إدراج المستخدم في قاعدة البيانات
            import sqlite3
            with sqlite3.connect(self.db_manager.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, password_hash, full_name, email, role)
                    VALUES (?, ?, ?, ?, ?)
                ''', (username, password_hash, full_name, email, role))
                
                user_id = cursor.lastrowid
                conn.commit()
                
                # تسجيل النشاط
                self.db_manager.log_activity(
                    user_id=self.current_user['id'],
                    action=f"إنشاء مستخدم جديد: {username}",
                    table_name="users",
                    record_id=user_id
                )
                
                messagebox.showinfo("تم الإنشاء", f"تم إنشاء المستخدم {username} بنجاح")
                window.destroy()
                
        except sqlite3.IntegrityError:
            messagebox.showerror("خطأ", "اسم المستخدم موجود مسبقاً")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في إنشاء المستخدم:\n{str(e)}")
