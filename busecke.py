#! /usr/bin/env python

import math

###########################################################################
# MB L/O 319 Eckenschnittvorlagenrechner
#
# Aussenhaut Profil folgt y = 0.5 * x^2 (in cm)
# fuer x>0.83cm
#
# Radius Ecke unten ist 24cm
# Radius Ecke Bodenhoehe ist 30cm
#
# Sinn dieses Scripts ist Erstellung eines "Schnittmusters"
# fuers Blech um eine Ecke nachzubauen.
#
#
# Zuerst wird eine Wertetabelle erstellt in 0.5cm schritten entlang y (h)
#
###########################################################################

c = 24 # Konstante fuer offset der Parabel vom Zentrum weg
n = 5 # Konstante fuer die Anzahl der "Blaetter"/Streben

z = 90 # Kreisbogen Ausschnitt (0...360 deg)

h_min = 0 # hoehe min in mm
h_max = 180 # hoehe max in mm

###########################################################################

z_rel = z/360.0
print z_rel


r_max = 0 # max. radius. wird waehrend Berechnung gefuellt

wertetabelle_profil = []

for h_mm in range(h_min,h_max+5,5): # hoehe in mm
    h = h_mm*0.1 # hoehe
    r = c + pow(2*h,0.5) # radius

    if r > r_max:
        r_max = r

    wertetabelle_profil.append([h,r])


# wir rechnen hier in Polarkoordinaten und keinem spherischen oder parabelfoermigen Koordinatensystem,
# d.h. je groesser der Winkel gegenueber der Senkrechten wird umso groesser wird der Fehler und es fehlt
# an der Stelle dann Blech in der Aussenhaut. Das sollte sich aber nur bei nicht-idealem Blech dicker als
# 0 mm bemerkbar machen. Wie viel das in der Praxis ausmacht muss anhand eine Pappschablone etc. getestet werden,
# ansonsten wird mir die Rechnerei zu wild.
#
# Moegliche Loesung: Neuberechnung der Y-Achse / hoehe. Wir kennen delta-radius und delta-hoehe,
# somit laesst sich also per Pythagoras berechnen wie viel extramaterial fuer die Schraege notwendig ist
#
# Rechnen wir mal die Streckfaktoren fuer die einzelnen Segmente aus...
# Anzahl der Werte ist eines geringer als Anzahl der Punkte die verbinden

streckwerte = []

for i in range(0,len(wertetabelle_profil)-1):
    h1 = wertetabelle_profil[i][0]
    r1 = wertetabelle_profil[i][1]
    h2 = wertetabelle_profil[i+1][0]
    r2 = wertetabelle_profil[i+1][1]

    strecke_1_2 = math.pow(math.pow(r2-r1,2)+math.pow(h2-h1,2),0.5)
    print "strecke %i %i ist %f bei deltaH %f"%(i,i+1,strecke_1_2,h2-h1)
    streckwerte.append(strecke_1_2)

# da jetzt bekannt ist wie lange die strecken wirklich sind kann man die
# y- bzw. h-werte entlang der Huelle neu berechnen


h_laufwert = wertetabelle_profil[0][0]
h_gestreckt = [h_laufwert]
for item in streckwerte: 
    h_laufwert+=item
    h_gestreckt.append( h_laufwert)

print h_gestreckt


wertetabelle_radius_relativ = []

for item in wertetabelle_profil: # werte ausgeben, relativen radius berechnen
    relativer_radius = item[1] / r_max # radius / radius max.

    # es wird immer das erste Element von h_gestreckt genommen und die restlichen Elemente ruecken nach
    h_neu = h_gestreckt.pop(0)


    wertetabelle_radius_relativ.append([item[0],item[1],relativer_radius,h_neu]) # h, r, r_rel, h_neu

    # Radius und Umfang sind, da umfang = 2 * pi * r, proportional zueinander
   
    print item[0],item[1], relativer_radius, h_neu 

# jetzt sind alle Daten vorhanden um die einzelnen Koordinaten
# eines Polygons das die Schnittkante beschreibt
# zu berechnen.
#
# Hierfuer wird fuer die Anzahl der Blaetter mal zwei (auf und abwaerts)
# mal der Anzahl der Punkte in der Wertetabelle
# die Berechnung der Koordinaten durchgefuerht
# und das Ergebnis wieder in eine Wertetabelle eingetragen

wertetabelle_polygon_schnitt = [[0,0]]

umfang_max = 2.0 * math.pi * r_max * z_rel # Kreisbogen Abschnitt. Definiert die Breite des Blechstuecks
print "Blechbreite ist ",umfang_max,"cm"
print "Blechhoehe ist ",(h_max-h_min)*0.1,"cm"

segmente = n*2 # anzahl blaetter mal zwei (aufwarts und abwaerts)
segment_aktuell = 0
segment_breite = umfang_max / segmente


for blattnr in range(0,n,1): # fuer alle Blaetter
    print "Berechne nun Blatt Nummer ",blattnr
    for ud in ["d","u"]: # auf- und abwaerts
        #print "Berechne nun Richtung ", ud

        # Reihenfolge umkehren je nach Richtung
        if ud == "d":
            wertetabelle_radius_relativ_umsortiert = wertetabelle_radius_relativ
        if ud == "u":
            wertetabelle_radius_relativ_umsortiert = reversed(wertetabelle_radius_relativ)

        for item in wertetabelle_radius_relativ_umsortiert:
            #print "Berechne nun fuer hoehe ",item[0]


            poly_x = 0
            poly_y = 0

            # y Richtung wird von korrigierten/gestreckten Werten uebernommen
            #poly_y = (item[0]-h_min*0.1)/((h_max - h_min)*0.1) * h_max*0.1
            poly_y = item[3]

            # x Richtung ergibt sich aus relativem Radiusanteil an umfang_max
            poly_x = item[2] * umfang_max / segmente + (segment_aktuell * segment_breite)


            #poly_x = (1-item[2]) * umfang_max / segmente

            poly_x = segment_breite * segment_aktuell

            poly_x_add = ( (1-item[2]) * umfang_max ) / segmente

            if ud == "u":
                poly_x+=poly_x_add - segment_breite /2
            if ud == "d":
                poly_x-=poly_x_add - segment_breite /2

            poly_x+=segment_breite/2

            #print "Koordinate ist ",poly_x,poly_y

            wertetabelle_polygon_schnitt.append([poly_x,poly_y])




        segment_aktuell+=1

wertetabelle_polygon_schnitt.append([umfang_max,0])

array_plot_x = []
array_plot_y = []

for item in wertetabelle_polygon_schnitt:
    print item[0],item[1]
    array_plot_x.append(item[0])
    array_plot_y.append(item[1])


import matplotlib.pyplot as plt
plt.plot(array_plot_x,array_plot_y)
plt.show()
