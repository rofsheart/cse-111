import random

from project import (
    ILLNESS_LENGTH,
    apply_social_distancing,
    build_history,
    count_status,
    create_population,
    initialize_infected,
    record_daily_statistics,
    recovery_rate,
    spread_disease,
    update_infected,
    vaccinate_population,
)


def test_create_population_size():
    population = create_population(350)
    assert len(population) == 350


def test_create_population_initial_status():
    population = create_population(7)
    for person in population:
        assert person["status"] == "susceptible"
        assert person["vaccinated"] is False
        assert person["days_infected"] == 0


def test_initialize_infection_count():
    population = create_population(350)
    initialize_infected(population, 7)
    assert count_status(population, "infected") == 7


def test_apply_social_distancing():
    result = apply_social_distancing(infection_rate=0.20,
                                     distancing_factor=0.50)
    assert result == 0.10


def test_count_status():
    population = create_population(350)
    initialize_infected(population, 7)
    assert count_status(population, "infected") == 7


def test_vaccinate_population():
    population = create_population(350)
    # rate 1.0 -> everyone vaccinated, deterministic
    vaccinate_population(population, vaccination_rate=1.0)
    vaccinated = sum(1 for p in population if p["vaccinated"])
    assert vaccinated == 350


def test_record_daily_statistics():
    population = create_population(50)
    history = build_history()
    record_daily_statistics(population, history)
    assert len(history["healthy"]) == 1
    assert len(history["infected"]) == 1
    assert len(history["recovered"]) == 1
    assert len(history["dead"]) == 1


def test_update_infections_recovery():
    # Force every infected person to have been sick long enough.
    population = [
        {"x": 0, "y": 0, "status": "infected",
         "vaccinated": False, "days_infected": ILLNESS_LENGTH}
        for _ in range(7)
    ]
    update_infected(population, recovery_rate=1.0, death_rate=0.0)
    assert count_status(population, "recovered") == 7


def test_update_infections_death():
    population = [
        {"x": 0, "y": 0, "status": "infected",
         "vaccinated": False, "days_infected": ILLNESS_LENGTH}
        for _ in range(7)
    ]
    update_infected(population, recovery_rate=0.0, death_rate=1.0)
    assert count_status(population, "dead") == 7


def test_spread_disease():
    # Two people, right next to each other, infection rate 1.0
    population = [
        {"x": 100, "y": 100, "dx": 0, "dy": 0,
         "status": "infected", "vaccinated": False, "days_infected": 0},
        {"x": 105, "y": 100, "dx": 0, "dy": 0,
         "status": "susceptible", "vaccinated": False, "days_infected": 0},
    ]
    spread_disease(population, infection_rate=1.0, infection_radius=15)
    assert population[1]["status"] == "infected"