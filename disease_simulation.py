"""Graphical simulation of disease spread.

Core simulation logic is separated from the Tkinter GUI so the logic can be
imported and tested without a display.
"""

import random
import tkinter as tk
from tkinter import ttk

import numpy as np

try:
    import matplotlib.pyplot as plt
except ImportError:  # pragma: no cover
    plt = None


# ----------------------------- Constants ---------------------------------
WIDTH = 900
HEIGHT = 800
POPULATION_SIZE = 350
INITIAL_INFECTED = 7
INFECTION_RADIUS = 15
CONTAGIOUS_LENGTH = 200
ILLNESS_LENGTH = 400
VACCINATION_RATE = 0.02
SOCIAL_DISTANCING = 0.0          # 0 = off, higher = slower movement
DEFAULT_MOVEMENT = 1.0
DEFAULT_TRANSMISSION = 0.05
DEFAULT_DEATH = 0.05

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
VACCINATED_COLOR = "gold"


# ----------------------- Core simulation functions -----------------------
def create_person(x=None, y=None):
    """Return one person dict with a random position and velocity."""
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
    """Return a list of `size` newly created people."""
    return [create_person() for _ in range(size)]


def initialize_infected(population, count):
    """Infect up to `count` susceptible, unvaccinated people."""
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
    """Give each person a chance to be vaccinated; return the count."""
    count = 0
    for person in population:
        if random.random() < vaccination_rate:
            person["vaccinated"] = True
            count += 1
    return count


def count_status(population, status):
    """Return how many people currently have `status`."""
    return sum(1 for p in population if p["status"] == status)


def apply_social_distancing(movement_rate, social_distance_factor):
    """Return the effective movement rate after social distancing.

    A factor of 0 means normal movement; 1 means nobody moves.
    """
    return movement_rate * (1.0 - social_distance_factor)


def distance(p1, p2):
    """Euclidean distance between two people."""
    return float(np.hypot(p1["x"] - p2["x"], p1["y"] - p2["y"]))


def spread_disease(population, infection_rate,
                   infection_radius=INFECTION_RADIUS,
                   contagious_length=CONTAGIOUS_LENGTH):
    """Infect susceptibles that are within radius of a contagious person.

    Uses a snapshot of the susceptible list so a person infected during
    this step cannot immediately re-infect others in the same step.
    """
    susceptibles = [
        p for p in population
        if p["status"] == SUSCEPTIBLE and not p["vaccinated"]
    ]

    for infected in population:
        if infected["status"] != INFECTED:
            continue
        if infected["days_infected"] > contagious_length:
            continue

        for person in susceptibles:
            if person["status"] != SUSCEPTIBLE:
                continue
            if distance(infected, person) <= infection_radius:
                if random.random() < infection_rate:
                    person["status"] = INFECTED
                    person["days_infected"] = 0


def update_infected(population, death_rate,
                    illness_length=ILLNESS_LENGTH):
    """Advance every infected person by one day.

    Once `days_infected >= illness_length`, the person either dies (with
    probability `death_rate`) or recovers. There is no limbo state.
    """
    recovered = 0
    dead = 0
    for person in population:
        if person["status"] != INFECTED:
            continue
        person["days_infected"] += 1
        if person["days_infected"] >= illness_length:
            if random.random() < death_rate:
                person["status"] = DEAD
                dead += 1
            else:
                person["status"] = RECOVERED
                recovered += 1
    return recovered, dead


def move_people(population, movement_rate, social_distance_factor=0.0):
    """Move every living person and bounce them off the walls."""
    effective = apply_social_distancing(movement_rate,
                                        social_distance_factor)
    for person in population:
        if person["status"] == DEAD:
            continue
        person["x"] += person["dx"] * effective
        person["y"] += person["dy"] * effective

        if person["x"] < 0:
            person["x"] = 0
            person["dx"] *= -1
        elif person["x"] > WIDTH:
            person["x"] = WIDTH
            person["dx"] *= -1

        if person["y"] < 0:
            person["y"] = 0
            person["dy"] *= -1
        elif person["y"] > HEIGHT:
            person["y"] = HEIGHT
            person["dy"] *= -1


def build_history():
    """Return an empty statistics history dictionary."""
    return {"healthy": [], "infected": [], "recovered": [], "dead": []}


def record_daily_statistics(population, history):
    """Append today's counts to the history dictionary."""
    history["healthy"].append(count_status(population, SUSCEPTIBLE))
    history["infected"].append(count_status(population, INFECTED))
    history["recovered"].append(count_status(population, RECOVERED))
    history["dead"].append(count_status(population, DEAD))


