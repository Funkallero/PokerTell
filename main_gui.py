#!bin/usr/python
"""
Just having some fun in Python.
//christianlindeneg, May, 2019//

GUI with Tkinter.. It works as it should but the code looks quite clunky (probably if not entirely due to my inadequate skills)
Say the text-frames, I can't seem to update a single frame continously and thus I create a new text-frame for each command.. 
That just seems so inefficient, so I must've missed something but I've failed to find out what thus far. 

To do list:
[1] Extend graphs
[2] Incorporate more Pandas
[3] In corporate percent variable in statistics
"""
import config
import json
import os
from time import sleep

from tkinter import Tk, Canvas, Frame, Button, Text, mainloop, INSERT, DISABLED, END, Label, Entry
from matplotlib.pyplot import title, xlabel, ylabel, legend, scatter, figure, show, plot, axis
from numpy import mean, median, max, min, percentile, array, sort, around
from pandas import DataFrame
from requests import get, put, post

class GuiMain:
    def __init__(self, master):
        """Acts as the Main Menu"""
        self.master = master
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        # Generate Canvas
        self.canvas = Canvas(self.master, bg=default_C, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()
        # Generate Frame
        self.main_frame = Frame(self.master, bg=default_C)
        self.main_frame.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.1)

        # Recent Tournaments
        self.rt_rb = Button(self.main_frame, text="Recent Tournaments", bg='#070707', fg='#196619', command=self.simple_overview_command)
        self.rt_rb.pack(side='left')

        # Statistics
        self.ss_rb = Button(self.main_frame, text="Statistics", bg='#070707', fg='#196619', command=self.simple_statistics_command)
        self.ss_rb.pack(side='left')

        # Graphs
        self.sg_rb = Button(self.main_frame, text="Graphs", bg='#070707', fg='#196619', command=self.simple_graphs)
        self.sg_rb.pack(side='left')

        # Complete History
        self.ch_rb = Button(self.main_frame, text="Complete History", bg='#070707', fg='#196619', command=self.complete_history_command)
        self.ch_rb.pack(side='left')

        # Add a Tournament
        self.at_rb = Button(self.main_frame, text="Add a Tournament", bg='#070707', fg='#196619', command=self.add_command)
        self.at_rb.pack(side='left')

        # Delete a Tournament
        self.dt_rb = Button(self.main_frame, text="Delete a Tournament", bg='#070707', fg='#196619', command=self.remove_command)
        self.dt_rb.pack(side='left')

        # Save & Exit
        self.se_rb = Button(self.main_frame, text="Save & Exit", bg='#070707', fg='#196619', command=self.exit_command)
        self.se_rb.pack(side='right')
            
        # Generates Intro Text Frame
        text_frame_intro = Frame(self.master, bg=default_C)
        text_frame_intro.place(relx=0.25, rely=0.4, relwidth=0.5, relheight=0.15)
        text_intro = Text(text_frame_intro, bg='#070707', bd=5, exportselection=0, fg='#196619', height=self.HEIGHT, width=self.WIDTH)
        text_intro.insert(INSERT, str(config.intro))
        text_intro.config(state=DISABLED)
        text_intro.pack()

    def simple_overview_command(self):
        """Displays the five recent tournaments in a text-frame"""
        simple_overview = MainOverview()
        
        text_frame_simpleoverview = Frame(self.master, bg=default_C)
        text_frame_simpleoverview.place(relx=0, rely=0.1, relwidth=1, relheight=0.9) 
        text_simpleoverview = Text(text_frame_simpleoverview, bg='#070707', bd=5, exportselection=0, fg='#196619', height=HEIGHT, width=WIDTH)
        text_simpleoverview.insert(INSERT, str(simple_overview))
        
        text_simpleoverview.config(state=DISABLED)
        text_simpleoverview.pack()
    
    def simple_statistics_command(self):
        """Displays some simple statistics in a text-frame"""
        simple_statistics = MainStat()

        text_frame_simple_statistics = Frame(self.master, bg=default_C)
        text_frame_simple_statistics.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        text_simple_statistics = Text(text_frame_simple_statistics, bg='#070707', bd=5, exportselection=0, fg='#196619', height=HEIGHT, width=WIDTH)
        text_simple_statistics.insert(INSERT, str(simple_statistics))
        
        text_simple_statistics.config(state=DISABLED)
        text_simple_statistics.pack()

    def simple_graphs(self):
        """One simple graph"""
        graph = Statistics()
        graph.simple_graph('winbuy')

    def complete_history_command(self):
        """Displays the complete tournament history ... in a text-frame"""
        read = SimpleOverview()
        comp_his = read.read_local
        pok_his = comp_his['poker']
        df = DataFrame(pok_his)
        cols = df.columns.tolist()
        
        i = 1        
        while i <= 6:
            # making date the first column by moving all columns to the right, 6 times. (apparantly that works)
            cols = cols[-1:] + cols[:-1]
            i += 1
        df = df[cols]

        text_frame_complete_history = Frame(self.master, bg=default_C)
        text_frame_complete_history.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        text_complete_history = Text(text_frame_complete_history, bg='#070707', bd=5, exportselection=0, fg='#196619', height=HEIGHT, width=WIDTH)
        text_complete_history.insert(INSERT, str(df))
        
        text_complete_history.config(state=DISABLED)
        text_complete_history.pack()

    def add_command(self):
        """Frame to add input values for a new tournament"""
        add_frame= Frame(self.master, bg=default_C)
        add_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

        Label(add_frame, text='ID\nExample: 456584726', bg=default_C, fg='#196619').grid(row=0)
        Label(add_frame, text='Date\nExample: 2019-05-19', bg=default_C, fg='#196619').grid(row=1)
        Label(add_frame, text='Type\nExample: Knockout', bg=default_C, fg='#196619').grid(row=2)
        Label(add_frame, text='Field\nExample: 1485', bg=default_C, fg='#196619').grid(row=3)
        Label(add_frame, text='Placement\nExample: 1', bg=default_C, fg='#196619').grid(row=4)
        Label(add_frame, text='Buy-in\nExample: 24.5', bg=default_C, fg='#196619').grid(row=5)
        Label(add_frame, text='Cashed\nExample: 265.86', bg=default_C, fg='#196619').grid(row=6)

        self.add_id = Entry(add_frame, bg='#373737', fg='#196619')
        self.add_date = Entry(add_frame, bg='#373737', fg='#196619')
        self.add_type = Entry(add_frame, bg='#373737', fg='#196619')
        self.add_field = Entry(add_frame, bg='#373737', fg='#196619')
        self.add_place = Entry(add_frame, bg='#373737', fg='#196619')
        self.add_buyin = Entry(add_frame, bg='#373737', fg='#196619')
        self.add_cashed = Entry(add_frame, bg='#373737', fg='#196619')

        self.add_id.grid(row=0, column=1)
        self.add_date.grid(row=1, column=1)
        self.add_type.grid(row=2, column=1)
        self.add_field.grid(row=3, column=1)
        self.add_place.grid(row=4, column=1)
        self.add_buyin.grid(row=5, column=1)
        self.add_cashed.grid(row=6, column=1)

        Button(add_frame, text='Update JSON', command=self.add_command_values, bg=default_C, fg='#196619').grid(row=10, column=0, pady=4)

    def add_command_values(self):
        """Checks the values for the correct type or the correct range
            and thereafter appends them into a list."""
        try:
            add_id = self.add_id.get()
            if not int(add_id) > 0:
                self.error()
        except:
            self.error()
        try:
            add_date = self.add_date.get()
            if type(add_date) == int() or type(add_date) == float():
                self.error()
        except:
            self.error()
        try:
            add_type = self.add_type.get()
            if type(add_type) == int() or type(add_type) == float():
                self.error()
        except:
            self.error()
        try:
            add_field = self.add_field.get()
            if not int(add_field) >= 2:
                self.error()
        except:
            self.error() 
        try:
            add_place = self.add_place.get()
            if not int(add_place) >= 1:
                self.error()
        except:
            self.error()
        try:
            add_buyin = self.add_buyin.get()
            if not float(add_buyin) >= 0.01:
                self.error()
        except:
            self.error()
        try:
            add_cashed = self.add_cashed.get()
            if not float(add_cashed) >= 0:
                self.error()
        except:
            self.error()
        
        text_frame_add = Frame(self.master, bg=default_C)
        text_frame_add.place(relx=0.25, rely=0.5, relwidth=0.43, relheight=0.048)
        text_add = Text(text_frame_add, bg='#070707', bd=5, exportselection=0, fg='#196619', height=self.HEIGHT, width=self.WIDTH)
        text_add.insert(INSERT, 'Adding new data to JSON ...')
        text_add.config(state=DISABLED)
        text_add.pack()
        text_add.update()

        try:
            text_add.insert(INSERT, 'Succesfully Added ...')
            text_add.update()
            add_remove = AddRemove()
            add_remove.add_to_json(add_id, add_date, add_type, add_field, add_place, add_buyin, add_cashed)
        except:
            self.error()
        
        sleep(0.5)
        text_add.destroy()

    def remove_command(self):
        """Frame to add input values for a new tournament"""
        remove_frame= Frame(self.master, bg=default_C)
        remove_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        Label(remove_frame, text='Enter index value of tournament to remove\n\nEnter -1 to remove latest added tournament', bg=default_C, fg='#196619').grid(row=0)
        
        self.remove_index = Entry(remove_frame, bg='#373737', fg='#196619')
        self.remove_index.grid(row=1, column=0)

        Button(remove_frame, text='Remove tournament', command=self.remove_command_value, bg=default_C, fg='#196619').grid(row=10, column=0, pady=4)

    def remove_command_value(self):
        """Removes the actual tournament with the index chosen"""
        text_frame_remove = Frame(self.master, bg=default_C)
        text_frame_remove.place(relx=0.25, rely=0.5, relwidth=0.43, relheight=0.048)
        text_remove = Text(text_frame_remove, bg='#070707', bd=5, exportselection=0, fg='#196619', height=self.HEIGHT, width=self.WIDTH)
        text_remove.insert(INSERT, 'Removing data from JSON ...')
        text_remove.config(state=DISABLED)
        text_remove.pack()

        try:
            text_remove.update()
            choice_remove = self.remove_index.get()
            add_remove = AddRemove()
            add_remove.del_from_json(choice_remove)
        except:
            self.error()

        sleep(0.5)
        text_remove.destroy()

    def exit_command(self):
        """Updates online JSON, deletes local JSON - exits thereafter"""
        text_frame_exit_command = Frame(self.master, bg=default_C)
        text_frame_exit_command.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        text_exit_command = Text(text_frame_exit_command, bg='#070707', bd=5, exportselection=0, fg='#196619', height=HEIGHT, width=WIDTH)
        text_exit_command.insert(INSERT, 'Updating JSON  ... Exiting thereafter ... Thanks for now ...')
        
        text_exit_command.config(state=DISABLED)
        text_exit_command.pack()
        text_exit_command.update()

        update = JsonBin()
        update.update_bin()
        update.remove_local_json()

        sleep(1.5)

        self.master.destroy()

    def error(self):
        """Error message displayed for errors in the input."""
        text_frame_error = Frame(self.master, bg=default_C)
        text_frame_error.place(relx=0.25, rely=0.5, relwidth=0.43, relheight=0.048)
        text_error = Text(text_frame_error, bg='#070707', bd=5, exportselection=0, fg='#196619', height=self.HEIGHT, width=self.WIDTH)
        text_error.insert(INSERT, 'VALUE ERROR | INPUT ERROR | TRY AGAIN')
        text_error.config(state=DISABLED)
        text_error.pack()
        text_error.update()
        sleep(0.5)
        text_error.destroy()

