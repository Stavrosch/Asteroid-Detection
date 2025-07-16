import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

def format_mpc_report(RAs, Decs,date,ms):
    mpc_text = ""
    for i, (ra, dec,m) in enumerate(zip(RAs, Decs,ms), start=1):
        ra_formatted = " ".join(f"{abs(x):02.0f}" if i == 0 or i == 1 else f"{abs(x):05.3f}" for i, x in enumerate(ra))
        dec_formatted = " ".join(f"{abs(x):02.0f}" if i == 0 or i == 1 else f"{abs(x):05.2f}" for i, x in enumerate(dec))
        dec_sign = "-" if dec[0] < 0 else "+"
        dec_formatted = dec_sign + dec_formatted
        m_formatted = f"{m:02.1f}"

        report_line = f"{i:05}         {date}{ra_formatted}{dec_formatted}         {m_formatted} R      XXX\n"
        mpc_text += report_line
    return mpc_text


def convert_date(date_string):
    date_obj = datetime.fromisoformat(date_string)
    
    day_fraction = (date_obj.hour + date_obj.minute / 60 + date_obj.second / 3600) / 24
    
    mpc_date = f"C{date_obj.year} {date_obj.month:02} {date_obj.day + day_fraction:09.6f}"
    return mpc_date


def show_report_window(RAs, Decs,DATE,m):
    report_window = tk.Toplevel()
    report_window.title("MPC Report")

    mpc_date=convert_date(DATE)
    report_text = format_mpc_report(RAs, Decs,mpc_date,m)
    text_box = tk.Text(report_window, wrap='word', height=15, width=70)
    text_box.insert(tk.END, report_text)
    text_box.config(state='disabled')
    text_box.pack(pady=10, padx=10)

    def copy_to_clipboard(text):
        report_window.clipboard_clear()
        report_window.clipboard_append(text)
        #messagebox.showinfo("Copied!", "Report text has been copied!")coψ

    copy_button = tk.Button(report_window, text="Copy Report", command=lambda: copy_to_clipboard(report_text))
    copy_button.pack(pady=5)

    close_button = tk.Button(report_window, text="Close", command=report_window.destroy)
    close_button.pack(pady=5)

