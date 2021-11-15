import random
import copy
import time
import tkinter

import numpy as np
from matplotlib import pyplot as plt

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

    def getMoves(self):
        return self.moves

    def checkSuccess(self):
        if len(self.treasures_array) == 0:
            return True
        return False

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
        treasures_f = self.collectedT / ((self.collectedT + len(self.treasures_array)) * 1)
        calculatedFitness = int(move_f * treasures_f * 10000) #4 miesta za desatinou čiarkou
        if calculatedFitness == 0:
            return int(move_f * 1000)
        return calculatedFitness

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
        global mutationType

        if not test:
            mutationType = random.randrange(4)

        ##komplement nejakých bitov
        if mutationType == 0:
            for i in range(64):
                oldBin = bin(self.memory[i])
                if len(oldBin) != 10:
                    oldBin = oldBin[:2] + "0" * (10 - len(oldBin)) + oldBin[2:]

                newBin = "0b"
                for c in oldBin[2:]:
                    if random.randrange(mutation_prob1) == 0:
                        newBin += str((int(c) + 1) % 2)
                    else:
                        newBin += c

                self.memory[i] = int(newBin, 2)

        ##komplement nejakých buniek
        elif mutationType == 1:
            for i in range(64):
                if random.randrange(mutation_prob2) == 0:
                    oldBin = bin(self.memory[i])
                    if len(oldBin) != 10:
                        oldBin = oldBin[:2] + "0" * (10 - len(oldBin)) + oldBin[2:]

                    newBin = "0b"
                    for c in oldBin[2:]:
                        newBin += str((int(c) + 1) % 2)

                    self.memory[i] = int(newBin, 2)

        ##výmena nejakých buniek
        elif mutationType == 2:
            for i in range(64):
                if random.randrange(mutation_prob3) == 0:
                    index2 = random.randrange(64)

                    cell = self.memory[i]

                    self.memory[i] = self.memory[index2]
                    self.memory[index2] = cell

        ##náhodný obsah v nejakých bunkách
        else:
            for i in range(64):
                if random.randrange(mutation_prob4) == 0:
                    self.memory[i] = random.randrange(256)





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

