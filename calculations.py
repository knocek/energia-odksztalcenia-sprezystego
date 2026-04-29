import numpy as np

def calculate_all(epsilon, E, nu):
    if E <= 0:
        raise ValueError("Moduł Younga E musi być większy od zera.")
    
    if not (-1 < nu < 0.5):
        raise ValueError("Współczynnik Poissona ν musi być w zakresie -1 < v < 0.5.")
    
    # odkształcenie średnie
    # np.trace liczy sumę elementów na przekątnej macierzy, czyli w tym przypadku sumę odkształceń normalnych
    epsilon_m = np.trace(epsilon) / 3

     # moduły materiałowe
    K = E / (3 * (1 - 2 * nu))
    mu = E / (2 * (1 + nu))

    # tensor jednostkowy
    I = np.identity(3)

    # tensor odkształceń dewiatorowych
    # iloczyn elementów macierzy epsilon i I, czyli mnożenie każdego elementu macierzy epsilon przez odpowiedni element macierzy I, odpowiada sumie ε′ij2
    epsilon_dev = epsilon - epsilon_m * I

    # energia odkształcenia objętościowego
    phi_v = 0.5 * K * (3 * epsilon_m)**2

    # energia odkształcenia postaciowego
    phi_s = mu * np.sum(epsilon_dev * epsilon_dev)

    # energia całkowita
    phi = phi_v + phi_s

    # naprężenie średnie
    sigma_m = 3 * K * epsilon_m

    return {
        "epsilon_m": epsilon_m,
        "K": K,
        "mu": mu,
        "epsilon_dev": epsilon_dev,
        "phi_v": phi_v,
        "phi_s": phi_s,
        "phi": phi,
        "sigma_m": sigma_m
    }

# przykładowe dane do testowania funkcji
# epsilon = np.array([
#     [0.001, 0.0, 0.0],
#     [0.0, 0.002, 0.0],
#     [0.0, 0.0, -0.001]
# ])

# E = 210e9
# nu = 0.3

# results = calculate_all(epsilon, E, nu)

# for key, value in results.items():
#     print(f"{key}: {value}")