# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 16:16:20 2020

@author: Ga
"""

import report
import graphs
import textMining
import sys

print("Watcha wanna see?")
print("-----------------")

while(True):
    action = input("Input -mining-, -report-, -graphs- or -exit- to end : ")
    
    while(True):     
        if(action == "mining"):
            textMining.executeMining()
            break
        elif(action == "report"):
            report.executeReport()
            break
        elif(action == "graphs"):
            graphs.executeGraphs()
            break
        else:
            print("Try again : ")
            continue
    if(action == "exit"):
            while(True):
                exitProg = input("Exit? y/n \n")
                if(exitProg == "y"):
                    print("Exiting program")
                    sys.exit(0)
                elif(exitProg == "n"):
                    break

#test2
#test 3