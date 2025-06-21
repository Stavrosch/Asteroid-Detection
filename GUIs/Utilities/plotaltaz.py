import matplotlib.pyplot as plt
from Utilities import split_segments
def plot_asteroid_altaz_path(canvas,ax,alt_list, time_list):
        ax.clear()

        above = [(t, alt) for t, alt in zip(time_list, alt_list) if alt >= 0]
        below = [(t, alt) for t, alt in zip(time_list, alt_list) if alt < 0]
        if above:
            for segment in split_segments(above):
                t_seg, alt_seg = zip(*segment)
                ax.plot(t_seg, alt_seg, 'r')
        if below:
            for segment in split_segments(below):
                t_seg, alt_seg = zip(*segment)
                ax.plot(t_seg, alt_seg, 'grey')

        ax.set_xlabel("Time (hours from now)")
        ax.set_ylabel("Altitude (deg)")
        ax.set_title("Altitude Path")
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.6)
        ax.grid(True)
        ax.set_xlim(min(time_list), max(time_list))
        ax.set_ylim(min(0, min(alt_list) - 5), max(0, max(alt_list) + 5))
        canvas.draw()

