import os
import os.path
import random
import math

global currentDir
currentDir = str(os.getcwd()+'/')
global randXLow, randXHigh, randYLow, randYHigh
randXLow = 4
randXHigh = 10
randYLow = 4
randYHigh = 10

def getCoords(tileList):
    allCoords = []
    for tile in tileList:
        allCoords.append((tile.x,tile.y))
    return allCoords

def getCenterCoords(tileList):
    lx = []
    ly = []
    for tile in tileList:
        lx.append(tile.x)
        ly.append(tile.y)
    centerCoords = (sum(lx)/len(lx), sum(ly)/len(ly))
    return centerCoords

def getDistance(tileList1, tileList2):
    distance = 0
    if type(tileList1) == list and type(tileList2) == list:
        centerX, centerY = getCenterCoords(tileList1)
        centerX2, centerY2 = getCenterCoords(tileList2)
        distance = math.sqrt((centerX-centerX2)**2+(centerY-centerY2)**2)
    if type(tileList1) == list and type(tileList2) != list:
        centerX, centerY = getCenterCoords(tileList1)
        centerX2, centerY2 = tileList2.x, tileList2.y
        distance = math.sqrt((centerX-centerX2)**2+(centerY-centerY2)**2)
    if type(tileList1) != list and type(tileList2) == list:
        centerX, centerY = tileList1.x, tileList1.y
        centerX2, centerY2 = getCenterCoords(tileList2)
        distance = math.sqrt((centerX-centerX2)**2+(centerY-centerY2)**2)
    if type(tileList1) != list and type(tileList2) != list:
        centerX, centerY = tileList1.x, tileList1.y
        centerX2, centerY2 = tileList2.x, tileList2.y
        distance = math.sqrt((centerX-centerX2)**2+(centerY-centerY2)**2)
    return distance

class tile:
    def __init__(self, x, y, ID):
        self.x = x
        self.y = y
        self.ID = ID
        self.attributes = []
        self.graphics = ''
        self.setGraphics()
    def setGraphics(self):
        if self.ID == 0:
            self.graphics = '#'
        elif self.ID == 1:
            self.graphics = ' '
        elif self.ID == -1:
            self.graphics = 'e'
        elif self.ID == 2:
            self.graphics = '*'
        elif self.ID == 3:
            self.graphics = '.'
    def setCustomGraphics(self, string):
        self.graphics = string
    def setNewID(self, ID):
        self.ID = ID
        self.attributes = []
        if self.ID == 0:
            self.addAttribute('wall')
            self.addAttribute('impassable')
        elif self.ID == 1:
            self.addAttribute('floor')
            self.addAttribute('walkable')
        elif self.ID == -1:
            self.addAttribute('debug')
        elif self.ID == 2:
            self.addAttribute('doorway')
            self.addAttribute('walkable')
        elif self.ID == 3:
            self.addAttribute('hallway')
            self.addAttribute('walkable')
        self.setGraphics()
    def addAttribute(self,newAttribute):
        self.attributes.append(newAttribute)

class room:
    def __init__(self, tileList, ID):
        self.ID = ID
        self.tileList = tileList
        self.size = len(tileList)
        self.borders = {'north':self.getBorder('north'),'west':self.getBorder('west'),'east':self.getBorder('east'),'south':self.getBorder('south')}
        self.width = len(self.borders['north'])
        self.height = len(self.borders['west'])
        self.coords = getCoords(self.tileList)
        self.attributes = []
        self.setRoomGraphics()
    def getBorder(self, side):
        border, lx, ly = [], [], []
        for tile in self.tileList:
            lx.append(tile.x)
            ly.append(tile.y)
        if side == 'north':
            for tile in self.tileList:
                if tile.y == min(ly):
                    border.append(tile)
        elif side == 'south':
            for tile in self.tileList:
                if tile.y == max(ly):
                    border.append(tile)
        elif side == 'west':
            for tile in self.tileList:
                if tile.x == min(lx):
                    border.append(tile)
        elif side == 'east':
            for tile in self.tileList:
                if tile.x == max(lx):
                    border.append(tile)
        return border
    def addAttribute(self,newAttribute):
        self.attributes.append(newAttribute)
    def setRoomGraphics(self):
        if len(str(self.ID)) > 1:
            self.tileList[0].setCustomGraphics(str(self.ID)[0])
            self.tileList[1].setCustomGraphics(str(self.ID)[1])
        else:
            self.tileList[0].setCustomGraphics(str(self.ID))
    
