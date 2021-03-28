from tkinter import *
import os
from PIL import Image, ImageDraw, ImageFont
from init_image import Example
import uuid
import easygui


def open_file():
    input_file = easygui.fileopenbox(filetypes=["*.docx"])
    return input_file


def createNewImageWindow(input_path):
    newWindow = Toplevel(window)

    imag_watermark = open_file()
    pos_label = Label(newWindow, text='Input position like two numbers ex. 0-0')
    pos_label.pack()
    pos = Entry(newWindow, width=26)
    pos.pack()

    submit_button = Button(newWindow,
                           text='Submit',
                           command=lambda: watermark_image(img_watermark=imag_watermark,
                                                           pos=pos.get(),
                                                           input_path=input_path,
                                                           ))
    Button(newWindow, text='Quit', command=newWindow.destroy).pack()
    submit_button.pack()
    newWindow.mainloop()


def createNewTextWindow(input):
    newWindow = Toplevel(window)

    text_label = Label(newWindow, text='Input your text')
    text_label.pack()
    text = Entry(newWindow, width=26)
    text.pack()

    pos_label = Label(newWindow, text='Input position like two numbers ex. 0-0')
    pos_label.pack()
    pos = Entry(newWindow, width=26)
    pos.pack()

    submit_button = Button(newWindow,
                           text='Submit',
                           command=lambda: watermark_text(text=text.get(),
                                                          pos=pos.get(),
                                                          input_path=input,
                                                          ))
    Button(newWindow, text='Quit', command=newWindow.destroy).pack()
    submit_button.pack()
    newWindow.mainloop()


def watermark_text(input_path, text, pos):
    filename = input_path.split(".")[-1]
    print(filename)
    output_path = os.environ['USERPROFILE'] + "\watermarked" + str(uuid.uuid4()) + "." + filename
    try:
        pos = tuple([int(x) for x in pos.split('-')])
    except:
        print('Wrong values! Position will be set as 0, 0')
        pos = (0, 0)
    photo = Image.open(input_path)
    drawing = ImageDraw.Draw(photo)
    black = (3, 8, 12)
    font = ImageFont.truetype("arial.ttf", 40)
    drawing.text(pos, text, fill=black, font=font)
    photo.show()
    if filename in ["jpeg", "jpg", "png"]:
        photo.save(output_path, format=f'{filename.upper()}')


def watermark_image(img_watermark, pos, input_path):
    filename = input_path.split(".")[-1]
    print(filename)
    output_path = os.environ['USERPROFILE'] + "\watermarked" + str(uuid.uuid4()) + "." + filename
    base_image = Image.open(input_path)
    watermark = Image.open(img_watermark).convert("RGBA")
    width, height = base_image.size
    try:
        pos = tuple([int(x) for x in pos.split('-')])
    except:
        print('Wrong values! Position will be set as 0, 0')
        pos = (0, 0)

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, pos, mask=watermark)
    transparent.show()
    if filename in ["jpeg", "jpg", "png"]:
        transparent.save(output_path, format=f'{filename.upper()}')


def main():
    ex = Example()
    start_button['state'] = 'disabled'
    add_text_button['state'] = 'active'
    add_text_button['command'] = lambda: createNewTextWindow(input=ex.input_file, )
    add_image_button['state'] = 'active'
    add_image_button['command'] = lambda: createNewImageWindow(input_path=ex.input_file)


def quit():
    window.destroy()


window = Tk()
window.title('Your watermark')
window.config(padx=100, pady=50)

start_button = Button(text="Download the image", highlightthickness=0, command=main)
start_button.pack()

add_text_button = Button(text="Add text",
                         highlightthickness=0, command=createNewTextWindow)
add_text_button.pack()

add_text_button['state'] = 'disabled'

add_image_button = Button(text="Add image", command=createNewImageWindow)
add_image_button.pack()
add_image_button['state'] = 'disabled'

Button(text="Quit", command=quit).pack()

window.mainloop()
