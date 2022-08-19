import csv
import turtle
from collections import namedtuple
import copy
import tkinter
from tkinter import font
import operator
from tkinter import messagebox


class GUI:
    """Class to display GUI interface"""
    def __init__(self):
        """Initial window setup"""
        self.window = tkinter.Tk()
        self.window.geometry('768x550+341+170')
        self.window.title("Your Transport System")
        self._record_listbox = 0

    def command_action_button(self):
        """ Method that takes both location and destination and outputs a sub-window with the shortest route possible"""
        caller.prepare_algorithm()  # calls the function that prepares neigboring stations for each station, to calculate the shortest path. We always
                                    # need to prepare the algorithm for every new path that needs to be calculated

        where_to = self.entry_where_to.get()
        where_from = self.entry_where_from.get()

        where_from_id = None
        where_to_id = None

        """For loop that obtains the corresponding id of the source point and destination point since the user passes text"""
        for each in caller._LondonStations:
            if each.name == where_from:
                where_from_id = each.station_id

            if each.name == where_to:
                where_to_id = each.station_id





        """ Error checking for the source and destinations passed into the source and destination text fields
        If a station that doesn't exist is inputted in either fields, an error dialog comes up"""
        if where_from_id == None and where_to_id==None:
            messagebox.showerror(title="Error in Address", message="Invalid Source and Destination Address. Please have a re-look")

        elif where_from_id == None:
            messagebox.showerror(title="Invalid", message="Invalid Source Address. Please have a re-look")

        elif where_to_id == None:
            messagebox.showerror(title="Invalid", message="Invalid Destination Address. Please have a re-look")

        else:
            res = caller.run_algorithm(caller.aller, where_from_id, where_to_id)  # algorithm to calculate shortest path
            #print(res)

            print(where_from_id)
            print(where_to_id)

            """ Fonts used for widgets in the result top level window"""
            selectedFont5 = font.Font(name='font_6', family='Arial', size=12, weight='bold', slant='roman',
                                      underline=0,
                                      overstrike=0)

            """ Widgets that are defined in the window that shows the route to the user"""
            result_toplevel = tkinter.Toplevel(self.window)
            result_toplevel.geometry("400x400+300+20")

            canvas_toplevel = tkinter.Canvas(result_toplevel, )
            canvas_toplevel.pack(side='bottom')

            frame_toplevel = tkinter.Frame(canvas_toplevel, )
            frame_toplevel.pack()

            canvas_toplevel.create_window((0, 0), window=frame_toplevel, anchor='n')

            scroll_toplevel_verti = tkinter.Scrollbar(master=result_toplevel, command=canvas_toplevel.yview)
            scroll_toplevel_verti.pack(side='right', fill='y')


            canvas_toplevel.config(yscrollcommand=scroll_toplevel_verti.set)




            label_result = tkinter.Label(master=result_toplevel, text="Your itenary is ready", font=selectedFont5)
            label_result.pack(side = "top", fill="x")

            label_time_result = tkinter.Label(master=result_toplevel, fg='red', font = selectedFont5, text="The trip will last {} minutes\n"
                                                                           "And will involve the following routes:\n\n".format(res[0]))
            label_time_result.pack(side='top', fill='x')

            """ For loop that creates a label on the Route window of all the intemediary stations (route) between the source and destination station"""
            for stops in res[1]:
                for each in caller._LondonStations:
                    if each.station_id == stops:
                        tkinter.Label(master=frame_toplevel, text="{}) \t{}, then to:".format(each.station_id, each.name)).pack()
            tkinter.Label(master=frame_toplevel, text="\nYou are there", anchor='n', font=('Arial',8,'bold')).pack()


            result_toplevel.bind("<Configure>", lambda event: canvas_toplevel.config(scrollregion=canvas_toplevel.bbox('all')))

    def command_menu_gui(self):
        pass



    def command_listbox(self, event):
        """Command that defines what happens when stations are selected from the Listbox widget"""

        # self.entry_where_from.delete(0, 'end')
        # self.entry_where_to.delete(0, 'end')

        if self._record_listbox == 0:
            self.entry_where_from.insert('end', self.listbox_stations.selection_get())
            self._record_listbox = 1

        elif self._record_listbox == 1:
            self.entry_where_to.insert('end', self.listbox_stations.selection_get())
            self._record_listbox = 0



    def command_menu_graph(self):
        """ Command that calls the function to create station graph in a Canvas window"""
        caller.create_station_graph()

    def create_widgets(self):
        """This method creates all the widgets on the main GUI window"""

        """Fonts for all the widgets defined on the main GUI window"""
        selectedFont1 = font.Font(name='font_1', family='Segoe UI', size=42, weight='bold', slant='roman', underline=0,
                                  overstrike=0)
        selectedFont3 = font.Font(name='font_3', family='Comic Sans MS', size=15, weight='bold', slant='italic',
                                  underline=0, overstrike=0)
        selectedFont4 = font.Font(name='font_4', family='Bradley Hand ITC', size=27, weight='bold', slant='roman',
                                  underline=1, overstrike=0)
        selectedFont6 = font.Font(name='font_6', family='Georgia', size=12, weight='bold', slant='roman', underline=0,
                                  overstrike=0)
        selectedFont7 = font.Font(name='font_7', family='Georgia', size=12, weight='bold', slant='roman', underline=0,
                                  overstrike=0)
        selectedFont8 = font.Font(name='font_8', family='Gill Sans MT', size=14, weight='normal', slant='roman',
                                  underline=0, overstrike=0)
        action_button = tkinter.Button(self.window, background='#dadada', font='font_8', image='', relief='sunken', takefocus=True,
                         text='Take me there', command=self.command_action_button)
        action_button.place(x=424, y=470, height=52, width=236, anchor='nw')
        self.entry_where_from = tkinter.Entry(self.window, exportselection=True, font='TkDefaultFont', takefocus=True, )
        self.entry_where_from.place(x=272, y=283, height=27, width=128, anchor='nw')
        self.entry_where_to = tkinter.Entry(self.window, exportselection=True, font='TkDefaultFont', takefocus=True, )
        self.entry_where_to.place(x=272, y=339, height=26, width=128, anchor='nw')
        label_title = tkinter.Label(self.window, background='cyan', font='font_1', image='', pady=42, takefocus=True, text='Transport Yourself', )
        label_title.place(x=132, y=13, height=140, width=499, anchor='nw')
        label_subtitle = tkinter.Label(self.window, font='font_3', image='', padx=8, pady=1, takefocus=True, text='.....Easily', )
        label_subtitle.place(x=529, y=168, height=40, width=104, anchor='nw')
        label_slogan = tkinter.Label(self.window, font='font_4', foreground='#5b50f1', image='', justify='center', takefocus=True,
                       text='In 2 Simple Steps:', )
        label_slogan.place(x=39, y=214, height=44, width=359, anchor='nw')
        label_where_from = tkinter.Label(self.window, font='font_6', image='', relief='flat', takefocus=True, text='Enter your location:', )
        label_where_from.place(x=53, y=276, height=39, width=179, anchor='nw')
        label_where_to = tkinter.Label(self.window, font='font_7', image='', justify='right', takefocus=True, text='Enter your destination:', )
        label_where_to.place(x=52, y=336, height=30, width=204, anchor='nw')

        frame_listbox_scrollbar = tkinter.Frame(self.window,)
        frame_listbox_scrollbar.place(x=450, y=250)

        scroll_x = tkinter.Scrollbar(frame_listbox_scrollbar, orient='horizontal')
        scroll_x.pack(side = 'bottom', fill='x')
        scroll_y = tkinter.Scrollbar(frame_listbox_scrollbar, orient='vertical')
        scroll_y.pack(side='right', fill ='y')



        tkinter.Label(frame_listbox_scrollbar, text="You can also simply click\n from this box:", font=('Arial',8,'bold')).pack(side='top')


        self.listbox_stations = tkinter.Listbox(frame_listbox_scrollbar, xscrollcommand = scroll_x.set, yscrollcommand=scroll_y.set)
        self.listbox_stations.pack(side='left', fill='both')
        self.listbox_stations.bind("<<ListboxSelect>>", self.command_listbox)


        scroll_x.config(command=self.listbox_stations.xview)
        scroll_y.config(command=self.listbox_stations.yview)

        """ For loop that inserts all station names into the Listbox on the main window"""
        for each_station in caller._LondonStations:
            self.listbox_stations.insert('end', each_station.name)

        """Menu that makes it possible to view the GRAPH TRANSPORT NETWORK INFORMATION"""
        menu_gui = tkinter.Menu(self.window)

        self.window.config(menu=menu_gui)

        menu_graph = tkinter.Menu(menu_gui)
        menu_graph.add_command(label="Show Entire Road Network Graph", command = self.command_menu_graph)
        menu_gui.add_cascade(label="Graph Options", menu=menu_graph)