class MainOverview:
    """Wrapping the data from JSON together into a string."""
    def __init__(self):
        self.simpleoverview = SimpleOverview()
        self.simple_overview = self.simpleoverview.winbuydate()
    
    def __repr__(self):
        return '\nPrinting last five tournaments ..\n{}'.format(self.simple_overview)

class MainStat:
    """Wrapping statistics into a neat string."""
    def __init__(self):
        self.stats = Statistics()
        self.stats.simple_stats()
        self.stats.winbuydate()
        self.stats.profit()
        self.stats.tourny_types()

    def __repr__(self):
        return """
POKERTELL TEST DATA | NOT ACTUAL DATA.

TOTAL PROFIT:

Cash ------------------> ${total_price}
Buy-ins ---------------> ${total_buy}

Profit ----------------> ${profit}

TOURNAMENT TYPES:

Amount of Tournaments -> {total_tourny}

Knockout --------------> {knockout_count} 
Cashed ----------------> ${knock_pro}
Buyins ----------------> ${knock_buy} 
Win or Loss -----------> ${knock_per} 

Regular ---------------> {regular_count}
Cashed ----------------> ${reg_pro}
Buyins ----------------> ${reg_buy}
Win or Loss -----------> ${reg_per}

Headsup ---------------> {headsup_count}    
Cashed ----------------> ${head_pro}        
Buyins ----------------> ${head_buy}        
Win or Loss -----------> ${head_per}        

Spin & Go -------------> {spin_count}
Cashed ----------------> ${spin_pro}
Buyins ----------------> ${spin_buy}
Win or Loss -----------> ${spin_per}

WIN STATS:

Max Win ---------------> ${max_win}
Min Win ---------------> ${min_win}
Average Wins ----------> ${avg_win}
Median Wins -----------> ${med_win}

Interquartile Range ---> {range_win} 

BUY-IN STATS:

Max Buy-in ------------> ${max_cost}
Min Buy-in ------------> ${min_cost}
Average Buy-in --------> ${avg_cost}
Median Buy-in ---------> ${med_cost}

Interquartile Range ---> {range_cost} 

PLACEMENT STATS:

Best Placement --------> {max_place}
Worst Placement -------> {min_place}
Average Placement -----> {avg_place}
Median Placement ------> {med_place}

Interquartile Range ---> {range_place} 

OPPONENTS STATS:

Larget Field ----------> {max_player}
Smallest Field --------> {min_player}
Average Field ---------> {avg_player}
Median Field ----------> {med_player}

Interquartile Range ---> {range_player}""".format(
            
            total_price=around(self.stats.wins, decimals=2),
            total_buy=around(self.stats.lost, decimals=2),
            profit=around(self.stats.diff, decimals=2),

            knockout_count=self.stats.knockout_count,
            knock_pro=around(self.stats.knockout_profit, decimals=2),
            knock_buy=around(self.stats.knockout_buyin, decimals=2),
            knock_per=around(self.stats.knockout_diff, decimals=2),

            regular_count=self.stats.regular_count,
            reg_pro=around(self.stats.regular_profit, decimals=2),
            reg_buy=around(self.stats.regular_buyin, decimals=2),
            reg_per=around(self.stats.regular_diff, decimals=2),
            
            spin_count=self.stats.spin_count,
            spin_pro=around(self.stats.spin_profit, decimals=2),
            spin_buy=around(self.stats.spin_buyin, decimals=2),
            spin_per=around(self.stats.spin_diff, decimals=2),
            
            headsup_count=self.stats.headsup_count,
            head_pro=around(self.stats.headsup_profit, decimals=2),
            head_buy=around(self.stats.headsup_buyin, decimals=2),
            head_per=around(self.stats.headsup_diff, decimals=2),
            
            total_tourny=self.stats.total_tourny,
            avg_win=around(self.stats.avg_win, decimals=2),
            max_win=around(self.stats.max_win, decimals=2),
            min_win=around(self.stats.min_win, decimals=2),
            med_win=around(self.stats.med_win, decimals=2),
            range_win=around(self.stats.range_win, decimals=2),
            
            avg_cost=around(self.stats.avg_cost, decimals=2),
            max_cost=around(self.stats.max_cost, decimals=2),
            min_cost=around(self.stats.min_cost, decimals=2),
            med_cost=around(self.stats.med_cost, decimals=2),
            range_cost=around(self.stats.range_cost, decimals=2),

            avg_place=around(self.stats.avg_place, decimals=2),
            max_place=around(self.stats.max_place, decimals=2),
            min_place=around(self.stats.min_place, decimals=2),
            med_place=around(self.stats.med_place, decimals=2),
            range_place=around(self.stats.range_place, decimals=2),

            avg_player=around(self.stats.avg_players, decimals=2),
            max_player=around(self.stats.max_players, decimals=2),
            min_player=around(self.stats.min_players, decimals=2),
            med_player=around(self.stats.med_players, decimals=2),
            range_player=around(self.stats.range_players, decimals=2)
            )

