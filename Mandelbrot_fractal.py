''' IMPORTING TKINTER,MATH AND TIME '''
from tkinter import font
from math import *
from tkinter import *
import time
from tkinter import colorchooser
import math

begin = time.time()

'''BASIC TKINTER CODE TO CRATE THE WINDOWS'''
mandelBrot = Tk()
mandelBrot.geometry('400x200')
mandelBrot.title("The Mandelbrot Fractal with Python")
mandelBrot.configure(background='#f5f3cb')
#window scales can be altered
window_width = 650  # in pixels
window_height = 650
mandelbrotDisplay = Canvas(mandelBrot, bd=0, height=window_height, width=window_width)
# Coordinate point. PLEASE DON'T CHANGE, otherwise the little boi will get chubby shape 
a_min = -2.10  # axis ranges:                                 
a_max = 1.15  # a horizontal, real numbers part
b_min = -1.80  # b vertical, imaginary numbers part
b_max = 1.7   #We could make the user have a distort button of some sorts if we do wanna mess with it

#some variables for the color
red_indicator=0
green_indicator=0
blue_indicator=0

rotation = False

settings=Tk()		#new window for the user to choose different settings like color
settings.title('Settings')
settings.configure(background='#f5f3cb')
"""
3D (Incompleted)
def mandelbrotSet(x_mdb, y_mdb,z_mdb):
	#comes from ||z||^2 = x^2 + y^2 , iterate x*x + y*y  <= 4 or until max_iteration
	#starting point at x,y(0,0)
	max_iteration = 20
	def recur_mandelbrot(x,y,z,iteration_count): #with Homogeneity approach for projective coordinates
		equation = pow(x,2) - pow(y,2)  + x_mdb 
		y = 2*x*y + 2*y*x + y_mdb
		z = 2*y*z + z_mdb
		x = equation
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
To project range on window (aka. plot each pixel)
"""

def draw_mdb(max_iterations):
	global strategy,a_min,a_max,b_max,b_min
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

'''getting the max ammount of itterations so we know how many itterations to draw'''
def get_max_iter():
	try:
		max_iterations=int(iteration_entry.get()) #this gets the text given in the iteration entry. 
	except:                                       #If none is given or the text is not an ineger, the max iterations becomes 20
		max_iterations = 20
	return max_iterations
"""
this function will take the value from drop down box 
for number of exponent for the Mandelbrot Set (2,3,4,5,10)
"""
def get_strategy_from_selection(selection): 
	global strategy,exponent
	exponent=selection
	update_info(zoom_slider.get())
	if selection == str(10):       #selection is the number picked by the user
		strategy = Strategy_Z10()
	elif selection == str(5):
		strategy = Strategy_Z5()
	elif selection == str(4):
		strategy = Strategy_Z4()
	elif selection == str(3):
		strategy = Strategy_Z3()
	else:
		strategy = Strategy_Z2()

'''This code can use themes. Here isn't one color chosen. A tuple is filled with colors that matches the colors of the theme.'''
def color_theme(red_indicator,numberOfIters,max_iter,theme,length_theme):
	if numberOfIters<max_iter:
		red_color =theme[numberOfIters%length_theme][0]		#Here the color is assigned. Every iteration has it's own color.
		green_color =theme[numberOfIters%length_theme][1]	#using modulo, the iterations will keep getting colors, going through the tuple
		blue_color =theme[numberOfIters%length_theme][2]
	else:													#the last iteration will be black, because that is just cooler
		red_color=0
		green_color=0
		blue_color=0
	return red_color, green_color, blue_color

'''clean_start will remove all the text and buttons from the main window.'''
def clean_start():
	mandelBrot.geometry('650x650')	#rescaling the window so the drawing of the mandelbrot will fit
	start_button.grid_forget()		#removing the start button
	Dini_Abdullahi.grid_forget()	#removing the text labels
	Myrthe_Post.grid_forget()
	Paworapas_Kakhai.grid_forget()
	Robin_Tollenaar.grid_forget()
	created_by.grid_forget()
	title.grid_forget()
	start_Label.grid_forget()

i=1 # a variable to keep count of the ammount of times that the program has drawn

'''This is the main function drawing the mandelbrot'''