class Lines:
    """ A class to handle Lines"""
    def __init__(self, line_id, colour):
        self.line_id = int(line_id)
        self.colour = str(colour)

    def load_lines(self, csv_file_london_lines):
        """ A method to load the londonlines.csv file
        This method simply creates an open file object, and reads the
        london lines CSV file"""
        london_lines = csv.reader(open(csv_file_london_lines))
        next(london_lines)  #skip attribute names

        """ A list to hold londonlines.csv data as Lines instances"""
        self._LondonLines = []
        for row in london_lines:
            self._LondonLines.append(Lines(row[0], row[2]))
        return self._LondonLines


class Connections:
    """ A class to to handle connections"""
    def __init__(self, station1, station2, line_id, time):
        self.station1 = int(station1)
        self.station2 = int(station2)
        self.line_id = int(line_id)
        self.time = int(time)

    def load_connections(self, csv_file_london_lines):
        """ A method to load the londonconnections .csv file
        This method simply creates an open file object, and reads the
        london connections CSV file"""
        london_connections = csv.reader(open(csv_file_london_lines))
        next(london_connections)  #skip attribute names

        """ A list to hold londonconnections.csv data as Connections instances"""
        self._LondonConnections = []
        for row in london_connections:
            self._LondonConnections.append(Connections(row[0], row[1], row[2], row[3]))
        return self._LondonConnections
            

        
    