class JsonMain:
    """Reads online JSON and creates local copy."""
    def __init__(self, url=config.cur_url, cur_file=config.cur_file):
        self.url = str(url)
        self.cur_file = str(cur_file)
        self.api_key = str(config.api_key)

    def read_bin(self):
        """Reads online JSON."""
        headers = {'secret-key': self.api_key}
        req = get(self.url, headers=headers)
        self.readbin = req.json()

        if int(req.status_code) == 200:
            return self.readbin
            
        elif int(req.status_code) != 200:
            print('\nError\n', self.readbin['message'])
            
            
        else:
            print('\nError. No Connection.')
           

    def write_to_json(self, read):
        """Creates local JSON."""
        data = json.dumps(read, indent=2)
        with open(self.cur_file, 'w') as poker_json:
            json.dump(data, poker_json)   

    def readjson(self):
        """Reads local JSON."""
        with open(self.cur_file) as poker:
            r_poker = json.load(poker)
            str_poker = json.loads(r_poker)
        return str_poker

class JsonBin(JsonMain):
    """Create, Read and Update online or local JSON."""
    def __init__(self, url=config.cur_url, cur_file=config.cur_file):
        super().__init__(url, cur_file)
        self.read_online = self.read_bin()
        self.write_to_json(self.read_online)
        self.read_local = self.readjson()

    def update_bin(self):
        """Updates online JSON."""
        headers = {
        'Content-Type': 'application/json',
        'secret-key': self.api_key,
        'versioning': 'false'
        }
        try:
            req = put(self.url, json=self.read_local, headers=headers)
            
            if int(req.status_code) == 200:
                return print('\nSuccessfully Updated JSON ..')
                
            
            elif int(req.status_code) != 200:
                print('\nError\n', readbin['message'])
                
            
            else:
                print('\nRecieved Connection but An Error Occured. Try Again.')
                

        except:
            print('\nCould Not Update JSON. Check Connection and/or Private Key.')
            
    def create_new_bin_id(self):
        """Creates a new online JSON and returns the bin id."""
        crurl = 'https://api.jsonbin.io/b'
        headers = {
        'Content-Type': 'application/json',
        'secret-key': self.api_key,
        'private': 'true'
        }
        try:
            req = post(crurl, json=self.read_local, headers=headers)
            bin_ = req.json()
            
            if bin_['success'] == True:
                self.new_bin_id = bin_['id']
                print('\nSuccessfully Created New Bin')
                print('\nBin ID: ' + str(self.new_bin_id))
                return self.new_bin_id
            
            elif bin_['success'] == False:
                print('\nError\n', bin_['message'])
                
            
            else:
                print('\nJSON Not Created. Try Again.')
                
        except:
            print('\nCould Not Connect. Check Connection and/or Private Key.')
            

    def remove_local_json(self):
        """Removes local file after it's been uploaded to jsonbin.io."""
        print('\nRemoving Local JSON ..')
        os.remove(self.cur_file)
        print('\nSucesfully Removed ..')