def drawSolution(subject):
    Window = tkinter.Tk()
    Window.geometry(f'{500}x{500}')
    canvas = tkinter.Canvas(Window, width="500", height="500")
    canvas.pack()


    moves = subject.getMoves()


    if sizeX > sizeY:
        size = 400 // sizeX
    else:
        size = 400 // sizeY

    count = -1

    foundT = []

    y = 50
    for i in range(sizeY):
        x = 50
        for j in range(sizeX):
            count += 1

            canvas.create_rectangle(x, y, x + size, y + size)
            if [j, i] in treasures:
                canvas.create_oval(x + 5, y + 5, x + size - 5, y + size - 5, fill="yellow")


            x += size
        y += size

    for i in range(len(treasures)):
        foundT.append(canvas.create_rectangle(0, 0, 0, 0, fill="lightyellow"))

    c_treasures = copy.copy(treasures)

    x = player[0]
    y = player[1]

    pX =  50 + player[0] * size + size//2
    pY =  50 + player[1] * size + size//2
    movingPlayer = canvas.create_oval(pX - size//4, pY - size//4, pX + size//4, pY + size//4, fill="blue")


    canvas.move(movingPlayer, 0, 0)
    Window.update()
    time.sleep(3)

    while len(moves) != 0:
        move = moves.pop(0)
        ##L-0;R-1;U-2,D-3

        if move == 0:
            moveX = -size
            moveY = 0
            x -= 1
        elif move == 1:
            moveX = size
            moveY = 0
            x += 1
        elif move == 2:
            moveX = 0
            moveY = -size
            y -= 1
        else:
            moveX = 0
            moveY = size
            y += 1

        if [x, y] in c_treasures:
            canvas.coords(foundT.pop(0), (pX + moveX) - size/2, (pY + moveY) - size/2, (pX + moveX) + size/2, (pY + moveY) + size/2)
            c_treasures.remove([x, y])


        canvas.create_line(pX, pY, pX + moveX/2, pY + moveY/2, fill="red", width=3)
        canvas.move(movingPlayer, moveX/2, moveY/2)
        Window.update()
        time.sleep(0.1)
        canvas.create_line(pX, pY, pX + moveX, pY + moveY, fill="red", width=3)
        canvas.move(movingPlayer, moveX/2, moveY/2)
        Window.update()
        time.sleep(0.1)

        pX += moveX
        pY += moveY

    #canvas.move(drownPlayer, pX - size, pY)
    #canvas.move(drownPlayer, -10, -10)

    #time.sleep(4)


    tkinter.mainloop()


def memoryGenerator(n):
    memory = list(range(64))

    for i in range(64):
        if i < n:
            memory[i] = random.randrange(256)
        else:
            memory[i] = 0

    return memory

def findBiggestFitness(generation):
    biggest_index = 0
    biggest_fitness = 0

    count = 0

    for subject in generation:
        if subject.getFitness() > biggest_fitness:
            biggest_index = count
            biggest_fitness = subject.getFitness()
        count += 1

    return biggest_index

def selectPair(generation):
    ##ruleta
    if selectionType == 0:
        sumFitness = 0
        ##spočítam si fitness celej generácie
        for subject in generation:
            sumFitness += subject.getFitness()

        selectedSubjects = [None, None]

        for i in range(2):
            while True: #do while
                index = -1
                randomN = random.randrange(sumFitness)

                while randomN >= 0:
                    index = (index + 1) % len(generation)

                    subject_fitness = generation[index].getFitness()
                    randomN -= subject_fitness

                if generation[index] not in selectedSubjects:
                    selectedSubjects[i] = generation[index]
                    break

        return selectedSubjects

    ##turnaj
    if selectionType == 1:

        selectedSubjects = [None, None]
        #selectedSubjects = []

        generation_len = len(generation)

        for i in range(2):



            r_generation = []


            for j in range(3):
                subject = generation[random.randrange(generation_len)]
                while subject in r_generation or subject == selectedSubjects[0]:
                    subject = generation[random.randrange(generation_len)]
                r_generation.append(subject)


            biggest_index = findBiggestFitness(r_generation)
            biggest_index = findBiggestFitness(r_generation)

            selectedSubjects[i] = r_generation[biggest_index]



        return selectedSubjects



def writeInfo(generation, num):
    global Best_fitness

    if writeProgress:
        print("\n\n-----------------------\n" + str(num) + ". generácia\n")

    count = 0
    for subject in generation:
        count += 1
        if subject.checkSuccess() and subject.getFitness() > Best_fitness and not test:
            print("\n\t\t" + str(count) + ". jedinec z " + str(num) + ". generácie našiel všetky (" + str(len(treasures)) + ") poklady na " + str(subject.getNumOfMoves()) + " krokov.\n\n")
            n = input("Ak si prajete pokračovať v hľadaní lepšieho jedinca (menej krokov) stlačte 'y': ")
            if n == "y":
                Best_fitness = subject.getFitness()
            else:
                drawSolution(subject)
                exit()
        elif writeProgress:
            print(str(count) + ". jedinec:  \tPočet krokov: " + str(subject.getNumOfMoves()) + "  \tPočet nájdených pokladov: " + str(subject.getNumOfCollectedT()) + "\t\tFitness: " + str(subject.getFitness()))


def run(player, treasures, sizeX, sizeY, numOfSubjects, numOfGenerations):
    oldGeneration = []


    for i in range(numOfSubjects):
        oldGeneration.append(Subject(memoryGenerator(64), player, treasures, sizeX, sizeY))

    writeInfo(oldGeneration, 0)

    #pre testovanie
    if test:
        dataFromTesting[-1].append([oldGeneration[findBiggestFitness(oldGeneration)].getFitness()])

    i = 0
    ##vykonanie reprodukcie
    while i < numOfGenerations:


        newGeneration = []

        ## --- kríženie ---
        for y in range((numOfSubjects - eliteNum) // 2):
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

        ## --- elitarizmus ---
        for y in range(eliteNum):
            ## najdeme najväčší prvok, vyberieme ho zo starej generácie a vložíme do novej
            biggest_index = findBiggestFitness(oldGeneration)
            newGeneration.append(oldGeneration.pop(biggest_index))

        oldGeneration = newGeneration

        writeInfo(oldGeneration, i + 1)

        # pre testovanie
        if test:
            dataFromTesting[-1][-1].append(oldGeneration[findBiggestFitness(oldGeneration)].getFitness())


        if i == numOfGenerations-1 and not test:
            best_subject = oldGeneration[findBiggestFitness(oldGeneration)]

            print("\n" + str(numOfGenerations+1) + " generácií vytvorených.\nNajviac bolo nájdených " + str(best_subject.getNumOfCollectedT()) + " z " + str(len(treasures)) + " pokladov na " + str(best_subject.getNumOfMoves()) + " krokov.")
            n = input("Ak si prajete vytvárať ďalšie generácie, zadajte ich počet (ak nie - 0): ")
            if n != "0":
                numOfGenerations += int(n)
            else:
                drawSolution(best_subject)

        i += 1

def drawGraph(A_fitness_array, S_type, E_num):
    y = []
    for fitness_array in A_fitness_array:
        num = len(fitness_array)
        fitness = []

        for i in range(len(fitness_array[0])):
            sum = 0
            for j in range(num):
                sum += fitness_array[j][i]
            fitness.append(sum / num)

        y.append(fitness)

    x = np.arange(numOfGenerations + 1)
    y1 = np.array(y[0])
    y2 = np.array(y[1])
    y3 = np.array(y[2])
    y4 = np.array(y[3])

    plt.title("Selekcia: " + S_type + "; Elitarizmus: " + E_num + "%")
    plt.xlabel("Generacie")
    plt.ylabel("Fitness")
    plt.plot(x, y1, label="Komplement bitov")
    plt.plot(x, y2, label="Komplement buniek")
    plt.plot(x, y3, label="Výmena buniek")
    plt.plot(x, y4, label="Náhodné bunky")
    plt.legend(loc="lower right", title="Druh mutácie")
    plt.show()

def testing():
    global mutationType, dataFromTesting, writeProgress, selectionType, eliteNum

    numOfTests = 20

    writeProgress = False

    #Ruleta, mutacia1 - mutacia4, Elit - 0%
    dataFromTesting = [[]]
    selectionType = 0
    mutationType = 0
    eliteNum = 0
    for k in range(4):
        for i in range(numOfTests):
            run(player,treasures,sizeX,sizeY,numOfSubjects,numOfGenerations)
        mutationType += 1
        dataFromTesting.append([])
    drawGraph(dataFromTesting[:4], "Ruleta", "0")

    # Turnaj, mutacia1 - mutacia4, Elit - 0%
    dataFromTesting = [[]]
    selectionType = 1
    mutationType = 0
    for k in range(4):
        for i in range(numOfTests):
            run(player,treasures,sizeX,sizeY,numOfSubjects,numOfGenerations)
        mutationType += 1
        dataFromTesting.append([])
    drawGraph(dataFromTesting[:4], "Turnaj", "0")


    # Ruleta, mutacia1 - mutacia4, Elit - 20%
    dataFromTesting = [[]]
    selectionType = 0
    mutationType = 0
    eliteNum = int(numOfSubjects * 0.2)
    for k in range(4):
        for i in range(numOfTests):
            run(player,treasures,sizeX,sizeY,numOfSubjects,numOfGenerations)
        mutationType += 1
        dataFromTesting.append([])
    drawGraph(dataFromTesting[:4], "Ruleta", "20")

    # Turnaj, mutacia1 - mutacia4, Elit - 20%
    dataFromTesting = [[]]
    selectionType = 1
    mutationType = 0
    for k in range(4):
        for i in range(numOfTests):
            run(player,treasures,sizeX,sizeY,numOfSubjects,numOfGenerations)
        mutationType += 1
        dataFromTesting.append([])
    drawGraph(dataFromTesting[:4], "Turnaj", "20")


    # Ruleta, mutacia1 - mutacia4, Elit - 50%
    dataFromTesting = [[]]
    selectionType = 0
    mutationType = 0
    eliteNum = numOfSubjects // 2
    for k in range(4):
        for i in range(numOfTests):
            run(player,treasures,sizeX,sizeY,numOfSubjects,numOfGenerations)
        mutationType += 1
        dataFromTesting.append([])
    drawGraph(dataFromTesting[:4], "Ruleta", "50")

    # Turnaj, mutacia1 - mutacia4, Elit - 50%
    dataFromTesting = [[]]
    selectionType = 1
    mutationType = 0
    for k in range(4):
        for i in range(numOfTests):
            run(player,treasures,sizeX,sizeY,numOfSubjects,numOfGenerations)
        mutationType += 1
        dataFromTesting.append([])
    drawGraph(dataFromTesting[:4], "Turnaj", "50")





    print("Testovanie dokončené.")


def read_input():
    ##načítanie vstupných hodnôt z input.csv
    f = open("input.txt", "r")

    alldata = []

    randomData = 0

    for i in range(14):
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




#pre testovanie
mutationType = 0
dataFromTesting = []

SUCCESS = False
Best_fitness = 0

input_data = read_input()

player = [input_data[0], input_data[1]]
sizeX = input_data[2]
sizeY = input_data[3]
treasures = input_data[4]
numOfSubjects = int(input_data[5])
selectionType = int(input_data[6])
mutation_prob1 = int(input_data[7])
mutation_prob2 = int(input_data[8])
mutation_prob3 = int(input_data[9])
mutation_prob4 = int(input_data[10])
numOfGenerations = int(input_data[11])
eliteNum = int(int(input_data[12]) / 100 * int(input_data[5]))


writeProgress = input_data[13] == "1"
test = input_data[14] == "1"





#x = np.arange(1,11)
#y = 2 * x + 5
#y2 = x + 2
#plt.title("Matplotlib demo")
#plt.xlabel("x axis caption")
#plt.ylabel("y axis caption")
#plt.plot(x,y, y2)
#plt.show()




if test:
    testing()
else:
    run(player, treasures, sizeX, sizeY, numOfSubjects, numOfGenerations)



