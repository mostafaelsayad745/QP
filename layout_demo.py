#!/usr/bin/env python3
"""
Layout Demo - Shows the improvements made to QFs form layout
This script demonstrates the key layout improvements without running the full application
"""

import tkinter as tk
from tkinter import ttk

def create_demo_form():
    """Create a demo form showing the layout improvements"""
    
    # Create main window with improved sizing
    root = tk.Tk()
    root.title("QFs Form Layout Improvements Demo")
    
    # Get screen dimensions for responsive sizing (90% instead of 80%)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Improved minimum limits and sizing
    min_width, min_height = 1200, 800  # Increased from 1000x700
    width = max(min_width, int(screen_width * 0.9))  # Increased from 0.8
    height = max(min_height, int(screen_height * 0.9))
    
    # Center the window on screen (NEW)
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.configure(bg="#f0f0f0")
    root.resizable(True, True)
    root.minsize(min_width, min_height)
    
    # Demo colors (similar to premium theme)
    colors = {
        'primary': '#1a237e',
        'accent': '#3f51b5',
        'surface': '#ffffff',
        'background': '#f5f5f5',
        'text_light': '#333333'
    }
    
    # Create scrollable frame with improved layout
    canvas = tk.Canvas(root, bg=colors['background'], highlightthickness=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=colors['background'])
    
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Improved packing with better space utilization
    canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
    scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))
    
    # Enhanced width configuration
    def _configure_scroll_width(event):
        canvas_width = event.width - 20
        canvas.itemconfig(canvas.find_all()[0], width=canvas_width)
        scrollable_frame.config(width=canvas_width)
    
    canvas.bind('<Configure>', _configure_scroll_width)
    
    # Title with improved styling and spacing
    title_label = tk.Label(scrollable_frame, 
                         text="QF-10-01-01: سجل مكونات النظام الإداري - Layout Demo", 
                         font=("Arial", 16, "bold"),
                         fg="white",
                         bg=colors['accent'],
                         padx=25, pady=20)  # Increased from 20, 15
    title_label.pack(fill=tk.X, pady=(0, 25), padx=20)  # Increased spacing
    
    # Section 1: Improved form fields
    section1_frame = tk.LabelFrame(scrollable_frame, 
                                 text="معلومات عامة - Improved Layout",
                                 font=("Arial", 12, "bold"),
                                 fg=colors['accent'],
                                 bg=colors['surface'],
                                 padx=25, pady=20)  # Increased from 20, 15
    section1_frame.pack(fill=tk.X, padx=25, pady=(0, 20))  # Increased spacing
    
    # Demo form fields with improved layout
    fields = [
        "Organization Name / اسم الجهة",
        "Responsible Department / القسم المسؤول", 
        "Record Manager / مسؤول السجل",
        "Last Update Date / تاريخ آخر تحديث"
    ]
    
    for i, field in enumerate(fields):
        # Improved field frame with better spacing
        field_frame = tk.Frame(section1_frame, bg=colors['surface'])
        field_frame.pack(fill=tk.X, padx=15, pady=8)  # Increased from 10, 5
        
        # Fixed width label for better alignment
        label = tk.Label(field_frame, 
                        text=field,
                        font=("Arial", 10),
                        fg=colors['text_light'],
                        bg=colors['surface'],
                        anchor="e",
                        width=25)  # Fixed width for consistency
        label.pack(side=tk.RIGHT, padx=(0, 15))
        
        # Improved entry field
        entry = tk.Entry(field_frame, 
                        font=("Arial", 10),
                        bg=colors['background'],
                        fg=colors['text_light'],
                        relief=tk.FLAT,
                        bd=1)
        entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 15), ipady=5)
        entry.insert(0, f"Sample data for {field.split('/')[0].strip()}")
    
    # Section 2: Improved table layout
    section2_frame = tk.LabelFrame(scrollable_frame, 
                                 text="Components Table - Enhanced Layout",
                                 font=("Arial", 12, "bold"),
                                 fg=colors['accent'],
                                 bg=colors['surface'],
                                 padx=25, pady=20)
    section2_frame.pack(fill=tk.X, padx=25, pady=(0, 20))
    
    # Demo table with improved layout
    table_frame = tk.Frame(section2_frame, bg=colors['surface'])
    table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    headers = ["#", "Type", "Name", "Code", "Status"]
    
    # Enhanced grid configuration
    for col, header in enumerate(headers):
        header_label = tk.Label(table_frame,
                              text=header,
                              font=("Arial", 10, "bold"),
                              fg="white",
                              bg=colors['accent'],
                              relief=tk.RAISED,
                              bd=1,
                              padx=8, pady=8)
        header_label.grid(row=0, column=col, sticky="ew", padx=1, pady=1)
    
    # Responsive column weights
    table_frame.grid_columnconfigure(0, weight=0, minsize=40)
    table_frame.grid_columnconfigure(1, weight=1, minsize=120)
    table_frame.grid_columnconfigure(2, weight=2, minsize=200)
    table_frame.grid_columnconfigure(3, weight=1, minsize=120)
    table_frame.grid_columnconfigure(4, weight=1, minsize=150)
    
    # Sample data rows
    sample_data = [
        ["1", "Policy", "Quality Policy", "POL-01", "Active"],
        ["2", "Procedure", "Assessment Procedure", "PR-05-02", "Updated"],
        ["3", "Form", "Certification Form", "QF-08-01-01", "Active"]
    ]
    
    for row_idx, row_data in enumerate(sample_data, start=1):
        for col_idx, cell_data in enumerate(row_data):
            if col_idx == 0:
                cell = tk.Label(table_frame,
                              text=cell_data,
                              font=("Arial", 9),
                              fg=colors['text_light'],
                              bg=colors['background'],
                              relief=tk.RAISED,
                              bd=1,
                              padx=5, pady=2)
            else:
                cell = tk.Entry(table_frame,
                              font=("Arial", 9),
                              bg=colors['background'],
                              fg=colors['text_light'],
                              relief=tk.FLAT,
                              bd=1,
                              justify='right')
                cell.insert(0, cell_data)
            
            cell.grid(row=row_idx, column=col_idx, sticky="ew", padx=2, pady=2, ipadx=5, ipady=3)
    
    # Section 3: Improved notes area
    section3_frame = tk.LabelFrame(scrollable_frame, 
                                 text="Notes Area - Better Space Utilization",
                                 font=("Arial", 12, "bold"),
                                 fg=colors['accent'],
                                 bg=colors['surface'],
                                 padx=25, pady=20)
    section3_frame.pack(fill=tk.X, padx=25, pady=(0, 20))
    
    notes_text = tk.Text(section3_frame, 
                        font=("Arial", 10),
                        height=8,  # Increased from 6
                        bg=colors['background'],
                        fg=colors['text_light'],
                        wrap=tk.WORD,
                        relief=tk.FLAT,
                        bd=1)
    notes_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    notes_text.insert(1.0, "This text area now uses improved layout:\n\n"
                           "✓ Better height utilization (8 lines vs 6)\n"
                           "✓ Responsive width expansion\n"
                           "✓ Enhanced padding and spacing\n"
                           "✓ Word wrapping enabled\n"
                           "✓ Flat modern appearance")
    
    # Improved button layout
    btn_frame = tk.Frame(scrollable_frame, bg=colors['background'])
    btn_frame.pack(fill=tk.X, padx=25, pady=25)
    
    buttons = [
        ("Save Form", "#4CAF50"),
        ("Export PDF", "#9C27B0"),
        ("Delete", "#F44336"),
        ("Edit", "#424242"),
        ("Add New", "#673AB7"),
        ("Clear", "#FF9800")
    ]
    
    # Grid layout for responsive buttons
    for i in range(len(buttons)):
        btn_frame.grid_columnconfigure(i, weight=1, pad=10)
    
    for i, (text, color) in enumerate(buttons):
        btn = tk.Button(btn_frame, 
                       text=text,
                       font=("Arial", 10),
                       fg="white",
                       bg=color,
                       height=2,
                       relief=tk.FLAT,
                       bd=0)
        btn.grid(row=0, column=i, sticky="ew", padx=5, pady=5, ipadx=10)
    
    # Add improvement summary
    summary_frame = tk.LabelFrame(scrollable_frame, 
                                text="Layout Improvements Summary",
                                font=("Arial", 12, "bold"),
                                fg=colors['accent'],
                                bg=colors['surface'],
                                padx=25, pady=20)
    summary_frame.pack(fill=tk.X, padx=25, pady=(0, 25))
    
    improvements = [
        "✓ Window size increased from 80% to 90% of screen",
        "✓ Minimum dimensions increased to 1200x800 (from 1000x700)",
        "✓ Added window centering for better UX",
        "✓ Enhanced padding and spacing throughout",
        "✓ Fixed label widths for better alignment",
        "✓ Responsive table columns with minimum widths",
        "✓ Improved text areas with better expansion",
        "✓ Grid-based button layout for responsiveness",
        "✓ Better scroll area width utilization"
    ]
    
    for improvement in improvements:
        label = tk.Label(summary_frame,
                        text=improvement,
                        font=("Arial", 10),
                        fg=colors['text_light'],
                        bg=colors['surface'],
                        anchor="w")
        label.pack(fill=tk.X, padx=10, pady=2)
    
    # Mouse wheel support
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _bind_to_mousewheel(event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def _unbind_from_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")
    
    canvas.bind('<Enter>', _bind_to_mousewheel)
    canvas.bind('<Leave>', _unbind_from_mousewheel)
    
    return root

if __name__ == "__main__":
    print("QFs Form Layout Improvements Demo")
    print("=================================")
    print("This demo shows the key improvements made to the form layout:")
    print("- Better window sizing and centering")
    print("- Enhanced space utilization")
    print("- Improved padding and spacing")
    print("- Responsive table and button layouts")
    print("- Better content expansion")
    print("\nStarting demo window...")
    
    try:
        root = create_demo_form()
        root.mainloop()
    except Exception as e:
        print(f"Note: GUI demo requires display. Layout improvements summary:")
        print("- Window size: 90% of screen (up from 80%) with 1200x800 minimum")
        print("- Centered window positioning")
        print("- Enhanced padding: 25px (up from 20px) in sections")
        print("- Better field spacing: 15px (up from 10px)")
        print("- Responsive table columns with proper minimum widths")
        print("- Text areas: 8 lines (up from 6) with better expansion")
        print("- Grid-based button layout for responsiveness")
        print("- Improved scroll area width calculation")