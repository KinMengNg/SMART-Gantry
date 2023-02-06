import turtle
  
# creating turtle pen
t = turtle.Turtle()


#hide the turtle(cursor)
t.hideturtle()

#Set speed to be fast
t.speed(0)

#Start with pen up
t.up()

#To create a gantyr object, each gantry is one object
class Gantry():
    def __init__(self, center_coordinate):
        #coordinate is a tuple (x,y)
        self.radius = 5

        self.x = center_coordinate[0]
        self.y = center_coordinate[1]

    def change_to_green(self):
        #make turtle go to center coordinate
        t.goto(self.x, self.y)

        #put pen down
        t.down()
        
        # set the fillcolor
        t.fillcolor("green") 
        
        # start the filling color
        t.begin_fill()
        
        # drawing the circle of radius r
        t.circle(self.radius)
        
        # ending the filling of the color
        t.end_fill()

        #put pen up
        t.up()


    def change_to_red(self):
        #make turtle go to center coordinate
        t.goto(self.x, self.y)
        
        #put pen down
        t.down()
        
        # set the fillcolor
        t.fillcolor("red") 
        
        # start the filling color
        t.begin_fill()
        
        # drawing the circle of radius r
        t.circle(self.radius)
        
        # ending the filling of the color
        t.end_fill()

        #put pen up
        t.up()


class Gantry_System():
    def __init__(self, num_gantries):
        self.num_gantries = num_gantries

        #get starting position of turtle
        self.current_coord = t.pos()

        #Create the list of gantry objects
        self.gantries = []
        for i in range(self.num_gantries):
            #Create the gantry
            self.gantries.append(Gantry(self.current_coord))

            #Move the turtle to the right
            original_x = self.current_coord[0]
            original_y = self.current_coord[1]

            self.current_coord = (original_x+20, original_y)
        

    #Assume we are looking from the outside of the station, so gantries in will be green, gantries out will be red
    def update_gantries(self, num_gantries_in, num_gantries_out):
        #For simplicity, the gantries to the right will be green, and the left will be red
        for i in range(num_gantries_in):
            gantry_to_update = self.gantries[i]

            gantry_to_update.change_to_green()

        for i in range(num_gantries_out):
            gantry_to_update = self.gantries[i+num_gantries_in]

            gantry_to_update.change_to_red()



if __name__ == "__main__":
    total_gantries = int(input("Enter total number of gantries: "))

    #create the object
    gantry_system = Gantry_System(total_gantries)
    
    while True:
        num_gantries_in = int(input("Enter number of gantries in: "))
        num_gantries_out = int(input("Enter number of gantries out: "))

        #Make sur eit sthe same, or else will error
        if total_gantries == num_gantries_in+num_gantries_out:    
            gantry_system.update_gantries(num_gantries_in, num_gantries_out)

        else:
            print("Total gantries not equal to the sum of in and out gantries entered!")








        






