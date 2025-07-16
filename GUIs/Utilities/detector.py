import tkinter as tk
from astropy.io import fits
import matplotlib.pyplot as plt
import Utilities as ut
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
import numpy as np
from astropy.visualization import SqrtStretch
from astropy.visualization.mpl_normalize import ImageNormalize
from photutils.aperture import CircularAperture
from astropy.table import QTable
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import ttk
import report_pop_up as popup
from astropy.visualization import ZScaleInterval,LogStretch,ImageNormalize,LinearStretch
import re
import time
from tkinter import BooleanVar



def detector(progs_bar,progs_lbl,progs_win,image_path,threshold,pltfrm,BG_COLOR,FG_COLOR,ACCENT_COLOR,HOVER_COLOR,tree,report_button,ax,fig,console):
        """
        Runs the asteroid detection pipeline on a given FITS image, updating a GUI with progress and results.
        This function performs the following steps:
        1. Loads a FITS image and extracts relevant header and image data.
        2. Calculates the field of view (FOV) and image center coordinates.
        3. Queries the Gaia catalog for stars within the FOV.
        4. Runs a blob detection algorithm to identify sources in the image.
        5. Removes duplicate detections and hot pixels.
        6. Filters out sources that match known stars from the Gaia catalog.
        7. Displays the results in a matplotlib plot embedded in a Tkinter GUI, including detected asteroids and stars.
        8. Provides a GUI interface for the user to select detected asteroids and generate a report.
        Parameters:
            progs_bar (ttk.Progressbar): Progress bar widget to update progress.
            progs_lbl (tk.Label): Label widget to display status messages.
            progs_win (tk.Toplevel): Progress window to be destroyed upon completion.
            image_path (str): Path to the FITS image file.
            threshold (float): Detection threshold for the blob detection algorithm.
            pltfrm (tk.Frame): Frame widget where the matplotlib plot and controls will be displayed.
        Returns:
            80 collumn table with detected asteroids, their coordinates, and magnitudes.
        Notes:
            - This function relies on several utility functions (e.g., ut.FOV_calc, ut.RA_deg, ut.Query_FOV_stars2, ut.blob_detection) and external libraries (astropy, numpy, matplotlib, etc.).
            - The function updates the GUI throughout the process to inform the user of progress.
            - Detected asteroid candidates are displayed and can be selected for reporting.
        """
        def print_to_console(*args, **kwargs):
            console.config(state='normal')
            console.insert(tk.END, ' '.join(map(str, args)) + '\n')
            console.config(state='disabled')
            console.see(tk.END)
        start=time.time()
        progs_bar['value']=0
        progs_bar.update()
        
        file=fits.open(image_path)
        image=file[0]
        img=file[0].data.astype(float)

        image_data=fits.getdata(image_path)
        header=image.header 
        
        progs_lbl.config(text="Loading FITS file...")        
        progs_bar['value']=10
        progs_bar.update()

        NAXIS1=image.header['NAXIS1']
        NAXIS2=image.header['NAXIS2']
        XPIXSZ=image.header['XPIXSZ']
        YPIXSZ=image.header['YPIXSZ']
        XPIXSZ=XPIXSZ*10**-3
        YPIXSZ=YPIXSZ*10**-3 #its in microns
        EXPTIME=image.header['EXPTIME']

        
        RA=image.header['RA']
        DEC=image.header['DEC']
        DATE=image.header['DATE-AVG']
        print(DATE)
        

        print_to_console('DATE-OBS: ',DATE)
        print_to_console('Right Ascension: ',RA)
        print_to_console('Declination: ',DEC)
        print('CCD Length (pixels): ',NAXIS1)
        print('CCD Width (pixels): ',NAXIS2)
        print('Pixel Width : ',XPIXSZ)
        #print(f"Loaded image data shape: {image_data.shape}")

        focal_length=620     #Focal length of Rasa11 CYPRUS
        w,h=ut.FOV_calc(NAXIS1,NAXIS2,XPIXSZ,YPIXSZ,focal_length)
        if isinstance(RA,str) and re.match(r"^\d{1,2} \d{1,2} \d{1,2}(\.\d+)?$",RA):
            RA=ut.RA_deg(RA)
            DEC=ut.Decl_deg(DEC)
            
        
        ax.clear()
        norm = ImageNormalize(image_data, interval=ZScaleInterval(), stretch=LinearStretch())
        ax.imshow(image_data, cmap='Greys', origin='lower', norm=norm)
        ax.set_title("Loading image...", fontsize=16, color='white')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')
        fig.canvas.draw()
            
        try:
            app_mag_hor=ut.get_apparent_mag(image_path)
        except Exception as e:
            app_mag_hor=None
        fov=1.5*max(w,h)

        wcs=WCS(image.header)
        
        ra_c,dec_c=ut.image_center(NAXIS1,NAXIS2,wcs)

        center1=SkyCoord(RA,DEC,frame='icrs',unit='deg')
        
        data=image.data[0:NAXIS2,0:NAXIS1]  
        
        #Here we check f zero point is in the header
        #Otherwise we calculate it in the blob detection function
        progs_lbl.config(text="Calculating Zero-point mag...")
        progs_bar['value']=40
        progs_bar.update()

        try:
            ZMAG=image.header['ZMAG']
        except KeyError:
            try:
                ZMAG=image.header['ZP']
            except KeyError:
                ZMAG=0
                print_to_console('Zero point not found in header, calculating it.')
        
        """Detecting sources in the image using blob detection and filtering."""
        progs_lbl.config(text="Detecting sources...")
        progs_bar['value']=50
        progs_bar.update()
        detect_srcs=ut.blob_detection(data,threshold,image,ZMAG,EXPTIME)
        radi=detect_srcs['radius']
        mags=detect_srcs['magnitude']
        detect_srcs=detect_srcs[
            (detect_srcs['xcentroid'] > 10) &
            (detect_srcs['xcentroid'] < (NAXIS1 - 10)) &
            (detect_srcs['ycentroid'] > 10) &
            (detect_srcs['ycentroid'] < (NAXIS2 - 10))]
        xcentroid_blob=detect_srcs['xcentroid']
        ycentroid_blob=detect_srcs['ycentroid']


        duplicate_indices=[]
        for i in range(len(detect_srcs) - 1):
            for j in range(i + 1,len(detect_srcs)):
                if (abs(detect_srcs['xcentroid'][j] - detect_srcs['xcentroid'][i]) < 3) and \
                (abs(detect_srcs['ycentroid'][j] - detect_srcs['ycentroid'][i]) < 3):
                    duplicate_indices.append(j)

        detect_srcs=detect_srcs[~np.in1d(range(len(detect_srcs)),duplicate_indices)]
        query_length = len(detect_srcs)
        ax.clear()
        ax.imshow(image_data, cmap='Greys', origin='lower', norm=norm)
        ax.scatter(detect_srcs['xcentroid'], detect_srcs['ycentroid'], 
                s=1, color='red', label='Initial Detections')
        ax.set_title(f"Initial Detections: {len(detect_srcs)} sources", fontsize=16, color='white')
        ax.legend(title='Legend', loc='center left', bbox_to_anchor=(1, 0.5))
        fig.canvas.draw()
        
        print_to_console(f"Number of stars detected: {len(detect_srcs)}")
        """    Queries the Gaia catalog for stars within the field of view (FOV) centered at the given RA and DEC coordinates."""
        r=ut.Query_FOV_stars3(ra_c,dec_c,width=w,height=h,query_length=query_length,NAXIS1=NAXIS1,NAXIS2=NAXIS2,wcs=wcs)
        #r=ut.Query_FOV_stars2(ra_c,dec_c,width=w,height=h,query_length=query_length)
        rad=np.array(r['ra'])
        ded=np.array(r['dec'])
        rmag=np.array(r['phot_g_mean_mag'])
    


        # rad_f=[]
        # ded_f=[]
        # rmag_f=[]
        # mag_max=35
        # for i in range(len(rmag)):
        #     if rmag[i] < mag_max:
        #         rad_f.append(rad[i])
        #         ded_f.append(ded[i])
        #         rmag_f.append(rmag[i])

        Xstar=[]
        Ystar=[]
        Mstar=[]
        for ra1,dec1,mag in zip(rad,ded,rmag):
            c=SkyCoord(ra1,dec1,frame='icrs',unit='deg')
            x,y=wcs.world_to_pixel(c)
            #if x>0 and y>0 and x<NAXIS2 and y<NAXIS2:
            Xstar.append(x)
            Ystar.append(y)
            Mstar.append(mag)

        gaia_centroids=QTable([Xstar,Ystar],names=('xcentroid','ycentroid'))
        mag_table=QTable([Xstar,Ystar,Mstar],names=('xcentroid','ycentroid','magnitude'))
        
        ax.scatter(Xstar, Ystar, s=0.1, color='yellow', label='Gaia Stars')
        ax.set_title(f"Gaia Stars: {len(Xstar)} stars", fontsize=16, color='white')
        ax.legend(title='Legend', loc='center left', bbox_to_anchor=(1, 0.5))
        fig.canvas.draw()
        
        gaia_centroids.sort('xcentroid')
        print_to_console("The number of stars in the field is:",len(gaia_centroids))
        """Query complete"""

        positions=np.transpose((detect_srcs['xcentroid'],detect_srcs['ycentroid']))
        apertures=CircularAperture(positions,r=6.0)
        norm=ImageNormalize(stretch=SqrtStretch())

        detect_srcs.sort('xcentroid')
        progs_lbl.config(text="Removing Hot Pixels...")
        progs_bar['value']=80
        progs_bar.update()

        r=detect_srcs.copy()
        rmv=[]  

        for j in range(len(r) - 1):
            xd=r['xcentroid'][j]
            yd=r['ycentroid'][j]
            
            for k in range(j + 1,len(r)):
                xd1=r['xcentroid'][k]
                yd1=r['ycentroid'][k]
                
                if abs(xd1 - xd) < 3 and abs(yd1 - yd) < 3:
                    rmv.append(k) 

        rmv=sorted(set(rmv))
        mask=[i not in rmv for i in range(len(r))]
        r=r[mask]  

        aperaturssrtd=sorted(apertures,key=lambda ap: ap.positions[0])
        aperaturesfltrd=[aperaturssrtd[i] for i in range(len(apertures)) if i not in rmv]
        positions=[ap.positions for ap in aperaturesfltrd]  
        radii=aperaturesfltrd[0].r 
        apertures1=CircularAperture(positions,r=radii)

        P=r.copy()
        #Py=sources['ycentroid'].copy()

        # print('Sources before')
        STARS=[]
        # for i in range(len(r)):
        #     print(P[i])
        progs_lbl.config(text="Extracting potential sources...")
        progs_bar['value']=90
        progs_bar.update()
        """    Filters out sources that match known stars from the Gaia catalog.
        """
        
        for i in range(len(r)):
            x=r['xcentroid'][i]
            y=r['ycentroid'][i]     
            # print(f"Checking source: {x},{y}")       
            for xg,yg in gaia_centroids:
                if abs(xg-x)<5 and abs(yg-y)<5:
                    P=P[P['xcentroid'] != x]
                    STARS.append((x,y))


        strs_st=set(STARS)
        mask=[(row['xcentroid'],row['ycentroid']) not in strs_st for row in r]
        filtered_r=r[mask]
        print('Here are the sources',filtered_r['magnitude'])
        print_to_console("Detection complete.")
        progs_bar['value']=100
        progs_bar.update()

        stop=time.time()
        print_to_console(f"Time taken: {stop-start:.2f} seconds")
        print(f"Apparent Magnitude: {app_mag_hor}")
        print(len(Xstar))
        # for widget in pltfrm.winfo_children():
        #     widget.destroy()
        ax.clear()

        # fig=Figure(figsize=(5,5),dpi=100,facecolor='#2b2b2b')
        # ax=fig.add_subplot(111)

        # plt.subplots_adjust(right=0.75)  

        norm=ImageNormalize(data,interval=ZScaleInterval(),stretch=LinearStretch())
        ax.set_title("Asteroid Detection",fontsize=16)
        ax.imshow(data,cmap='Greys',origin='lower',norm=norm)
        ax.scatter(Xstar,Ystar,s=0.1,color='yellow',label='Stars')
        ax.tick_params(colors='white')  # Tick labels and ticks
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        for spine in ax.spines.values():
            spine.set_color('white')
        #ax.scatter(P['xcentroid'],P['ycentroid'],s=50,color='green',marker='x',label='Possible Asteroids')
        ax.scatter(filtered_r['xcentroid'],filtered_r['ycentroid'],s=50,color='green',marker='+',label='Possible Asteroids')
        for i, (x, y) in enumerate(zip(filtered_r['xcentroid'], filtered_r['ycentroid']), start=1):
            ax.text(x + 5, y + 5, str(i), color='green', fontsize=10, weight='bold')
        ax.scatter([],[],color='red',label='Apertures')
        ax.text(10,10,f'FOV: {w:.2f} x {h:.2f} deg',color='red',fontsize=12,bbox=dict(facecolor='white',alpha=0.8))
        apertures1.plot(ax=ax,color='red',lw=1.5,alpha=0.5)

        ax.legend(title='Legend',loc='center left',bbox_to_anchor=(1,0.5),borderaxespad=0.)

        fig.canvas.draw()

        # toolbar = NavigationToolbar2Tk(canvas, pltfrm)
        # toolbar.update()

        # toolbar.config(background=BG_COLOR)
        # toolbar._message_label.config(background=BG_COLOR, foreground=FG_COLOR)

        # for button in toolbar.winfo_children():
        #     if isinstance(button, tk.Button):
        #         button.config(bg=ACCENT_COLOR, fg=FG_COLOR, 
        #                     activebackground=HOVER_COLOR,
        #                     relief=tk.FLAT)
        # toolbar.pack(side=tk.TOP,fill=tk.X)
        
        pltfrm.pack_propagate(False)
        
        # coordfrm=tk.Frame(pltfrm)
        # coordfrm.pack(side=tk.LEFT,fill=tk.BOTH,expand=False)
        tree.delete(*tree.get_children())
        for i in range(len(filtered_r)):
            x = filtered_r['xcentroid'][i]
            y = filtered_r['ycentroid'][i]
            m = filtered_r['magnitude'][i]
            coord = wcs.pixel_to_world(x, y)
            ra = ut.ra_hms(coord.ra.deg)
            dec = ut.dec_dms(coord.dec.deg)
            tree.insert(parent='', index='end', iid=i, values=(f"{x}", f"{y}", f"{m:.2f}",f"{ra}", f"{dec}"))




        report_button.config(command=lambda: generate_report())
        progs_win.destroy()


        
        def generate_report():
            selected = tree.get_checked_items()
            detRAs = []
            setDecs = []
            ms = []
            for iid in selected:
                i = int(iid)
                x = filtered_r['xcentroid'][i]
                y = filtered_r['ycentroid'][i]
                m = filtered_r['magnitude'][i]
                coord = wcs.pixel_to_world(x, y)
                ra = ut.ra_hms(coord.ra.deg)
                dec = ut.dec_dms(coord.dec.deg)
                detRAs.append(ra)
                setDecs.append(dec)
                ms.append(m)
            if detRAs:
                popup.show_report_window(detRAs, setDecs, DATE, ms)
                

