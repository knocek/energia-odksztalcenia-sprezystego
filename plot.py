import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter


def create_plot(K, mu, epsilon):
    eps_m_range = np.linspace(-0.01, 0.01, 200)

    epsilon_m = np.trace(epsilon) / 3
    I = np.identity(3)
    epsilon_dev = epsilon - epsilon_m * I

    phi_v_values = []
    phi_s_values = []

    for eps_m in eps_m_range:
        epsilon_plot = epsilon_dev + eps_m * I

        eps_m_current = np.trace(epsilon_plot) / 3
        epsilon_dev_current = epsilon_plot - eps_m_current * I

        phi_v = 0.5 * K * (3 * eps_m_current) ** 2
        phi_s = mu * np.sum(epsilon_dev_current * epsilon_dev_current)

        phi_v_values.append(phi_v)
        phi_s_values.append(phi_s)

    fig, ax = plt.subplots(figsize=(7, 4.0), dpi=100)

    ax.plot(eps_m_range, phi_v_values, label="Φv")
    ax.plot(eps_m_range, phi_s_values, label="Φs")

    ax.set_xlabel(r"Odkształcenie średnie $\varepsilon_m$")
    ax.set_ylabel("Energia [J/m³]")
    ax.set_title(
    r"Zależność energii objętościowej ($\Phi_v$)" "\n"
    r"i postaciowej ($\Phi_s$) od odkształcenia średniego ($\varepsilon_m$)"
    )
    ax.legend()
    ax.grid(True, linewidth=0.5)
    formatter = ScalarFormatter(useMathText=False)
    formatter.set_scientific(False)
    formatter.set_useOffset(False)

    ax.yaxis.set_major_formatter(formatter)
    ax.ticklabel_format(style="plain", axis="y")

    ax.tick_params(axis="both", labelsize=8)
    fig.tight_layout()

    return fig