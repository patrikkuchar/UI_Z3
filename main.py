import random
import copy

class Subject:
    def __init__(self, memory, player, treasures_array, sizeX, sizeY):
        self.memory = memory
        self.player = copy.copy(player)
        self.treasures_array = copy.copy(treasures_array)
        self.sizeX = sizeX
        self.sizeY = sizeY

        self.collectedT = 0
        self.moves = []

        self.VM(copy.copy(memory))

        self.fitness = self.calculateFitness()

    def getNumOfMoves(self):
        return len(self.moves)

    def getNumOfCollectedT(self):
        return self.collectedT

    def getFitness(self):
        return self.fitness

    def getLeftSide(self, n):
        return self.memory[:n]

    def getRightSide(self, n):
        return self.memory[n:]

    def calculateFitness(self):
        move_f = 1 - len(self.moves)/1000
        treasures_f = self.collectedT / (self.collectedT + len(self.treasures_array))
        return move_f * treasures_f

    def getLastBits(self, bitNumber, num):
        mask = (1 << num) - 1
        return bitNumber & mask

    def checkTreasure(self):
        if self.player in self.treasures_array:
            self.collectedT += 1
            self.treasures_array.remove(self.player)
            if len(self.treasures_array) == 0:
                return True
        return False

    def mutate(self):

        ##komplement jedného bytu v jednej bunke
        ##pravdepodobnosť 1:20
        if random.randrange(mutation_prob1) == 0:
            index = random.randrange(64)

            oldBin = bin(self.memory[index])
            if len(oldBin) != 10:
                oldBin = oldBin[:2] + "0" * (10 - len(oldBin)) + oldBin[2:]
            r = random.randrange(len(oldBin) - 2)
            newBin = oldBin[:r+2] + str((int(oldBin[r+2]) + 1) % 2) + oldBin[r+3:]

            self.memory[index] = int(newBin, 2)


        ##komplement jednej celej bunky
        ##pravdepodobnosť 1:100
        if random.randrange(mutation_prob2) == 0:
            index = random.randrange(64)

            oldBin = bin(self.memory[index])
            if len(oldBin) != 10:
                oldBin = oldBin[:2] + "0" * (10 - len(oldBin)) + oldBin[2:]
            newBin = '0b'

            for c in oldBin[2:]:
                newBin += str((int(c) + 1) % 2)

            self.memory[index] = int(newBin, 2)


        ##výmena dvoch susediacich buniek
        ##pravdepodobnosť 1:120
        if random.randrange(mutation_prob3) == 0:
            index1 = random.randrange(64)
            index2 = random.randrange(64)

            cell = self.memory[index1]

            self.memory[index1] = self.memory[index2]
            self.memory[index2] = cell


        ##jedna bunka sa vymení za novú - náhodnú
        ##pravdepodobnosť 1:200
        if random.randrange(mutation_prob4) == 0:
            self.memory[random.randrange(64)] = random.randrange(256)


    def VM(self, memory):
        PC = 0 #program counter

        for i in range(500):
            cell = memory[PC] #bunka v pamäti s ktorou budeme pracovať

            #rozdelím si bunku na inštrukciu (prvé 2 bity) a adresu bunky, ktorú budem upravovať
            instruction = cell >> 6
            target = self.getLastBits(cell, 6)

            ##inkrementácia
            if instruction == 0:
                memory[target] += 1
                if memory[target] == 256:
                    memory[target] = 0

            ##dekrementácia
            if instruction == 1:
                memory[target] -= 1
                if memory[target] == -1:
                    memory[target] = 255

            ##skok
            if instruction == 2:
                PC = target
            else:
                PC = (PC + 1) % 64

            ##vypis
            if instruction == 3:
                move = self.getLastBits(memory[target], 2)

                ##L - 0; R - 1; U - 2; D - 3

                self.moves.append(move)

                ##vlavo
                if move == 0:
                    if self.player[0] == 0:
                        break
                    self.player[0] -= 1

                ##vpravo
                elif move == 1:
                    if self.player[0] == self.sizeX - 1:
                        break
                    self.player[0] += 1

                ##hore
                elif move == 2:
                    if self.player[1] == 0:
                        break
                    self.player[1] -= 1

                ##dole
                else:
                    if self.player[1] == self.sizeY - 1:
                        break
                    self.player[1] += 1

                if self.checkTreasure():
                    break


def memoryGenerator(n):
    memory = list(range(64))

    for i in range(64):
        if i < n:
            memory[i] = random.randrange(256)
        else:
            memory[i] = 0

    return memory

