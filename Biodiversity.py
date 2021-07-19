# Script that finds the number of animals at a given distance from a specified location. The birds and mammals txt's contain the corresponding
# animals with their locations as Latitudes and Lognitudes. After finding the distance, the locations of the animals are wirtten in a kml format
# for Google Earth, showing the locations as pins on the globe. Finally, the biodiversity (unique species) in a give area is calculated.
# The data is taken from gbif.org

import math

class dist:
    """Calculate the distance in kilometres (km) between two locations. Each location is set according to its Latitude and Lognitute."""
    
    def __init__(self, Lat1, Lon1, Lat2, Lon2):
        self.Lat1 = float(Lat1)
        self.Lon1 = float(Lon1)
        self.Lat2 = float(Lat2)
        self.Lon2 = float(Lon2)
    
    def latlon(self):

        nDLat = (self.Lat1 - self.Lat2) * 0.017453293
        nDLon = (self.Lon1 - self.Lon2) * 0.017453293

        Lat1 = self.Lat1 * 0.017453293
        Lat2 = self.Lat2 * 0.017453293

        nA = (math.sin(nDLat/2) ** 2) + math.cos(Lat1) * math.cos(Lat2) * (math.sin(nDLon/2) ** 2 )
        nC = 2 * math.atan2(math.sqrt(nA),math.sqrt( 1 - nA ))
        nD = 6372.797 * nC
        return nD


def LineToList(Str):
    """Makes values tab delimited."""
    
    Str = Str.rstrip()
    
    return Str.split("\t")


def LocationCount(animal, FileName, Distance, Lat, Lon):
    """Find the number of animals in a give distance(km)."""
    
    animal_type = str(animal)
    with open(FileName, "r") as FIn:
        
        MammalList = FIn.readlines()
        ancount = 0

        for x in range(len(MammalList)):    # For loop to check if the distance between the given Lat and Lon is <= to Distance
            
            alist = LineToList(MammalList[x])
            
            dista = dist(alist[1], alist[2], Lat, Lon)  # dist class call
            Dis = dista.latlon()
                        
            if Dis <= Distance: # Checking if calculated distance is <= to given distance.
                ancount += 1
        FIn.close()
    
    print('\n%s:' %animal_type)
    print("Number of %s within %skm: %d" %(animal_type, Distance, ancount))
    return ancount


def PrintLocation(FileName, Distance, Lat, Lon):
    """Output animal locations in kml for Google Earth."""
    
    with open(FileName, "r") as FIn:

        KMLList = FIn.readlines()
        
        with open("Output.kml", "w") as FOut:
            print("<Document>", file = FOut)
            
            for y in range(len(KMLList)):   # Print all strings from the KMLList in a kml file with the corresponding species names and coordinates 
                                            # in a tab delimited format, with Lon printed first instead of Lan.

                alist = LineToList(KMLList[y])
                 
                dista = dist(alist[1], alist[2], Lat, Lon)  # dist class call
                Dis = dista.latlon()

                if Dis <= Distance:    # if calculated distance is <= to given distance, write to kml.
                    print("\t<Placemark>", file = FOut)
                    print("\t\t<description>" + alist[0] + "</description>", file = FOut)
                    print("\t\t<Point>", file = FOut)
                    print("\t\t\t<coordinates>" + alist[2] + ", " + alist[1] + "</coordinates>", file = FOut)
                    print("\t\t</Point>", file = FOut)
                    print("\t</Placemark>", file = FOut)
            print("</Document>", file = FOut)
        FOut.close()


def BiodiversityCount(FileName, Distance, Lat, Lon):
    """Calculate the number of unique species within a give distance(km)."""
    
    with open(FileName, "r") as FIn:
        
        BioList = FIn.readlines()

        DiverseAnimals = []
        
        for z in range(len(BioList)):   # Add all unique species into the empty list

            alist = LineToList(BioList[z])

            dista = dist(alist[1], alist[2], Lat, Lon)  # dist class call
            Dis = dista.latlon()

            if Dis <= Distance:    # Checking if calculated distance is <= to given distance.
                if not DiverseAnimals:
                    DiverseAnimals.append(alist[0])
                
                elif not alist[0] in DiverseAnimals:                    
                    DiverseAnimals.append(alist[0])
                    
        result = len(DiverseAnimals)
        print("Number of species within %skm: %d" %(Distance,result))
        FIn.close()
    return result


if __name__ == "__main__":
    
    # Files.
    mammals_f = 'Mammal.txt'
    birds_f = 'Birds.txt'
    
    # For Mammals.
    LocationCount('Mammals', mammals_f, 15.0, 54.988056, -1.619444) # The Town Moor park in Newcastle, Lat, Lon
    PrintLocation(mammals_f, 15.0, 51.452884, -0.973906)    # Reading Borough Council, Lat, Lon
    BiodiversityCount(mammals_f, 25.0, 51.508129, -0.128005)    # Trafalgar square, Lat, Lon
    
    # For Birds
    LocationCount('Birds', birds_f, 15.0, 54.988056, -1.619444) # The Town Moor park in Newcastle, Lat, Lon
    PrintLocation(birds_f, 15.0, 51.452884, -0.973906)    # Reading Borough Council, Lat, Lon
    BiodiversityCount(birds_f, 25.0, 51.508129, -0.128005)    # Trafalgar square, Lat, Lon