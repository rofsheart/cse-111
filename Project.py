import random
import tkinter as tk
from tkinter import ttk

import numpy as np

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


# ---------- Simulation constants ----------
WIDTH = 900
HEIGHT = 800
POPULATION_SIZE = 350
INITIAL_INFECTED = 7
INFECTION_RADIUS = 15
CONTAGIOUS_LENGTH = 200
ILLNESS_LENGTH = 400
VACCINATION_RATE = 0.02
SOCIAL_DISTANCING = 0.03
DEFAULT_TRANSMISSION = 0.05
DEFAULT_DEATH = 0.05
recovery_rate = 0.10  # default recovery rate used by tests

SUSCEPTIBLE = "susceptible"
INFECTED = "infected"
RECOVERED = "recovered"
DEAD = "dead"

COLORS = {
    SUSCEPTIBLE: "blue",
    INFECTED: "red",
    RECOVERED: "green",
    DEAD: "black",
}


# ---------- Core simulation functions (testable) ----------
def create_person(x=None, y=None):
    """Return one person dict with random position and velocity."""
    if x is None:
        x = random.randint(20, WIDTH - 20)
    if y is None:
        y = random.randint(20, HEIGHT - 20)
    return {
        "x": x,
        "y": y,
        "dx": random.uniform(-2, 2),
        "dy": random.uniform(-2, 2),
        "status": SUSCEPTIBLE,
        "vaccinated": False,
        "days_infected": 0,
    }


def create_population(size):
    """Return a list of `size` new person dicts."""
    return [create_person() for _ in range(size)]


def initialize_infected(population, count):
    """Infect `count` susceptible people. Return number infected."""
    infected = 0
    attempts = 0
    max_attempts = len(population) * 10
    while infected < count and attempts < max_attempts:
        person = random.choice(population)
        if person["status"] == SUSCEPTIBLE and not person["vaccinated"]:
            person["status"] = INFECTED
            person["days_infected"] = 0
            infected += 1
        attempts += 1
    return infected


def vaccinate_population(population, vaccination_rate):
    """Give each person a chance to be vaccinated. Return count."""
    count = 0
    for person in population:
        if random.random() < vaccination_rate:
            person["vaccinated"] = True
            count += 1
    return count


def count_status(population, status):
    """Return how many people currently have the given status."""
    return sum(1 for p in population if p["status"] == status)


def apply_social_distancing(infection_rate, distancing_factor):
    """Return the effective infection rate after distancing."""
    return infection_rate * (1 - distancing_factor)


def distance(p1, p2):
    """Euclidean distance between two person dicts."""
    return np.sqrt((p1["x"] - p2["x"]) ** 2 + (p1["y"] - p2["y"]) ** 2)


def spread_disease(population, infection_rate,
                   infection_radius=INFECTION_RADIUS):
    """Infect susceptible people who are close to an infected person."""
    infected_people = [p for p in population if p["status"] == INFECTED]
    for infected in infected_people:
        if infected["days_infected"] > CONTAGIOUS_LENGTH:
            continue
        for person in population:
            if person["status"] != SUSCEPTIBLE or person["vaccinated"]:
                continue
            if distance(infected, person) <= infection_radius:
                if random.random() < infection_rate:
                    person["status"] = INFECTED
                    person["days_infected"] = 0


def update_infected(population, recovery_rate, death_rate):
    """Advance each infected person by one day; resolve recovery/death."""
    recovered = 0
    dead = 0
    for person in population:
        if person["status"] != INFECTED:
            continue
        person["days_infected"] += 1
        if person["days_infected"] >= ILLNESS_LENGTH:
            if random.random() < death_rate:
                person["status"] = DEAD
                dead += 1
            elif random.random() < recovery_rate:
                person["status"] = RECOVERED
                recovered += 1
    return recovered, dead


def move_people(population, movement_rate, social_distance_factor=1.0):
    """Move every living person and bounce them off the walls."""
    effective = movement_rate * social_distance_factor
    for person in population:
        if person["status"] == DEAD:
            continue
        person["x"] += person["dx"] * effective
        person["y"] += person["dy"] * effective
        if person["x"] < 0 or person["x"] > WIDTH:
            person["dx"] *= -1
        if person["y"] < 0 or person["y"] > HEIGHT:
            person["dy"] *= -1


def build_history():
    """Return an empty statistics history dictionary."""
    return {"healthy": [], "infected": [], "recovered": [], "dead": []}


