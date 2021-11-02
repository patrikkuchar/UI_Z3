import random

class Subject:
    def __init__(self, memory, player, treasures_array, sizeX, sizeY):
        self.memory = memory
        self.player = player
        self.treasures_array = treasures_array
        self.sizeX = sizeX
        self.sizeY = sizeY

        self.collectedT = 0
        self.moves = []

        self.VM()

        self.daco = 0

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

    def VM(self):
        PC = 0 #program counter

        for i in range(500):
            cell = self.memory[PC] #bunka v pamäti s ktorou budeme pracovať

            #rozdelím si bunku na inštrukciu (prvé 2 bity) a adresu bunky, ktorú budem upravovať
            instruction = cell >> 6
            target = self.getLastBits(cell, 6)

            ##inkrementácia
            if instruction == 0:
                self.memory[target] += 1
                if self.memory[target] == 256:
                    self.memory[target] = 0

            ##dekrementácia
            if instruction == 1:
                self.memory[target] -= 1
                if self.memory[target] == 0:
                    self.memory[target] = 255

            ##skok
            if instruction == 2:
                PC = target
            else:
                PC = (PC + 1) % 64

            ##vypis
            if instruction == 3:
                move = self.getLastBits(self.memory[target], 2)

                ##L - 0; R - 1; U - 2; D - 3

                self.moves.append(move)

                if move == 0:
                    if self.player[0] == 0:
                        break
                    self.player[0] -= 1

                elif move == 1:
                    if self.player[0] == self.sizeX - 1:
                        break
                    self.player[0] += 1

                elif move == 2:
                    if self.player[1] == 0:
                        break
                    self.player[1] -= 1

                else:
                    if self.player[1] == self.sizeY - 1:
                        break
                    self.player[1] += 1

                if self.checkTreasure():
                    break

        print("a")


memory = list(range(64))

for i in range(64):
    memory[i] = random.randrange(256)

player = [3,4]
treasures_array = [[4,1], [2,2], [6,3], [1,4], [4,5]]
sizeX = 7
sizeY = 7

subject = Subject(memory, player, treasures_array, sizeX, sizeY)



