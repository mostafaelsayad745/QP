#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced Arabic Text Rendering Module for QB Academy Quality Management System
This module provides premium Arabic text rendering with proper RTL support
"""

import arabic_reshaper
from bidi.algorithm import get_display

class ArabicTextRenderer:
    """Premium Arabic text rendering class for enhanced display"""
    
    @staticmethod
    def reshape_arabic_text(text):
        """
        Reshape Arabic text for proper display with RTL support
        
        Args:
            text (str): Raw Arabic text
            
        Returns:
            str: Properly formatted Arabic text for display
        """
        try:
            if not text:
                return text
                
            # Reshape Arabic characters for proper connection
            reshaped_text = arabic_reshaper.reshape(text)
            
            # Apply bidirectional algorithm for RTL display
            bidi_text = get_display(reshaped_text)
            
            return bidi_text
        except Exception as e:
            print(f"Error reshaping Arabic text: {e}")
            return text
    
    @staticmethod
    def get_premium_arabic_font():
        """
        Get the best available Arabic font for premium display
        
        Returns:
            str: Font name
        """
        # Premium Arabic fonts in order of preference
        premium_fonts = [
            "Traditional Arabic",      # Windows Arabic font
            "Arabic Typesetting",     # Professional Arabic font
            "Microsoft Sans Serif",   # Good Arabic support
            "Tahoma",                 # Excellent Arabic rendering
            "Arial Unicode MS",       # Unicode support
            "Segoe UI",              # Modern Windows font
            "Calibri"                # Fallback with Arabic support
        ]
        
        # Return the first available font (in real app, you'd test availability)
        return premium_fonts[3]  # Tahoma - excellent for Arabic
    
    @staticmethod
    def get_premium_colors():
        """
        Get premium color scheme for Arabic applications
        
        Returns:
            dict: Color scheme dictionary
        """
        return {
            'primary': '#1a237e',         # Deep indigo
            'secondary': '#283593',       # Rich blue  
            'accent': '#e91e63',          # Elegant pink/red
            'success': '#2e7d32',         # Professional green
            'warning': '#f57c00',         # Orange
            'error': '#c62828',           # Red
            'text_light': '#ffffff',      # White text
            'text_dark': '#212121',       # Dark text
            'text_secondary': '#757575',  # Secondary text
            'background': '#0d1421',      # Very dark blue
            'surface': '#1a237e',         # Card/surface color
            'hover': '#e91e63',           # Hover state
            'border': '#424242',          # Border color
            'gradient_start': '#1a237e',  # Gradient start
            'gradient_end': '#283593'     # Gradient end
        }

def apply_premium_arabic_styling(widget, text, font_size=14, font_weight='normal', color_scheme=None):
    """
    Apply premium Arabic styling to a widget
    
    Args:
        widget: Tkinter widget to style
        text (str): Arabic text to display
        font_size (int): Font size
        font_weight (str): Font weight ('normal', 'bold')
        color_scheme (dict): Color scheme to use
    """
    if color_scheme is None:
        color_scheme = ArabicTextRenderer.get_premium_colors()
    
    # Reshape Arabic text
    renderer = ArabicTextRenderer()
    formatted_text = renderer.reshape_arabic_text(text)
    
    # Get premium font
    font_name = renderer.get_premium_arabic_font()
    
    # Configure widget
    try:
        widget.configure(
            text=formatted_text,
            font=(font_name, font_size, font_weight),
            fg=color_scheme['text_light'],
            bg=color_scheme['surface']
        )
    except Exception as e:
        print(f"Error applying Arabic styling: {e}")

# Example usage function for integration
def enhance_existing_app_with_arabic():
    """
    Example function showing how to enhance existing app with Arabic rendering
    This can be integrated into the main qb.py application
    """
    print("Arabic Enhancement Module Loaded Successfully!")
    print("Use ArabicTextRenderer.reshape_arabic_text() for premium Arabic display")
    print("Use apply_premium_arabic_styling() for automatic widget enhancement")

if __name__ == "__main__":
    # Test the Arabic rendering
    test_texts = [
        "QB Academy - أكاديمية كيو بي",
        "نظام إدارة الجودة المتطور",
        "QP-10-01: النظام الإداري",
        "QF-10-01-01: سجل مكونات النظام الإداري",
        "QF-10-01-02: تقرير مراجعة النظام الإداري",
        "QF-10-01-03: سجل التحسين المستمر"
    ]
    
    renderer = ArabicTextRenderer()
    
    print("Premium Arabic Text Rendering Test:")
    print("=" * 50)
    
    for text in test_texts:
        original = text
        enhanced = renderer.reshape_arabic_text(text)
        print(f"Original: {original}")
        print(f"Enhanced: {enhanced}")
        print("-" * 30)
