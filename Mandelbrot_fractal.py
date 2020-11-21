def mandelbrotSet(x_mdb, y_mdb):
	#comes from ||z||^2 = x^2 + y^2 , iterate x*x + y*y  <= 4 or until max_iteration
    #starting point at x,y(0,0)

	x = 0
	y = 0

	iteration = 0
	max_iteration = 500
	
	while (x*x + y*y  <= 4 and iteration < max_iteration ):
		equation = x*x - y*y + x_mdb 
		y = 2*x*y + y_mdb
		x = equation
		iteration += 1
	
	if (iteration == max_iteration):
		iterations = max_iteration
	else:
		iterations = iteration
	
	return(iterations)

# Coordinate point. PLEASE DONT CHANGE, otherwise the little boi will get chubby shape
a_min = -2.10			# axis ranges:
a_max = 1.15				# a horizontal, real numbers part
b_min = -1.80			# b vertical, imaginary numbers part
b_max = 1.60

#window scales can be altered

window_width = 600	# in pixels
window_height = 600

iteration_list=[]			# list of coordinates on complex numbers and number of iterations on that point
a_axis = []		# list of points on the real number axis
b_axis = []		# list of points on the imaginary number axis
tu_extending=()		# tuple with complex numbers and iterations for extending iterList

"""
project range on window
a_axis is list of coordinates -2.10  and 1.15 divided over window size pixels
"""

step_a = (a_max - a_min) / window_width		# coordinates between each pixel
step_b = (b_max - b_min) / window_height    # coordinates between each pixel
temporary = a_min  #temporary variable to store values of a_min
while temporary < a_max:
	a_axis = a_axis + [temporary]
	temporary += step_a
temporary = b_min  #temporary variable to store values of b_min 
while temporary < b_max:
	b_axis = b_axis + [temporary]
	temporary += step_b



"""Calculation part contained the lists of complex numbers + iterations"""

present_iterations = set()	# To find numbers of current iterations.

for i in range(len(b_axis)):
	k = len(b_axis) - (i+1)

	for j in range(len(a_axis)):
		iters = mandelbrotSet(a_axis[j],b_axis[k])
		tu_extending=()
		tu_extending = (a_axis[j],b_axis[k],iters)		
		iteration_list.append(tu_extending)

		if iters not in present_iterations:
			present_iterations.add(iters)
			
highest_iteration = max(present_iterations)		# highest and lowest iteration numbers
lowest_iteration = min(present_iterations)

colour_step = int(255/(highest_iteration - lowest_iteration))		# divide 255 colours linearly over the found iteration range
iter_range = (highest_iteration - lowest_iteration)

# Draw picture.
from math import *				
from tkinter import *			

mandelBrot = Tk()
mandelBrot.title("Mandelbrot Set with Python")

mandelbrotDisplay = Canvas(mandelBrot, bd=0, height = window_height, width = window_width)

point_previous = a_min		# To keep track of the end of a pixel line in the window
point_current = 0

"""offset"""
x=2		
y=3

"""
Loop 
"""
for point in iteration_list:
	point_current = point[0] #point on real number

	if point_current >= point_previous:	
		x += 1
		numberOfIters = point[2] # numbers of iterations

	else:						# new line starts
		x = 3
		y += 1
		numberOfIters = point[2] #point on imaginary numbers

	point_previous = point_current
	point_plot = [x, y, x, y] #2D mandelbrot

	colour = log(numberOfIters, iter_range) * 255		

	colour = int(colour)
	if colour > 255:
		colour = 255
       
	tk_rgb = "#%02x%02x%02x" % (colour, 0, 0) #put green and blue color as 0 
	
	pixel = mandelbrotDisplay.create_rectangle(point_plot, fill=tk_rgb, outline="yellow", width=0)
print ('Test the Mandelbrot with python')
print ('Total Iterations', present_iterations)

mandelbrotDisplay.pack()
mandelBrot.mainloop()
