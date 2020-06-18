#c64 floyd steinberg
from PIL import Image
from tkinter import Tk, messagebox, simpledialog
from tkinter.filedialog import askopenfilename, asksaveasfilename
from getpass import getuser

root = Tk()
root.withdraw()
location = askopenfilename()
img = Image.open(location)
img.load()

def closest_pallette(pixel):
    #C64 Color palatte
    #https://www.c64-wiki.com/wiki/Color
    palette = ((0,0,0),(255,255,255),(136,0,0),(170,255,238),(204,68,204),(0,204,85),(0,0,170),(238,238,119),(221,136,85),(102,68,0),(255,119,119),(51,51,51),(119,119,119),(170,255,102),(0,136,255),(187,187,187))
    
    #closest point algorithm
    best_color = palette[0]
    best_distance = 195075 #255^2 *3
    for color in palette:
        distance = (color[0]-pixel[0])**2 + (color[1]-pixel[1])**2 + (color[2]-pixel[2])**2
        if distance < best_distance:
            best_distance = distance
            best_color = color
    return best_color

for y in range(img.size[1]-1):
    for x in range(1,img.size[0]-1):
        pixel = img.getpixel((x,y))
        newpixel = closest_pallette(pixel)
        img.putpixel((x,y),newpixel)
        errpixel = tuple(val - newval for val,newval in zip(pixel, newpixel))
        
        img.putpixel((x+1,y  ),tuple(int(val + err*7/16) for val,err in zip(img.getpixel((x+1,y  )),errpixel)))

        img.putpixel((x-1,y+1),tuple(int(val + err*3/16) for val,err in zip(img.getpixel((x-1,y+1)),errpixel)))

        img.putpixel((x  ,y+1),tuple(int(val + err*5/16) for val,err in zip(img.getpixel((x  ,y+1)),errpixel)))

        img.putpixel((x+1,y+1),tuple(int(val + err*1/16) for val,err in zip(img.getpixel((x+1,y+1)),errpixel)))


new_location = asksaveasfilename(initialdir = f"C:/Users/{getuser()}/Pictures",title = "Save file",filetypes = (("PNG files","*.png"),("all files","*.*")))
if len(new_location) <= 4 or new_location[-4:].lower() != ".png":
    new_location += ".png"
img.save(new_location)

