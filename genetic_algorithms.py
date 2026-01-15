import streamlit as st
import numpy as np

POPULATION_SIZE = 300
CHROMOSOME_LENGTH = 80
GENERATIONS = 50
FITNESS_PEAKS_AT_ONES= 40
MAX_FITNESS = 80

def fitness(individual):
    ones = np.sum(individual)
    return MAX_FITNESS - abs(FITNESS_PEAKS_AT_ONES - ones)

def initialize_population():
    return np.random.randint(2, size=(POPULATION_SIZE, CHROMOSOME_LENGTH))

def select(population, fitness_scores):
    probabilities = fitness_scores / fitness_scores.sum()
    idx = np.random.choice(len(population), size=2, p=probabilities)
    return population[idx[0]], population[idx[1]]

def crossover(parent1, parent2):
    point = np.random.randint(1, CHROMOSOME_LENGTH-1)
    child = np.concatenate((parent1[:point], parent2[point:]))
    return child

def mutate(individual, rate=0.01):
    for i in range(CHROMOSOME_LENGTH):
        if np.random.rand() < rate:
            individual[i] = 1 - individual[i]
    return individual

st.title("Genetic Algorithm ")

if st.button("Run Genetic Algorithm"):

    population = initialize_population()
    best_fitness_list = []

    for gen in range(GENERATIONS):
        fitness_scores = np.array([fitness(ind) for ind in population])
        best_fitness_list.append(fitness_scores.max())

        new_population = []


        elite = population[np.argmax(fitness_scores)]
        new_population.append(elite)

        while len(new_population) < POPULATION_SIZE:
            p1, p2 = select(population, fitness_scores)
            child = crossover(p1, p2)
            child = mutate(child)
            new_population.append(child)

        population = np.array(new_population)

    best_solution = population[np.argmax([fitness(ind) for ind in population])]
    best_ones = np.sum(best_solution)

    st.subheader("Best Pattern")
    st.write(best_solution)
    st.write("Number of 1s:", best_ones)

    st.subheader("Fitness Progress")
    st.line_chart(best_fitness_list)