class SimpleOverview(JsonBin):
    """Creates a simple overview of tournaments and profits."""
    def __init__(self, url=config.cur_url, cur_file=config.cur_file):
        super().__init__(url, cur_file)

    def winbuydate(self):
        self.totwin = 0
        self.totbuy = 0
        self.overview = str()
        i = -1
        
        while i >= -5: 
            # perhaps add field-size and placement
            self.win = self.read_local['poker'][i]['win']  
            self.totwin += self.read_local['poker'][i]['win']
            self.totbuy += self.read_local['poker'][i]['buyin']
            self.buyin = self.read_local['poker'][i]['buyin']
            self.date = self.read_local['poker'][i]['date']
            
            self.overview += '''
Cashed:  ${}
Buy-in:  ${}
Date  :  {}'''.format(self.win, self.buyin, self.date)
            self.overview += '\n'
            i -= 1

        return self.overview

    def profit(self):
        self.wins = float()
        self.lost = float()
        for item in self.read_local['poker']:    
            self.wins += item['win'] 
            self.lost += item['buyin']
            self.diff = self.wins - self.lost

        return self.diff, self.wins, self.lost

class Statistics(SimpleOverview):
    """Creates simple statistics using data from the SimpleOverview class."""
    def __init__(self, url=config.cur_url, cur_file=config.cur_file):
        super().__init__(url, cur_file)
        self.raw_data = self.read_local['poker']

    def simple_graph(self, mode):
        """Generates a graph, still WIP."""
        self.mode = mode
        self.simple_stats()
       
        if self.mode == 'winbuy':
            # scatter graph, x=buyins, y=cashed
            fig = figure()
            ax = fig.add_subplot(1, 1, 1)
            title("Cashed & Buyins")
            xlabel("Buyins in $")
            ylabel("Cashed in $")
            legend(['USD'])
            ax.scatter(self.cost_unsort, self.prize_unsort, alpha=0.8, edgecolors='none', s=30)
            return show()     

        elif self.mode == 'winbuy2':
            # not done yet
            x_start = 0 
            x_end = float(self.data[1][0][-1]) + 50
            y_start = 0
            y_end = float(self.data[0][0][-1]) + 50
            plot(self.cost_unsort, self.prize_unsort, 'r')
            axis([float(x_start), float(x_end), float(y_start), float(y_end)])
            return show()

        else:
            print('\nError. Try again.')
        """
        MORE GRAPHS
        """

    def tourny_types(self):
        """Evaluates the occurance and profits from different tournament types."""
        search_list = list()
        tour_type = self.read_local['poker']
        self.total_tourny = len(tour_type)

        self.knockout_profit = float()
        self.knockout_buyin = float()
        self.regular_profit = float()
        self.regular_buyin = float()
        self.spin_profit = float()
        self.spin_buyin = float()
        self.headsup_profit = float()
        self.headsup_buyin = float()
        for item in tour_type:
            search_list.append(item['type'])

        self.knockout_count = search_list.count('Knockout')
        self.regular_count = search_list.count('Regular')
        self.spin_count = search_list.count('Spin')
        self.headsup_count = search_list.count('Headsup')
        for item in tour_type:

            if item['type'] == 'Knockout':
                self.knockout_buyin += item['buyin']
                self.knockout_profit += item['win'] 
            elif item['type'] == 'Regular':
                self.regular_profit += item['win'] 
                self.regular_buyin += item['buyin']
            elif item['type'] == 'Spin':
                self.spin_profit += item['win'] 
                self.spin_buyin += item['buyin']
            elif item['type'] == 'Headsup':
                self.headsup_profit += item['win']
                self.headsup_buyin += item['buyin']

    def simple_stats(self):
        """Using numpy to calculate simple statistics."""
        self.tourny_types()
        self.profit()
        self.create_array()
        # means
        self.avg_win = mean(self.data[0][0])
        self.avg_cost = mean(self.data[1][0])
        self.avg_place = mean(self.data[2][0])
        self.avg_players = mean(self.data[3][0])      
        # medians
        self.med_win = median(self.data[0][0])
        self.med_cost = median(self.data[1][0])
        self.med_place = median(self.data[2][0])
        self.med_players = median(self.data[3][0])       
        # max's
        self.max_win = max(self.data[0][0])
        self.max_cost = max(self.data[1][0])
        self.max_place = min(self.data[2][0])
        self.max_players = max(self.data[3][0])        
        # min's
        self.min_win = min(self.data[0][0])
        self.min_cost = min(self.data[1][0])
        self.min_place = max(self.data[2][0])
        self.min_players = min(self.data[3][0])        
        # percentiles
        self.percentile_25_win = percentile(self.data[0][0], 25)
        self.percentile_75_win = percentile(self.data[0][0], 75)
        self.range_win = self.percentile_75_win - self.percentile_25_win

        self.percentile_25_cost = percentile(self.data[1][0], 25)
        self.percentile_75_cost = percentile(self.data[1][0], 75)
        self.range_cost = self.percentile_75_cost - self.percentile_25_cost

        self.percentile_25_place = percentile(self.data[2][0], 25)
        self.percentile_75_place = percentile(self.data[2][0], 75)
        self.range_place = self.percentile_75_place - self.percentile_25_place

        self.percentile_25_players = percentile(self.data[3][0], 25)
        self.percentile_75_players = percentile(self.data[3][0], 75)
        self.range_players = self.percentile_75_players - self.percentile_25_players
        #percentages
        self.knockout_diff = ((self.knockout_profit - self.knockout_buyin))
        self.regular_diff = ((self.regular_profit - self.regular_buyin))
        self.spin_diff = ((self.spin_profit - self.spin_buyin))
        self.headsup_diff = ((self.headsup_profit - self.headsup_buyin))

    def create_array(self):
        """
        Creating array for calculations.
        Format:
            [WIN]  :0 
            [COST] :1 
            [PLACE]:2 
            [FIELD]:3"""
        self.sort_data()
        self.data = array(
            [
            [self.prize],
            [self.cost],
            [self.place],
            [self.players]
            ])
        return self.data

    def sort_data(self):
        """Sorting data for arrays and graphs."""
        self.prize_unsort = list()
        self.cost_unsort = list()
        self.players_unsort = list()
        self.place_unsort = list()
        
        for item in self.raw_data:
            self.prize_unsort.append(item['win'])
            self.cost_unsort.append(item['buyin'])
            self.players_unsort.append(item['players'])
            self.place_unsort.append(item['place'])

        self.prize = sort(self.prize_unsort)
        self.cost = sort(self.cost_unsort)
        self.players = sort(self.players_unsort)
        self.place = sort(self.place_unsort)

