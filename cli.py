#!bin/usr/python
"""
Just having some fun in Python.
//christianlindeneg, April, 2019//

To do list:
[1] Extend graphs
[2] Incorporate more Pandas
[3] In corporate percent variable in statistics
more ..
"""
import config
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

def start():
    """Acts as the Main Menu"""
    print('\nPokerTell Test Version.\nContains only test data.')
    print('\n[1] Overview of Recent Tournaments\n[2] Statistics & Graphs\n[3] Complete History\n[4] Add a Tournament\n[5] Delete a Tournament\n[0] Save & Exit')
    try:
        choice = input('\nEnter Choice Here: ')
        if not int(choice) >= 0 and int(choice) <= 6:
            ValueError()
    except:
        ValueError()

    if int(choice) == 1:
        simple_overview = MainOverview()
        print(simple_overview)
        start()
    
    elif int(choice) == 2:
            simple_statistics = MainStat()
            print(simple_statistics)
            try:
                yes_no = input('\nShow Graphs?\n\n[1] Yes [2] No\n\nEnter Here: ')
                if not int(yes_no) >= 0 and int(yes_no) <= 2:
                    ValueError()
            except:
                ValueError()
            
            if int(yes_no) == 1:
                graph = Statistics()
                graph.simple_graph('winbuy')
                start()
            
            elif int(yes_no) == 2:
                start()
            
            else:
                print('\nError. Try again.')
                start()

    elif int(choice) == 3:
        read = SimpleOverview()
        comp_his = read.read_local

        print('\n[1] Formatted Table\n[2] JSON String')
        try:
            ta_ja = input('\nEnter Here: ')
            if not int(ta_ja) >= 0 and int(ta_ja) <= 2:
                ValueError()
        except:
            ValueError()
            
        if int(ta_ja) == 1:
            pok_his = comp_his['poker']
            df = pd.DataFrame(pok_his)
            cols = df.columns.tolist()
            i = 1    
            
            while i <= 6:
                # making date the first column by moving all columns to the right, 6 times. (apparantly that works)
                cols = cols[-1:] + cols[:-1]
                i += 1
            df = df[cols]
            print('\nPrinting Complete History ..\n')

            print(df)
            start()

        elif int(ta_ja) == 2:
            print(json.dumps(comp_his['poker'], indent=2))
            print('\nComplete History Printed ..')
            start()
            
        else:
            print('\nError. Try again.')
            start()

    elif int(choice) == 4:
            add_remove = AddRemove()
            add_remove.add_to_json()
            print('\nSucesfully Added Item ..')
            start()
        
    elif int(choice) == 5:
        add_remove = AddRemove()
        add_remove.del_from_json()
        print('\nSucesfully Deleted Item ..')
        start()
        
    elif int(choice) == 6 or int(choice) == 0:
        update = JsonBin()
        update.update_bin()
        update.remove_local_json()
        print('\nGoodbye. Thanks for now.')
        exit()

    else:
        print('\nNot A Valid Command.\nTry Again.')

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
            
            total_price=np.around(self.stats.wins, decimals=2),
            total_buy=np.around(self.stats.lost, decimals=2),
            profit=np.around(self.stats.diff, decimals=2),

            knockout_count=self.stats.knockout_count,
            knock_pro=np.around(self.stats.knockout_profit, decimals=2),
            knock_buy=np.around(self.stats.knockout_buyin, decimals=2),
            knock_per = np.around(self.stats.knockout_diff, decimals=2),

            regular_count=self.stats.regular_count,
            reg_pro=np.around(self.stats.regular_profit, decimals=2),
            reg_buy=np.around(self.stats.regular_buyin, decimals=2),
            reg_per = np.around(self.stats.regular_diff, decimals=2),
            
            spin_count=self.stats.spin_count,
            spin_pro=np.around(self.stats.spin_profit, decimals=2),
            spin_buy=np.around(self.stats.spin_buyin, decimals=2),
            spin_per = np.around(self.stats.spin_diff, decimals=2),
            
            headsup_count=self.stats.headsup_count,
            head_pro=np.around(self.stats.headsup_profit, decimals=2),
            head_buy=np.around(self.stats.headsup_buyin, decimals=2),
            head_per = np.around(self.stats.headsup_diff, decimals=2),
            
            total_tourny=self.stats.total_tourny,
            avg_win=np.around(self.stats.avg_win, decimals=2),
            max_win=np.around(self.stats.max_win, decimals=2),
            min_win=np.around(self.stats.min_win, decimals=2),
            med_win=np.around(self.stats.med_win, decimals=2),
            range_win=np.around(self.stats.range_win, decimals=2),
            
            avg_cost=np.around(self.stats.avg_cost, decimals=2),
            max_cost=np.around(self.stats.max_cost, decimals=2),
            min_cost=np.around(self.stats.min_cost, decimals=2),
            med_cost=np.around(self.stats.med_cost, decimals=2),
            range_cost=np.around(self.stats.range_cost, decimals=2),

            avg_place=np.around(self.stats.avg_place, decimals=2),
            max_place=np.around(self.stats.max_place, decimals=2),
            min_place=np.around(self.stats.min_place, decimals=2),
            med_place=np.around(self.stats.med_place, decimals=2),
            range_place=np.around(self.stats.range_place, decimals=2),

            avg_player=np.around(self.stats.avg_players, decimals=2),
            max_player=np.around(self.stats.max_players, decimals=2),
            min_player=np.around(self.stats.min_players, decimals=2),
            med_player=np.around(self.stats.med_players, decimals=2),
            range_player=np.around(self.stats.range_players, decimals=2)
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
        req = requests.get(self.url, headers=headers)
        self.readbin = req.json()

        if int(req.status_code) == 200:
            return self.readbin
            
        elif int(req.status_code) != 200:
            print('\nError\n', self.readbin['message'])
            start()
            
        else:
            print('\nError. No Connection.')
            start()

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
            req = requests.put(self.url, json=self.read_local, headers=headers)
            upbin = req.json()
            
            if int(req.status_code) == 200:
                return print('\nSuccessfully Updated JSON ..')
                
            elif int(req.status_code) != 200:
                print('\nError\n', upbin['message'])
                start()
            
            else:
                print('\nRecieved Connection but An Error Occured. Try Again.')
                start()

        except:
            print('\nCould Not Update JSON. Check Connection and/or Private Key.')
            start()

    def create_new_bin_id(self):
        """Creates a new online JSON and returns the bin id."""
        crurl = 'https://api.jsonbin.io/b'
        headers = {
        'Content-Type': 'application/json',
        'secret-key': self.api_key,
        'private': 'true'
        }
        try:
            req = requests.post(crurl, json=self.read_local, headers=headers)
            bin_ = req.json()
            
            if bin_['success'] == True:
                self.new_bin_id = bin_['id']
                print('\nSuccessfully Created New Bin')
                print('\nBin ID: ' + str(self.new_bin_id))
                return self.new_bin_id
            
            elif bin_['success'] == False:
                print('\nError\n', bin_['message'])
                start()
            
            else:
                print('\nJSON Not Created. Try Again.')
                start()
        except:
            print('\nCould Not Connect. Check Connection and/or Private Key.')
            start()

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
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            plt.title("Cashed & Buyins")
            plt.xlabel("Buyins in $")
            plt.ylabel("Cashed in $")
            plt.legend(['USD'])
            ax.scatter(self.cost_unsort, self.prize_unsort, alpha=0.8, edgecolors='none', s=30)
            return plt.show()     

        elif self.mode == 'winbuy2':
            # not done yet
            x_start = 0 
            x_end = float(self.data[1][0][-1]) + 50
            y_start = 0
            y_end = float(self.data[0][0][-1]) + 50
            plt.plot(self.cost_unsort, self.prize_unsort, 'r')
            plt.axis([float(x_start), float(x_end), float(y_start), float(y_end)])
            return plt.show()

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
        self.avg_win = np.mean(self.data[0][0])
        self.avg_cost = np.mean(self.data[1][0])
        self.avg_place = np.mean(self.data[2][0])
        self.avg_players = np.mean(self.data[3][0])      
        # medians
        self.med_win = np.median(self.data[0][0])
        self.med_cost = np.median(self.data[1][0])
        self.med_place = np.median(self.data[2][0])
        self.med_players = np.median(self.data[3][0])       
        # max's
        self.max_win = np.max(self.data[0][0])
        self.max_cost = np.max(self.data[1][0])
        self.max_place = np.min(self.data[2][0])
        self.max_players = np.max(self.data[3][0])        
        # min's
        self.min_win = np.min(self.data[0][0])
        self.min_cost = np.min(self.data[1][0])
        self.min_place = np.max(self.data[2][0])
        self.min_players = np.min(self.data[3][0])        
        # percentiles
        self.percentile_25_win = np.percentile(self.data[0][0], 25)
        self.percentile_75_win = np.percentile(self.data[0][0], 75)
        self.range_win = self.percentile_75_win - self.percentile_25_win

        self.percentile_25_cost = np.percentile(self.data[1][0], 25)
        self.percentile_75_cost = np.percentile(self.data[1][0], 75)
        self.range_cost = self.percentile_75_cost - self.percentile_25_cost

        self.percentile_25_place = np.percentile(self.data[2][0], 25)
        self.percentile_75_place = np.percentile(self.data[2][0], 75)
        self.range_place = self.percentile_75_place - self.percentile_25_place

        self.percentile_25_players = np.percentile(self.data[3][0], 25)
        self.percentile_75_players = np.percentile(self.data[3][0], 75)
        self.range_players = self.percentile_75_players - self.percentile_25_players
        #percentages
        self.knockout_diff = ((self.knockout_profit - self.knockout_buyin))
        self.regular_diff = ((self.regular_profit - self.regular_buyin))
        self.spin_diff = ((self.spin_profit - self.spin_buyin))
        self.headsup_diff = ((self.headsup_profit - self.headsup_buyin))

    def create_array(self):
        """
        Creating arrary for calculations.
        Format:
            [WIN]  :0 
            [COST] :1 
            [PLACE]:2 
            [FIELD]:3"""
        self.sort_data()
        self.data = np.array(
            [
            [self.prize],
            [self.cost],
            [self.place],
            [self.players]
            ])
        return self.data

    def sort_data(self):
        """Sorting data for arrarys and graphs."""
        self.prize_unsort = list()
        self.cost_unsort = list()
        self.players_unsort = list()
        self.place_unsort = list()
        
        for item in self.raw_data:
            self.prize_unsort.append(item['win'])
            self.cost_unsort.append(item['buyin'])
            self.players_unsort.append(item['players'])
            self.place_unsort.append(item['place'])

        self.prize = np.sort(self.prize_unsort)
        self.cost = np.sort(self.cost_unsort)
        self.players = np.sort(self.players_unsort)
        self.place = np.sort(self.place_unsort)

