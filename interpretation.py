import numpy as np


def interpret_results(results):
    phi_v = results["phi_v"]
    phi_s = results["phi_s"]
    phi = results["phi"]
    epsilon_m = results["epsilon_m"]
    K = results["K"]
    mu = results["mu"]
    epsilon_dev = results["epsilon_dev"]

    tol = 1e-12

    dev_norm = np.sum(epsilon_dev * epsilon_dev)

    # Udział energii objętościowej i postaciowej
    percent_v = phi_v / phi * 100
    percent_s = phi_s / phi * 100

    difference = abs(percent_v - percent_s)

    if difference <= 5:
        dominant = (
            "Energia objętościowa i postaciowa mają zbliżone wartości, "
            "więc żadna z nich wyraźnie nie dominuje."
        )
    elif phi_v > phi_s:
        dominant = "Dominuje zmiana objętości materiału."
    else:
        dominant = "Dominuje zmiana kształtu materiału."

    if dev_norm < tol:
        dev_text = "Tensor dewiatorowy jest równy zero, więc nie występuje zmiana kształtu."
    elif abs(epsilon_m) < tol:
        dev_text = "Odkształcenie średnie jest równe zero, więc nie występuje zmiana objętości."
    else:
        dev_text = "Tensor dewiatorowy jest różny od zera, więc występuje również zmiana kształtu."

    if K > mu:
        material_text = "K > μ, więc materiał silniej przeciwstawia się zmianie objętości niż zmianie kształtu."
    elif mu > K:
        material_text = "μ > K, więc materiał silniej przeciwstawia się zmianie kształtu niż zmianie objętości."
    else:
        material_text = "K = μ, więc opór przeciw zmianie objętości i kształtu jest taki sam."

    return (
        f"- Energia objętościowa stanowi około {percent_v:.2f}% energii całkowitej.\n"
        f"- Energia postaciowa stanowi około {percent_s:.2f}% energii całkowitej.\n"
        f"- {dominant}\n"
        f"- {dev_text}\n"
        f"- {material_text}"
    )