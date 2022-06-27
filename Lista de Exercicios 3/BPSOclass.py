import random
from random import randint
import numpy as np
from numpy import *
import random
import math
import matplotlib.pyplot as plt

particle_size = 50  # number of particles
iterations = 100  # max number of iterations
nd = 50 # num dimensions
w = 0.75  # inertia constant
c1 = 1  # cognative constant
c2 = 2  # social constant

def sigmoid(v):
  return 1 / (1 + math.exp(-v))

class Individuo:
    def __init__(self):
        self.particle_position = np.random.binomial(1, .5, nd)  # particle position
        self.particle_velocity = np.random.uniform(-1, 1, nd)  # particle velocity
        self.local_best_particle_position = []  # best position of the particle
        self.fitness_particle_position = -float("inf")  # objective function value of the particle position
        self.fitness_local_best_particle_position = -float("inf")  # initial objective function value of the best particle position

    def evaluate(self):
        self.fitness_particle_position = sum(self.particle_position)
        if self.fitness_particle_position > self.fitness_local_best_particle_position:
            self.local_best_particle_position = self.particle_position  # update the local best
            self.fitness_local_best_particle_position = self.fitness_particle_position  # update the fitness of the local best

    def update_velocity(self, global_best_particle_position):
        for d in range(nd):
            r1 = random.uniform(0, 1)
            r2 = random.uniform(0, 1)
            cognitive_velocity = c1 * r1 * (self.local_best_particle_position[d] - self.particle_position[d])
            social_velocity = c2 * r2 * (global_best_particle_position[d] - self.particle_position[d])
            self.particle_velocity[d] = w * self.particle_velocity[d] + cognitive_velocity + social_velocity

    def update_position(self):
        for d in range(nd):
            if random.uniform(0, 100) >= sigmoid(self.particle_velocity[d]):
                self.particle_position[d] = 1
            else:
                self.particle_position[d] = 0

# EXECUÇÃO DO ALGORITMO
global_best_particle_position = []
fitness_global_best_particle_position = -float("inf")
fitness_global_worst_particle_position = float("inf")

swarm_particle = []
num_ite, ev_minimo, ev_medio, ev_maximo = [], [], [], []

for i in range(particle_size): # criação do grupo de individuos
    ind = Individuo()
    swarm_particle.append(ind)

for ite in range(iterations):
    num_ite += [ite]

    # calculando o fitness dos individuos
    for ind in swarm_particle:
        ind.evaluate()

    fitness_global_worst_particle_position = float("inf")
    # verifica quem é o melhor da iteração
    for ind in swarm_particle:
        if ind.fitness_particle_position > fitness_global_best_particle_position:
            global_best_particle_position = ind.particle_position
            fitness_global_best_particle_position = ind.fitness_particle_position

        if ind.fitness_particle_position < fitness_global_worst_particle_position:
            fitness_global_worst_particle_position = ind.fitness_particle_position

    soma = 0
    for cat in swarm_particle:
        soma += cat.fitness_particle_position

    ev_medio += [soma / particle_size]
    ev_minimo += [fitness_global_worst_particle_position]
    ev_maximo += [fitness_global_best_particle_position]

    # verfica a convergencia
    if fitness_global_best_particle_position - fitness_global_worst_particle_position < 2:
        print('Iteration:', ite + 1)
        break

    # atualiza velocidade e posição
    for ind in swarm_particle:
        ind.update_velocity(global_best_particle_position)
        ind.update_position()

print('Optimal solution:', global_best_particle_position)
print('Objective function value:', fitness_global_best_particle_position)

fig = plt.figure("Lista de Exercicios 3",figsize=plt.figaspect(1))
ax = fig.add_subplot(1,1,1)

ax.title.set_text("BPSO Classico")
ax.set_xlabel('Iterações')
ax.set_ylabel('Fitness')
ax.set_xticks(num_ite)

plt.plot(num_ite, ev_minimo, label="Fitness Minimo")
plt.plot(num_ite, ev_medio, label="Fitness Médio")
plt.plot(num_ite, ev_maximo, label="Fitness Maximo")

plt.legend()

plt.show()