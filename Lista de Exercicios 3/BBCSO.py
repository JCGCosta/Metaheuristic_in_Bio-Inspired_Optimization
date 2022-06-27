import random
from random import randint
import numpy as np
from numpy import *
import random
import math as mt
import matplotlib.pyplot as plt

cats_num = 50  # number of cats
tracing_percentage = .4 # cats in tracing mode percentage
cats_num_tracing_mode = mt.floor(cats_num * tracing_percentage)
smp = 6
pmo = .2
cdc = 20
iterations = 100  # max number of iterations
nd = 500 # num dimensions

class Gato:
    def __init__(self, mode):
        self.mode = mode
        self.position = np.random.binomial(1, .5, nd)  # particle position
        self.velocity = np.random.uniform(-1, 1, nd)  # particle velocity
        self.fitness_particle_position = -float("inf")  # objective function value of the particle position
        self.clones = []
        self.clones_evaluation = []

    def populate_clones(self, clones_qtd):
        for c in range(clones_qtd):
            clone = self.position
            contador_cdc = 0
            for d in clone:
                if random.uniform(0, 1) < pmo and contador_cdc <= cdc:
                    if d == 0: d = 1
                    else: d = 0
                    contador_cdc += 1
            self.clones += [clone]

    def evaluate_clones(self):
        for c in self.clones:
            self.clones_evaluation += [sum(c)]

    def roulette_selection(self):
        participantes_torneio = list(zip(self.clones, self.clones_evaluation))
        max_value = sum(self.clones_evaluation)
        pick, current = random.uniform(0, max_value), 0
        for participante in participantes_torneio:
            current += participante[1]
            if current > pick:
                return participante[0]

    def evaluate(self):
        self.fitness_particle_position = sum(self.position)

    def update_velocity(self, global_best_particle_position):
        for d in range(nd):
            r1 = random.uniform(0, 1)
            self.velocity[d] = int(d != r1 and (global_best_particle_position[d] or self.position[d]))

    def update_position(self):
        for d in range(nd):
            self.position[d] = int(self.position[d] or self.velocity[d])

# EXECUÇÃO DO ALGORITMO
global_best_particle_position = []
fitness_global_best_particle_position = -float("inf")
fitness_global_worst_particle_position = float("inf")

swarm_particle = []
num_ite, ev_minimo, ev_medio, ev_maximo = [], [], [], []

for i in range(cats_num): # criação do grupo de individuos
    cat = Gato("seeking")
    swarm_particle.append(cat)

for ite in range(iterations):
    num_ite += [ite]
    tracing_mode_count = 0

    # calculando o fitness dos individuos
    for cat in swarm_particle:
        cat.evaluate()

    fitness_global_worst_particle_position = float("inf")
    # verifica quem é o melhor da iteração
    for cat in swarm_particle:
        if cat.fitness_particle_position > fitness_global_best_particle_position:
            global_best_particle_position = cat.position
            fitness_global_best_particle_position = cat.fitness_particle_position
        if cat.fitness_particle_position < fitness_global_worst_particle_position:
            fitness_global_worst_particle_position = cat.fitness_particle_position

    soma = 0
    for cat in swarm_particle:
        soma += cat.fitness_particle_position

    ev_medio += [soma / cats_num]
    ev_minimo += [fitness_global_worst_particle_position]
    ev_maximo += [fitness_global_best_particle_position]

    # verfica a convergencia
    if fitness_global_best_particle_position - fitness_global_worst_particle_position < 2:
        print('Iteration:', ite + 1)
        break

    # define os gatos em tracing e seeking mode
    for cat in swarm_particle:
        cat.mode = "seeking"
    for cat in swarm_particle:
        if random.randint(0, 1) == 1 and tracing_mode_count < cats_num_tracing_mode:
            cat.mode = "tracing"
            tracing_mode_count += 1

    for cat in swarm_particle:
        if cat == "tracing": # SE EM TRAICING MODE
            cat.populate_clones(smp)
            cat.evaluate_clones()
            cat.position = cat.roulette_selection()

        if cat.mode == "seeking": # SE EM SEEKING MODE
            cat.update_velocity(global_best_particle_position)
            cat.update_position()

print('Optimal solution:', global_best_particle_position)
print('Objective function value:', fitness_global_best_particle_position)

fig = plt.figure("Lista de Exercicios 3",figsize=plt.figaspect(1))
ax = fig.add_subplot(1,1,1)

ax.title.set_text("BBCSO")
ax.set_xlabel('Iterações')
ax.set_ylabel('Fitness')
ax.set_xticks(num_ite)

plt.plot(num_ite, ev_minimo, label="Fitness Minimo")
plt.plot(num_ite, ev_medio, label="Fitness Médio")
plt.plot(num_ite, ev_maximo, label="Fitness Maximo")

plt.legend()

plt.show()