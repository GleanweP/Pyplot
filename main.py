import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def plot_graph():
    x_values = entry_x.get().split(';')
    y1_values = entry_y1.get().split(';')
    y2_values = entry_y2.get().split(';')
    legend_entries = entry_legend.get().split(';')

    fig, ax1 = plt.subplots(figsize=(5, 4), dpi=100)

    colors = ['blue', 'red', 'green', 'purple', 'cyan', 'magenta', 'yellow', 'black', 'orange']

    for i in range(len(x_values)):
        x_data = [float(xi) for xi in x_values[i].split(',')]
        y1_data = [float(yi) for yi in y1_values[i].split(',')]
        legend_label = f'Data {i + 1}' if i >= len(legend_entries) else legend_entries[i]
        color = colors[i % len(colors)]
        #ax1.plot(x_data, y1_data, label=f'{legend_label}', color=color)
        ax1.scatter(x_data, y1_data, label=f'{legend_label}', color=color)


    ax1.set_xlabel(entry_xlabel.get())
    ax1.set_ylabel(entry_ylabel1.get())
    ax1.set_title(entry_title.get())
    ax1.set_ylim(bottom=0, top=100)
    lines1, labels1 = ax1.get_legend_handles_labels()

    if var.get() == 1:
        ax2 = ax1.twinx()
        for i in range(len(x_values)):
            x_data = [float(xi) for xi in x_values[i].split(',')]
            y2_data = [float(yi) for yi in y2_values[i].split(',')]
            legend_label = f'Data {i + 1}' if i >= len(legend_entries) else legend_entries[i+1]
            color = colors[-i-1 % len(colors)]
            ax2.plot(x_data, y2_data, label=f'{legend_label}', color=color)

        ax2.set_ylabel(entry_ylabel2.get())
        lines2, labels2 = ax2.get_legend_handles_labels()
        lines = lines1 + lines2
        labels = labels1 + labels2
        ax1.legend(lines, labels, loc='lower right')
    else:
        ax1.legend(lines1, labels1, loc='lower right')

    new_window = tk.Toplevel(window)
    new_window.title('Matplotlib Plot')

    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    def save_image():
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            fig.savefig(file_path, dpi=100)
            print(f"Image saved as {file_path}")

    save_button = tk.Button(new_window, text="Save as Image", command=save_image)
    save_button.pack()


def update_window_size():
    window.update()
    rwidth = window.winfo_reqwidth()
    rheight = window.winfo_reqheight()
    xs = (window.winfo_screenwidth() // 2) - (rwidth // 2)
    ys = (window.winfo_screenheight() // 2) - (rheight // 2)
    slave_x = xs + rwidth
    slave_y = ys
    window.geometry('{}x{}+{}+{}'.format(rwidth, rheight, xs, ys))
    info_window.geometry(f"{250}x{rheight}+{slave_x}+{slave_y}")


def on_check():
    if var.get() == 0:
        ylabel2_entry.grid_remove()
        label_ylabel2.grid_remove()
        label_y2.grid_remove()
        entry_y2.grid_remove()
        label_y2info.grid_remove()
    else:
        ylabel2_entry.grid()
        label_ylabel2.grid()
        label_y2.grid()
        entry_y2.grid()
        label_y2info.grid()
    update_window_size()


def toggle_info_panel():
    global info_window_visible
    if not info_window_visible:
        master_x = window.winfo_rootx()
        master_y = window.winfo_rooty()
        master_width = window.winfo_width()
        master_height = window.winfo_height()

        slave_width = 250
        slave_height = master_height

        slave_x = master_x + master_width
        slave_y = master_y

        info_window.geometry(f"{slave_width}x{slave_height}+{slave_x}+{slave_y}")
        info_window.deiconify()
        info_window_visible = True
        extend_button.config(text="Collapse")
    else:
        info_window.withdraw()
        info_window_visible = False
        extend_button.config(text="Info")


window = tk.Tk()
window.title('PyPlotter')

label_x = tk.Label(window, text='Enter X values (comma to separate each values):')
label_x.grid(row=0, column=0)
entry_x = tk.Entry(window)
entry_x.grid(row=0, column=1)

label_y1 = tk.Label(window, text='Enter Y1 values (comma to separate each values):')
label_y1.grid(row=1, column=0)
entry_y1 = tk.Entry(window)
entry_y1.grid(row=1, column=1)

label_y2 = tk.Label(window, text='Enter Y2 values (comma to separate each values):')
label_y2.grid(row=2, column=0)
entry_y2 = tk.Entry(window)
entry_y2.grid(row=2, column=1)
label_y2.grid_remove()
entry_y2.grid_remove()

label_legend = tk.Label(window, text='Enter Legends (semicolon-separated for multiple datasets):')
label_legend.grid(row=3, column=0)
entry_legend = tk.Entry(window)
entry_legend.grid(row=3, column=1)

label_xlabel = tk.Label(window, text='X-axis Label:')
label_xlabel.grid(row=4, column=0)
entry_xlabel = tk.Entry(window)
entry_xlabel.grid(row=4, column=1)

label_ylabel1 = tk.Label(window, text='Y1-axis Label:')
label_ylabel1.grid(row=5, column=0)
entry_ylabel1 = tk.Entry(window)
entry_ylabel1.grid(row=5, column=1)

label_ylabel2 = tk.Label(window, text='Y2-axis Label:')
label_ylabel2.grid(row=6, column=0)
entry_ylabel2 = tk.Entry(window)
ylabel2_entry = tk.Entry(window)
ylabel2_entry.grid(row=6, column=1)
label_ylabel2.grid_remove()
ylabel2_entry.grid_remove()

label_title = tk.Label(window, text='Plot Title:')
label_title.grid(row=7, column=0)
entry_title = tk.Entry(window)
entry_title.grid(row=7, column=1)

var = tk.IntVar()
var.set(0)

check_double_yaxis = tk.Checkbutton(window, text='Double Y-axis', variable=var, command=on_check)
check_double_yaxis.grid(row=8, columnspan=2)

info_window = tk.Toplevel(window)
info_window.title('')

label_xinfo = tk.Label(info_window, text='  semicolon-separated for multiple plots')
label_xinfo.grid(row=0, column=0)

label_yinfo = tk.Label(info_window, text='  semicolon-separated for multiple plots')
label_yinfo.grid(row=1, column=0)

label_y2info = tk.Label(info_window, text='  semicolon-separated for multiple plots')
label_y2info.grid(row=2, column=0)
label_y2info.grid_remove()

info_width = info_window.winfo_width()
info_height = info_window.winfo_height()
x_info = (window.winfo_screenwidth() // 2) - (info_width // 2)
y_info = (window.winfo_screenheight() // 2) - (info_height // 2)
info_window.geometry('{}x{}+{}+{}'.format(info_width, info_height, x_info, y_info))  # Set initial size
info_window.withdraw()  # Hide the info panel initially
info_window.overrideredirect(True)

info_window_visible = False

extend_button = tk.Button(window, text="Info", command=toggle_info_panel)
extend_button.grid(row=9, column=1, sticky="SE")
plot_button = tk.Button(window, text='Plot', command=plot_graph)
plot_button.grid(row=9, columnspan=2)

window.update_idletasks()
width = window.winfo_width()
height = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 2) - (height // 2)
window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

window.mainloop()