# -------------------------------- GUI ------------------------------------
def draw_population(canvas, population):
    """Draw every person at their actual (x, y) position."""
    canvas.delete("all")
    radius = 4
    for person in population:
        if person["vaccinated"] and person["status"] == SUSCEPTIBLE:
            color = VACCINATED_COLOR
        else:
            color = COLORS.get(person["status"], "gray")

        x, y = person["x"], person["y"]
        canvas.create_oval(x - radius, y - radius,
                           x + radius, y + radius,
                           fill=color, outline="")


def main():
    root = tk.Tk()
    root.title("Disease Spread Simulation")

    state = {
        "population": create_population(POPULATION_SIZE),
        "history": build_history(),
        "running": False,
        "movement_rate": DEFAULT_MOVEMENT,
        "transmission": DEFAULT_TRANSMISSION,
        "contagious_length": CONTAGIOUS_LENGTH,
        "illness_length": ILLNESS_LENGTH,
        "death": DEFAULT_DEATH,
        "social_distance": SOCIAL_DISTANCING,
    }
    initialize_infected(state["population"], INITIAL_INFECTED)
    vaccinate_population(state["population"], VACCINATION_RATE)

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
    canvas.pack()

    info_label = tk.Label(root, text="", font=("Arial", 12))
    info_label.pack()

    # ----------------------- Sliders -----------------------
    movement_slider = tk.Scale(root, from_=0.0, to=5.0, resolution=0.1,
                               orient="horizontal", label="Movement Rate")
    movement_slider.set(DEFAULT_MOVEMENT)
    movement_slider.pack(fill="x")

    transmission_slider = tk.Scale(root, from_=0.0, to=1.0, resolution=0.01,
                                   orient="horizontal",
                                   label="Transmission Probability")
    transmission_slider.set(DEFAULT_TRANSMISSION)
    transmission_slider.pack(fill="x")

    contagious_slider = tk.Scale(root, from_=10, to=500, resolution=1,
                                 orient="horizontal",
                                 label="Length of Contagiousness (days)")
    contagious_slider.set(CONTAGIOUS_LENGTH)
    contagious_slider.pack(fill="x")

    illness_slider = tk.Scale(root, from_=10, to=1000, resolution=1,
                              orient="horizontal",
                              label="Length of Illness (days)")
    illness_slider.set(ILLNESS_LENGTH)
    illness_slider.pack(fill="x")

    death_slider = tk.Scale(root, from_=0.0, to=1.0, resolution=0.01,
                            orient="horizontal",
                            label="Death Probability")
    death_slider.set(DEFAULT_DEATH)
    death_slider.pack(fill="x")

    distancing_slider = tk.Scale(root, from_=0.0, to=1.0, resolution=0.05,
                                 orient="horizontal",
                                 label="Social Distancing Factor")
    distancing_slider.set(SOCIAL_DISTANCING)
    distancing_slider.pack(fill="x")

    # ----------------------- Buttons -----------------------
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
        update_info_label()

    def apply_settings():
        state["movement_rate"] = movement_slider.get()
        state["transmission"] = transmission_slider.get()
        state["contagious_length"] = int(contagious_slider.get())
        state["illness_length"] = int(illness_slider.get())
        state["death"] = death_slider.get()
        state["social_distance"] = distancing_slider.get()

    def show_graph():
        if plt is None:
            return
        plt.figure(figsize=(10, 6))
        for key, label in [("healthy", "Susceptible"),
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

    def update_info_label():
        info_label.config(
            text=(f"Healthy: {count_status(state['population'], SUSCEPTIBLE)}  "
                  f"Infected: {count_status(state['population'], INFECTED)}  "
                  f"Recovered: {count_status(state['population'], RECOVERED)}  "
                  f"Dead: {count_status(state['population'], DEAD)}")
        )

    def update():
        if state["running"]:
            move_people(state["population"],
                        state["movement_rate"],
                        state["social_distance"])
            spread_disease(state["population"],
                           state["transmission"],
                           contagious_length=state["contagious_length"])
            update_infected(state["population"],
                            state["death"],
                            illness_length=state["illness_length"])
            record_daily_statistics(state["population"], state["history"])
            draw_population(canvas, state["population"])
            update_info_label()
        root.after(30, update)

    draw_population(canvas, state["population"])
    update_info_label()
    update()
    root.mainloop()


if __name__ == "__main__":
    main()
    