class AddRemove(SimpleOverview):
    """
    Adds and removes tournaments from local JSON.
    Then uploads that to online JSON."""
    def __init__(self, url=config.cur_url, cur_file=config.cur_file):
        super().__init__(url, cur_file)
        self.read = self.read_local

    def del_json(self, choice_remove):
        """Deletes tournament specified by the user from local JSON."""
        data_d = self.read

        if int(choice_remove) == -1:
            del data_d['poker'][-1]

        elif int(choice_remove) >= 0 and int(choice_remove) <= (len(data_d['poker'])) - 1:
                del data_d['poker'][int(choice_remove)]     
        else:
            print('\nCommand Not Found. Try Again.')

        return data_d

    def add_to_json(self, input_id, input_date, input_type, input_field, input_place, input_buyin, input_win):
        """Adds the new tournament and then writes new file to a local JSON."""
        data_n = self.read

        data_n['poker'].append(
            {'id': int(input_id), 
            'date': str(input_date), 
            'type': str(input_type), 
            'players': int(input_field), 
            'place': int(input_place), 
            'buyin': float(input_buyin), 
            'win': float(input_win)}
            )
        self.write_to_json(data_n)
        self.update_bin()

    def del_from_json(self, choice_remove):
        """Deletes the tournament and then writes new file to a local JSON."""
        data_del = self.del_json(choice_remove)
        self.write_to_json(data_del)  
        self.update_bin()

class Error(Exception):
    """Base class for exceptions in this module.
        Only one Error class added thus far."""

class ValueError(Error):
    """Exception raised for errors in the input."""
    def __init__(self):
        pass

if __name__ == '__main__':
    """Kick starts the app"""
    HEIGHT = 800
    WIDTH = 750
    default_C = '#060606'
    
    root = Tk()
    root.iconbitmap('ptlogo.ico')
    root.title('PokerTell - Version 0.1')
    GuiMain(root)
    root.resizable(False, False)
    root.mainloop()