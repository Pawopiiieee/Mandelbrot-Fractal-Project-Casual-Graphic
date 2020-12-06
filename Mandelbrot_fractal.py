
# Coordinate point. PLEASE DON'T CHANGE, otherwise the little boi will get chubby shape 
a_min = -2.10  # axis ranges:                                 
a_max = 1.15  # a horizontal, real numbers part
b_min = -1.80  # b vertical, imaginary numbers part
b_max = 1.60   #We could make the user have a distort button of some sorts if we do wanna mess with it

# window scales can be altered
window_width = 600  # in pixels
window_height = 600

def mandelbrotSet(x_mdb, y_mdb,max_iterations): 
    # Escape part comes from ||z||^2 = x^2 + y^2 , iterate x*x + y*y  <= 4 or until max_iteration
    # starting point at x,y(0,0)
	# Recursive Function added, no more hard code
    def recur_mandelbrot(x,y,iteration_count):
        equation = pow(x,2) - pow(y,2)  + x_mdb 
        y = 2*x*y + y_mdb
        x = equation
        iteration_count += 1
        if pow(x,2) + pow(y,2) <= 4 and iteration_count < max_iterations:
            return recur_mandelbrot(x,y,iteration_count)
        else:
            return iteration_count 

    mandelbrot_value = recur_mandelbrot(0,0,0) #the intial values for x,y,iteration_count = 0
    return mandelbrot_value


"""
project range on window
a_axis is list of coordinates -2.10  and 1.15 divided over window size pixels
"""
def draw_mdb(max_iterations):
    a_axis = []  # list of points on the real number axis
    b_axis = []  # list of points on the imaginary number axis
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

    #Calculation part contained the lists of complex numbers + iterations
    present_iterations = set()  # To find numbers of current iterations.
    iteration_list = []  # list of coordinates on complex numbers and number of iterations on that point
    tu_extending = ()  # tuple with complex numbers and iterations for extending iterList
    for i in range(len(b_axis)):
        k = len(b_axis) - (i + 1)

        for j in range(len(a_axis)):
            iters = mandelbrotSet(a_axis[j], b_axis[k],max_iterations)
            tu_extending = ()
            tu_extending = (a_axis[j], b_axis[k], iters)
            iteration_list.append(tu_extending)

            if iters not in present_iterations:
                present_iterations.add(iters)

    highest_iteration = max(present_iterations)  # highest and lowest iteration numbers
    lowest_iteration = min(present_iterations)
    iter_range = (highest_iteration - lowest_iteration)
    return (iteration_list, iter_range) #both of them are going to pass through another function




# Draw picture.
from math import *
from tkinter import *

mandelBrot = Tk()
mandelBrot.geometry('600x600')
mandelBrot.title("The Mandelbrot Fractal with Python")

mandelbrotDisplay = Canvas(mandelBrot, bd=0, height=window_height, width=window_width)

point_previous = a_min  # To keep track of the end of a pixel line in the window
point_current = 0

def print_function(red_indicator,green_indicator, blue_indicator,point_previous):     #this draws the mandelbrot set.. It is very slow now
	mandelbrotDisplay.delete("all")     #removes the previous mandelbrot so you don't draw over it, I think this will make it more stable and will speed it up
	x = 2
	y = 3
	try:
		max_iterations=int(iteration_entry.get())
	except:
		max_iterations=20
	todo_rename_later = draw_mdb(max_iterations)
	iteration_list=todo_rename_later[0]
	iter_range=todo_rename_later[1]
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

		red_color = log(numberOfIters, iter_range)*  red_indicator
		green_color = log(numberOfIters, iter_range) * green_indicator
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

		mandelbrotDisplay.create_rectangle(point_plot, fill=tk_rgb, outline="yellow", width=0)

	mandelbrotDisplay.pack()        #This displays the just made mandelbrot
	print("Succssfully DONE")

print("Test the Mandelbrot with Python")

def red():		#These change the color in the mandelbrot set. Changing the color takes a lot of time, but works
	start_button.forget()
	print_function(255,0,0,a_min)	#the numbers represent the rgb
	print("red")

def yellow():
	start_button.forget()
	print_function(255,255,0,a_min)
	print("yellow")

def purple():
	start_button.forget()
	print_function(98,0,58,a_min)
	print("purple")

def start():            #the start button makes a white mandelbrot and makes the settings window appear
	start_button.forget()
	print_function(255,255,255,a_min)
	print("white")


settings=Tk()		#new window for the user to choose different settings like color
settings.title('Settings')
color_label=Label(settings,text='Choose a color')
 
color_label.grid(row=0,column=0)
red_button=Button(settings,bg='red',text='RED',fg='red',width=12,command=red,activeforeground='dark red',activebackground='dark red')		    #a red button, starting the function red()
red_button.grid(row=2,column=1)
yellow_button=Button(settings,bg='yellow',width=12,fg='yellow',text='YELLOW',activeforeground='gold',command=yellow,activebackground='gold')  	#a yellow button, starting the function yellow()
yellow_button.grid(row=2,column=0)                                                              
purple_button=Button(settings,bg='#62003a',width=12,fg='#62003a',text='PURPLE',activeforeground='#43002d',command=purple,activebackground='#43002d')	#a purple button, starting the function purple()
purple_button.grid(row=2,column=2)

iteration_label1=Label(settings,text='Amount of itterations, Lowering it will increase the speed, but decrease the quality)')
                                        #Gotta find a way to make the label spand over multiple columns
                                        #Maybe some of y'all can help out?

iteration_entry=Entry(settings)             #a useless entry. I will have the user put in the amount of itterations
iteration_label1.grid(row=3,column=0, columnspan =3)
iteration_entry.grid(row=4)

start_button=Button(mandelBrot,text='start',command=start)
start_button.pack()

mandelBrot.mainloop()

settings.mainloop()

