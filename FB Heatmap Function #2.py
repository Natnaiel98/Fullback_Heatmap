# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 18:09:04 2021

@author: natem
"""

def FBHeatmap(Team_Name):
 
 import math
 import matplotlib.pyplot as plt
 import json
 import numpy as np
 import pandas as pd
 import matplotlib.pyplot as plt
 import seaborn as sns
 from pandas.io.json import json_normalize
 from scipy.spatial import ConvexHull
 from matplotlib.patches import Arc

 pitchLengthX=120
 pitchWidthY=80
 #making sure we are putting the match Ids of all 64 WC matches
 with open('43/3.json') as f:
    matches = json.load(f)
    
    
 match_ids1=[]
 for match in matches:
    if match['away_team']['away_team_name']== Team_Name or match['home_team']['home_team_name']== Team_Name:
        match_ids1.append(match['match_id'])

 #creating a dictionary with our file paths for matches in the MATCH IDS list
 aa={}
 for number in range(len(match_ids1)):
    aa["keys%s" %number]= str(match_ids1[number])+'.json'
    
 bb={}
 for  hh in range(len(match_ids1)):
    bb["keys%s" %hh]=json.load(open('events/'+aa["keys%s" %hh],encoding="utf8"))
 cc={}
 for  hh in range(len(match_ids1)):
    cc["keys%s" %hh]=json_normalize(bb["keys%s" %hh], sep = "_").assign(match_id = aa["keys%s" %hh][:-5])
 
    
#merge all tables by creating list with all of the tables in it and merging the list
 listofall=[]
 for i in range(len(cc)):
     listofall.append(cc["keys%s" %i] )
     
 dff=pd.concat(listofall)
 
 
 # let's try another function that collects the names of all defenders of a team and applies the heatmap function on all 
 # what I can do is use a loop to use match id to load the line based one each team's first WC lineup
 # for this find every unique player_name in the event data for the National teams' matches (append to a new list)
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
  Playe=Playe[['player_name','team_name','minute','location','position_name']]
  Playerr=Playe['player_name']
  Minute=Playe['minute']
  Team=Playe['team_name']
  position_name=Playe['position_name']
 


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
  Playe1=pd.DataFrame({"Player":Playerr,"Position":position_name,"Team":Team,"Minute":Minute,"x":x,"y":y})
  defpoints = Playe1[['x', 'y']].values
  #try creating a heatmap this for all of the Player's game
  #to do this, have list of match
  #over lay these points onto the plot ()
  
  #over lay these points onto the plot only if a player passes a threshold of events
  trufb=Playe1.query('(Position=="Left Back" or Position=="Right Back")')
  if len(trufb.index)>50:
  #Create pitch and heatmap
  #Pitch Outline & Centre Line
      #Create figure
   fig=plt.figure()
   ax=fig.add_subplot(1,1,1)

   #Pitch Outline & Centre Line
   plt.plot([0,0],[0,90], color="black")
   plt.plot([0,130],[90,90], color="black")
   plt.plot([130,130],[90,0], color="black")
   plt.plot([130,0],[0,0], color="black")
   plt.plot([65,65],[0,90], color="black")
    
   #Left Penalty Area
   plt.plot([16.5,16.5],[65,25],color="black")
   plt.plot([0,16.5],[65,65],color="black")
   plt.plot([16.5,0],[25,25],color="black")
    
   #Right Penalty Area
   plt.plot([130,113.5],[65,65],color="black")
   plt.plot([113.5,113.5],[65,25],color="black")
   plt.plot([113.5,130],[25,25],color="black")
    
   #Left 6-yard Box
   plt.plot([0,5.5],[54,54],color="black")
   plt.plot([5.5,5.5],[54,36],color="black")
   plt.plot([5.5,0.5],[36,36],color="black")
    
   #Right 6-yard Box
   plt.plot([130,124.5],[54,54],color="black")
   plt.plot([124.5,124.5],[54,36],color="black")
   plt.plot([124.5,130],[36,36],color="black")
    
   #Prepare Circles
   centreCircle = plt.Circle((65,45),9.15,color="black",fill=False)
   centreSpot = plt.Circle((65,45),0.8,color="black")
   leftPenSpot = plt.Circle((11,45),0.8,color="black")
   rightPenSpot = plt.Circle((119,45),0.8,color="black")
    
   #Draw Circles
   ax.add_patch(centreCircle)
   ax.add_patch(centreSpot)
   ax.add_patch(leftPenSpot)
   ax.add_patch(rightPenSpot)
    
   #Prepare Arcs
   leftArc = Arc((11,45),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color="black")
   rightArc = Arc((119,45),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color="black")

   #Draw Arcs
   ax.add_patch(leftArc)
   ax.add_patch(rightArc)
    
   #Tidy Axes
   plt.axis('off')
   sns.kdeplot(Playe1["x"],Playe1["y"], shade="True", n_levels=50)
   plt.title( Player_name +' WC Heatmap' +'\nDirection of Play ->')

   plt.show()