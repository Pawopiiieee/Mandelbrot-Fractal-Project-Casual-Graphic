from math import *
from tkinter import *
import time
begin = time.time()

mandelBrot = Tk()
mandelBrot.geometry('400x200')
mandelBrot.title("The Mandelbrot Fractal with Python")

# window scales can be altered
window_width = 650  # in pixels
window_height = 650
mandelbrotDisplay = Canvas(mandelBrot, bd=0, height=window_height, width=window_width)
# Coordinate point. PLEASE DON'T CHANGE, otherwise the little boi will get chubby shape 
a_min = -2.10  # axis ranges:                                 
a_max = 1.15  # a horizontal, real numbers part
b_min = -1.80  # b vertical, imaginary numbers part
b_max = 1.7   #We could make the user have a distort button of some sorts if we do wanna mess with it

"""
3D (Incompleted)
def mandelbrotSet(x_mdb, y_mdb,z_mdb):
	#comes from ||z||^2 = x^2 + y^2 , iterate x*x + y*y  <= 4 or until max_iteration
	#starting point at x,y(0,0)

	max_iteration = 20

	def recur_mandelbrot(x,y,z,iteration_count):
		equation = pow(x,2) - pow(y,2)  + x_mdb 
		y = 2*x*y + y_mdb
		x = equation * 0.5
		z = 2*x*y + z_mdb
		if pow(x,2) + pow(y,2) + pow(z,2)<= 4 and iteration_count < max_iteration:
			return recur_mandelbrot(x,y,z,iteration_count+1)
		else:
			return iteration_count 

	x = 0
	y = 0
	z = 0

	mandelbrot_value = recur_mandelbrot(x,y,z,0)          
	
	return mandelbrot_value
"""
"""
Use strategy pattern for the Mandelbrot 
so it could be easier to program the varient calculation/escape part 
in case we want to add more feature to it
"""
class MandelbrotStrategy():
	def mdb_calculation(self,x_mdb,y_mdb,x,y):
		return (x,y)

class Strategy_Z10(MandelbrotStrategy): #when z^10 => (x+yi)^10 + c
	def mdb_calculation(self, x_mdb, y_mdb, x, y):
		equation_x = pow(x,10) - 45*pow(x,8)*pow(y,2) + 210*pow(x,6)*pow(y,4) - 210*pow(x,4)*pow(y,6) + 45*pow(x,2)*pow(y,8) - pow(y,10) + x_mdb
		y = 10*pow(x,9)*y + 10*x*pow(y,9) - 120*pow(x,3)*pow(y,7) - 120*pow(x,7)*pow(y,3) + 252*pow(x,5)*pow(y,5)+ y_mdb 
		x = equation_x
		return (x, y)
class Strategy_Z5(MandelbrotStrategy): #when z^5 => (x+yi)^5 + c
	def mdb_calculation(self, x_mdb, y_mdb, x, y):
		equation_x = pow(x,5) - 10*pow(x,3)*pow(y,2) + 5*x*pow(y,4) + x_mdb
		y = pow(y,5) - 10*pow(x,2)*pow(y,3) +5*pow(x,4)*y+ y_mdb 
		x = equation_x
		return (x, y)
class Strategy_Z4(MandelbrotStrategy): #when z^4 => (x+yi)^4 + c
	def mdb_calculation(self, x_mdb, y_mdb, x, y):
		equation_x = pow(x,4) - 6*pow(x,2)*pow(y,2) + pow(y,4) + x_mdb
		y = 4*pow(x,3)*y - 4*x*pow(y,3)+ y_mdb 
		x = equation_x
		return (x, y)
class Strategy_Z3(MandelbrotStrategy): #when z^3 => (x+yi)^3 + c
	def mdb_calculation(self, x_mdb, y_mdb, x, y):
		equation_x = pow(x,3) - 3*x*pow(y,2)  + x_mdb
		y = -pow(y,3) +3*y*pow(x,2)+ y_mdb 
		x = equation_x
		return (x, y)
class Strategy_Z2(MandelbrotStrategy): #when z^2 => (x+yi)^2 + c
	def mdb_calculation(self, x_mdb, y_mdb, x, y):
		equation_x =  pow(x,2) - pow(y,2)    + x_mdb 
		y = 2*x*y + y_mdb
		x = equation_x  
		return (x, y)

