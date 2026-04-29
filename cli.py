import numpy as np
from calculations import calculate_all
import math
import matplotlib.pyplot as plt
from plot import create_plot
from interpretation import interpret_results

# format naukowy
def format_sci(x):
    if x == 0:
        return "0"
    exp = int(math.floor(math.log10(abs(x))))
    mant = x / (10**exp)
    return f"{mant:.3f} × 10^{exp}"

# funkcja do mnozenia tensora odkształceń przez wspólny mnożnik
def read_multiplier():
    print("\nPodaj wspólny mnożnik dla tensora (np. 1, 1e-3, 10^-3)")
    val = input("mnożnik = ")

    val = val.replace(",", ".").strip()

    if val.startswith("10^"):
        exp = float(val[3:])
        return 10 ** exp

    return parse_input(val)

# funkcja do parsowania liczby z różnych formatów
def parse_input(value):
    value = value.replace(",", ".").strip() # obsługa , i .

    # obsługa formatu 3*10^-4
    if "*10^" in value:
        base, exp = value.split("*10^")
        return float(base) * (10 ** float(exp))

    return float(value)

def read_float(prompt):
    while True:
        try:
            val = input(prompt)
            return parse_input(val)
        except ValueError:
            print("Błąd: wpisz np. 0.001, 1e-3 lub 3*10^-4")

# sprawdzenie symetrii tensora odkształceń
def check_tensor_symmetry(epsilon):
    if np.allclose(epsilon, epsilon.T):
        return True

    print("\nUWAGA: podany tensor odkształceń nie jest symetryczny.")
    print("Dla fizycznego tensora odkształceń powinno być:")
    print("εxy = εyx, εxz = εzx, εyz = εzy")
    print("\nWpisane wartości:")
    print(f"εxy = {epsilon[0,1]}, εyx = {epsilon[1,0]}")
    print(f"εxz = {epsilon[0,2]}, εzx = {epsilon[2,0]}")
    print(f"εyz = {epsilon[1,2]}, εzy = {epsilon[2,1]}")
    print("\nProgram może wykonać obliczenia, ale wynik nie ma poprawnej interpretacji fizycznej.")

    answer = input("Czy mimo to kontynuować obliczenia? [t/n]: ").lower()

    return answer == "t"

# funkcja do wczytania tensora odkształceń z konsoli
def read_epsilon_tensor():
    print("\nPodaj tensor odkształceń 3x3.")

    multiplier = read_multiplier()

    values = []
    names = [
        "εxx", "εxy", "εxz",
        "εyx", "εyy", "εyz",
        "εzx", "εzy", "εzz"
    ]

    for name in names:
        val = read_float(f"{name} = ")
        values.append(val * multiplier)

    return np.array(values).reshape(3, 3)

# funkcja do pokazywania wyników w konsoli
def print_results(results):
    print("\n--------------------------")
    print("\nWYNIKI OBLICZEŃ")

    print(f"odkształcenie średnie εm = {format_sci(results['epsilon_m'])}")
    print(f"moduł objętościowy K = {format_sci(results['K'])} Pa")
    print(f"moduł Kirchoffa μ = {format_sci(results['mu'])} Pa")
    print(f"naprężenie średnie σm = {format_sci(results['sigma_m'])} Pa")

    print("\nTensor dewiatorowy ε':")
    print(results["epsilon_dev"])

    print("\nenergia objętościowa Φv =", format_sci(results["phi_v"]), "J/m³")
    print("energia postaciowa Φs =", format_sci(results["phi_s"]), "J/m³")
    print("energia całkowita Φ  =", format_sci(results["phi"]), "J/m³")
    print("\n--------------------------")
    print("\nINTERPRETACJA WYNIKÓW:")
    print(interpret_results(results))


def run_cli():
    print("Program: Energia odkształcenia sprężystego")
    print("Tryb konsolowy CLI")

    epsilon = read_epsilon_tensor()
    if not check_tensor_symmetry(epsilon):
        print("Przerwano obliczenia.")
        return

    print("\nPodaj parametry materiałowe:")
    E = read_float("Moduł Younga E [Pa] = ")
    nu = read_float("Współczynnik Poissona ν = ")

    try:
        results = calculate_all(epsilon, E, nu)
    except ValueError as e:
        print(f"\nBłąd danych wejściowych: {e}")
        return

    print_results(results)

    answer = input("\nCzy wyświetlić wykres? [t/n]: ").lower()

    if answer == "t":
        fig = create_plot(results["K"], results["mu"], epsilon)
        plt.show()


if __name__ == "__main__":
    run_cli()