def record_daily_statistics(population, history):
    """Append today's counts to the history."""
    history["healthy"].append(count_status(population, SUSCEPTIBLE))
    history["infected"].append(count_status(population, INFECTED))
    history["recovered"].append(count_status(population, RECOVERED))
    history["dead"].append(count_status(population, DEAD))


# ---------- GUI ----------
def draw_population(canvas, population):
    canvas.delete("all")
    x0, y0 = 10, 10
    spacing = 15
    per_row = 30
    for i, person in enumerate(population):
        color = COLORS.get(person["status"], "gray")
        if person["vaccinated"] and person["status"] == SUSCEPTIBLE:
            color = "gold"
        row = i // per_row
        col = i % per_row
        x1 = col * spacing + x0
        y1 = row * spacing + y0
        canvas.create_oval(x1, y1, x1 + 10, y1 + 10,
                           fill=color, outline="")


def main():
    root = tk.Tk()
    root.title("Disease Spread Simulation")

    state = {
        "population": create_population(POPULATION_SIZE),
        "history": build_history(),
        "running": False,
        "movement_rate": 1.0,
        "transmission": DEFAULT_TRANSMISSION,
        "death": DEFAULT_DEATH,
        "social_distance": 1.0,
    }
    initialize_infected(state["population"], INITIAL_INFECTED)
    vaccinate_population(state["population"], VACCINATION_RATE)

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
    canvas.pack()

    info_label = tk.Label(root, text="", font=("Arial", 12))
    info_label.pack()

    movement_slider = tk.Scale(root, from_=0.1, to=5.0, resolution=0.1,
                               orient="horizontal", label="Movement Rate")
    movement_slider.set(1.0)
    movement_slider.pack(fill="x")

    transmission_slider = tk.Scale(root, from_=0.0, to=1.0, resolution=0.01,
                                   orient="horizontal",
                                   label="Transmission Probability")
    transmission_slider.set(DEFAULT_TRANSMISSION)
    transmission_slider.pack(fill="x")

    death_slider = tk.Scale(root, from_=0.0, to=1.0, resolution=0.01,
                            orient="horizontal",
                            label="Death Probability")
    death_slider.set(DEFAULT_DEATH)
    death_slider.pack(fill="x")

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    def start_simulation():
        state["running"] = True

    def stop_simulation():
        state["running"] = False

    def reset_simulation():
        state["running"] = False
        state["population"] = create_population(POPULATION_SIZE)
        state["history"] = build_history()
        initialize_infected(state["population"], INITIAL_INFECTED)
        vaccinate_population(state["population"], VACCINATION_RATE)
        draw_population(canvas, state["population"])

    def apply_settings():
        state["movement_rate"] = movement_slider.get()
        state["transmission"] = transmission_slider.get()
        state["death"] = death_slider.get()

    def show_graph():
        if plt is None:
            return
        plt.figure(figsize=(10, 6))
        for key, label in [("healthy", "Healthy"),
                           ("infected", "Infected"),
                           ("recovered", "Recovered"),
                           ("dead", "Dead")]:
            plt.plot(state["history"][key], label=label)
        plt.title("Disease Spread Statistics")
        plt.xlabel("Time Steps")
        plt.ylabel("Population")
        plt.legend()
        plt.grid(True)
        plt.show()

    ttk.Button(button_frame, text="Start",
               command=start_simulation).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Stop",
               command=stop_simulation).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Reset",
               command=reset_simulation).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Apply Settings",
               command=apply_settings).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Show Graph",
               command=show_graph).pack(side="left", padx=5)

    def update():
        if state["running"]:
            move_people(state["population"], state["movement_rate"],
                        state["social_distance"])
            spread_disease(state["population"], state["transmission"])
            update_infected(state["population"], recovery_rate,
                            state["death"])
            record_daily_statistics(state["population"], state["history"])
            draw_population(canvas, state["population"])
            info_label.config(
                text=(f"Healthy: {count_status(state['population'], SUSCEPTIBLE)}  "
                      f"Infected: {count_status(state['population'], INFECTED)}  "
                      f"Recovered: {count_status(state['population'], RECOVERED)}  "
                      f"Dead: {count_status(state['population'], DEAD)}")
            )
        root.after(30, update)

    draw_population(canvas, state["population"])
    update()
    root.mainloop()


if __name__ == "__main__":
    main()