class Strategy_Surprised(MandelbrotStrategy): #when z + z^5 => (x+yi) + (x+yi)^5 + c
	def mdb_calculation(self, x_mdb, y_mdb, x, y):
		equation_x =  x+pow(x,5) - 10*pow(x,3)*pow(y,2) + 5*x*pow(y,4)    + x_mdb 
		y = y+pow(y,5)-10*pow(x,2)*pow(y,3)+5*pow(x,4)*y + y_mdb
		x = equation_x
		return (x, y) 
strategy = Strategy_Z2()
"""     
Escape part comes from ||z||^2 = x^2 + y^2 , iterate x*x + y*y  <= 4 or until max_iteration
starting point at x,y(0,0)
Recursive Function added, no more hard code
This whole function could be used for 3D Mandelbulb, made for z axis extension. 
"""
def mandelbrotSet(x_mdb, y_mdb,max_iterations, strategy): 

	def recur_mandelbrot(x,y,iteration_count):

		(x,y) = strategy.mdb_calculation(x_mdb, y_mdb, x, y)

		iteration_count += 1

		if pow(x,2) + pow(y,2) <= 4 and iteration_count < max_iterations:
			return recur_mandelbrot(x,y,iteration_count)
		else:
			return iteration_count 

	mandelbrot_value = recur_mandelbrot(0,0,0) #the intial values for x,y,iteration_count = 0
	return mandelbrot_value


"""
To project range on window

"""
def draw_mdb(max_iterations):
	global strategy

	a_axis = []  # list of points on the real number axis
	b_axis = []  # list of points on the imaginary number axis
	step_a = (a_max - a_min) / (window_width) # coordinates between each pixel
	step_b = (b_max - b_min) / (window_height)  # coordinates between each pixel
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
			iters = mandelbrotSet(a_axis[j], b_axis[k],max_iterations, strategy)
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
point_previous = a_min  # To keep track of the end of a pixel line in the window
point_current = 0

def get_max_iter():
	
	try:
		max_iterations=int(iteration_entry.get())
	except:
		max_iterations = 20
	return max_iterations
"""
this function will take the value from drop down box 
for number of exponent for the Mandelbrot Set (2,3,4,5,10)
"""
def get_strategy_from_selection(selection): 
	global strategy
	#selection = variable.get()
		
	if selection == str(10):
		strategy = Strategy_Z10()
	elif selection == str(5):
		strategy = Strategy_Z5()
	elif selection == str(4):
		strategy = Strategy_Z4()
	elif selection == str(3):
		strategy = Strategy_Z3()
	else:
		strategy = Strategy_Z2()


def print_function(red_indicator,green_indicator, blue_indicator):     #this draws the mandelbrot set..
	global a_min, point_previous, color
	mandelbrotDisplay.delete("all")     #removes the previous mandelbrot so you don't draw over it, I think this will make it more stable and will speed it up

	x = 0
	y = 0
	max_iter=get_max_iter()
	to_draw = draw_mdb(get_max_iter())
	iteration_list=to_draw[0]
	iter_range=to_draw[1]
	for point in iteration_list:
		point_current = point[0]  # point on real number

		if point_current >= point_previous:
			x += 1
			numberOfIters = point[2]  # numbers of iterations

		else:  # new line starts
			x = 0
			y += 1
			numberOfIters = point[2]  # point on imaginary numbers
		
#		if color==red:                  gives you checkers
#			if i>20:
#				green_indicator=255
#				if i>40:
#					green_indicator=0
#					i=0
		
		rainbow=((255,50,50),(255,130,255),(100,100,255),(80,255,80),(255,255,0),(255,170,0))
		if color=='rainbow':
			if numberOfIters<max_iter:
#				if numberOfIters<23:
				red_color =rainbow[numberOfIters%6][0]
				green_color =rainbow[numberOfIters%6][1]
				blue_color =rainbow[numberOfIters%6][2]
