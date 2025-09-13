#!/bin/bash
echo "QB Academy Quality Management System v2.0 Setup"
echo "Premium Arabic Enhancement Edition"
echo "=========================================="
echo ""

echo "Installing required Python packages..."
pip install arabic-reshaper python-bidi Pillow reportlab

echo ""
echo "Setup complete!"
echo ""
echo "To run the application:"
echo "python qb.py"
echo ""
echo "For premium Arabic demo:"
echo "python premium_arabic_demo.py"
echo ""
