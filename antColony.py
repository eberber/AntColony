import random

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

#returns a list of links from the file
def initLinks(file):
    linkList = []

    with open(file) as file:
        lines = [line.split() for line in file]
    for i in range(1,len(lines)):
        print(lines[i])
        for j in range(1,len(lines[i])):
            print(lines[i][j])
            if lines[i][j] == '0':
                continue
            else:
                newLink = link(lines[i][0], lines[0][j-1], 0.000001, lines[i][j], 0)
                linkList.append(newLink)

    #create cities and each link associated with that starting city
    availableCities = lines[0]
    citiesList = []
    for i in availableCities:
        newCity = city(i, 2, [])
        for j in range(len(linkList)):
            if i == linkList[j].start:
                newCity.atttachedLinks.append(linkList[j])
        citiesList.append(newCity)
    return citiesList, availableCities

def inTabuList(city, tabuList):
    for i in tabuList:
        if city == tabuList:
            return True
    return False

def citySelection(newAnt, city, alpha, beta):
    if inTabuList(city.city, newAnt.tabuList):
        return False
    #compute probability of each link and sum them for each link from where the ant currently is
    for i in city.atttachedLinks:
        link = i
        denominator = pow(link.linkPheromoneAmount, alpha) * pow(1/ link.distance, beta)
        denominator += denominator
    #compute prob using diff numerator for each link and sum them
    for i in city.atttachedLinks:
        link  = i
        numerator = pow(link.linkPheromoneAmount, alpha) * pow(1/ link.distance, beta)
        link.probability = numerator / denominator      
        totalProb += link.probability
    finalProb = random.uniform(0, totalProb) #choose rand value between  0 and sum of all links prob
    x = 0
    for i in city.atttachedLinks:
        y += link.probability
        if finalProb in range(x, y): # if our guess is within prev link and curr, choose curr links destination city
            link.linkPheromoneAmount = newAnt.antPheromoneAmount / link.distance #add pheromone
            return link.end
        else:
            x += link.probability

    return False #error

#recursively selects a new city until all are visited
def antTour(newAnt, city, cityList):
    if inTabuList(city.city, newAnt.tabuList): #check if we have visited this city
        return
    newAnt.tabuList.append(city.city)#add the ants current city to its tabu list  
    choice = citySelection(newAnt, city, 1 ,1)
    if choice == False:
        return
    else:
        for i in cityList:
            if choice == i.city: #search for the next city to start from
                antTour(newAnt, i.city, cityList)


def cityTour(numbAnts):
    file = "map1.txt"
    cities, availableCities = initLinks(file)
    #iterate through each city and the num ants there
    for i in cities:
        for j in i.numberAnts:
            newAnt = ant(120,0.0, [])
            #each ant is completing a tour
            antTour(newAnt, i, cities)           

    
def main():    
    numbAnts = 2
    cityTour(numbAnts)

if __name__ == "__main__":
    main()