def print_function():
	global a_min, point_previous,i,red_indicator,green_indicator,blue_indicator, rotation
	print('amount of times drawn: {}'.format(i))	#To keep up/check the ammount of times drawn, making it easier to check if zoom if working
	if i==1:
		clean_start() #cleaning up the starting screen, but only the first time
	else:
		mandelbrotDisplay.delete("all")     #removes the previous mandelbrot so you don't draw over it
	if type(red_indicator)==str:			#if red_indicator is used as a variable for the themes, it is a string
		if red_indicator=='rainbow':
			theme=((255,50,50),(255,130,255),(100,100,255),(80,255,80),(255,255,0),(255,170,0))	#these are tuples filled with tuples containing rgb
		elif red_indicator=='blue_pink':														#every pair of 3 is one color
			theme=((155,79,150),(0,56,168),(212,20,110))										#these colors are the colors used in the themes
		elif red_indicator=='orange_purple':
			theme=((165,0,98),(214,41,0),(255,155,85),(255,255,255),(212,97,166),(165,0,98))
		len_theme=len(theme)
	x = 0
	y = 0
	max_iter=get_max_iter()
	to_draw = draw_mdb(get_max_iter())
	iteration_list=to_draw[0]
	iter_range=to_draw[1]

	for point in iteration_list:	#here starts the drawing of the brot, it draws every pixel one by one
		point_current = point[0]  # point on real number
		if point_current >= point_previous:
			x += 1
			numberOfIters = point[2]  # number of iterations
		else:  # new line starts
			x = 0
			y += 1
			numberOfIters = point[2]
		
		if type(red_indicator)==str:	#if red indicator is a string, than a theme must be used
			red_color, green_color, blue_color = color_theme(red_indicator,numberOfIters,max_iter,theme,len_theme)
		else:
			red_color=log(numberOfIters, iter_range)*red_indicator			#if a single color is choosen, the fist few iterations will be dark
			green_color=log(numberOfIters, iter_range)*green_indicator		#this is because the colors get a low value.the higher the iteration, the brighter the color
			blue_color=log(numberOfIters, iter_range)*blue_indicator		#the difference in darkness is smaller with a bigger max iterations
		point_previous = point_current
		point_plot = [x, y, x, y]  # 2D mandelbrot
		red_color = int(red_color)		#instead of using floats
		green_color=int(green_color)
		blue_color=int(blue_color)
		if red_color>255:		#making sure the code doesn't die if somehow the colors get a higher value than the max of 255
			red_color=255		#this code may be useless, look into if it can be removed, that would speed up the code
		if green_color>255:
			green_color=255
		if blue_color>255:
			blue_color=255
		tk_rgb = "#%02x%02x%02x" % (red_color, green_color, blue_color)		#turning the rgb into hex

		"""
		rotate the mandelbrot to make layer. This part can be manipulated for x or y axis rotation.
		But I'll leave it for further development due to limited resources. Plus, to be able to look 
		into 3D layer we need extra code for making camera, more vector calculation (//linear algebra)
		"""
		if rotation == True:
			color = log(numberOfIters, iter_range) * 255 		
			color = int(color)
			if color > 255 :
				color = 20
			tk_rgb = "#%02x%02x%02x" % (0, 15 , color)
			def rotate(x,y, degree,window_width,window_height):
				degree = math.radians(degree)
				cos_v = math.cos(degree)
				sin_v = math.sin(degree)
				cen_x = window_width
				cen_y = window_height
				new_points = []
				x -= cen_x #rotation point
				y -= cen_y #rotation point
				x_new = x * cos_v - y * sin_v
				y_new = x * sin_v + y * cos_v
				new_points.append([x_new + cen_x, y_new + cen_y,x_new + cen_x, y_new + cen_y])
				return new_points
		
			if color != 0:     #red_color != 0 or green_color != 0 or blue_color != 0:

				for i in range (0,10,2):	
					new_mdb = rotate(x,y,i, window_width,window_height)
					mandelbrotDisplay.create_rectangle(new_mdb, fill=tk_rgb, outline="#f5f3cb", width=0)
		else:
			mandelbrotDisplay.create_rectangle(point_plot, fill=tk_rgb, outline="#f5f3cb", width=0)	#creating a pixel that is filled with the correct color
		
	#if i == 1:
		mandelbrotDisplay.grid(row=0, column=0)        #This displays the just made mandelbrot
	print("Succssfully DONE")
	i+=1
	
"""
Shallow zoom in / out
"""

def compute_zoom(cen_x,cen_y):
	global a_min,a_max,b_min,b_max
	try:
		zoom_zoom=zoom_slider.get()
	except:
		zoom_zoom=3
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
	half_width = (window_width / zoom_zoom) / 12
	half_height = (window_height / zoom_zoom) / 12
	mandelbrotDisplay.delete("all")
	zoom_rect = mandelbrotDisplay.create_rectangle(event.x-half_width,event.y - half_height,event.x+half_width,event.y+half_height, width = 1)
