import numpy as np
import os
import logging
import logging.config
# import matplotlib.pyplot as plt
import tkinter as tk
from PIL import Image
from mod_tk import ListFrame
from tkinter import ttk, messagebox
from tkinter.filedialog import askdirectory
from tkinter.colorchooser import askcolor

logging.config.fileConfig('config.ini')

logger = logging.getLogger()


def set_save_path():
    path = askdirectory()
    if path is None:
        return
    save_path.set(path)


def crop(im: Image.Image):
    im_grey = im.convert('L')
    arr = np.asarray(im_grey)
    h, w = arr.shape
    mask = 1 * (arr < 250)

    row = 0
    while np.max(mask[row]) == 0:
        row += 1
    upper = row

    row = h - 1
    while np.max(mask[row]) == 0:
        row -= 1
    lower = row

    column = 0
    while np.max(mask[:, column]) == 0:
        column += 1
    left = column

    column = w - 1
    while np.max(mask[:, column]) == 0:
        column -= 1
    right = column
    return im.crop((left, upper, right, lower))

def recolor(im: Image.Image):
    arr_0 = np.asarray(im)
    print(arr_0.shape)
    arr = np.min(arr_0, axis=2)
    mask = arr < 255

    sh = arr.shape
    a1 = np.ones(sh)
    a2 = np.ones(sh)
    a3 = np.ones(sh)
    a1 = a1 * 255
    a2 = a2 * 255
    a3 = a3 * 255
    a4 = 255 - arr 

    a1[mask] = recolor_rgb[0]
    a2[mask] = recolor_rgb[1]
    a3[mask] = recolor_rgb[2]
    temp = np.asarray([a1, a2, a3, a4], dtype='uint8')
    new_arr = np.transpose(temp, (1, 2, 0))
    new_im = Image.fromarray(new_arr, mode='RGBA')
    return new_im


def resize(im: Image.Image, width: int, height: int, filter_: int):
    return im.resize((width, height), resample=filter_)

def auto_brightness(im: Image.Image):
    im = np.asarray(im)
    hist, bins = np.histogram(im, 255)
    threshold = im.size / 5000
    num_pix = 0
    min_im = 0
    max_im = np.max(im)

    for i in range(255):
        num_pix += hist[i]
        if num_pix > threshold:
            min_im = bins[i]
            break

    num_pix = 0
    for j in range(1, 255):
        num_pix += hist[-j]
        if num_pix > threshold:
            max_im = bins[-j]
            break
    
    fp = np.zeros(bins.shape)
    fp[:i] = 1
    fp[-j:] = 255
    for index in range(i, 256 - j):
        range_ = 256 - j - i
        step = 254 / range_
        fp[index] = (index - i) * step + 1

    im2 = np.interp(im.flatten(), bins, fp).reshape(im.shape).astype(np.uint8)
    return Image.fromarray(im2)

def process():
    try:
        dpi = float(dpi_tk.get())
    except:
        dpi = 300.0
    try:
        dir_ = save_path.get()
    except:
        dir_ = './'
    suffix = suffix_tk.get()
    ext = saved_file_type.get()
    for i in f.files:
        im = Image.open(i)
        if is_crop.get():
            im = crop(im)
        if is_gray.get():
            im = im.convert('L')
        if is_recolor.get():
            im = recolor(im)
        if not is_size.get():
            try:
                w = float(width_tk.get())
                h = float(height_tk.get())
            except:
                size_tk.set('ratio')
                w = 1.0
                h = 1.0
            if size_tk.get() == 'ratio':
                width = im.size[0] * w
                height = im.size[1] * h
            else:
                width = w
                height = h
            print(width, height)
            filter_ = filters.index(filter_tk.get())
            im = resize(im, int(width), int(height), filter_)
        if is_brightness.get():
            im = auto_brightness(im)
        path = ''.join((dir_, '/', os.path.basename(i), suffix, ext))
        im.save(path, dpi=(dpi, dpi))
    messagebox.showinfo(title='Done.', message='Done!')


def state():
    if not is_size.get():
        rb_size.config(state='normal')
        rb_ratio.config(state='normal')
        e_height.config(state='normal')
        e_width.config(state='normal')
    else:
        rb_size.config(state='disabled')
        rb_ratio.config(state='disabled')
        e_height.config(state='disabled')
        e_width.config(state='disabled')


def choose_color():
    global recolor_rgb
    recolor_rgb, color_str = askcolor()
    recolor_tk.set(color_str)


