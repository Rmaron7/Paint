from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import *
class Paint(object):
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(self.root, text='ручка', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.color_button = Button(self.root, text='цвет', command=self.choose_color)
        self.color_button.grid(row=0, column=1)

        self.eraser_button = Button(self.root, text='ластик', command=self.use_eraser)
        self.eraser_button.grid(row=1, column=0)

        self.clear_button = Button(self.root, text='стереть все', command=self.clear)
        self.clear_button.grid(row=2, column=0)

        self.choose_size_button = Scale(self.root, from_=1, to=30, orient=HORIZONTAL)
        self.choose_size_button.grid(row=1, column=1)

        self.sqare = Button(self.root, text='прямоугольник', command=self.sqare_draw)
        self.sqare.grid(row=0, column=3)

        self.height_size = Entry(self.root)
        self.height_size.grid(row=0, column=2)

        self.width_size = Entry(self.root)
        self.width_size.grid(row=1, column=2)

        self.paint_color = ''

        self.points = []

        self.luc = int()
        self.rdc = int()
        self.click_counter = int(0)
        self.isfigure = int(0)

        self.w_and_h_config = Button(self.root, text='подтвердить', command=self.change_size)
        self.w_and_h_config.grid(row=2, column=2)

        self.c = Canvas(self.root, bg='white', width=1000, height=750)
        self.c.grid(row=3, columnspan=5)
        self.setup()
        self.root.mainloop()
    def b2(self, event):
        if self.isfigure == 1:
            if self.click_counter == 0:
                self.luc = [event.x, event.y]
                self.click_counter = 1
            elif self.click_counter == 1:
                self.rdc = [event.x, event.y]
                self.click_counter = 0
                self.figure()
    def sqare_draw(self):
        self.points = [[0, 0], [1, 0], [1, 1], [0, 1]]
        self.isfigure = 1
        self.click_counter = 0
    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.root.bind('<Button-3>', self.b2)
    def change_size(self):
        if self.height_size.get().isdigit() and self.width_size.get().isdigit():
            self.c.config(height=self.height_size.get(), width=self.width_size.get())
            self.temp_width = int(self.width_size.get())
            self.temp_height = int(self.height_size.get())
    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]
    def clear(self):
        self.c.delete('all')
    def use_pen(self):
        self.activate_button(self.pen_button)
        self.isfigure = 0
    def figure(self):
        self.line_width = self.choose_size_button.get()
        if self.luc[0] > self.rdc[0]:
            a = self.luc[0]
            self.luc[0] = self.rdc[0]
            self.rdc[0] = a
        if self.luc[1] > self.rdc[1]:
            a = self.luc[1]
            self.luc[1] = self.rdc[1]
            self.rdc[1] = a
        deltax = self.rdc[0]-self.luc[0]
        deltay = self.rdc[1]-self.luc[1]
        self.paint_color = self.color
        for i in range(len(self.points)):
            self.c.create_line(self.points[i][0]*deltax+self.luc[0], self.points[i][1]*deltay+self.luc[1],
                              self.points[(i+1)%len(self.points)][0]*deltax+self.luc[0], self.points[(i+1)%len(self.points)][1]*deltay+self.luc[1],
                              width=self.line_width, fill=self.paint_color, capstyle=ROUND, smooth=TRUE, splinesteps=36)
    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)
        self.isfigure = 0
    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode
    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        if self.eraser_on:
            self.paint_color = 'white'
        else:
            self.paint_color = self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=self.paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y
    def reset(self, event):
        self.old_x, self.old_y = None, None
if __name__ == '__main__':
    Paint()