#			else:
#				red_color = 0	#to avoid confetti, the middle turns gray/black
#				green_color = 0
#				blue_color = log(numberOfIters, iter_range)*50
			else:
				red_color=0
				green_color=0
				blue_color=0
		else:
			red_color=log(numberOfIters, iter_range)*red_indicator
			green_color=log(numberOfIters, iter_range)*green_indicator
			blue_color=log(numberOfIters, iter_range)*blue_indicator

		point_previous = point_current
		point_plot = [x, y, x, y]  # 2D mandelbrot

		red_color = int(red_color)
		green_color=int(green_color)
		blue_color=int(blue_color)
		if red_color>255:
			red_color=255
		if green_color>255:
			green_color=255
		if blue_color>255:
			blue_color=255
		tk_rgb = "#%02x%02x%02x" % (red_color, green_color, blue_color)

		mandelbrotDisplay.create_rectangle(point_plot, fill=tk_rgb, outline="yellow", width=0)

		
	mandelbrotDisplay.grid(row=0, column=0)        #This displays the just made mandelbrot
	print("Succssfully DONE")

"""
try rough zoom in / out
For the zoom function, it's just a rought one. Also the scale for y-axis is up side down. Thus, this needs to be fixed
FYI, I'm thinking about the redrawing part. Not sure if it successfully works, prolly I'll debug and see next week
"""
zoom_zoom = 5

def compute_zoom(cen_x,cen_y):
	global a_min,a_max,b_min,b_max,zoom_zoom

	new_width = abs(a_max - a_min) / float(zoom_zoom)
	new_height = abs(b_max - b_min) / float(zoom_zoom)
	mouse_x = (cen_x / float(window_width)) * abs(a_max-a_min) + a_min
	mouse_y = -((cen_y / float(window_height)) * abs(b_max-b_min) + b_min) #fixed

	zoom_rect = [0,0,0,0]
	zoom_rect[0] = mouse_x - (new_width / float(zoom_zoom))
	zoom_rect[1] = mouse_y - (new_height / float(zoom_zoom))
	zoom_rect[2] = mouse_x + (new_width / float(zoom_zoom))
	zoom_rect[3] = mouse_y + (new_height / float(zoom_zoom))

	return zoom_rect

def move_point(event):
	global mandelbrotDisplay, window_height,window_width,zoom_rect
	half_width = (window_width / zoom_zoom) / 3
	half_height = (window_height / zoom_zoom) / 3

	mandelbrotDisplay.delete("all")
	zoom_rect = mandelbrotDisplay.create_rectangle(event.x-half_width,event.y - half_height,event.x+half_width,event.y+half_height, width = 1)

def zoom(event):
	global a_max,a_min,b_max,b_min,color

	react = compute_zoom(event.x,event.y)
	a_min = react[0]
	b_min = react[1]
	a_max = react[2]
	b_max = react[3]   
	draw_mdb(get_max_iter())   #let's redraw a fractal , but it didn't work :/
	if color=='red':
		red()
	elif color=='white':
		start()
	elif color=='rainbow':
		rainbow()
	elif color=='purple':
		purple()
	elif color=='yellow':
		yellow()
	else:
		print("Error in zooming and colors")

zoom_rect = mandelbrotDisplay.create_rectangle(0,0,0,0)
mandelbrotDisplay.bind('<Button-1>',zoom)
mandelbrotDisplay.bind('<Button-2>',move_point)

def red():		#These change the color in the mandelbrot set.
	global color
	color='red'
	clean_start()	#removes the names etc. from the startscreen
	print("red")	#To know you pushed the button
	print_function(255,0,0)	#the numbers represent the rgb

def yellow():
	global color
	color='yellow'
	clean_start()
	print_function(255,255,0)
	print("yellow")

def purple():
	global color
	color='purple'
	clean_start()
	print_function(98,0,58)
	print("purple")


def rainbow():
	global color
	color='rainbow'
	clean_start()
	print_function(666,0,0) #I put in 666 because we don't need rgb
	print("rainboww")


def start():            #the start button makes a white mandelbrot (and will make the settings window appear)
	global color
	color='white'
	clean_start()
	print_function(255,255,255)
	print("white")

def surprised_mdb(): #this surprised Mandelbrot Fractal will take iteration = 20, rainbow color
	global strategy, color
	color='rainbow'
	clean_start()
	strategy = Strategy_Surprised()
	print_function(666,0,0)
	print("SURPRISED")


