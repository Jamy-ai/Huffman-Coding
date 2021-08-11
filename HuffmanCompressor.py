import tkinter as tk
from huffmanCoding import HuffmanCoding
from tkinter import filedialog
# from PIL import Image, ImageTk

window = tk.Tk()
window.title("File Compressor")
canvas = tk.Canvas(window, width=550, height=700, bg='bisque2')
canvas.grid(columnspan=3, rowspan=4)
window.resizable(False, False)

#path of selected file to compress or decompress
path = ""

#instructions
instruct = tk.Label(window, text="Select a file to compress/decompress", bg='bisque2', font=('Arial Bold', 23))
instruct.grid(columnspan=3, column=0, row=0)

#browse button to select file
browse_text = tk.StringVar()
browse_btn = tk.Button(window, textvariable=browse_text, command=lambda:select_file(), bg="#20bebe", fg="white", height=2, width=15)
browse_text.set("Browse")
browse_btn.grid(column=0, row=1)

#compress button
compress_text = tk.StringVar()
compress_btn = tk.Button(window, textvariable=compress_text, command=lambda:compress_file(), bg="#20bebe", fg="white", height=2, width=15)
compress_text.set("Compress")
compress_btn.grid(column=1,row=1)

#decompress button
decompress_text = tk.StringVar()
decompress_btn = tk.Button(window, textvariable=decompress_text, command=lambda:decompress_file(), bg="#20bebe", fg="white", height=2, width=15)
decompress_text.set("DeCompress")
decompress_btn.grid(column=2,row=1)

# text box to show the status of actions like what happened
text_box = tk.Text(window, height=10, width=50, padx=15, pady=15)
text_box.insert(1.0, "Actions will be displayed here")
text_box.tag_configure("center", justify="center")
text_box.tag_add("center", 1.0, "end")
text_box.grid(columnspan=3,column=0, row=2)

#write in text box to update the status
def write_in_text_box(output):
    text_box.delete(1.0,"end")
    text_box.insert(1.0, output)

#function for browse button to select file
def select_file():
    global path
    path = ""
    file = filedialog.askopenfilename(parent=window, title="Choose a file")
    path = file

    output = ""
    if(path == ()):
        output = "No file selected"
        path = ""
    else:
        output = "Selected file :- " + path

    write_in_text_box(output)
    # h = HuffmanCoding(file)
    # output = h.decompress()
    # if file:
    #     with open(file, 'r') as f:
    #         for line in f:
    #             print(line)

#function for compress button
def compress_file():
    h = HuffmanCoding(path)
    output = "Compressed file :- " + h.compress()
    write_in_text_box(output)

#function for decompress button
def decompress_file():
    h = HuffmanCoding(path)
    output = "Decompressed file :- " + h.decompress()
    write_in_text_box(output)

window.mainloop()