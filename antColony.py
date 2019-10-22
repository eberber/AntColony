import random
import numpy
#################       GLOBAL VARIABLES        ###################
max = 0.0
avg = 0.0
min = 0.0
totalDistance = 0.0
alpha = 0.0
beta = 0.0
QPheromone = 0.0
antPerCity = 0
file = ""
numIterations = 0
#################       OBJECTS     #########################
class ant:
    antPheromoneAmount = 0.0
    totalDistanceTraveled = 0.0
    tabuList = []
    def __init__(self, antPheromoneAmount, totalDistanceTraveled, tabuList):
        self.antPheromoneAmount = antPheromoneAmount
        self.totalDistanceTraveled = totalDistanceTraveled
        self.tabuList = tabuList
class link:
    start = ""
    end = ""
    linkPheromoneAmount = 0.0
    distance = 0.0
    probability = 0.0

    def __init__(self, start, end, linkPheromoneAmount, distance, probability):
        self.start = start
        self.end = end
        self.linkPheromoneAmount = linkPheromoneAmount
        self.distance = float(distance)
        self.probability = probability
class city:
    city = ""
    numberAnts = 0
    atttachedLinks = []
    def __init__(self, city, numberAnts, atttachedLinks):
        self.city = city
        self.numberAnts = numberAnts        
        self.atttachedLinks = atttachedLinks
################        GLOBAL FUNCTIONS        ##################
#returns a list of links from the file
def initLinks():
    linkList = []
    global file
    global antPerCity

    with open(file) as file:
        lines = [line.split() for line in file]
    for i in range(1,len(lines)):
        #print(lines[i])
        for j in range(1,len(lines[i])):
            #print(lines[i][j])
            if lines[i][j] == '0':
                continue
            else:
                newLink = link(lines[i][0], lines[0][j-1], 0.000001, lines[i][j], 0)
                linkList.append(newLink)

    #create cities and each link associated with that starting city
    availableCities = lines[0]
    citiesList = []
    for i in availableCities:
        newCity = city(i, antPerCity, [])
        for j in range(len(linkList)):
            if i == linkList[j].start:
                newCity.atttachedLinks.append(linkList[j])
        citiesList.append(newCity)
    return citiesList, availableCities

def inTabuList(city, tabuList):
    for i in tabuList:
        if city == i: #compares two chars of the city ex: 'C' and 'A'
            return True
    return False
#compute min, max ,avg
def stats(newAnt, antCount):
    global max
    global min
    global avg
    global totalDistance
    #set init max and min to first ants travel distance
    if min == 0.0:
        min = newAnt.totalDistanceTraveled
    if max == 0.0:
        max = newAnt.totalDistanceTraveled

    if newAnt.totalDistanceTraveled < min:
        min = newAnt.totalDistanceTraveled
    elif newAnt.totalDistanceTraveled > max:
        max = newAnt.totalDistanceTraveled
    totalDistance += newAnt.totalDistanceTraveled
    avg = round(totalDistance / antCount, 2)
    print("MAX: ",max)
    print("MIN: ",min)
    print("AVG: ",avg)    

def citySelection(newAnt, city):
    global alpha
    global beta
    #compute probability of each link and sum them for each link from where the ant currently is
    for i in city.atttachedLinks:
        if i.end in newAnt.tabuList: #skip over links that take us to a city we have already been to
            continue
        else:
            denominator = pow(i.linkPheromoneAmount, alpha) * pow(1/ i.distance, beta)
            denominator += denominator
    #compute prob using diff numerator for each link and sum them
    totalProb = 0
    for i in city.atttachedLinks:
        if i.end in newAnt.tabuList:#skip over links that take us to a city we have already been to
            continue
        else:
            numerator = pow(i.linkPheromoneAmount, alpha) * pow(1/ i.distance, beta)
            i.probability = numerator / denominator  #each links prob is updated 
            totalProb += i.probability
    finalProb = round(random.uniform(0, totalProb), 2) #choose rand value between  0 and sum of all links prob
    x = 0
    y = 0
    for i in city.atttachedLinks:
        if i.end in newAnt.tabuList:
            continue
        else:
            y += i.probability
            if x <= finalProb <= y: # if our guess is within prev link and curr, choose curr links destination city
                i.linkPheromoneAmount = newAnt.antPheromoneAmount / i.distance #add pheromone
                newAnt.totalDistanceTraveled += i.distance #update distance traveled
                return i.end
            else:
                x += i.probability
    return False #error

#recursively selects a new city until all are visited
def antTour(newAnt, city, cityList):
    if inTabuList(city.city, newAnt.tabuList): #check if we have visited this city
        return
    newAnt.tabuList.append(city.city)#add the ants current city to its tabu list  
    choice = citySelection(newAnt, city)

    if not choice:
        return
    else:
        for i in cityList:
            if choice == i.city: #search for the next city to start from
                print("Ant is going to: ", i.city)
                antTour(newAnt, i, cityList) #pass that city object recursively

#finds the link that takes you home from the current city ant is at
def returnHome(newAnt, cityList):
    for i in cityList:
        if i.city == newAnt.tabuList[-1]: #if the city was the last visited by ant
            for j in i.atttachedLinks:
                if j.end == newAnt.tabuList[0]:#if the destination is the start of where ant traveled
                    newAnt.totalDistanceTraveled += j.distance
                    print("Going home...", j.end)               


def cityTour():
    global QPheromone
    global numIterations

    cities, availableCities = initLinks()
    antCount = 0
    for n in range(numIterations): # run for n iterations
        print("######################### ITERATION #######################", n)
        #iterate through each city and the num ants there
        for i in cities:
            print("###########       START CITY        #########", i.city)
            for j in range(i.numberAnts):
                newAnt = ant(QPheromone,0.0, [])
                antCount += 1
                #each ant is completing a tour
                print("####     ANT     ####", j)
                antTour(newAnt, i, cities)
                returnHome(newAnt, cities)
                print("Distance traveled: ", newAnt.totalDistanceTraveled)
                stats(newAnt, antCount)           

def main():        
    global alpha
    global beta
    global QPheromone
    global file
    global antPerCity
    global numIterations

    print("ANT PER CITY: ")
    antPerCity = int(input())
    print("ALPHA: ")
    alpha = float(input())
    print("BETA: ")
    beta = float(input())
    print("ANT PHEROMONE Q: ")
    QPheromone = float(input())
    print("NUMBER OF ITERATIONS TO RUN: ")
    numIterations = int(input())
    print("FILE NAME: ")
    file = input()

    cityTour()

if __name__ == "__main__":
    main()