#!/usr/bin/env python

data = [[2.65,0.00],[2.64,10.00],[2.60,20.01],[2.51,31.56],[2.45,36.61],[2.37,41.69],[2.27,46.83],[2.17,50.50],[2.06,52.48],[3.25,52.48],[3.13,50.50],[3.04,46.83],[2.93,41.69],[2.85,36.61],[2.79,31.56],[2.71,20.01],[2.66,10.00],[2.65,0.00],[2.71,20.01],[2.66,10.00],[2.65,0.00]]

header = '<svg xmlns="http://www.w3.org/2000/svg" height="500cm" width="500cm">'
footer = '</svg>'


print header

lastrow = False
for row in data:
    if lastrow != False:
        svgrow = "<line x1=\"%fcm\" y1=\"%fcm\" x2=\"%fcm\" y2=\"%fcm\" style=\"stroke:rgb(255,0,0);stroke-width:1mm\" />"%(row[0],row[1],lastrow[0],lastrow[1])
        print svgrow
    lastrow = row

print footer
