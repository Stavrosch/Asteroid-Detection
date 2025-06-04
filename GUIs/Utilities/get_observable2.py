import tkinter as tk
from tkinter import ttk, messagebox
import requests
import base64
from io import BytesIO
from PIL import Image, ImageTk


class SelectableTreeView(ttk.Treeview):
    def __init__(self, master=None, **kwargs):
        ttk.Treeview.__init__(self, master, **kwargs)

        checked_b64 = '''iVBORw0KGgoAAAANSUhEUgAAABYAAAAXCAYAAAAP6L+eAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAACxEAAAsRAX9kX5EAAAI0SURBVEhLrZVPTxNRFEfPe1Ps/wFaBytVCqV2QGgR41YWxsSFiStNiCa6UWOAD+HSnQtSogs3gisSF34Lg4kFEjKNpITEGCVIoSEYSmfGRVMybSkkpWd55+Zk7v29vCfeff9qf9veomxZtIMOKZmIRBH6p/f2j+Iulm3X97SEIgTjYQ3ZTimAadtkd7aR7ZRWKVsWsr7YClf8AaK+QE3t3OJYQGVaTzOlp+j1+o/r5xL3+YNM6SmeDg7xoC9OxNcGcTyoMjOU5klcp2SafN5c59fB/vH3lsSJYCfTDunHvEEmt8rvfwfHPTXiqC+A5vE6Sw3Egyozw2NM9icpWxYLGzkyuVW2HFKc4ojXx6vkKC+ujaK5PTVNVWIBlemhNI9iCcqWxXw+x5yx0iDFKR4IqDyMJXieHOGlnuKyI2EcQU32Jzk0TRbyOWaN5ZrxnSjcv/sawKMohNwebnRr3AxrKEKwtrfDQblMPKgypVd2emSazOcNMrkV/jSR4hQXSocYxQLdbjfXu0KMdWvYgInNs8QwjwcqQVWkq6dKcYoBdksljL0C/o4ORrtCjIc1BtVO7vXGKjttEtRJNBy3jf0ib9eyLG6u41VcTPREzwzqJGr+uErxqIRRLKC5vYQueFjcXGfWWD5zfCeCuTdNr7dEsJM7kat8+Zlvmn4zThULwCUlRy28Lg07dmJDS1IAKYWor50bl5DIka4QShvlLiG5dbEH8SG7ZC/93Wp55HrcUnL7UpT/edTeairZ+1kAAAAASUVORK5CYII='''
        unchecked_b64 = '''iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAACxEAAAsRAX9kX5EAAACcSURBVEhL7dSxDYQgFIDhH4XG4Cq0jMIKNCbu4hROwCC0djYugV51Lzm7UxsTvoQGXn66p6ZpOpZlYd93ntC2Lc45miejAKUUcs6oYRgOgBgj1trz3F/WdWWeZwCa76W1lr7vb52u6+QTCT+thkUNixoWNSzeF5ZFH0L42adXbNtGSgkANY7jUUo5z9xijKFxzqG1Pr9dZozBe88Hi78t3eij8ZUAAAAASUVORK5CYII='''

        checked_img = Image.open(BytesIO(base64.b64decode(checked_b64))).resize((23,23), Image.ANTIALIAS)
        unchecked_img = Image.open(BytesIO(base64.b64decode(unchecked_b64))).resize((23,23), Image.ANTIALIAS)
        self.checked_img = ImageTk.PhotoImage(checked_img)
        self.unchecked_img = ImageTk.PhotoImage(unchecked_img)

        self.tag_configure('unchecked', image=self.unchecked_img)
        self.tag_configure('checked', image=self.checked_img)

        self.bind("<Button-1>", self.handle_click)

    def insert(self, parent, index, iid=None, **kw):
        if 'tags' not in kw:
            kw['tags'] = ('unchecked',)
        return super().insert(parent, index, iid, **kw)

    def handle_click(self, event):
        region = self.identify("region", event.x, event.y)
        if region == "tree":
            item = self.identify_row(event.y)
            if item:
                tags = self.item(item, "tags")
                if 'checked' in tags:
                    self.item(item, tags=('unchecked',))
                else:
                    self.item(item, tags=('checked',))

    def get_checked_items(self):
        return [item for item in self.get_children() if 'checked' in self.item(item, 'tags')]


def get_observable_objects(lat, lon, height, obs_time, angle=None, min_mag=None, max_mag=None, object_type=None,on_select_callback=None):
    print("observation time:", obs_time)
    print(obs_time.split("T")[0])

    params = {
        "optical": "true",
        "lat": lat,
        "lon": lon,
        "alt": height,
        "obs-time": obs_time.split("T")[0],
        "sb-kind": "a",
        "maxoutput": 1000,
        "output-sort": "name",
        "output-sort-r": "false",
    }

    if angle:
        params["elev-min"] = angle
    if min_mag:
        params["vmag-min"] = min_mag
    if max_mag:
        params["vmag-max"] = max_mag
    if object_type:
        params["sb-group"] = object_type
    #print(params)
    response = requests.get("https://ssd-api.jpl.nasa.gov/sbwobs.api", params=params)
    begin_twilight = response.json().get("begin_astronomical")
    print("Begin Astronomical Twilight:", begin_twilight)

    if response.status_code != 200:
        messagebox.showerror("API Error", f"Failed to get data ({response.status_code})")
        return

    data = response.json()
    if "data" not in data:
        messagebox.showinfo("No Results", "No observable objects found.")
        return

    headers = data["fields"]
    rows = data["data"]
    fields_to_suppress = ["Designation","Object-Observer-Sun (deg)", "Topo.range (au)", "Galactic latitude (deg)", "Object-Observer-Moon (deg)", ""]
    suppress_indices = [headers.index(field) for field in fields_to_suppress if field in headers]
    filtered_headers = [header for i, header in enumerate(headers) if i not in suppress_indices]
    filtered_rows = [
        [value for j, value in enumerate(row) if j not in suppress_indices]
        for row in rows
    ]

    result_win = tk.Toplevel()
    result_win.title("Observable Objects")

    tree = SelectableTreeView(result_win, columns=filtered_headers, show="tree headings", height=10)
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # The Select column
    tree.heading("#0", text="Select")
    tree.column("#0", width=50, anchor="center")

    for col in filtered_headers:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    for row in filtered_rows:
        tree.insert("", "end", text="", values=row)


    def add_selected_to_list():
        selected = tree.get_checked_items()
        selected_data = [tree.item(item)["values"] for item in selected]
        if on_select_callback:
            on_select_callback(selected_data,filtered_headers)  
        #result_win.destroy()

    btn = tk.Button(result_win, text="Add Object", command=add_selected_to_list)
    btn.pack(pady=5)
