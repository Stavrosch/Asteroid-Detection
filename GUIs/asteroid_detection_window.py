import tkinter as tk
from tkinter import filedialog, messagebox
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import Utilities as ut 
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
import numpy as np
from astropy.visualization import SqrtStretch
from astropy.visualization.mpl_normalize import ImageNormalize
from photutils.aperture import CircularAperture
from astropy.table import QTable
from matplotlib.lines import Line2D

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import ttk
import report_pop_up as popup

def create_window(parent):
    new_window = tk.Toplevel(parent)
    new_window.title("Asteroid Detection Window")
    new_window.geometry("800x600")

    # Row 1: Label and button next to each other
    label_frame = tk.Frame(new_window)
    label_frame.pack(pady=10)

    label = tk.Label(label_frame, text="Select a FITS file for analysis")
    label.pack(side=tk.LEFT, padx=5)
    
    file_button = tk.Button(label_frame, text="Choose File", command=lambda: choose_file(new_window, mag_slider.get(), plot_frame))
    file_button.pack(side=tk.LEFT, padx=5)
    
    global file_label
    file_label = tk.Label(new_window, text="No file selected", fg="blue")
    file_label.pack(pady=2)

    # Row 2: Magnitude slider and its label next to each other
    slider_frame = tk.Frame(new_window)
    slider_frame.pack(pady=2)

    mag_slider_label = tk.Label(slider_frame, text="Select Magnitude Threshold (for filtering stars):")
    mag_slider_label.pack(side=tk.LEFT, padx=5)

    mag_slider = tk.Scale(slider_frame, from_=0.01, to=0.05, orient=tk.HORIZONTAL, length=100, resolution=0.01)
    mag_slider.set(0.03)
    mag_slider.pack(side=tk.LEFT, padx=5)

    # # Magnitude value label
    # mag_value_label = tk.Label(new_window)
    # mag_value_label.pack(pady=2)
    
    global run_button
    run_button = tk.Button(new_window, text="Run Detection", state=tk.DISABLED, command=lambda: show_progress_and_run(new_window, plot_frame,file_path,mag_slider.get()))
    run_button.pack(anchor='n',pady=2)

    plot_label = tk.Label(new_window, text=f"Asteroid Detection Plot",font=("Helvetica", 18))
    plot_label.pack(anchor='n',pady=5)
    # Frame for embedding the plot
    plot_frame = tk.Frame(new_window)
    plot_frame.pack(pady=5, fill=tk.BOTH, expand=True)
    
    
    # def update_mag_value(val):
    #     mag_value_label.config(text=f"Current Magnitude Threshold: {float(val):.2f}")
    
    # mag_slider.config(command=update_mag_value)
    
    
def choose_file(window,threshold,plot_frame):
    global file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("FITS Files", "*.fits"), ("All Files", "*.*")],
        title="Select a FITS file"
    )
    if file_path:
        file_label.config(text=f"Selected File: {file_path}", fg="green")
        run_button.config(state=tk.NORMAL)
    else:
        messagebox.showwarning("No File Selected", "Please select a valid FITS file.")
        file_label.config(text="No file selected", fg="red")
        run_button.config(state=tk.DISABLED)
        
def show_progress_and_run(parent_window, plot_frame,image_path,threshold):
    # Create a new window with the progress bar
    progress_window = tk.Toplevel(parent_window)
    progress_window.title("Processing...")
    progress_window.geometry("300x100")
    
    # Create the progress bar
    progress_label = tk.Label(progress_window, text="Running detection...")
    progress_label.pack(pady=10)
    
    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=200, mode="determinate")
    progress_bar.pack(pady=10)

    # Run the detection and update progress randomly
    run_asteroid_detection(progress_bar,progress_label, progress_window, image_path ,threshold, plot_frame)
    