class level:
    def __init__(self, levelX, levelY, skipChance, nameString):
        self.levelX = levelX
        self.levelY = levelY
        self.skipChance = skipChance
        self.name = str(nameString)
        self.tileList = self.generateTileList(tile)
        self.roomList = []
        self.unconnectedRooms = []
        self.connectedRooms = []
        self.generateLevel(self.skipChance,25)
        self.numberOfRooms = len(self.roomList)
        self.numberOfTiles = levelX*levelY
    def generateTileList(self,tile):
        tileList = []
        for j in range(0,self.levelY):
            currentRow = []
            for i in range(0,self.levelX):
                currentRow.append(tile(i,j,1))
                currentRow[i].addAttribute('debug')
            tileList.append(currentRow)
        for j in range(0,self.levelY):
            if j == 0:
                for tile in tileList[j]:
                    tile.setNewID(0)
            elif j > 0 and j < (self.levelY-1):
                tileList[j][0].setNewID(0)
                tileList[j][self.levelX-1].setNewID(0)
            elif j == (self.levelY-1):
                for tile in tileList[j]:
                    tile.setNewID(0)
        return tileList
    def generateRoom(self,x,y,roomX,roomY,ID):
        print 'Adding Room:',ID
        roomTileList = []
        for j in range(y, y+roomY):
            for i in range(x, x+roomX):
                self.tileList[j][i].setNewID(1)
                self.tileList[j][i].addAttribute("room")
                roomTileList.append(self.tileList[j][i])
        for j in range(y-1, y+roomY):
            self.tileList[j][x-1].setNewID(0)
            self.tileList[j][x+roomX].setNewID(0)
        for i in range(x-1, x+roomX+1):
            self.tileList[y-1][i].setNewID(0)
            self.tileList[y+roomY][i].setNewID(0)
        newRoom = room(roomTileList,ID)
        self.roomList.append(newRoom)
        if ID >= 2:
            # Connect room to the previous ones
            # Check if it's already connected
            self.connectRoom(newRoom)
    def generateLevel(self, skipChance, maxRooms):
        # FILL THE EDGE
        for row in self.tileList:
            for tile in row:
                 if tile.ID == 1:
                    tile.setNewID(-1)
        for row in self.tileList:
            for tile in row:
                if tile.x == 0 or tile.x == self.levelX:
                    tile.setNewID(0)
                elif tile.y == 0 or tile.y == self.levelY:
                    tile.setNewID(0)
        self.roomList = []
        ID = 0
        roomX = random.randint(randXLow,randXHigh)
        roomY = random.randint(randYLow,randYHigh)
        # Generate the first room
        self.generateRoom(1,1, roomX, roomY, ID)
        # Generate all the other rooms
        for row in self.tileList:
            for tile in row:
                roomX = random.randint(randXLow,randXHigh)
                roomY = random.randint(randYLow,randYHigh)
                isRoom = 0
                yes = random.random()
                if yes > 1-skipChance:
                    continue              
                else:
                    if ID == maxRooms-1:
                        break
                    elif 'impassable' in tile.attributes:
                        continue
                    elif 'room' in tile.attributes:
                        continue
                    elif tile.y>1 and tile.y<self.levelY-roomY-1 and tile.x >1 and tile.x<self.levelX-roomX-1:
                        for j in range(tile.y, tile.y+roomY):
                            for i in range(tile.x, tile.x+roomX):
                                if 'debug' in self.tileList[j][i].attributes:
                                    isRoom += 1
                if isRoom == roomX*roomY:
                    ID += 1
                    self.generateRoom(tile.x,tile.y,roomX,roomY,ID)
        self.connectRoom(self.roomList[0])
        print ID+1,'/',maxRooms, 'rooms generated on a',self.levelX,'*',self.levelY,'map'
        for room in self.unconnectedRooms:
            print '##############################'
            print room.ID, 'is unconnected.'
            if self.bruteConnectRoom(room) == 0:
                print 'Could not fix.'
            else:
                print 'Connected.'
            print '##############################'
        self.cleanup()
        
    def generateRoomConnectionList(self):
        roomConnectionList = []
        for room in self.roomList:
            comparisonMinima = {}
            otherRooms = []
            for room_ in self.roomList:
                if room_.ID != room.ID:
                    otherRooms.append(room_.ID)
            distances = []
            for room_ in self.roomList:
                if room.ID < max(otherRooms):
                    if (room_ != room and "connected" not in room_.attributes):
                        distances.append(getDistance(room.tileList, room_.tileList))
                    elif room_ != room and "connected" in room_.attributes:
                        distances.append(2000)
                elif room.ID > max(otherRooms) and room_ != room:
                    distances.append(getDistance(room.tileList, room_.tileList))
            closestID = otherRooms[distances.index(min(distances))]
            # Check which sides are closest between the two rooms
            comparison = {'north':{},'west':{},'east':{},'south':{}}
            comparisonSideMinima = {'north':(),'west':(),'east':(),'south':()}
            room2 = self.roomList[closestID]
            for side in room.borders:
                for side2 in room2.borders:
                    comparison[side][side2] = getDistance(room.borders[side], room2.borders[side2])
            for side in comparison:
                for side_ in comparison[side]:
                    if comparison[side][side_] == min(comparison[side].values()):
                        comparisonSideMinima[side] = {side_:comparison[side][side_]}
            ds = {}
            for side in comparisonSideMinima:
                ds[side]=comparisonSideMinima[side].values()[0]
            for side in ds:
                if ds[side] == min(list(ds.values())):
                    sideToConnect = side
            closestSide = comparisonSideMinima[sideToConnect].keys()[0]
            roomConnectionList.append([room.ID, sideToConnect, closestID, closestSide])
        return roomConnectionList
    def getTileID(self,x,y):
        for row in self.tileList:
            for tile in row:
                if tile.x == x and tile.y == y:
                    return tile.ID
    def bruteConnectRoom(self, room):
        # Random start tile
        randomizedList = []
        i = 0
        for side in room.borders:
            for tile in room.borders[side]:
                randomizedList.append([tile,side])
        random.shuffle(randomizedList)
        maxLength = max([self.levelX,self.levelY])
        # Elongate for max length
        connected = 0
        for item in randomizedList:
            i += 1
            tile = item[0]
            side = item[1]
            x = tile.x
            y = tile.y
            hallwayTileList = []
            success = 0
            length = 0
            if connected != 0:
                room.addAttribute("connected")
                break
            hallwayTileList.append(tile) #landing
            tries = 0
            while side == 'north' and y > 1 and connected == 0:
                y -= 1
                hallwayTileList.append(self.tileList[y][x])
                print tries  
                if 'room' in self.tileList[y][x].attributes:
                    print 'Connected to a room!'
                    connected = 1
                    break
                elif 'room' not in self.tileList[y][x].attributes and self.tileList[y][x].ID == 1:
                    print 'Connected to a hallway!'
                    connected = 2
                tries +=1
            while side == 'west' and x > 1:
                x -= 1
                hallwayTileList.append(self.tileList[y][x])
                print tries  
                if 'room' in self.tileList[y][x].attributes:
                    print 'Connected to a room!'
                    connected = 1
                    break
                elif 'room' not in self.tileList[y][x].attributes and self.tileList[y][x].ID == 1:
                    print 'Connected to a hallway!'
                    connected = 2
                tries +=1
            while side == 'east' and x < self.levelX-1:
                x += 1
                hallwayTileList.append(self.tileList[y][x])
                print tries  
                if 'room' in self.tileList[y][x].attributes:
                    print 'Connected to a room!'
                    connected = 1
                    break
                elif 'room' not in self.tileList[y][x].attributes and self.tileList[y][x].ID == 1:
                    print 'Connected to a hallway!'
                    connected = 2
                tries +=1
            while side == 'south' and y < self.levelY-1:
                y += 1
                hallwayTileList.append(self.tileList[y][x])
                print tries  
                if 'room' in self.tileList[y][x].attributes:
                    print 'Connected to a room!'
                    connected = 1
                    break
                elif 'room' not in self.tileList[y][x].attributes and self.tileList[y][x].ID == 1:
                    print 'Connected to a hallway!'
                    connected = 2
                tries +=1
            if connected == 1 and hallwayTileList != []:
                for i in range(1, len(hallwayTileList)-1):
                    hallwayTileList[i].setNewID(3)
                hallwayTileList[1].setNewID(2)
                hallwayTileList[-2].setNewID(2)
                return 1
            elif connected == 2 and hallwayTileList != []:
                for i in range(1, len(hallwayTileList)):
                    hallwayTileList[i].setNewID(3)
                hallwayTileList[1].setNewID(2)
                hallwayTileList[-1].setNewID(3)
                return 1
        print 'Could not connect room.'
        return 0
    def connectRoom(self, roomToConnect):
        roomConnectionList = self.generateRoomConnectionList()
        # Do connection between room1 and room2 stored in a roomConnectionList item
        room1, border1, side1, room2, border2, side2 = 0, 0, 0, 0, 0, 0
        print roomConnectionList
        for item in roomConnectionList:
            if self.roomList[item[0]] == roomToConnect: 
                print item
                room1 = self.roomList[item[0]]
                border1 = self.roomList[item[0]].borders[item[1]]
                side1 = item[1]
                room2 = self.roomList[item[2]]
                border2 = self.roomList[item[2]].borders[item[3]]
                side2 = item[3]
                print room1.ID, side1
        i = 0
        connected = 0
        while i in range(0,len(border1)-1) and connected == 0:
            for startTile in border1:
                if connected != 0:
                    roomToConnect.addAttribute("connected")
                    break
                hallwayTileList = []
                print 'tile:', i
                i+=1
                print startTile.ID
                x = startTile.x
                y = startTile.y
                hallwayTileList.append(startTile) #landing
                previousDistance = getDistance(self.tileList[y][x], border2)
                triesMax = max([self.levelX,self.levelY])
                tries = 0
                while side1 == 'north' and tries < triesMax:
                    y -= 1
                    print tries, '/', triesMax
                    currentDistance = getDistance(self.tileList[y][x], border2)                  
                    if self.tileList[y][x] in border2:
                        print 'Connected!'
                        connected = 1
                        break
                    elif self.tileList[y][x].ID == 1 and self.tileList[y][x] not in border2:
                        if 'room' in self.tileList[y][x].attributes:
                            connected = 2
                        else:
                            connected = 3
                        break
                    elif currentDistance <= previousDistance:
                        hallwayTileList.append(self.tileList[y][x]) #doorway at first, then hallway
                        previousDistance = currentDistance
                        currentDistance = getDistance(self.tileList[y][x], border2)
                    else:
                        hallwayTileList = []
                        break
                    tries +=1
                while side1 == 'west' and tries < triesMax:
                    x -= 1
                    print tries, '/', triesMax
                    currentDistance = getDistance(self.tileList[y][x], border2)                  
                    if self.tileList[y][x] in border2:
                        print 'Connected!'
                        connected = 1
                        break
                    elif self.tileList[y][x].ID == 1 and self.tileList[y][x] not in border2:
                        if 'room' in self.tileList[y][x].attributes:
                            connected = 2
                        else:
                            connected = 3
                        break
                    elif currentDistance <= previousDistance:
                        hallwayTileList.append(self.tileList[y][x]) #doorway at first, then hallway
                        previousDistance = currentDistance
                        currentDistance = getDistance(self.tileList[y][x], border2)
                    else:
                        hallwayTileList = []
                        break
                    tries +=1
                while side1 == 'east' and tries < triesMax:
                    x += 1
                    print tries, '/', triesMax
                    print tries
                    currentDistance = getDistance(self.tileList[y][x], border2)                  
                    if self.tileList[y][x] in border2:
                        print 'Connected!'
                        connected = 1
                        break
                    elif self.tileList[y][x].ID == 1 and self.tileList[y][x] not in border2:
                        if 'room' in self.tileList[y][x].attributes:
                            connected = 2
                        else:
                            connected = 3
                        break
                    elif currentDistance <= previousDistance:
                        hallwayTileList.append(self.tileList[y][x]) #doorway at first, then hallway
                        previousDistance = currentDistance
                        currentDistance = getDistance(self.tileList[y][x], border2)
                    else:
                        hallwayTileList = []
                        break
                    tries +=1
                while side1 == 'south' and tries < triesMax:
                    y += 1
                    print tries, '/', triesMax
                    currentDistance = getDistance(self.tileList[y][x], border2)                  
                    if self.tileList[y][x] in border2:
                        print 'Connected!'
                        connected = 1
                        break
                    elif self.tileList[y][x].ID == 1 and self.tileList[y][x] not in border2:
                        if 'room' in self.tileList[y][x].attributes:
                            connected = 2
                        else:
                            connected = 3
                        break
                    elif currentDistance <= previousDistance:
                        hallwayTileList.append(self.tileList[y][x]) #doorway at first, then hallway
                        previousDistance = currentDistance
                        currentDistance = getDistance(self.tileList[y][x], border2)
                    else:
                        hallwayTileList = []
                        break
                    tries +=1
            if connected == 1 and hallwayTileList != []:
                print 'Hit appropriate room.'
                for i in range(1, len(hallwayTileList)):
                    hallwayTileList[i].setNewID(3)
                hallwayTileList[1].setNewID(2)
                hallwayTileList[-1].setNewID(2)
            elif connected == 2 and hallwayTileList != []:
                print 'Hit hallway!'
                for i in range(1, len(hallwayTileList)):
                    hallwayTileList[i].setNewID(3)
                hallwayTileList[1].setNewID(2)
                hallwayTileList[-1].setNewID(3)
            elif connected == 3 and hallwayTileList != []:
                print 'Hit another room!'
                for i in range(1, len(hallwayTileList)):
                    hallwayTileList[i].setNewID(3)
                hallwayTileList[1].setNewID(2)
                hallwayTileList[-1].setNewID(2)
            else:
                print 'Could not connect room.'
                self.unconnectedRooms.append(roomToConnect)
    def getTile(self,x,y):
        for row in self.tileList:
            for tile in row:
                if tile.x == x and tile.y == y:
                    return tile
    def cleanup(self):
        debugToWall = []
        for row in self.tileList:
            for tile in row:
                if self.getTileID(tile.x, tile.y) == 3:
                    x = tile.x
                    y = tile.y
                    debugToWall.append(self.getTile(x+1,y))
                    debugToWall.append(self.getTile(x+1,y-1))
                    debugToWall.append(self.getTile(x+1,y+1))
                    debugToWall.append(self.getTile(x,y+1))
                    debugToWall.append(self.getTile(x,y-1))
                    debugToWall.append(self.getTile(x-1,y))
                    debugToWall.append(self.getTile(x-1,y-1))
                    debugToWall.append(self.getTile(x-1,y+1))
        for tile in debugToWall:
            if tile.ID == -1:
                tile.setNewID(0)
        for row in self.tileList:
            for tile in row:
                if self.getTileID(tile.x, tile.y) == -1:
                    self.tileList[tile.y][tile.x].setNewID(0)
                    """
                elif self.getTileID(tile.x,tile.y) == 2:
                    neighbours = []
                    neighbours.append(self.getTile(tile.x+1,tile.y))
                    neighbours.append(self.getTile(x+1,y))
                    neighbours.append(self.getTile(x,y+1))
                    neighbours.append(self.getTile(x,y-1))
                    neighbours.append(self.getTile(x-1,y))
                    empty = 0
                    for tile in neighbours:
                        if tile.ID == 1 or tile.ID == 2:
                            empty += 1
                        if tile.ID == 3:
                            tile.setNewID(2)
                    if empty > 2:
                        self.getTile(tile.x,tile.y).setNewID(2)
                    """
                    
    def display(self):
        # DISPLAY
        f = open(currentDir+'map.txt', 'w')
        for row in self.tileList:
            currentRow = []
            for tile in row:
                currentRow.append(tile.graphics)
            f.write(' '.join(currentRow)+'\n')
        #f.write(str(self.roomConnections))
        f.close()

a = level(54, 54, 0.95, 'level')
a.display()