def selectPair(generation):
    ##ruleta
    if selectionType == 0:
        sumFitness = 0
        ##spočítam si fitness celej generácie
        for subject in generation:
            sumFitness += int(subject.getFitness() * 1000)

        ##vyberiem 2 náhodné čísla v rozmedzí od 0 do súčtu celej generácie
        randomN1 = random.randrange(sumFitness)
        randomN2 = random.randrange(sumFitness)

        subject1 = None
        subject2 = None
        index = -1

        ##cyklus prechádza generáciu a odpočitáva fitness od vygenerovaných čísel až kým dane čísla nesú menšie ako 0 -> vyžrebovaný jedinec
        while subject1 == None or subject2 == None:

            index = (index + 1) % len(generation)

            subject_fitness = int(generation[index].getFitness() * 1000)
            if subject_fitness == 0:
                continue

            randomN1 -= subject_fitness
            randomN2 -= subject_fitness

            if randomN1 < 0 and subject1 == None:
                subject1 = generation[index]

                ##či sa nevyžrebovali rovnaké chromozómy
                if randomN2 < 0 and subject2 == None:
                    randomN2 += subject_fitness

            elif randomN2 < 0 and subject2 == None:
                subject2 = generation[index]


        return [subject1, subject2]

    ##turnaj
    if selectionType == 1:
        subject1 = None
        subject2 = None

        for i in range(2):
            biggest_index = 0
            biggest_index_p = 0
            biggest_fitness = 0

            for j in range(3):
                r_index = random.randrange(len(generation))

                if generation[r_index].getFitness() >= biggest_fitness:
                    biggest_index_p = biggest_index
                    biggest_fitness = generation[r_index].getFitness()
                    biggest_index = r_index

            if subject1 == None:
                subject1 = generation[biggest_index]
            elif generation[biggest_index] == subject1:
                subject2 = generation[biggest_index_p]
            else:
                subject2 = generation[biggest_index]

        return [subject1, subject2]



def writeInfo(generation, num):
    print("\n\n-----------------------\n" + str(num) + ". generácia\n")

    count = 0
    for subject in generation:
        count += 1
        print(str(count) + ". jedinec:  \tPočet krokov: " + str(subject.getNumOfMoves()) + "  \tPočet nájdených pokladov: " + str(subject.getNumOfCollectedT()))


def init(player, treasures, sizeX, sizeY, numOfSubjects, numOfGenerations):
    oldGeneration = []

    for i in range(numOfSubjects):
        oldGeneration.append(Subject(memoryGenerator(64), player, treasures, sizeX, sizeY))

    writeInfo(oldGeneration, 0)


    ##vykonanie reprodukcie
    for i in range(numOfGenerations):

        newGeneration = []

        ## --- kríženie ---
        for y in range(numOfSubjects // 2):
            pair = selectPair(oldGeneration)

            r = random.randrange(64)

            firstSubject = Subject(pair[0].getLeftSide(r) + pair[1].getRightSide(r), player, treasures, sizeX, sizeY)
            secondSubject = Subject(pair[1].getLeftSide(r) + pair[0].getRightSide(r), player, treasures, sizeX, sizeY)

            ## --- mutácia ---
            firstSubject.mutate()
            secondSubject.mutate()

            ##pridanie jedincov do novej generácie
            newGeneration.append(firstSubject)
            newGeneration.append(secondSubject)

        oldGeneration = newGeneration

        writeInfo(oldGeneration, i + 1)

    print("hej")

def read_input():
    ##načítanie vstupných hodnôt z input.csv
    f = open("input.txt", "r")

    alldata = []

    randomData = 0

    for i in range(11):
        line = f.readline()

        if line == '':
            print("Chyba v stupnom súbore.")
            exit()

        data = line.split(';')
        data.pop()

        if i == 0 or i == 1:
            data_a = data[1].split(',')
            alldata.append(int(data_a[0]))
            alldata.append(int(data_a[1]))
        elif i == 2:
            randomData = int(data[1])
        elif i == 3:
            treasures_array = []#poklady
            if randomData != 0:
                for j in range(randomData):
                    treasure = [random.randrange(alldata[2]), random.randrange(alldata[3])]
                    while treasure in treasures_array:
                        treasure = [random.randrange(alldata[2]), random.randrange(alldata[3])]
                    treasures_array.append(treasure)
            else:
                for oneData in data[1:]:
                    positions = oneData.split(',')
                    treasures_array.append([int(positions[0]), int(positions[1])])
            alldata.append(treasures_array)


        else:
            alldata.append(data[1])

    return alldata








input_data = read_input()

player = [input_data[0], input_data[1]]
sizeX = input_data[2]
sizeY = input_data[3]
treasures = input_data[4]

selectionType = int(input_data[6])
mutation_prob1 = int(input_data[7])
mutation_prob2 = int(input_data[8])
mutation_prob3 = int(input_data[9])
mutation_prob4 = int(input_data[10])

#player = [3,4]
#treasures = [[4,1], [2,2], [6,3], [1,4], [4,5]]
#sizeX = 7
#sizeY = 7

init(player, treasures, sizeX, sizeY, int(input_data[5]), int(input_data[11]))