class Stations:
    """ A class to handle and port the londonstations.csv file into Python"""
    def __init__(self, station_id, latitude, longitude, name):
        """for now, our concern is the station_id, latitude and longitude attributes in the londonstations.csv file"""
        self.station_id = int(station_id)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.name = str(name)

        


    """ method to load the londonstations CSV file into Python """
    def load_stations(self, csv_file_london_stations):
        """ Create file object, and read londonstations.csv file"""
        london_stations = csv.reader(open(csv_file_london_stations))

        next(london_stations)   # skips attribute names


        self._LondonStations = []

        for row in london_stations:
            """ for each record in londonstations.csv, create an instance of 'Stations' class
            using the attributes id, latitude, longitude respectively """
            self._LondonStations.append(Stations(row[0], row[1], row[2], row[3]))
        return self._LondonStations
        


    def create_station_graph(self):
        """
        This method creates a rough graph showing dispersion of stations using the turtles library

        The following variables are called within this method:
            caller._LondonStations - This contains a list of instances from the Stations class
            conn._LondonConnections - This contains a list of instances from the Connections class
            line._LoadLines - This contains a list of instances from the Lines class

        """

        """Sets up window and canvas to accomodate the graph"""
        toplevel_transport_network = tkinter.Toplevel(width=1500, height=800)
        canvas_transport_network = tkinter.Canvas(toplevel_transport_network, width=1500, height=800)
        canvas_transport_network.place(width=1500, height=800)

        scroll_y = tkinter.Scrollbar(canvas_transport_network, orient='vertical', command=canvas_transport_network.yview)
        scroll_y.pack(side='right', fill='y')

        scroll_x = tkinter.Scrollbar(canvas_transport_network, orient='horizontal', command=canvas_transport_network.xview)
        scroll_x.pack(side='bottom', fill='x')

        canvas_transport_network.config(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        """Sets up turtle for graph plotting on the canvas created above"""
        turtle_screen = turtle.TurtleScreen(canvas_transport_network)
        turtle_ops = turtle.RawTurtle(turtle_screen)
        turtle_screen.setworldcoordinates(0.40, -0.7, 0.71, 0.255)    #set coordinates for window


        """# list that holds coordinates of every (start_here, end_here) station pair. This helps to identify
        any 2 station that may have several lines between them. """
        check_station_preexist = []

        """ A function: 'redraw' that draws every station as a dot on the graph canvas"""
        def redraw(color, shift, draw_dot):
            """ parameters defined here:
            :color (type: str) > defines the london line color, as obtained from londonlines.csv
            :shift (type: float)> defines value to shift the x-axis by; in the case there pre-exists a line between any given 2 stations
            draw_dot (type: bool) > defines whether to draw a dot for a station or not

            """
            turtle_ops.speed(0)
            turtle_ops.pencolor(f"#{select_line_colour[0]}")
            turtle_ops.pensize(2)
            turtle_ops.penup()
            turtle_ops.goto(start_here[0][0] - 51 + shift,
                        start_here[0][1])  # pen goes to latitude/longitude coord. of the start station
            """if condition that does not draw a start station if the station already exists"""
            if draw_dot is True:
                turtle_ops.dot(10, 'grey')
                turtle_ops.pencolor('black')
                turtle_ops.write(station1, font=('Arial', 5, 'bold'))
                turtle_ops.pencolor(f"#{select_line_colour[0]}")
            turtle_ops.pendown()
            turtle_ops.goto(end_here[0][0] - 51 + shift,
                        end_here[0][1])  # pen goes to latitude/longitude coord. of the end station
            """if condition that does not draw an end station if the station already exists"""
            if draw_dot is True:
                turtle_ops.dot(10, 'grey')
                turtle_ops.pencolor('black')
                turtle_ops.write(station2, font=('Arial', 5, 'bold'))
                turtle_ops.pencolor(f"#{select_line_colour[0]}")

        """ For loop that loops through each connection in the londonconnections.csv file. For each connection in the file,
        this For loop obtains:
            (1) the colour of the line of the connection (see the select_line_colour variable)
            (2) the latitude and longitude coordinates of station1 (see the start_here variable)
            (3) the latittude and longitude coordinates of station2 (see the end_here variable)"""

        for each_connection in conn._LondonConnections:
            station1, station2 = each_connection.station1, each_connection.station2  #gets the id of both stations in a
                                                                                     #connection instance of the connections file
            line_id = each_connection.line_id  #gets the line_id of the connection instance

            start_here = [(x.latitude, x.longitude) for x in caller._LondonStations if x.station_id == station1]
            end_here = [(x.latitude, x.longitude) for x in caller._LondonStations if x.station_id == station2]
            select_line_colour = [x.colour for x in line._LondonLines if x.line_id == line_id]


            """Now, given the parameters above (start_here, end_here, select_line_colour), we use turtle library to draw
            a line between start_here and end_here for every connection in londonconnections.csv"""

            """ The below function (redraw) defines what happens if different lines exist between the two stations. 
            Instead of drawing each line directly ontop of the other, the 'redraw' function, shifts the x-axis by a 
            predetermined value before drawing. This way, different lines between any given start-end station pair
            would be visible on the graph
            """

            if (start_here, end_here) in check_station_preexist:
                redraw(select_line_colour, 0.0008*check_station_preexist.count((start_here, end_here)), draw_dot=False)

            else:
                redraw(select_line_colour, 0, draw_dot=True)
                check_station_preexist.append((start_here, end_here))


        toplevel_transport_network.mainloop()

    """This function below, creates a copy of the londonconnections.csv such that the station1 field becomes station2;
    and the station2 field becomes station1. Creating this copy assumes that:
        If a line connects a given station1 to a given station2; then, the line also connects the given station2 to station1;
        such that: if one is able to use a line directly from station 1 to station2, then, the person can also go from
        station2 to station1 directly with the same line
    Doing this makes our algorithm work."""
    def copy_London_Connections(self):
        self.conn_LondonConnections_Copy = conn._LondonConnections.copy()
        for each in conn._LondonConnections:
            copy_station1 = each.station2
            copy_station2 = each.station1
            self.conn_LondonConnections_Copy.append(Connections(copy_station1, copy_station2, each.line_id, each.time))

    def prepare_algorithm(self):
        """ This method prepares our algorithm by processing the copy connections (explained earlier) into a dictionary"""
        self.aller = {x: {} for x in range(1, 304)}

        for each in caller.conn_LondonConnections_Copy:
            if each.station1 in self.aller:
                self.aller[each.station1][each.station2] = each.time

        """ Because we created a dictionary with all 1 to 303 stations; we use for loop to remove any station that
        doesn't exist in the londonstations.csv file; but that is found in our dictionary"""
        for i in range(1, 304):
            if self.aller[i] == {}:
                self.aller.pop(i)
        print(self.aller)


    def run_algorithm(self, station_coords, where_from, where_to):
        """ Runs the algorithm that finds the shortest path... Here, we implement djikstra's algorithm
        :param station_coords - takes in the returned dictionary from 'prepare_algorithm()' method
        :param where_from - takes in the start station
        :param where_to - takes in the end station

        :station_coords is a dictionary of dictionaries ofo the form: {s1: {n1:t1, n2:t2, n3:t3}, s2: {n1:t1, n2:t2} } etc....
        where s reps stations;
        n reps neigbouring stations to s (i.e, stations directly connected to s); AND
        t reps the time between a start station s and its neibouring stations n
        

        returns a tuple with two values: (1) the time taken between where_from and where_to
        (2) A list of intermediary stations betwmin_time_een the source and destination
        
        """

        lowest_time = {}    # Holds time from start station/point to neighbours and updates to the shortest time path as we move through the graph
        track_me = {}   # Tracks the path as created from :where_from; as the loop executes
        route = []  # This stores the route for easy reference after destination is reached.
        unvisited = station_coords


        for each in unvisited:
            lowest_time[each] = float('inf')  # We defined an infinity values for every station other than source station. Since we don't yet known if there's 
                                                # a path to them from source
        lowest_time[where_from] = 0   # we define the time to our start point as 0 since this time is already known. Time from a station to
                                        # itself (that is, we don't move) is 0.

        while unvisited:
            """Initially, we group all stations and its neigbours in the :unvisited variable as a dictionary form. We name the variable this way since it contains a number
            of stations that have not been visited by the path from the starting point.
            This while loop holds true as long as elements (in this case) stations still exist in the :unvisited variable. Every station is processed following the below
            code until no unvisited station remains. This is to ensure every station is considered relative to the source"""

            min_time_ee = None # variable to hold the minimum time between a station s and all its neigbouring stations. This is initially defined as :None
                            # since we are yet to find the closest/shortest neigbour 

            for each in unvisited:
                """Note that the :unvisited variable holds a dictionary of dictionaries of the form: {1: {73:2, 234:4, 265:3, 52:2} etc (as mentioned above).
                Hence, this :for loop loops through each key (station) in :unvisited """
                if min_time_ee is None:
                    min_time_ee = each
                elif lowest_time[each] < lowest_time[min_time_ee]:
                    min_time_ee = each
            
            route_options = station_coords[min_time_ee].items() # After the above if condition, for each instance/while loop, for each lowest time from source to neigbours,
                                                        # we obtain the possible routes from the next station to other neigbouring stations. Please note, it's a loop
            
            #print(route_options)
            #print(lowest_time)
            
            for sub_s, time in route_options:

                """ checks for a more optimal route with lower time """
                if time + lowest_time[min_time_ee] < lowest_time[sub_s]:
                    lowest_time[sub_s] = time + lowest_time[min_time_ee]
                    track_me[sub_s] = min_time_ee # tracks route

            unvisited.pop(min_time_ee) # By popping stations as visited, we ensure loop doesn't go zombie and run endlessly

        searching_station = where_to

        while searching_station != where_from:
            """ While loop to trace back route/journey; going in reverse from :where_to"""
            try:
                route.insert(0, searching_station)
                searching_station = track_me[searching_station]

            except KeyError:
                """ what happens if no path during back tracking"""
                print("No such path")
                break
        route.insert(0, where_from)
        if lowest_time[where_to] != float('inf'):
            return lowest_time[where_to], route



        


    
       
            
            

line = Lines(0, '0')  # Nothing special. Just initialising our class to make it work
line.load_lines("londonlines.csv")

conn = Connections(0, 0, 0, 0)  # Nothing special. Just initialising our class to make it work
conn.load_connections("londonconnections.csv")

caller = Stations(0, 0, 0, 0)  # Nothing special. Just initialising our class to make it work
caller.load_stations("londonstations.csv")
caller.copy_London_Connections()
caller.prepare_algorithm()

start_gui = GUI()
start_gui.create_widgets()


start_gui.window.mainloop()