class AddRemove(SimpleOverview):
    """
    Adds and removes tournaments from local JSON.
    Then uploads that to online JSON."""
    def __init__(self, url=config.cur_url, cur_file=config.cur_file):
        super().__init__(url, cur_file)
        self.read = self.read_local

    def add_json(self):
        """
        Adds new tournament from user input.
        Too many times I've hit space or a wrong key and exited,
        not anymore!"""
        data_n = self.read
        try:
            new_id = input('\nTournament ID\nExample: 958472652\n\nEnter Here: ')
            if not int(new_id) > 0:
                ValueError()
        except:
            ValueError()
        try:
            new_date = input('\nTournament Date\nExample: 2019-05-19\n\nEnter Here: ')
            if type(new_date) == int() or type(new_date) == float():
                ValueError()
        except:
            ValueError()
        try:
            new_type = input('\nTournament Type\nExample: Knockout | Regular | Spin | Headsup\n\nEnter Here: ')
            if type(new_type) == int() or type(new_type) == float():
                ValueError()
        except:
            ValueError()
        try:
            new_players = input('\nTournament Field\nExample: 4500\n\nEnter Here: ')
            if not int(new_players) >= 2:
                ValueError()
        except:
            ValueError()
        try:
            new_place = input('\nTournament Placement\nExample: 1\n\nEnter Here: ')
            if not int(new_place) >= 1:
                ValueError()
        except:
            ValueError()
        try:
            new_buyin = input('\nTournament Buy-in\nExample: 10.5\n\nEnter Here: ')
            if not float(new_buyin) >= 0.01:
                ValueError()
        except:
            ValueError()
        try:
            new_win = input('\nTournament Cashed\nExample: 175.54\n\nEnter Here: ')
            if not float(new_win) >= 0:
                ValueError()
        except:
            ValueError()
        data_n['poker'].append(
            {'id': int(new_id), 
            'date': str(new_date), 
            'type': str(new_type), 
            'players': int(new_players), 
            'place': int(new_place), 
            'buyin': float(new_buyin), 
            'win': float(new_win)}
            )
        return data_n

    def del_json(self):
        """Deletes tournament specified by the user from local JSON."""
        data_d = self.read
        print('\n[1] Remove Tournament by Index\n[2] Remove Latest Added Tournament\n[3] Return to Start')
        choice_remove = input('\nEnter Here: ')

        if int(choice_remove) == 2:
            del data_d['poker'][-1]

        elif int(choice_remove) == 1:
            index_remove = input('\nIndex Value to Remove\nEnter Here: ')
        
            if int(index_remove) <= (len(data_d['poker'])) - 1:
                del data_d['poker'][int(index_remove)]

            else:
                print('\nIndex Value Not Found. Try Again.')
                start()

        elif int(choice_remove) == 3 or int(choice_remove) == 0:
            start()

        else:
            print('\nCommand Not Found. Try Again.')

        return data_d

    def add_to_json(self):
        """Adds the new tournament and then writes new file to a local JSON."""
        data_new = self.add_json()
        self.write_to_json(data_new)
        self.update_bin()

    def del_from_json(self):
        """Deletes the tournament and then writes new file to a local JSON."""
        data_del = self.del_json()
        self.write_to_json(data_del)  
        self.update_bin()

class Error(Exception):
    """Base class for exceptions in this module.
        Only one Error class added thus far."""

class ValueError(Error):
    """Exception raised for errors in the input."""
    def __init__(self):
        self.pointer()
        
    def pointer(self):
        print('\nVALUE ERROR | INPUT ERROR\nRETURNING TO START.')
        start()

if __name__ == '__main__':
    """Kick starts the app"""
    start()


