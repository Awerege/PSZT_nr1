#####################################################
#                   ALGORYTM GENETYCZNY             #
#####################################################

import random
import sys
import operator

from datetime import datetime


class Knapsack(object):

    # inicjalizajca zmiennych i list
    def __init__(self):

        self.C = 0
        self.volumes = []
        self.value = []
        self.opt = []
        self.parents = []
        self.newparents = []
        self.bests = []
        self.best_score_progress = []
        self.best_p = []
        self.iterated = 1
        self.population = 0

        # maksymalna ilość wykonań
        iMaxStackSize = 15000
        sys.setrecursionlimit(iMaxStackSize)

    # stworz pierwsza populacje
    def initialize(self):

        for i in range(self.population):
            parent = []
            for k in range(0, 5):
                k = random.randint(0, 1)
                parent.append(k)
            self.parents.append(parent)

    # podaj detale tego problemu
    def properties(self, weights, profits, opt, C, population):

        self.volumes = weights
        self.value = profits
        self.opt = opt
        self.C = C
        self.population = population
        self.initialize()

    # wyliczyć funkcję przystosowania każdej listy
    def fitness(self, item):

        sum_ob = 0
        sum_w = 0

        # obliczyć całkowitą objętość oraz 
        for index, i in enumerate(item):
            if i == 0:
                continue
            else:
                sum_ob += self.volumes[index]
                sum_w += self.value[index]

        # if greater than the optimal return -1 or the number otherwise
        if sum_ob > self.C:
            return -1
        else:
            return sum_w

    # run generations of GA
    def evaluation(self):

        # wyliczyc najleprzy sposrod rodzicow
        best_pop = self.population // 2
        for i in range(len(self.parents)):
            parent = self.parents[i]
            ft = self.fitness(parent)
            self.bests.append((ft, parent))

        # sortowanie najleprzych
        self.bests.sort(key=operator.itemgetter(0), reverse=True)
        self.best_p = self.bests[:best_pop]
        self.best_p = [x[1] for x in self.best_p]

    # mutacja odbywa się losowo
    def mutation(self, ch):

        for i in range(len(ch)):
            k = random.uniform(0, 1)
            if k > 0.5:
                # jeżęli randomowo wybrana liczba jest > 0.5, zamienić 0 z 1 i na odwrót
                if ch[i] == 1:
                    ch[i] = 0
                else:
                    ch[i] = 1
        return ch

    # skrzyżowanie dwóch rodziców, aby uzyskać dwoje dzieci, mieszając je losowo za każdym razem
    def crossover(self, ch1, ch2):

        threshold = random.randint(1, len(ch1) - 1)
        tmp1 = ch1[threshold:]
        tmp2 = ch2[threshold:]
        ch1 = ch1[:threshold]
        ch2 = ch2[:threshold]
        ch1.extend(tmp2)
        ch2.extend(tmp1)

        return ch1, ch2

    # uruchomić Algorytm Genetyczny
    def run(self):

        # uruchom ocenę raz
        self.evaluation()
        newparents = []
        pop = len(self.best_p) - 1

        # utwórz listę z unikalnymi losowymi liczbami całkowitymi
        sample = random.sample(range(pop), pop)
        for i in range(0, pop):
            # wybierz losowy indeks najlepszych dzieci, aby randomizować proces
            if i < pop - 1:
                r1 = self.best_p[i]
                r2 = self.best_p[i + 1]
                nchild1, nchild2 = self.crossover(r1, r2)
                newparents.append(nchild1)
                newparents.append(nchild2)
            else:
                r1 = self.best_p[i]
                r2 = self.best_p[0]
                nchild1, nchild2 = self.crossover(r1, r2)
                newparents.append(nchild1)
                newparents.append(nchild2)

        # mutować nowe dzieci i potencjalnych rodziców, aby zapewnić globalną optymalizację
        for i in range(len(newparents)):
            newparents[i] = self.mutation(newparents[i])

        if self.opt in newparents:
            print("najleprzy wynnik znaleziono po {} generacjach".format(self.iterated))
            print(self.opt)
            print(self.parents)
        else:
            self.iterated += 1
            print("utworzono {} generacij".format(self.iterated))
            self.parents = newparents
            self.bests = []
            self.best_p = []
            self.run()


def run_evolution():
    """
    :param volume - objętość rzeczy
    :param profit - wartość poszczególych rzeczy
    :param opt - rozwiązanie optymalne podawanę ręcznie
    :param C - objętość walizki
    :param population - rozmiar populacji
    :return:
    """

    # zmienne dla dannego algorytmu
    volume = [12, 7, 11, 8, 9]
    profits = [24, 13, 23, 15, 16]
    opt = [0, 1, 1, 1, 0]

    while True:
        C = int(input("Podaj objętość walizki: "))
        if C > 0:
            break

    while True:
        population = int(input("Podaj wielkość pierwszej populacji: "))
        if population > 0:
            break

    k = Knapsack()
    k.properties(volume, profits, opt, C, population)
    start_time = datetime.now()
    k.run()
    finish_time = datetime.now() - start_time
    print(f'czas wykonania: {finish_time}')


if __name__ == "__main__":
    run_evolution()