def zoom(event):
	global a_max,a_min,b_max,b_min,red_indicator,green_indicator,blue_indicator
	react = compute_zoom(event.x,event.y)
	a_min = react[0]
	b_min = react[1]
	a_max = react[2]
	b_max = react[3]
	draw_mdb(get_max_iter())   #let's redraw a fractal , but it didn't work well. 
	print_function()
zoom_rect = mandelbrotDisplay.create_rectangle(0,0,0,0)
mandelbrotDisplay.bind('<Button-1>',zoom)
mandelbrotDisplay.bind('<Button-2>',move_point)

'''
COLOR FUNCTIONS

Here are the functions that the buttons call. If a function starts it will start out with calling some global variables. This is so when the mandelbrot draws again,
(like with zoom) the color indicators aren't forgotten. Then the color will be chosen. This will be printed so you can check that the button works. Then the
print_function will be called. This initialises the drawing of the mandelbrot
'''
exponent=2
color=None
def update_info(zoom):
	global exponent,color
	max_iter=get_max_iter()
	info=Label(settings,text='Color= {}, Exponent= {}, Amount of iterations= {}, Amount of zoom= {}'.format(color,exponent,max_iter,zoom),bg='#f5f3cb')
	info.grid(row=10,column=0,columnspan=3)

def start():
	global red_indicator,green_indicator,blue_indicator
	print_function()

def choose_color():
	global red_indicator,green_indicator,blue_indicator,rotation,color
	rotation = FALSE
	color_code = colorchooser.askcolor()
	print(color_code)
	red_indicator=int(color_code[0][0])
	green_indicator=int(color_code[0][1])
	blue_indicator=int(color_code[0][2])
	color=str( "#%02x%02x%02x" % (red_indicator, green_indicator, blue_indicator))
	update_info(zoom_slider.get())

def rainbow():
	global red_indicator,rotation,color
	rotation = FALSE
	red_indicator='rainbow'      #The red_indicator is used as a variable to store the theme. The fact that it is a string makes it so that the program doesn't draw one color.
	print("rainboww")
	color='rainbow'
	update_info(zoom_slider.get())

def blue_pink():
	global red_indicator,rotation
	rotation = FALSE
	red_indicator='blue_pink'
	print("Blue/Pink")
	update_info(zoom_slider.get())

def orange_purple():
	global red_indicator,rotation
	rotation = FALSE
	red_indicator='orange_purple'
	print("Orange_Purple")
	update_info(zoom_slider.get())

def white():            #the start button on the main window makes a white mandelbrot (and will make the settings window appear)
	global red_indicator,rotation,green_indicator,blue_indicator
	rotation = FALSE
	red_indicator=255
	green_indicator=255
	blue_indicator=255
	print("white")

def surprised_mdb(): #this surprised Mandelbrot Fractal will take iteration = 20, rainbow color
	global strategy, rotation,red_indicator
	rotation = FALSE
	strategy = Strategy_Surprised()
	red_indicator='rainbow'
	print("SURPRISED")
	update_info(zoom_slider.get())

def rotation(): #this rotation Mandelbrot Fractal will take iteration = 20 as defult, but it can be altered.
	global strategy,rotation #,red_indicator,green_indicator,blue_indicator
	rotation = True
	#red_indicator=0
	#green_indicator= 15
	#blue_indicator= 199
	strategy = Strategy_Z2() #the rotation makes layers only on Z^2. For another higher polynomials, it's skeptical 
	print("Layers", "Pancake Time!")
	print_function()

'''Color Buttons'''
color_label=Label(settings,text='Choose a color',  font= 'Helvetica 9 bold', padx = 2, pady = 1, bg = '#f5f3cb',height=2)
color_label.grid(row=0,column=0,columnspan=4,sticky=W)

