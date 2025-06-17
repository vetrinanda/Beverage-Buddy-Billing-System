import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import ImageTk, Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import os

# Menu Items and Prices
menu = {
    "Tea": 20,
    "Coffee": 30,
    "Black Coffee": 35,
    "Strong Coffee": 40,
    "Hot Milk": 25,
    "Hot Water": 10,
    "Cake": 40,
    "Biscuits": 10
}

# Initialize Order
order = {item: 0 for item in menu}

# --- GUI Setup ---
root = tk.Tk()
root.title("☕ Beverage Buddy Billing System")
root.geometry("550x600")
root.config(bg="#f8f8f8")

title = tk.Label(root, text="🧾 Beverage Buddy", font=("Arial", 20, "bold"), bg="#f8f8f8", fg="#333")
title.pack(pady=10)

# --- Quantity Selector ---
frame = tk.Frame(root, bg="#f8f8f8")
frame.pack()

qty_labels = {}

def update_qty(item, change):
    order[item] += change
    if order[item] < 0:
        order[item] = 0
    qty_labels[item].config(text=str(order[item]))

row = 0
for item in menu:
    tk.Label(frame, text=f"{item} (₹{menu[item]})", font=("Arial", 12), width=20, anchor="w", bg="#f8f8f8").grid(row=row, column=0, padx=10, pady=5)

    tk.Button(frame, text="-", command=lambda i=item: update_qty(i, -1), bg="#e57373", width=2).grid(row=row, column=1)
    qty_labels[item] = tk.Label(frame, text="0", font=("Arial", 12), width=4, bg="#f8f8f8")
    qty_labels[item].grid(row=row, column=2)
    tk.Button(frame, text="+", command=lambda i=item: update_qty(i, 1), bg="#81c784", width=2).grid(row=row, column=3)

    row += 1

# --- Functions ---

def reset_order():
    for item in order:
        order[item] = 0
        qty_labels[item].config(text="0")

def generate_pdf_bill():
    if not any(order.values()):
        messagebox.showwarning("Empty Order", "Please select at least one item.")
        return

    # Prepare bill lines and total
    bill_lines = []
    total = 0
    for item, qty in order.items():
        if qty > 0:
            price = menu[item] * qty
            bill_lines.append(f"{item} x {qty} = ₹{price}")
            total += price

    bill_text = "\n".join(bill_lines) + f"\nTotal: ₹{total}"

    # Save QR Code
    qr = qrcode.make(bill_text)
    qr_path = "temp_qr.png"
    qr.save(qr_path)

    # Create PDF folder if needed
    os.makedirs("bills", exist_ok=True)
    pdf_path = f"bills/bill_styled.pdf"

    # Generate PDF
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Logo
    try:
        c.drawImage("logo.png", 50, height - 100, width=120, preserveAspectRatio=True)
    except:
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 90, "(Logo Missing)")

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width / 2, height - 120, "Beverage Buddy - Bill Receipt")

    # Separator line
    c.setStrokeColor(colors.lightgrey)
    c.setLineWidth(1)
    c.line(50, height - 130, width - 50, height - 130)

    # Bill content
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    y = height - 160
    for line in bill_lines:
        c.drawString(60, y, line)
        y -= 20

    # Total
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(colors.green)
    c.drawString(60, y, f"Total: ₹{total}")
    y -= 30

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.black)
    c.drawString(60, y, "Thank you for visiting ☕ | Beverage Buddy")

    # QR
    c.drawImage(qr_path, width - 150, 50, 100, 100)
    c.save()

    messagebox.showinfo("PDF Generated", f"Bill saved as {pdf_path}")

# --- Buttons ---
btn_frame = tk.Frame(root, bg="#f8f8f8")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="Reset Order", command=reset_order, bg="#f44336", fg="white", font=("Arial", 12), padx=10).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Generate PDF + QR", command=generate_pdf_bill, bg="#4CAF50", fg="white", font=("Arial", 12), padx=10).grid(row=0, column=1, padx=10)

root.mainloop()
