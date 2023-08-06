from mobspy import *
import matplotlib.pyplot as plt
import os

if __name__ == '__main__':

    Color, Disease = BaseSpecies()
    Tree, Person = New(Color * Disease)

    Color.blue, Color.red, Color.yellow
    Disease.not_sick, Disease.sick

    Disease.not_sick >> Disease.sick[1]

    Tree.yellow(100), Tree.red(100), Tree.blue(100)
    # Person.yellow(50), Person.red(50), Person.blue(50)

    S = Simulation(Tree | Person)
    S.method = 'stochastic'
    S.repetitions = 2
    S.duration = 5
    S.plot_data = False
    S.run()
    S.plot_stochastic(Tree.sick, Tree.not_sick, Person.blue)

