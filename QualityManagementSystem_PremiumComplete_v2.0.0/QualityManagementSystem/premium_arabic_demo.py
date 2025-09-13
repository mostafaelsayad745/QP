#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import arabic_reshaper
from bidi.algorithm import get_display
import os

class ArabicTextRenderer:
    """Premium Arabic text rendering class"""
    
    @staticmethod
    def reshape_arabic_text(text):
        """Reshape Arabic text for proper display"""
        try:
            reshaped_text = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped_text)
            return bidi_text
        except Exception as e:
            print(f"Error reshaping Arabic text: {e}")
            return text
    
    @staticmethod
    def get_arabic_font():
        """Get the best available Arabic font"""
        # Try different Arabic fonts in order of preference
        fonts = [
            "Traditional Arabic",
            "Arabic Typesetting", 
            "Microsoft Sans Serif",
            "Tahoma",
            "Arial Unicode MS",
            "Segoe UI"
        ]
        
        for font in fonts:
            try:
                # Test if font is available
                test_font = (font, 12)
                return font
            except:
                continue
        
        return "Arial"  # Fallback

class PremiumArabicApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.text_renderer = ArabicTextRenderer()
        
    def setup_window(self):
        """Setup main window with premium styling"""
        self.root.title("QB Academy - نظام إدارة الجودة المحدث")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a2e')
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        # Modern window styling
        self.root.attributes('-alpha', 0.98)  # Slight transparency for modern look
        
    def setup_styles(self):
        """Setup premium color scheme and fonts"""
        self.colors = {
            'primary': '#16213e',      # Deep navy blue
            'secondary': '#0f3460',    # Rich blue
            'accent': '#e94560',       # Elegant red accent
            'success': '#0f4c75',      # Professional blue
            'text_light': '#ffffff',   # White text
            'text_dark': '#2c3e50',    # Dark text
            'background': '#1a1a2e',   # Dark background
            'card': '#16213e',         # Card background
            'hover': '#e94560',        # Hover color
            'border': '#3c3c3c'        # Border color
        }
        
        # Premium Arabic font
        self.arabic_font = self.text_renderer.get_arabic_font()
        
        self.fonts = {
            'title': (self.arabic_font, 24, 'bold'),
            'subtitle': (self.arabic_font, 18, 'bold'),
            'heading': (self.arabic_font, 16, 'bold'),
            'body': (self.arabic_font, 14),
            'small': (self.arabic_font, 12),
            'button': (self.arabic_font, 14, 'bold')
        }
        
    def create_widgets(self):
        """Create the main interface"""
        # Main container with gradient effect
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header with premium styling
        self.create_header(main_frame)
        
        # Content area
        content_frame = tk.Frame(main_frame, bg=self.colors['background'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Sidebar and main content
        self.create_sidebar(content_frame)
        self.create_main_content(content_frame)
        
    def create_header(self, parent):
        """Create premium header with Arabic text"""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Add subtle border
        border_frame = tk.Frame(header_frame, bg=self.colors['accent'], height=3)
        border_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Title with properly rendered Arabic
        title_text = "QB Academy - أكاديمية كيو بي"
        formatted_title = self.text_renderer.reshape_arabic_text(title_text)
        
        title_label = tk.Label(
            header_frame,
            text=formatted_title,
            font=self.fonts['title'],
            fg=self.colors['text_light'],
            bg=self.colors['primary']
        )
        title_label.pack(expand=True)
        
        # Subtitle
        subtitle_text = "نظام إدارة الجودة المتطور - Premium Quality Management System"
        formatted_subtitle = self.text_renderer.reshape_arabic_text(subtitle_text)
        
        subtitle_label = tk.Label(
            header_frame,
            text=formatted_subtitle,
            font=self.fonts['body'],
            fg=self.colors['text_light'],
            bg=self.colors['primary']
        )
        subtitle_label.pack()
        
    def create_sidebar(self, parent):
        """Create premium sidebar with Arabic menu items"""
        self.sidebar_frame = tk.Frame(parent, bg=self.colors['card'], width=300)
        self.sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20))
        self.sidebar_frame.pack_propagate(False)
        
        # Sidebar header
        sidebar_header = tk.Frame(self.sidebar_frame, bg=self.colors['secondary'], height=60)
        sidebar_header.pack(fill=tk.X, pady=(0, 10))
        
        header_text = "الإجراءات والنماذج"
        formatted_header = self.text_renderer.reshape_arabic_text(header_text)
        
        tk.Label(
            sidebar_header,
            text=formatted_header,
            font=self.fonts['subtitle'],
            fg=self.colors['text_light'],
            bg=self.colors['secondary']
        ).pack(expand=True)
        
        # Scrollable menu area
        self.create_scrollable_menu()
        
    def create_scrollable_menu(self):
        """Create scrollable menu with premium Arabic items"""
        # Canvas for scrolling
        canvas = tk.Canvas(self.sidebar_frame, bg=self.colors['card'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.sidebar_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['card'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Sample menu items with proper Arabic rendering
        menu_items = [
            "QP-04: إدارة الموارد",
            "QP-05: هيكل الإدارة", 
            "QP-06: إدارة المعلومات والسرية",
            "QP-07: متطلبات الأشخاص الطبيعيين",
            "QP-08: عملية الاعتماد",
            "QP-09: قرار الاعتماد",
            "QP-10-01: النظام الإداري",
            "QF-10-01-01: سجل مكونات النظام الإداري",
            "QF-10-01-02: تقرير مراجعة النظام الإداري",
            "QF-10-01-03: سجل التحسين المستمر"
        ]
        
        for i, item in enumerate(menu_items):
            self.create_premium_menu_button(scrollable_frame, item, i)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_premium_menu_button(self, parent, text, index):
        """Create premium styled menu button with Arabic text"""
        formatted_text = self.text_renderer.reshape_arabic_text(text)
        
        # Button frame for hover effects
        button_frame = tk.Frame(parent, bg=self.colors['card'])
        button_frame.pack(fill=tk.X, pady=2, padx=10)
        
        # Main button
        button = tk.Button(
            button_frame,
            text=formatted_text,
            font=self.fonts['body'],
            fg=self.colors['text_light'],
            bg=self.colors['card'],
            activebackground=self.colors['hover'],
            activeforeground=self.colors['text_light'],
            relief=tk.FLAT,
            bd=0,
            anchor='e',  # Right align for Arabic
            padx=20,
            pady=12,
            cursor='hand2',
            command=lambda: self.show_form_content(text)
        )
        button.pack(fill=tk.X)
        
        # Hover effects
        def on_enter(e):
            button.configure(bg=self.colors['hover'])
            
        def on_leave(e):
            button.configure(bg=self.colors['card'])
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        # Add subtle separator
        separator = tk.Frame(button_frame, bg=self.colors['border'], height=1)
        separator.pack(fill=tk.X, pady=(0, 5))
        
    def create_main_content(self, parent):
        """Create main content area"""
        self.content_frame = tk.Frame(parent, bg=self.colors['background'])
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Welcome content
        self.show_welcome_content()
        
    def show_welcome_content(self):
        """Show welcome content with premium Arabic styling"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Welcome card
        welcome_card = tk.Frame(self.content_frame, bg=self.colors['card'], relief=tk.RAISED, bd=2)
        welcome_card.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Welcome message
        welcome_text = "مرحباً بكم في نظام إدارة الجودة المتطور"
        formatted_welcome = self.text_renderer.reshape_arabic_text(welcome_text)
        
        welcome_label = tk.Label(
            welcome_card,
            text=formatted_welcome,
            font=self.fonts['title'],
            fg=self.colors['text_light'],
            bg=self.colors['card']
        )
        welcome_label.pack(pady=(50, 20))
        
        # Description
        description_text = """
نظام شامل لإدارة الجودة في أكاديمية كيو بي
        
يشمل النظام:
• إدارة الإجراءات والسياسات
• نماذج الاعتماد المتخصصة  
• تتبع التحسين المستمر
• إدارة الموارد والمعلومات
• نظام إداري متكامل وفقاً لمعايير ISO 9001

تم تطوير هذا النظام ليوفر تجربة مستخدم متميزة
مع دعم كامل للغة العربية والتخطيط من اليمين إلى اليسار
        """
        
        formatted_description = self.text_renderer.reshape_arabic_text(description_text)
        
        description_label = tk.Label(
            welcome_card,
            text=formatted_description,
            font=self.fonts['body'],
            fg=self.colors['text_light'],
            bg=self.colors['card'],
            justify=tk.RIGHT,
            wraplength=600
        )
        description_label.pack(pady=20, padx=40)
        
        # Action buttons
        self.create_action_buttons(welcome_card)
        
    def create_action_buttons(self, parent):
        """Create premium action buttons"""
        button_frame = tk.Frame(parent, bg=self.colors['card'])
        button_frame.pack(pady=30)
        
        buttons = [
            ("ابدأ الاستخدام", self.colors['accent']),
            ("عرض النماذج", self.colors['success']),
            ("إعدادات النظام", self.colors['secondary'])
        ]
        
        for text, color in buttons:
            formatted_text = self.text_renderer.reshape_arabic_text(text)
            
            btn = tk.Button(
                button_frame,
                text=formatted_text,
                font=self.fonts['button'],
                fg=self.colors['text_light'],
                bg=color,
                activebackground=self.colors['hover'],
                activeforeground=self.colors['text_light'],
                relief=tk.FLAT,
                bd=0,
                padx=30,
                pady=15,
                cursor='hand2',
                command=lambda t=text: self.button_action(t)
            )
            btn.pack(side=tk.RIGHT, padx=10)
            
            # Hover effects
            def on_enter(e, button=btn, orig_color=color):
                button.configure(bg=self.colors['hover'])
                
            def on_leave(e, button=btn, orig_color=color):
                button.configure(bg=orig_color)
                
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
    
    def show_form_content(self, form_name):
        """Show form content with premium Arabic styling"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Form card
        form_card = tk.Frame(self.content_frame, bg=self.colors['card'], relief=tk.RAISED, bd=2)
        form_card.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Form title
        formatted_title = self.text_renderer.reshape_arabic_text(form_name)
        
        title_label = tk.Label(
            form_card,
            text=formatted_title,
            font=self.fonts['subtitle'],
            fg=self.colors['accent'],
            bg=self.colors['card']
        )
        title_label.pack(pady=(30, 20))
        
        # Sample form content for QP-10-01 forms
        if "QF-10-01" in form_name:
            self.create_sample_form(form_card, form_name)
        else:
            # Generic content
            content_text = f"محتوى النموذج: {form_name}\n\nهذا مثال على عرض النماذج بتنسيق متقدم باللغة العربية"
            formatted_content = self.text_renderer.reshape_arabic_text(content_text)
            
            content_label = tk.Label(
                form_card,
                text=formatted_content,
                font=self.fonts['body'],
                fg=self.colors['text_light'],
                bg=self.colors['card'],
                justify=tk.RIGHT
            )
            content_label.pack(pady=20)
    
    def create_sample_form(self, parent, form_name):
        """Create a sample form with premium Arabic styling"""
        # Form content area
        form_content = tk.Frame(parent, bg=self.colors['card'])
        form_content.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Sample fields for different forms
        if "QF-10-01-01" in form_name:
            fields = [
                "التاريخ",
                "اسم مكون النظام",
                "نوع المكون", 
                "وصف المكون",
                "الجهة المسؤولة",
                "حالة التنفيذ"
            ]
        elif "QF-10-01-02" in form_name:
            fields = [
                "تاريخ المراجعة",
                "اسم المراجع",
                "نطاق المراجعة",
                "النتائج",
                "التوصيات"
            ]
        elif "QF-10-01-03" in form_name:
            fields = [
                "رقم التحسين",
                "مجال التحسين",
                "الوضع الحالي",
                "التحسين المقترح",
                "الشخص المسؤول"
            ]
        else:
            fields = ["حقل نموذجي", "حقل آخر", "حقل ثالث"]
        
        # Create fields with premium styling
        for i, field in enumerate(fields):
            self.create_premium_field(form_content, field, i)
        
        # Action buttons
        self.create_form_buttons(form_content)
    
    def create_premium_field(self, parent, label_text, row):
        """Create premium styled form field"""
        field_frame = tk.Frame(parent, bg=self.colors['card'])
        field_frame.pack(fill=tk.X, pady=10)
        
        # Label
        formatted_label = self.text_renderer.reshape_arabic_text(f"{label_text}:")
        
        label = tk.Label(
            field_frame,
            text=formatted_label,
            font=self.fonts['body'],
            fg=self.colors['text_light'],
            bg=self.colors['card'],
            anchor='e'
        )
        label.pack(side=tk.RIGHT, padx=(0, 20))
        
        # Entry field with premium styling
        entry = tk.Entry(
            field_frame,
            font=self.fonts['body'],
            bg=self.colors['background'],
            fg=self.colors['text_light'],
            insertbackground=self.colors['accent'],
            relief=tk.FLAT,
            bd=5,
            justify='right'  # Right-align for Arabic
        )
        entry.pack(side=tk.RIGHT, padx=(20, 0), ipady=8, ipadx=10, fill=tk.X, expand=True)
        
    def create_form_buttons(self, parent):
        """Create form action buttons"""
        button_frame = tk.Frame(parent, bg=self.colors['card'])
        button_frame.pack(pady=30)
        
        buttons = [
            ("حفظ", self.colors['success']),
            ("تحميل", self.colors['secondary']),
            ("مسح", self.colors['accent'])
        ]
        
        for text, color in buttons:
            formatted_text = self.text_renderer.reshape_arabic_text(text)
            
            btn = tk.Button(
                button_frame,
                text=formatted_text,
                font=self.fonts['button'],
                fg=self.colors['text_light'],
                bg=color,
                activebackground=self.colors['hover'],
                relief=tk.FLAT,
                bd=0,
                padx=25,
                pady=12,
                cursor='hand2',
                command=lambda t=text: self.form_action(t)
            )
            btn.pack(side=tk.RIGHT, padx=10)
    
    def button_action(self, action):
        """Handle button actions"""
        formatted_action = self.text_renderer.reshape_arabic_text(action)
        messagebox.showinfo("إجراء", f"تم تنفيذ: {formatted_action}")
    
    def form_action(self, action):
        """Handle form actions"""
        formatted_action = self.text_renderer.reshape_arabic_text(action)
        messagebox.showinfo("نموذج", f"تم {formatted_action} النموذج بنجاح")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = PremiumArabicApp()
    app.run()