'''
#beginning of colorpicker, Dini made this, I'll save it here till I work on it						
def color():
    clean_start
    my_color = colorchooser.askcolor()
    return mandelbrotDisplay.grid(row=1)
'''
def clean_start():
	mandelBrot.geometry('650x650')
	start_button.grid_forget()
	Dini_Abdullahi.grid_forget()
	Myrthe_Post.grid_forget()
	Paworapas_Kakhai.grid_forget()
	Robin_Tollenaar.grid_forget()
	created_by.grid_forget()
	title.grid_forget()

settings=Tk()		#new window for the user to choose different settings like color
settings.title('Settings')

'''Color Buttons'''
color_label=Label(settings,text='Choose a color')
color_label.grid(row=0,column=0)

red_button=Button(settings,bg='red',text='RED',fg='red',width=12,command=red,activeforeground='dark red',activebackground='dark red')		    #a red button, starting the function red()
red_button.grid(row=2,column=1)

yellow_button=Button(settings,bg='yellow',width=12,fg='yellow',text='YELLOW',activeforeground='gold',command=yellow,activebackground='gold')  	#a yellow button, starting the function yellow()
yellow_button.grid(row=2,column=0)                                                              

purple_button=Button(settings,bg='#62003a',width=12,fg='#62003a',text='PURPLE',activeforeground='#43002d',command=purple,activebackground='#43002d')	#a purple button, starting the function purple()
purple_button.grid(row=2,column=2)

rainbow_button=Button(settings,bg='#969696',width=12,fg='#3058d1',text='RAINBOW',activeforeground='#323232',command=rainbow,activebackground='#323232')	#a purple button, starting the function purple()
rainbow_button.grid(row=3,column=0)

'''Entry for iterations'''
iteration_label1=Label(settings,text='Amount of itterations, Lowering it will increase the speed, but decrease the quality)')
iteration_entry=Entry(settings)

iteration_label1.grid(row=4,column=0, columnspan =5)
iteration_entry.grid(row=5)

'''label for zoom'''
zoom_label=Label(settings,text="click the fractal to zoom in(takes a long time, be patient. This is still in alpha)")
zoom_label.grid(row=6,column=0,columnspan=5)

'''label for exponent '''
exp_option = ["2", "3", "4", "5", "10"] 
variable = IntVar(settings)
variable.set(exp_option[0])
menu_option = OptionMenu(settings,variable, *exp_option,command=get_strategy_from_selection)
option_label = Label(settings,text= " Input the Exponent for the Mandelbrot Set")
option_label.grid(row = 9, column = 0)
menu_option.grid(row = 9, column = 1)

'''label for surprised fractal''' #Incase a user is curious about the mandelbrot
surprised_button=Button(settings,bg='#969696',width=15,fg='#003333',text='Surprised Me',activeforeground='#323232',command=surprised_mdb)
surprised_button.grid(row=11,column=2)
surprised_label = Label(settings,text= " Do you want to see the secret surprise? Just click here!")
surprised_label.grid(row = 11, column = 0,columnspan=2)



'''starting screen'''
title=Label(mandelBrot,text='MANDELBROT FRACTAL PROJECT')
title.grid(row=0,column=1)
start_button=Button(mandelBrot,text='start',command=start)
start_button.grid(row=1,column=1)

created_by=Label(mandelBrot,text='Created by')
created_by.grid(row=2,column=0)

Dini_Abdullahi=Label(mandelBrot,text='Dini Abdullahi ME2',fg='blue')
Dini_Abdullahi.grid(row=3,column=0)
Myrthe_Post=Label(mandelBrot,text='Myrthe Post ME1',fg='blue')
Myrthe_Post.grid(row=4,column=0)
Paworapas_Kakhai=Label(mandelBrot,text='Paworapas Kakhai ME1',fg='blue')
Paworapas_Kakhai.grid(row=5,column=0)
Robin_Tollenaar=Label(mandelBrot,text='Robin Tollenaar ME1',fg='blue')
Robin_Tollenaar.grid(row=6,column=0)


end_time = time.time()
print("Test the Mandelbrot with Python")
total = end_time - begin
print ("Total time consumption = ", total)
mandelBrot.mainloop()

settings.mainloop()