app = tk.Tk()
app.title('Image Crop by Q. Dong')
save_path = tk.StringVar()
save_path.set('./')
saved_file_type = tk.StringVar()
saved_file_type.set('.tif')
dpi_tk = tk.StringVar()
dpi_tk.set('300.0')
suffix_tk = tk.StringVar()
suffix_tk.set('')
is_crop = tk.IntVar()
is_crop.set(1)
is_gray = tk.IntVar()
is_gray.set(0)
is_recolor = tk.IntVar()
is_recolor.set(0)
is_brightness = tk.IntVar()
is_brightness.set(0)
is_size = tk.IntVar()
is_size.set(1)
size_tk = tk.StringVar()
size_tk.set('ratio')
width_tk = tk.StringVar()
width_tk.set('1.0')
height_tk = tk.StringVar()
height_tk.set('1.0')
filter_tk = tk.StringVar()
filter_tk.set('NEAREST')
recolor_tk = tk.StringVar()
recolor_tk.set('')
recolor_rgb = (0, 0, 0)

frame_left = ttk.Frame(app)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, ipadx=5, ipady=5, expand=1)
frame_right = ttk.Frame(app)
frame_right.pack(side=tk.LEFT, fill=tk.Y, ipadx=5, ipady=5)
f = ListFrame(label='Files to be processed', default_type='.tif',
              file_types=[("All Files", "*.*"), ("Images", "*.jpg"), ("Images", "*.tif"),
                          ("Images", "*.png")], master=frame_left)
f.pack(side=tk.TOP, fill=tk.BOTH, expand=1, ipadx=5, ipady=5)

f_save = ttk.Labelframe(master=frame_left, text='Save files in this folder')
f_save.pack(side=tk.TOP, fill=tk.X)
ttk.Entry(master=f_save, textvariable=save_path).pack(side=tk.LEFT, fill=tk.X, expand=1)
ttk.Button(master=f_save, text='Browse', command=set_save_path).pack(side=tk.LEFT)

f_setting = ttk.Labelframe(master=frame_right, text='Setting')
f_setting.pack(side=tk.TOP, fill=tk.X, expand=0, anchor=tk.N, ipady=5)
f_setting.columnconfigure(0, weight=1)
f_setting.columnconfigure(1, weight=1)
ttk.Label(master=f_setting, text='Save as: ').grid(row=0, column=0, sticky=tk.E)
ttk.Combobox(master=f_setting, textvariable=saved_file_type,
             values=['.tif', '.png', '.jpg']).grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
ttk.Label(master=f_setting, text='dpi: ').grid(row=1, column=0, sticky=tk.E)
ttk.Entry(master=f_setting, textvariable=dpi_tk).grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
ttk.Label(master=f_setting, text='suffix: ').grid(row=2, column=0, sticky=tk.E)
ttk.Entry(master=f_setting, textvariable=suffix_tk).grid(row=2, column=1, sticky=tk.N+tk.S+tk.E+tk.W)


f_process = ttk.Labelframe(master=frame_right, text='Process')
f_process.pack(side=tk.TOP, fill=tk.X, expand=0, ipady=5)
ttk.Checkbutton(master=f_process, text='crop image', variable=is_crop).pack(side=tk.TOP, fill=tk.X)
ttk.Checkbutton(master=f_process, text='gray image', variable=is_gray).pack(side=tk.TOP, fill=tk.X)
ttk.Checkbutton(master=f_process, text='recolor image', variable=is_recolor, command=choose_color).pack(side=tk.TOP, fill=tk.X)
ttk.Checkbutton(master=f_process, text='Auto brightness', variable=is_brightness).pack(side=tk.TOP, fill=tk.X)


f_size = ttk.LabelFrame(master=frame_right, text='size')
f_size.pack(side=tk.TOP, fill=tk.X, expand=0, ipady=5)
ttk.Checkbutton(master=f_size, text='Original size', variable=is_size, command=state).pack(side=tk.TOP, fill=tk.X)

f_size_option = ttk.Frame(master=f_size)
f_size_option.pack(side=tk.TOP, fill=tk.X)

rb_size = ttk.Radiobutton(master=f_size_option, text='Size', variable=size_tk, value='size', state='disabled')
rb_ratio = ttk.Radiobutton(master=f_size_option, text='Ratio', variable=size_tk, value='ratio', state='disabled')
rb_size.pack(side=tk.LEFT)
rb_ratio.pack(side=tk.LEFT)

f_wh = ttk.Frame(f_size)
f_wh.pack(side=tk.TOP, fill=tk.X)
ttk.Label(f_wh, text='Width').pack(side=tk.LEFT)
e_width = ttk.Entry(f_wh, textvariable=width_tk, width=5, state='disabled')
e_width.pack(side=tk.LEFT)
ttk.Label(f_wh, text='Height').pack(side=tk.LEFT)
e_height = ttk.Entry(f_wh, textvariable=height_tk, width=5, state='disabled')
e_height.pack(side=tk.LEFT)
filters = ['NEAREST', 'BOX', 'BILINEAR', 'HAMMING', 'LANCZOS']
ttk.Label(f_size, text='interpolation: ').pack(side=tk.LEFT)
ttk.Combobox(master=f_size, textvariable=filter_tk, values=filters).pack(side=tk.LEFT, fill=tk.X)

ttk.Button(master=frame_right, text='Start', command=process).pack(side=tk.BOTTOM, fill=tk.X, expand=0, pady=5)

app.mainloop()