rainbow_button=Button(settings,bg='#969696',width=15,fg='#3058d1',text='RAINBOW',activeforeground='#323232',command=rainbow,activebackground='#323232', relief = GROOVE,height=1 )	#a purple button, starting the function purple()
rainbow_button.grid(row=1,column=1,sticky=W)
blue_pink_button=Button(settings, bg='#990099',width=15,text='Blue/Pink',command=blue_pink,height=1)
blue_pink_button.grid(row=1,column=2,sticky=W)
orange_purple_button=Button(settings, bg='#A50062',width=15,text='Orange/Purple',command=orange_purple,height=1)
orange_purple_button.grid(row=1,column=3,sticky=W)
'''Button for choosing a color, a colorwindow will pop up'''
color_chooser_button = Button(settings, text = "Select color",width=12 , command = choose_color, bg = '#f5f3cb' ,height=1) 
color_chooser_button.grid(row=1, column=0,sticky=W)
'''Entry for iterations'''
iteration_label1=Label(settings,text='Amount of itterations', bg = '#f5f3cb',height=2)
iteration_entry=Entry(settings,bg = 'white',width=12)
iteration_entry.grid(row=2,column=3,sticky=W)
iteration_label1.grid(row=2,column=0,columnspan=2,sticky=W)
'''labels and slider for zoom'''
zoom_label=Label(settings,text="Click the fractal to zoom in(Please, be patient.)", bg = '#f5f3cb',height=2)
zoom_label.grid(row=9,column=0,columnspan=5,sticky=W)
zoom_slider_label=Label(settings,text='Choose the ammount you want to zoom, 1 for zoom out.',bg='#f5f3cb',height=2)
zoom_slider_label.grid(row=8,column=0, columnspan=3,sticky=W)
zoom_slider=Scale(settings, from_=1,to=10,orient=HORIZONTAL,bg='#f5f3cb',command=update_info)
zoom_slider.grid(row=8,column=3,sticky=W)
zoom_slider.set(2)
'''exponent'''
exp_option = ["2", "3", "4", "5", "10"] 
variable = IntVar(settings)
variable.set(exp_option[0])
menu_option = OptionMenu(settings,variable, *exp_option,command=get_strategy_from_selection)
option_label = Label(settings,text= " Input the Exponent for the Mandelbrot Set", bg = '#f5f3cb',height=2)
menu_option.grid(row = 5, column = 3,sticky=W)
option_label.grid(row = 5, column = 0, columnspan=2,sticky=W)
menu_option.config(bg = '#f5f3cb')
'''label for surprised fractal''' #Incase a user is curious about the mandelbrot
surprised_button=Button(settings,bg='#f5f3cb',width=15,fg='#003333',text='Surprised Me',activeforeground='#323232',command=surprised_mdb,height=1)
surprised_button.grid(row=6,column=3,sticky=W)
surprised_label = Label(settings,text= " Do you want to see the secret surprise? Just click here!", bg = '#f5f3cb',height=2)
surprised_label.grid(row = 6, column = 0,columnspan=3,sticky=W)
'''label for Layers/3D''' #try 3D by rotation 
layer_button=Button(settings,bg='#969696',width=15,fg='#003333',text='Layers',activeforeground='#323232', command=rotation,height=1)
layer_button.grid(row=7,column=3,sticky=W)
layer_label = Label(settings,text= " An attempt to make 3D by adding layers. (draws immediately)", bg = '#f5f3cb',height=2)
layer_label.grid(row = 7, column = 0,columnspan=3,sticky=W)
'''starting button for settings window'''
start_button_settings=Button(settings,fg='#f5f3cb',width=10,bg='#9c9b8f',text='start',command=start,height=1)
start_button_settings.grid(row=10,column=3,sticky=W)

'''starting screen'''
title=Label(mandelBrot,text='MANDELBROT FRACTAL PROJECT', bg  = '#f5f3cb')
title.grid(row=0,column=1)
title.configure(font="Verdana 8 underline")
start_button=Button(mandelBrot,text='start',command=white, bg = '#f5f3cb', height = 2, width = 15, )
start_Label = Label(mandelBrot, text = " Start the mandelbrot:", bg = '#f5f3cb',  justify = CENTER)

start_Label.grid(row = 3, column = 1, )
start_button.grid(row=5,column=1, sticky = NS)

created_by=Label(mandelBrot,text='Created by:', bg = '#f5f3cb')
created_by.grid(row=2,column=0)


Dini_Abdullahi=Label(mandelBrot,text='Dini Abdullahi ME1',fg='blue', bg = '#f5f3cb',)
Dini_Abdullahi.grid(row=3,column=0)
Dini_Abdullahi.configure(font="Verdana 8 underline")
Myrthe_Post=Label(mandelBrot,text='Myrthe Post ME1',fg='blue',bg = '#f5f3cb')
Myrthe_Post.grid(row=4,column=0)
Myrthe_Post.configure(font="Verdana 8 underline")
Paworapas_Kakhai=Label(mandelBrot,text='Paworapas Kakhai ME1',fg='blue',bg = '#f5f3cb')
Paworapas_Kakhai.grid(row=5,column=0)
Paworapas_Kakhai.configure(font="Verdana 8 underline")
Robin_Tollenaar=Label(mandelBrot,text='Robin Tollenaar ME1',fg='blue',bg = '#f5f3cb')
Robin_Tollenaar.grid(row=6,column=0)
Robin_Tollenaar.configure(font="Verdana 8 underline")
end_time = time.time()
print("Test the Mandelbrot with Python")
total = end_time - begin
print ("Total time consumption = ", total)
mandelBrot.mainloop()
settings.mainloop()
