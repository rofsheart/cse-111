"""Pytest tests for the core simulation functions.

Run with:  pytest test_simulation.py -v
"""

import random

import pytest

from disease_simulation import (
    SUSCEPTIBLE, INFECTED, RECOVERED, DEAD,
    WIDTH, HEIGHT,
    create_person, create_population, initialize_infected,
    vaccinate_population, count_status, apply_social_distancing,
    distance, spread_disease, update_infected, move_people,
    build_history, record_daily_statistics,
)


# ----------------------------- create_person -----------------------------
def test_create_person_sets_position():
    p = create_person(100, 200)
    assert p["x"] == 100
    assert p["y"] == 200


def test_create_person_defaults():
    p = create_person()
    assert p["status"] == SUSCEPTIBLE
    assert p["vaccinated"] is False
    assert p["days_infected"] == 0


def test_create_person_position_in_bounds():
    for _ in range(50):
        p = create_person()
        assert 20 <= p["x"] <= WIDTH - 20
        assert 20 <= p["y"] <= HEIGHT - 20


# ---------------------------- create_population --------------------------
def test_create_population_length():
    pop = create_population(50)
    assert len(pop) == 50


def test_create_population_empty():
    assert create_population(0) == []


# --------------------------- initialize_infected -------------------------
def test_initialize_infected_sets_count():
    pop = create_population(20)
    n = initialize_infected(pop, 5)
    assert n == 5
    assert count_status(pop, INFECTED) == 5


def test_initialize_infected_skips_vaccinated():
    pop = create_population(5)
    for p in pop:
        p["vaccinated"] = True
    n = initialize_infected(pop, 3)
    assert n == 0
    assert count_status(pop, INFECTED) == 0


# --------------------------- vaccinate_population ------------------------
def test_vaccinate_population_all():
    pop = create_population(10)
    n = vaccinate_population(pop, 1.0)
    assert n == 10
    assert all(p["vaccinated"] for p in pop)


def test_vaccinate_population_none():
    pop = create_population(10)
    n = vaccinate_population(pop, 0.0)
    assert n == 0
    assert not any(p["vaccinated"] for p in pop)


# ------------------------------ count_status -----------------------------
def test_count_status():
    pop = create_population(5)
    pop[0]["status"] = INFECTED
    pop[1]["status"] = RECOVERED
    pop[2]["status"] = DEAD
    assert count_status(pop, SUSCEPTIBLE) == 2
    assert count_status(pop, INFECTED) == 1
    assert count_status(pop, RECOVERED) == 1
    assert count_status(pop, DEAD) == 1


# ----------------------- apply_social_distancing -------------------------
def test_apply_social_distancing_off():
    assert apply_social_distancing(2.0, 0.0) == 2.0


def test_apply_social_distancing_half():
    assert apply_social_distancing(2.0, 0.5) == 1.0


def test_apply_social_distancing_full():
    assert apply_social_distancing(2.0, 1.0) == 0.0


# -------------------------------- distance -------------------------------
def test_distance_pythagorean():
    a = {"x": 0, "y": 0}
    b = {"x": 3, "y": 4}
    assert distance(a, b) == pytest.approx(5.0)


def test_distance_same_point():
    a = {"x": 10, "y": 20}
    assert distance(a, a) == 0.0


# ---------------------------- spread_disease -----------------------------
def test_spread_disease_infects_close_susceptible():
    random.seed(0)
    infected = create_person(100, 100)
    infected["status"] = INFECTED
    healthy = create_person(105, 100)
    spread_disease([infected, healthy], infection_rate=1.0)
    assert healthy["status"] == INFECTED


def test_spread_disease_skips_far_person():
    infected = create_person(100, 100)
    infected["status"] = INFECTED
    far = create_person(500, 500)
    spread_disease([infected, far], infection_rate=1.0)
    assert far["status"] == SUSCEPTIBLE


def test_spread_disease_skips_vaccinated():
    infected = create_person(100, 100)
    infected["status"] = INFECTED
    v = create_person(105, 100)
    v["vaccinated"] = True
    spread_disease([infected, v], infection_rate=1.0)
    assert v["status"] == SUSCEPTIBLE


def test_spread_disease_skips_non_contagious():
    infected = create_person(100, 100)
    infected["status"] = INFECTED
    infected["days_infected"] = 10_000   # way past contagious_length
    healthy = create_person(105, 100)
    spread_disease([infected, healthy], infection_rate=1.0,
                   contagious_length=100)
    assert healthy["status"] == SUSCEPTIBLE


def test_spread_disease_zero_transmission():
    infected = create_person(100, 100)
    infected["status"] = INFECTED
    healthy = create_person(105, 100)
    spread_disease([infected, healthy], infection_rate=0.0)
    assert healthy["status"] == SUSCEPTIBLE


# ---------------------------- update_infected ----------------------------
def test_update_infected_always_dies():
    p = create_person(0, 0)
    p["status"] = INFECTED
    p["days_infected"] = 0
    recovered, dead = update_infected([p], death_rate=1.0, illness_length=5)
    for _ in range(5):
        update_infected([p], death_rate=1.0, illness_length=5)
    assert p["status"] == DEAD


def test_update_infected_always_recovers():
    p = create_person(0, 0)
    p["status"] = INFECTED
    for _ in range(5):
        update_infected([p], death_rate=0.0, illness_length=5)
    assert p["status"] == RECOVERED


def test_update_infected_ignores_healthy():
    p = create_person(0, 0)
    update_infected([p], death_rate=1.0, illness_length=5)
    assert p["status"] == SUSCEPTIBLE
    assert p["days_infected"] == 0


# ------------------------------ move_people ------------------------------
def test_move_people_moves_person():
    p = create_person(100, 100)
    p["dx"] = 1.0
    p["dy"] = 0.0
    move_people([p], movement_rate=1.0, social_distance_factor=0.0)
    assert p["x"] == pytest.approx(101.0)
    assert p["y"] == pytest.approx(100.0)


def test_move_people_bounces_off_left_wall():
    p = create_person(0, 100)
    p["dx"] = -1.0
    p["dy"] = 0.0
    move_people([p], movement_rate=1.0, social_distance_factor=0.0)
    assert p["x"] == 0
    assert p["dx"] == 1.0


def test_move_people_dead_stay_still():
    p = create_person(100, 100)
    p["status"] = DEAD
    p["dx"] = 5.0
    p["dy"] = 5.0
    move_people([p], movement_rate=1.0, social_distance_factor=0.0)
    assert p["x"] == 100
    assert p["y"] == 100


# ---------------------- history and statistics ---------------------------
def test_build_history_keys():
    h = build_history()
    assert set(h.keys()) == {"healthy", "infected", "recovered", "dead"}
    assert all(v == [] for v in h.values())


def test_record_daily_statistics_counts():
    pop = [create_person() for _ in range(4)]
    pop[0]["status"] = INFECTED
    pop[1]["status"] = RECOVERED
    pop[2]["status"] = DEAD
    history = build_history()
    record_daily_statistics(pop, history)
    assert history["healthy"] == [1]
    assert history["infected"] == [1]
    assert history["recovered"] == [1]
    assert history["dead"] == [1]


def test_record_daily_statistics_appends():
    pop = create_population(3)
    history = build_history()
    record_daily_statistics(pop, history)
    record_daily_statistics(pop, history)
    assert len(history["healthy"]) == 2