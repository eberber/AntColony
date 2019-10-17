class ant:
    antPheromoneAmount = 0.0
    totalDistanceTraveled = 0.0
    tabuList = []
    def __init__(self, antPheromoneAmount, totalDistanceTraveled):
        self.antPheromoneAmount = antPheromoneAmount
        self.totalDistanceTraveled = totalDistanceTraveled
        self.tabuList
class link:
    start = ""
    end = ""
    linkPheromoneAmount = 0.0
    distance = 0.0

    def __init__(self, start, end, linkPheromoneAmount, distance):
        self.start = start
        self.end = end
        self.linkPheromoneAmount = linkPheromoneAmount
        self.distance = float(distance)

#returns a list of links from the file
def initLinks(file):
    linkList = []
    cities = []
    with open(file) as file:
        lines = [line.split() for line in file]
    for i in range(1,len(lines)):
        print(lines[i])
        for j in range(1,len(lines[i])):
            print(lines[i][j])
            if lines[i][j] == '0':
                continue
            else:
                newLink = link(lines[i][0], lines[0][j-1], 0.000001, lines[i][j])
                linkList.append(newLink)
    cities = lines[0]
    return linkList, cities

def antTour(links):
    newAnt = ant(120,0.0)
    




def main():
    file = "map1.txt"
    initLinks(file)

if __name__ == "__main__":
    main()