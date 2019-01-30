import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class Window(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		menu = tk.Menu(self.master)
		master.config(menu=menu)
		file_menu = tk.Menu(menu)
		file_menu.add_command(label="Exit", command=self.quit)
		file_menu.add_command(label="Open", command=self.openFile)
		menu.add_cascade(label="File", menu=file_menu)
		analyze = tk.Menu(menu)
		self.canvas = tk.Canvas(self)
		self.canvas.pack(fill=tk.BOTH, expand=True)
		self.image = None

	def openFile(self):
		filename = filedialog.askopenfilename(initialdir=os.getcwd())
		if not filename:
			return
		b_string = get_binary_sting(filename)
		img = create_image(b_string)
		img.save('./test1.bmp')
		load = Image.open('test1.bmp')
		w, h = load.size
		self.render = ImageTk.PhotoImage(load)
		if self.image is not None:
			self.canvas.delete(self.image)
		self.image = self.canvas.create_image((w / 2, h / 2), image=self.render)


def main():
	root = tk.Tk()
	root.geometry("%dx%d" % (640, 480))
	root.title("BMP Image GUI")
	app = Window(root)
	app.pack(fill=tk.BOTH, expand=1)
	root.mainloop()

def create_image(b_string):
	bin_iter = iter(b_string)
	img = Image.new(mode='1', size = (640, 480))
	pixels = img.load()
	for i in range(img.size[1]):
		for j in range(img.size[0]):
			try:
				bit = bin_iter.__next__()
			except StopIteration:
				return img
			if bit == '1':
				pixels[j, i] = 1
	return img


def get_binary_sting(path):
	file = open(path, mode='rb')
	content = file.read()
	b_data = bytes(content)
	b_string = ""
	for byte in b_data:
		b_string += '{:08b}'.format(byte)
	return b_string


if __name__ == "__main__":
	main()