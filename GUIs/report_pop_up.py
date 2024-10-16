import tkinter as tk
from tkinter import messagebox

def format_mpc_report(RAs, Decs):
    mpc_text = "MPC Report Format:\n\n"
    for ra, dec in zip(RAs, Decs):
        mpc_text += f"RA: {ra}, Dec: {dec}\n"
    return mpc_text

def show_report_window(RAs, Decs):
    # Create a new popup window
    report_window = tk.Toplevel()
    report_window.title("MPC Report")

    # Textbox to display the MPC report
    report_text = format_mpc_report(RAs, Decs)
    text_box = tk.Text(report_window, wrap='word', height=15, width=50)
    text_box.insert(tk.END, report_text)
    text_box.pack(pady=10, padx=10)

    # Copy to clipboard button
    def copy_to_clipboard():
        report_window.clipboard_clear()
        report_window.clipboard_append(report_text)
        messagebox.showinfo("Copy", "MPC Report copied to clipboard!")

    copy_button = tk.Button(report_window, text="Copy", command=copy_to_clipboard)
    copy_button.pack(pady=5)

# Add any additional logic needed for popup
