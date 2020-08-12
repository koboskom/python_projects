from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import matplotlib.cm as cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from src import network2, load_image, multiple_digits


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Recognize handwritten digits")
        self.minsize(500, 400)
        self.labelFrame = LabelFrame(self, text="Otwórz plik")
        self.labelFrame.grid(column=1, row=1, padx=20, pady=20)
        self.button1()
        self.button2()
        self.label_file = ttk.Label(self.labelFrame, text="")
        self.label_result = ttk.Label(self.labelFrame, text="")
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.net = network2.load('../data/network_params')

    def button1(self):
        self.button = ttk.Button(self.labelFrame, text="Wybierz obrazek",
                                 command=lambda: [self.file_search(), self.button3()])
        self.button.grid(column=1, row=1)

    def button2(self):
        self.button = ttk.Button(self.labelFrame, text="Wybierz obrazek z wieloma cyframi",
                                 command=lambda: [self.file_search_many_digits(), self.button4()])
        self.button.grid(column=1, row=6)

    def button3(self):
        if self.filename != '':
            self.button = ttk.Button(self.labelFrame, text="Sprawdź",
                                     command=lambda: [self.show_result()])
            self.button.grid(column=1, row=9)

    def button4(self):
        if self.filename != '':
            self.button = ttk.Button(self.labelFrame, text="Sprawdź",
                                     command=lambda: [self.show_result_many_digits()])
            self.button.grid(column=1, row=9)

    def show_result(self):
            self.label_result.grid(column=1, row=11)
            self.label_result.configure(text='')
            test_data = load_image.data_from_image(self.filename)
            result = self.net.network_result(test_data)
            self.label_result.configure(text="Rozpoznana cyfra: " + str(result[0]))

    def show_result_many_digits(self):
            self.label_result.grid(column=1, row=11)
            self.label_result.configure(text='')
            test_data = multiple_digits.chooseImage(self.filename)
            result = self.net.network_result(test_data=test_data)
            text = "Rozpoznane cyfry:"
            for x in result:
                text += " " + str(x)
            self.label_result.configure(text=text)
            multiple_digits.chooseImage("{}".format(self.filename), self.net)

    def file_search(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Wybierz obrazek",
                                                   filetype=(("png", "*.png"), ("jpg", "*.jpg"), ("All files", "*.*")))
        if self.filename != '':
            self.label_file.grid(column=1, row=2)
            self.label_file.configure(text='')
            self.label_file.configure(text='Wybrano plik: ' + self.filename)
            train_x = load_image.data_from_image("{}".format(self.filename))[0]
            self.fig.clear()
            a = self.fig.add_subplot(111)
            a.imshow(train_x.reshape((28, 28)), cmap=cm.Greys_r)
            canvas = FigureCanvasTkAgg(self.fig, master=self)
            canvas.get_tk_widget().grid(row=3, column=0, columnspan=3, rowspan=20)
            canvas.draw()

    def file_search_many_digits(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Wybierz obrazek z wieloma cyframi",
                                                   filetype=(("png", "*.png"), ("jpg", "*.jpg"), ("All files", "*.*")))
        if self.filename != '':
            self.label_file.grid(column=1, row=2)
            self.label_file.configure(text='Wybrano plik: ' + self.filename)
            train_x = multiple_digits.chooseImage("{}".format(self.filename))
            x = len(train_x)
            self.fig.clear()
            for i in range(x):
                a = self.fig.add_subplot(1, x, i + 1)
                a.imshow(train_x[i].reshape((28, 28)), cmap=cm.Greys_r)
            canvas = FigureCanvasTkAgg(self.fig, master=self)
            canvas.get_tk_widget().grid(row=3, column=0, columnspan=3, rowspan=20)
            canvas.draw()


if __name__ == '__main__':
    root = Root()
    root.mainloop()
