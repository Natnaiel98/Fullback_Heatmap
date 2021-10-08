# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 22:01:44 2021

@author: natem
"""
# I would work on the speed/efficiency of this function
# to improve the efficiency, I should revise what the current function does
# the current function, we basically put all the events in the WC in one dataframe
# ideally, we could use the player name to filter out the dataframes we merge to only include that player's actions
# the earlier in the code we do this, the more efficient our code is
# perhaps we can do this when deciding which match id is put into the list??
# or when
#settled on adding team name as an argument so we can filter out match Ids involving that national team(seemed to work in increasing the efficiency)

def FBHeatmap(Team_Name):
 
 from scipy.spatial import ConvexHull
 import math
 import matplotlib.pyplot as plt
 import json
 import numpy as np
 import pandas as pd
 import matplotlib.pyplot as plt
 from matplotlib.patches import Arc
 import seaborn as sns
 import FCPython 
 from FCPython import createPitch  
 from pandas.io.json import json_normalize
 
 
 pitchLengthX=120
 pitchWidthY=80
 #making sure we are putting the match Ids of all 64 WC matches
 #can I look at exclude match id based on the 
 competition_id=43
 with open('Statsbomb/data/matches/'+str(competition_id)+'/3.json') as f:
    matches = json.load(f)
    
    
 match_ids1=[]
 for match in matches:
    if match['away_team']['away_team_name']== Team_Name or match['home_team']['home_team_name']== Team_Name:
        match_ids1.append(match['match_id'])


 #creating a dict with our file paths for matches in the MATCH IDS list(figure out a way to make this list given a player name)
 aa={}
 for number in range(len(match_ids1)):
    aa["keys%s" %number]= str(match_ids1[number])+'.json'
    
 bb={}
 for  hh in range(len(match_ids1)):
    bb["keys%s" %hh]=json.load(open('Statsbomb/data/events/'+aa["keys%s" %hh],encoding="utf8"))
 cc={}
 for  hh in range(len(match_ids1)):
    cc["keys%s" %hh]=json_normalize(bb["keys%s" %hh], sep = "_").assign(match_id = aa["keys%s" %hh][:-5])
 
    
#merge all tables by creating list with all of the tables in it and merging the list
 listofall=[]
 for i in range(len(cc)):
     listofall.append(cc["keys%s" %i] )
     
 dff=pd.concat(listofall)
 
 #dropping missing values 
 
# let's try another function that collects the names of all defenders of a team and applies the heatmap function on all 
# what I can do is use a loop to use match id to load the line based one each team's first WC lineup

#tried to load in team data to identify each player, weird formatting though so better to find these player names from the event data
#for this find every unique player_name in the event data for the National teams' matches (append to a new list)
#nned to add the @ since that is the only way to refenrence a var in .query
 df1=np.array(dff)
 ff=dff.query('(team_name==@Team_Name) & (position_name=="Left Back" or position_name=="Right Back" )')
 Fbnames=ff['player_name'].unique()
 FBnames=Fbnames.tolist()
 dfff=dff.dropna(subset=['location'])
 
 
 #find all a specific player's matches [the player name given in the function]
 #change takes place here, instead of having player_name as an input, we get it from the FBnames list
 
 #fix table and plot heat map for each player in the FBnames list
 for Player_name in FBnames:
  Playe=dfff[dfff['player_name']==Player_name ]
  Playe=Playe[['player_name','team_name','minute','location']]
  Playerr=Playe['player_name']
  Minute=Playe['minute']
  Team=Playe['team_name']
 


  #split location into x and y
  x=[]
  y=[]
  ll=Playe['location'].tolist()
  ll2=[]
  for kk in ll:
       if np.any(np.isnan(kk) == False):
        ll2.append(kk)

  for jj in range(len(ll)):
     x.append(ll[jj][0])
     y.append(ll[jj][1])
 #FINAL DATAFRAME
  Playe1=pd.DataFrame({"Player":Playerr,"Team":Team,"Minute":Minute,"x":x,"y":y})
  defpoints = Playe1[['x', 'y']].values
  #try creating a heatmap this for all of the Player's game
  #to do this, have list of match
  #over lay these points onto the plot ()
  (fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')
  #Plot one - include shade
  sns.kdeplot(Playe1["x"],Playe1["y"], shade="True", n_levels=50)
  #sns.kdeplot(Playe1["x"],Playe1["y"], shade="True", shade_lowest=False,n_levels=4,cmap='magma') Alternate format
  
  plt.title( Player_name +' WC Heatmap' +'\nDirection of Play ->')
    
    
    