def run_asteroid_detection(progress_bar,progress_label,progress_window,image_path,threshold,plot_frame):
    try:
        progress_bar['value'] = 0
        progress_bar.update()
        
        file = fits.open(image_path)
        image = file[0]
        img = file[0].data.astype(float)

        image_data = fits.getdata(image_path)
        header = image.header 
        
        progress_label.config(text="Loading FITS file...")        
        progress_bar['value'] = 10
        progress_bar.update()

        # plt.figure(figsize=(15, 15))
        # plt.imshow(image_data, cmap='gray')
        # plt.show()

        ### FITS HEADER information ###
        NAXIS1 = image.header['NAXIS1']
        NAXIS2 = image.header['NAXIS2']
        XPIXSZ = image.header['XPIXSZ']
        YPIXSZ = image.header['YPIXSZ']
        XPIXSZ = XPIXSZ*10**-3
        YPIXSZ = YPIXSZ*10**-3 #its in microns

        #OBJECT
        RA = image.header['RA']
        DEC = image.header['DEC']
        DATE = image.header['DATE-OBS']

        #wsc = WCS(image.header)
        #BINNING = image.header['CCDSUM']

        print('DATE-OBS: ', DATE)
        print('Right Ascension (hh:mm:ss): ', RA)
        print('Declination (degrees: arcmin: arcsec): ', DEC)
        print('CCD Length (pixels): ', NAXIS1)
        print('CCD Width (pixels): ', NAXIS2)
        print('Pixel Width : ',XPIXSZ)


        ### FOV Query for Stars ###
        focal_length=620 #Focal length of Rasa11 CYPRUS
        w,h = ut.FOV_calc(NAXIS1,NAXIS2,XPIXSZ,YPIXSZ,focal_length)
        RA=ut.RA_deg(RA)
        DEC=ut.Decl_deg(DEC)

        center = SkyCoord(RA, DEC, unit=["deg", "deg"])

        fov = max(w,h)
        #wcs,radec,stars = ut.plate_solve(image_path,fov,RA,DEC)
        wcs= WCS(image.header)


        # 2. Processing data
        progress_label.config(text="Quering stars...")
        progress_bar['value'] = 40
        progress_bar.update()

        r=ut.Query_FOV_stars2(RA,DEC,width=1.5*w,height=1.5*h)
        rad = np.array(r['ra'])
        ded = np.array(r['dec'])
        rmag = np.array(r['phot_g_mean_mag'])
        
        progress_label.config(text="Running detection algorithm...")
        progress_bar['value'] = 70
        progress_bar.update()

        ### Removing all stars above Magnitude 15 ###
        rad_f = []
        ded_f = []
        rmag_f = []
        mag_max = 17
        for i in range(len(rmag)):
            if rmag[i] < mag_max:
                rad_f.append(rad[i])
                ded_f.append(ded[i])
                rmag_f.append(rmag[i])
            
        ### From coordinate to pixel ###
        Xstar = []
        Ystar = []
        border = min(NAXIS1,NAXIS2)
        for ra1,dec1 in zip(rad_f,ded_f):
            c = SkyCoord(ra1, dec1, frame='icrs', unit='deg')
            x, y = wcs.world_to_pixel(c)
            if x>0 and y>0 and x<border and y<border:
                Xstar.append(x)
                Ystar.append(y)
                
        gaia_centroids = QTable([Xstar, Ystar], names=('xcentroid', 'ycentroid'))
        gaia_centroids.sort('xcentroid')

        center1=SkyCoord(RA, DEC, frame='icrs', unit='deg')
        x_c, y_c = wcs.world_to_pixel(center1)

        # Get Sources Detections
        data = image.data[0:NAXIS1,0:NAXIS2]  
        detected_sources = ut.blob_detection(data,threshold)
        detected_sources = detected_sources[
            (detected_sources['xcentroid'] > 10) &
            (detected_sources['xcentroid'] < (NAXIS1 - 10)) &
            (detected_sources['ycentroid'] > 10) &
            (detected_sources['ycentroid'] < (NAXIS2 - 10))]
        xcentroid_blob = detected_sources['xcentroid']
        ycentroid_blob = detected_sources['ycentroid']



        # # Plot detected sources (blobs)
        # plt.figure(figsize=(8, 8))
        # plt.imshow(data, cmap='plasma', origin='lower')
        # plt.scatter(xcentroid_blob, ycentroid_blob, s=50, facecolors='none', edgecolors='red', label='Detected Sources (Blobs)')
        # plt.colorbar()
        # plt.title("Source Detection using Blob Detection (LoG)")
        # plt.legend(loc='upper right')
        # plt.show()

        duplicate_indices = []
        for i in range(len(detected_sources) - 1):
            for j in range(i + 1, len(detected_sources)):
                if (abs(detected_sources['xcentroid'][j] - detected_sources['xcentroid'][i]) < 3) and \
                (abs(detected_sources['ycentroid'][j] - detected_sources['ycentroid'][i]) < 3):
                    duplicate_indices.append(j)

        # Remove duplicates
        detected_sources = detected_sources[~np.in1d(range(len(detected_sources)), duplicate_indices)]


        #sources.pprint(max_width=74)   
        positions = np.transpose((detected_sources['xcentroid'], detected_sources['ycentroid']))
        apertures = CircularAperture(positions, r=6.0)
        norm = ImageNormalize(stretch=SqrtStretch())

        detected_sources.sort('xcentroid')
        #sources.pprint(max_width=74)   

        ### Remove Duplices that photoutils Detected ###
        d_sources = detected_sources.copy()
        to_remove = []  # indices to remove

        for j in range(len(d_sources) - 1):
            xd = d_sources['xcentroid'][j]
            yd = d_sources['ycentroid'][j]
            
            for k in range(j + 1, len(d_sources)):
                xd1 = d_sources['xcentroid'][k]
                yd1 = d_sources['ycentroid'][k]
                
                if abs(xd1 - xd) < 3 and abs(yd1 - yd) < 3:
                    to_remove.append(k) 

        to_remove = sorted(set(to_remove))
        mask = [i not in to_remove for i in range(len(d_sources))]
        d_sources = d_sources[mask]  

        apertures_sorted=sorted(apertures,key=lambda ap: ap.positions[0])
        apertures_filtered = [apertures_sorted[i] for i in range(len(apertures)) if i not in to_remove]
        positions = [ap.positions for ap in apertures_filtered]  
        radii = apertures_filtered[0].r 
        apertures1 = CircularAperture(positions, r=radii)

        ### Possible Comets ###
        P = d_sources.copy()
        #Py = sources['ycentroid'].copy()
        #Remove from list the ones that are in the catalog
        # print('Sources before')
        STARS=[]
        # for i in range(len(d_sources)):
        #     print(P[i])
        for i in range(len(d_sources)):
            x=d_sources['xcentroid'][i]
            y=d_sources['ycentroid'][i]     
            # print(f"Checking source: {x}, {y}")       
            for xg,yg in gaia_centroids:
                if abs(xg-x)<5 and abs(yg-y)<5:
                    P = P[P['xcentroid'] != x]
                    # print('Removed')
                    # print(x,y)
                    STARS.append((x,y))
                #elif abs(xg-x)>5 and abs(yg-y)>5:
                # elif x<5 or y<5:
                #     P = P[P['xcentroid'] != x]
                #     print('Removed')
                #     print(x,y)
        # print('Sources left')
        # print(P)           
        # print('There are',len(P),'sources that do not correspond to stars.')
        # Convert the list of tuples to a set for faster lookups
        stars_set = set(STARS)

        # Filter d_sources to keep only rows not in STARS
        mask = [(row['xcentroid'], row['ycentroid']) not in stars_set for row in d_sources]

        # Apply the mask to filter the QTable
        filtered_d_sources = d_sources[mask]
        
        print("Detection complete.")
        progress_bar['value'] = 100
        progress_bar.update()

        # Close the progress window after detection completes
        progress_window.destroy()


        for widget in plot_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(6, 6), dpi=100)
        ax = fig.add_subplot(111)

        # Adjust the subplot to make space for the legend
        plt.subplots_adjust(right=0.75)  # Adjust the right boundary of the plot

        # Plot the data on the figure's axis
        ax.imshow(data, cmap='Greys', origin='lower', norm=norm, interpolation='nearest')
        ax.scatter(Xstar, Ystar, s=1, color='blue', label='Stars')
        ax.scatter(P['xcentroid'], P['ycentroid'], s=50, color='green', marker='x', label='Possible Asteroids')
        ax.scatter(filtered_d_sources['xcentroid'], filtered_d_sources['ycentroid'], s=50, color='magenta', marker='+', label='Asteroids filtered')
        ax.scatter([], [], color='red', label='Apertures')
        apertures1.plot(ax=ax, color='red', lw=1.5, alpha=0.5)

        # Adjust the legend to the right, outside the plot
        ax.legend(title='Legend', loc='center left', bbox_to_anchor=(1, 0.5), borderaxespad=0.)

        # Create the canvas and add the figure to it
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()

        # Add the canvas to the Tkinter frame
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add the navigation toolbar for the plot
        toolbar = NavigationToolbar2Tk(canvas, plot_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        # Add the navigation toolbar for the plot
        toolbar = NavigationToolbar2Tk(canvas, plot_frame)
        toolbar.update()
        #canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Coordinates list on the right with a checkbox and a "Report" button
        coord_frame = tk.Frame(plot_frame)
        coord_frame.pack(side=tk.RIGHT, padx=10)
        
        print('There are',len(filtered_d_sources),'sources that do not correspond to stars.')
        # print(filtered_d_sources)

        # # Matrix P IS SOURCES-GAIA=POTENTIAL_ASTEROIDS
        # plt.figure(figsize=(8, 8))
        # plt.imshow(data, cmap='Greys', origin='lower', norm=norm, interpolation='nearest')
        # plt.colorbar()
        # plt.scatter(Xstar, Ystar, s=1, color='blue', label='Stars')
        # plt.scatter(P['xcentroid'], P['ycentroid'], s=50, color='green', marker='x', label='Possible Asteroids')
        # plt.scatter(filtered_d_sources['xcentroid'], filtered_d_sources['ycentroid'],s=50,color='magenta',marker = '+',label = 'Asteroids filtered')
        # plt.scatter([], [], color='red', label='Apertures')
        # apertures1.plot(color='red', lw=1.5, alpha=0.5)
        # plt.legend(title='Legend', loc='upper right')
        # plt.tight_layout()
        # plt.show()

        ### Get Potential Asteroid Coords ###
        RAs=[]
        Decs=[]
        for i in range(len(P)):
            x=P['xcentroid'][i]
            y=P['ycentroid'][i]
            coord=wcs.pixel_to_world(x,y)
            ra=ut.ra_hms(coord.ra.deg)
            dec=ut.dec_dms(coord.dec.deg)
            RAs.append(ra)
            Decs.append(dec)

        print('The coordinates for the Possible asteroids:',RAs,Decs)
        
        # Add a checkbox (for selection purposes, if needed)
        checkbox_var = tk.IntVar()
        checkbox = tk.Checkbutton(coord_frame, text="Select all", variable=checkbox_var)
        checkbox.pack(anchor='w')        

        # Report button
        report_button = tk.Button(coord_frame, text="Report", command=lambda: popup.show_report_window(RAs, Decs))
        report_button.pack(pady=10)
        
    except Exception as e:
        print(f"Error processing file: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")
