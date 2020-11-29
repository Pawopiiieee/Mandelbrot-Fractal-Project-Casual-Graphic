import sys

def mandelbrotSet(x_mdb, y_mdb, ):
    # comes from ||z||^2 = x^2 + y^2 , iterate x*x + y*y  <= 4 or until max_iteration
    # starting point at x,y(0,0)
    validInput = False
    while not validInput:

        try:
            x = 0
            y = 0

            iteration = 0
            max_iteration = 500      #lower this number to run the file faster

            while x * x + y * y <= 4 and iteration < max_iteration:
                equation = x * x - y * y + x_mdb
                y = 2 * x * y + y_mdb
                x = equation
                iteration += 1

            if iteration == max_iteration:
                iterations = max_iteration
            else:
                iterations = iteration

            return iterations
        except validInput:
            print("Invalid Input. Try again")


# Coordinate point. PLEASE DON'T CHANGE, otherwise the little boi will get chubby shape
a_min = -2.10  # axis ranges:
a_max = 1.15  # a horizontal, real numbers part
b_min = -1.80  # b vertical, imaginary numbers part
b_max = 1.60

# window scales can be altered

window_width = 600  # in pixels
window_height = 600

iteration_list = []  # list of coordinates on complex numbers and number of iterations on that point
a_axis = []  # list of points on the real number axis
b_axis = []  # list of points on the imaginary number axis
tu_extending = ()  # tuple with complex numbers and iterations for extending iterList

"""
project range on window
a_axis is list of coordinates -2.10  and 1.15 divided over window size pixels
"""

step_a = (a_max - a_min) / window_width  # coordinates between each pixel
step_b = (b_max - b_min) / window_height  # coordinates between each pixel
temporary = a_min  # temporary variable to store values of a_min
while temporary < a_max:
    a_axis = a_axis + [temporary]
    temporary += step_a
temporary = b_min  # temporary variable to store values of b_min
while temporary < b_max:
    b_axis = b_axis + [temporary]
    temporary += step_b

"""Calculation part contained the lists of complex numbers + iterations"""

present_iterations = set()  # To find numbers of current iterations.

for i in range(len(b_axis)):
    k = len(b_axis) - (i + 1)

    for j in range(len(a_axis)):
        iters = mandelbrotSet(a_axis[j], b_axis[k])
        tu_extending = ()
        tu_extending = (a_axis[j], b_axis[k], iters)
        iteration_list.append(tu_extending)

        if iters not in present_iterations:
            present_iterations.add(iters)

highest_iteration = max(present_iterations)  # highest and lowest iteration numbers
lowest_iteration = min(present_iterations)

colour_step = int(
    255 / (highest_iteration - lowest_iteration))  # divide 255 colours linearly over the found iteration range
iter_range = (highest_iteration - lowest_iteration)

# Draw picture.
from math import *
from tkinter import *

mandelBrot = Tk()
mandelBrot.title("Mandelbrot Set with Python")

mandelbrotDisplay = Canvas(mandelBrot, bd=0, height=window_height, width=window_width)

point_previous = a_min  # To keep track of the end of a pixel line in the window
point_current = 0


def print_function(red_indicator,green_indicator, blue_indicator, point_previous):     #this draws the mandelbrot set.. It is very slow now
	mandelbrotDisplay.delete("all")     #removes the previous mandelbrot so you don't draw over it, I think this will make it more stable and will speed it up
	x = 2
	y = 3
	for point in iteration_list:
		point_current = point[0]  # point on real number

		if point_current >= point_previous:
			x += 1
			numberOfIters = point[2]  # numbers of iterations

		else:  # new line starts
			x = 3
			y += 1
			numberOfIters = point[2]  # point on imaginary numbers

		point_previous = point_current
		point_plot = [x, y, x, y]  # 2D mandelbrot

		red_color = log(numberOfIters, iter_range) *  red_indicator
		green_color = log(numberOfIters, iter_range) *  green_indicator
		blue_color = log(numberOfIters, iter_range) *  blue_indicator

		red_color = int(red_color)
		green_color=int(green_color)
		blue_color=int(blue_color)
		if red_color>250:
			red_color=250
		if green_color>250:
			green_color=250
		if blue_color>250:
			blue_color=250
		tk_rgb = "#%02x%02x%02x" % (red_color, green_color, blue_color)

		pixel = mandelbrotDisplay.create_rectangle(point_plot, fill=tk_rgb, outline="yellow", width=0)
	mandelbrotDisplay.pack()        #This displays the just made mandelbrot
	print('done')

print('Test the Mandelbrot with python')
print('Total Iterations', present_iterations)
def red():		#These change the color in the mandelbrot set. Changing the color takes a lot of time, but works
	print_function(255,0,0,a_min)	#the numbers represent the rgb
	print("red")
def yellow():
	print_function(255,255,0,a_min)
	print("yellow")

def purple():
    print_function(98,0,58,a_min)
    print("purple")

def start():
	print_function(255,255,255,a_min)
	print("white")


settings=Tk()		#new window for the user to choose different settings like color
settings.title('Settings')
color_label=Label(settings,text='Choose a color')
 
color_label.grid(row=1,column=0)
red_button=Button(settings,bg='red',width=12,command=red,activebackground='dark red')		    #a red button, starting the function red()
red_button.grid(row=2,column=1)
yellow_button=Button(settings,bg='yellow',width=12,command=yellow,activebackground='gold')  	#a yellow button, starting the function yellow()
yellow_button.grid(row=2,column=0)                                                              
purple_button=Button(settings,bg='#62003a',width=12,command=purple,activebackground='#43002d')	#a purple button, starting the function purple()
purple_button.grid(row=2,column=2)

start_button=Button(settings,text='start',command=start)
start_button.grid(row=0)



mandelBrot.mainloop()
'''OwO'''
settings.mainloop()

# This is the zoom function but doesnt work right now. to be updated
""""
def zoom(mouse_x, mouse_y, width, height, zoom_x, zoom_y, calculate=None):
    start_x = mouse_x - zoom_x
    end_x = mouse_x + zoom_x
    start_y = mouse_y - zoom_y
    end_y = mouse_y + zoom_y
    x = 0
    y = 0

    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    with open('results.txt', 'r') as f:
        for line in f:
            if x % width == 0:
                x = 0
                y += 1

            # Checks if line in file matches a vertex of the zoom
            # rectangle and sets 
            if x == start_x and y == start_y:
                point = line.split(',')
                min_x = float(point[1])
                min_y = float(point[2])
            elif x == end_x and y == end_y:
                point = line.split(',')
                max_x = float(point[1])
                max_y = float(point[2])

            x += 1

    calculate.find_points(width, height, min_x, max_x, min_y, max_y)
"""""
