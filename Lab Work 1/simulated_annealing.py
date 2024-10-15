import numpy as np
import random
from math import exp
from collections import Counter
import cProfile
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PySide2.QtCore import Signal, QObject, Slot
from PySide2.QtWidgets import QMessageBox

class SimulatedAnnealing(QObject):
    def __init__(self, t_min, t_max, alpha, n, iterations):
        QObject.__init__(self)
        self.t_min = t_min
        self.t_max = t_max
        self.t_current = t_max
        self.alpha = alpha
        self.n = n
        self.iterations = iterations

        # Initial solutions and energies
        self.start_solution = self.initialize_solution()
        self.start_energy = self.check_conflicts(self.start_solution)

        # Current best solution and energy
        self.current_solution = self.start_solution.copy()
        self.current_energy = self.start_energy

        # Global best solution and energy
        self.best_solution = self.start_solution.copy()
        self.best_energy = self.start_energy

        # Statistics to track during the annealing process
        self.stats = {
            "iterations": [0],
            "bad_solutions": [0],
            "temperature": [self.t_max],
            "energy": [self.start_energy]
        }

    def check_conflicts(self, solution):
        # Count the number of conflicts in the current solution
        conflicts = 0
        for i in range(self.n - 1):
            for j in range(i + 1, self.n):
                if (
                    solution[i] == solution[j] or
                    abs(i - j) == abs(solution[i] - solution[j])
                ):
                    conflicts += 1
        return conflicts

    def initialize_solution(self):
        # Randomly initialize the queen positions
        solution = list(range(self.n))
        random.shuffle(solution)
        return solution

    def generate_swappos(self):
        # Generate two distinct random positions for swapping queens
        v = random.sample(range(self.n - 1), 2)
        return v[0], v[1]

    def calculate(self):
        # Annealing process to find a solution
        bad_solutions = 0
        total_iterations = 0
        while self.t_current > self.t_min:
            for current_iteration in range(self.iterations - 1):
                solution = self.current_solution.copy()
                energy = self.current_energy

                # Generate two positions for swapping queens
                x, y = self.generate_swappos()
                solution[x], solution[y] = solution[y], solution[x]

                # Calculate conflicts in the new solution
                energy = self.check_conflicts(solution)

                if energy < self.current_energy:
                    # Accept the new solution if it improves
                    self.current_solution = solution.copy()
                    self.current_energy = energy
                else:
                    # Accept the new solution with a certain probability if it doesn't improve
                    p = exp(-(energy - self.current_energy) / self.t_current)
                    if p > random.random():
                        self.t_current *= self.alpha
                        self.current_solution = solution.copy()
                        self.current_energy = energy
                        bad_solutions += 1

                # Update global best solution if needed
                if self.current_energy < self.best_energy:
                    self.best_solution = self.current_solution.copy()
                    self.best_energy = self.current_energy

                # Update statistics
                self.stats['iterations'].append(total_iterations)
                self.stats['bad_solutions'].append(bad_solutions)
                self.stats['temperature'].append(self.t_current)
                self.stats['energy'].append(self.current_energy)
                total_iterations += 1

                if self.current_energy == 0:
                    return {
                        "array": self.best_solution,
                        "energy": self.best_energy
                    }

        return {
            "array": self.best_solution,
            "energy": self.best_energy
        }

    @Slot()
    def plot(self):
        # Plot the annealing process with temperature, bad solutions, and energy
        blue_patch = mpatches.Patch(color='blue', label='Temperature')
        red_patch = mpatches.Patch(color='red', label='Number of accepted bad solutions')
        green_patch = mpatches.Patch(color='green', label='Energy of the best solution')

        plt.plot(
            self.stats['iterations'],
            self.stats['temperature'],
            color="blue",
            label='Temperature'
        )
        plt.plot(
            self.stats['iterations'],
            self.stats['bad_solutions'],
            color="red",
            label='Number of accepted bad solutions'
        )
        plt.plot(
            self.stats['iterations'],
            self.stats['energy'],
            color="green",
            label='Energy of the best solution'
        )

        plt.legend(handles=[red_patch, blue_patch, green_patch])
        plt.title("Simulated Annealing Optimization Process")
        plt.show()
