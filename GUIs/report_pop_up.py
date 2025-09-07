import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import Utilities as ut

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

def format_ades_report(ras, decs, date, ms):
    """Generate ADES XML format report"""
    ades_xml = """
<ades version="2022">
    <obsBlock>
        <obsContext>
            <observatory>
                <mpcCode>XXX</mpcCode>
            </observatory>
            <submitter>
                <name>Your Name</name>
                <institution>Your Institution</institution>
            </submitter>
            <observers>
                <name>Observer Name</name>  
            </observers>
            <measurers>
                <name>Measurer Name</name>
            </measurers>
            <telescope>
                <name>Your Telescope</name>
                <design>Telescope Design</design>
                <aperture>0.0</aperture>
                <detector>Your Detector</detector>
            </telescope>
            <comment>
                <line>Observatory details</line>
            </comment>
        </obsContext>
        <obsData>
"""
    


            
    for ra, dec, mag in zip(ras, decs, ms):
        # ra_deg = (ra_tuple[0] * 15) + (ra_tuple[1] / 4) + (ra_tuple[2] / 240)
        
        # dec_sign = -1 if dec_tuple[0] < 0 else 1
        # dec_deg = abs(dec_tuple[0]) + (dec_tuple[1] / 60) + (dec_tuple[2] / 3600)
        # dec_deg *= dec_sign
        # ra_str = f"{ra_tuple[0]} {ra_tuple[1]} {ra_tuple[2]:.3f}"
        # dec_str = f"{dec_tuple[0]} {dec_tuple[1]} {dec_tuple[2]:.2f}"
        
        ra_deg = ra
        dec_deg = dec
        
        ades_xml += f"""            <optical>
                <permID>00000</permID>
                <mode>CCD</mode>
                <stn>XXX</stn>
                <obsTime>{date}</obsTime>
                <ra>{ra_deg:.6f}</ra>
                <dec>{dec_deg:.6f}</dec>
                <astCat>Gaia3</astCat>
                <mag>{mag:.1f}</mag>
                <band>R</band>
            </optical>"""
    
    ades_xml += """
        </obsData>
    </obsBlock>
</ades>"""
    
    return ades_xml


def convert_date(date_string):
    date_obj = datetime.fromisoformat(date_string)
    
    day_fraction = (date_obj.hour + date_obj.minute / 60 + date_obj.second / 3600) / 24
    
    mpc_date = f"C{date_obj.year} {date_obj.month:02} {date_obj.day + day_fraction:09.6f}"
    return mpc_date


def show_report_window(RAs, Decs,DATE,m,report_format):
    print('the format',report_format)
    if report_format == "80-column":
        mpc_date = convert_date(DATE)
        report_text=format_mpc_report(RAs, Decs,mpc_date,m)
    else:
        mpc_date = convert_date(DATE)
        report_text = format_ades_report(RAs, Decs, DATE, m)

    report_window = tk.Toplevel()
    report_window.title("MPC Report")
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

