import tkinter as tk
from tkinter import messagebox
import numpy as np
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from plot import create_plot
from tkinter import filedialog

from calculations import calculate_all
from interpretation import interpret_results

# format naukowy
def format_sci(x):
    if x == 0:
        return "0"
    exp = int(math.floor(math.log10(abs(x))))
    mant = x / (10 ** exp)
    return f"{mant:.3f} × 10^{exp}"

# formatowanie macierzy 3x3
def format_matrix(matrix):
    lines = []
    for row in matrix:
        formatted_row = [f"{format_sci(value):>14}" for value in row]
        lines.append("[ " + "  ".join(formatted_row) + " ]")
    return "\n".join(lines)

# funkcja do parsowania liczby z różnych formatów
def parse_number(value):
    value = value.replace(",", ".").strip()

    if value.startswith("10^"):
        exp = float(value[3:])
        return 10 ** exp

    if "*10^" in value:
        base, exp = value.split("*10^")
        return float(base) * (10 ** float(exp))

    return float(value)

# funkcja do uruchomienia GUI
def run_gui():
    root = tk.Tk()
    root.title("Energia odkształcenia")

    current_fig = None

    entries = []

    # tensor odkształceń
    tk.Label(root, text="Tensor odkształceń ε").grid(row=0, column=0, columnspan=3)

    labels = [
    ["εxx", "εxy", "εxz"],
    ["εyx", "εyy", "εyz"],
    ["εzx", "εzy", "εzz"]
    ]

    for i in range(3):
        row = []
        for j in range(3):
            cell = tk.Frame(root)
            cell.grid(row=i + 1, column=j, padx=8, pady=4)

            tk.Label(cell, text=labels[i][j]).pack(side="left")
            e = tk.Entry(cell, width=10, justify="center")
            e.pack(side="left", padx=3)

            e.insert(0, "0")
            row.append(e)

        entries.append(row)

    tk.Label(root, text="Mnożnik tensora").grid(row=4, column=0, sticky="e")
    entry_multiplier = tk.Entry(root, width=20)
    entry_multiplier.grid(row=4, column=1, columnspan=2, pady=3)
    entry_multiplier.insert(0, "1")

    #parametry materiałowe
    tk.Label(root, text="Moduł Younga E [Pa]").grid(row=5, column=0, sticky="e")
    entry_E = tk.Entry(root, width=20)
    entry_E.grid(row=5, column=1, columnspan=2, pady=3)
    entry_E.insert(0, "210e9")

    tk.Label(root, text="Współczynnik Poissona ν").grid(row=6, column=0, sticky="e")
    entry_nu = tk.Entry(root, width=20)
    entry_nu.grid(row=6, column=1, columnspan=2, pady=3)
    entry_nu.insert(0, "0.3")

    # pole wyników
    frame_results = tk.Frame(root)
    frame_results.grid(row=8, column=0, columnspan=3, padx=5, pady=5)

    scrollbar = tk.Scrollbar(frame_results)

    result_box = tk.Text(
        frame_results,
        height=18,
        width=85,
        font=("Consolas", 10),
        yscrollcommand=scrollbar.set,
        wrap="word"
    )

    scrollbar.config(command=result_box.yview)

    result_box.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ramka na wykres
    canvas_frame = tk.Frame(root)
    canvas_frame.grid(row=8, column=0, columnspan=3, padx=5, pady=5)

    # funkcja do zapisywania wykresów
    def save_plot():
        if current_fig is None:
            messagebox.showwarning("Brak wykresu", "Najpierw wykonaj obliczenia.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"),
                    ("PDF files", "*.pdf"),
                    ("All files", "*.*")]
        )

        if file_path:
            current_fig.savefig(file_path)
            messagebox.showinfo("Zapisano", "Wykres zapisany poprawnie.")

    def calculate():
        nonlocal current_fig
        try:
            multiplier = parse_number(entry_multiplier.get())

            epsilon = np.array([
                [parse_number(entries[i][j].get()) * multiplier for j in range(3)]
                for i in range(3)
            ])

            E = parse_number(entry_E.get())
            nu = parse_number(entry_nu.get())

            if not np.allclose(epsilon, epsilon.T):
                proceed = messagebox.askyesno(
                    "Ostrzeżenie",
                    "Tensor nie jest symetryczny!\n\n"
                    "Dla fizycznego tensora odkształceń powinno być:\n"
                    "εxy = εyx, εxz = εzx, εyz = εzy.\n\n"
                    "Program może wykonać obliczenia, ale wynik nie ma poprawnej "
                    "interpretacji fizycznej.\n\n"
                    "Czy chcesz kontynuować?"
                )
                if not proceed:
                    return

            try:
                results = calculate_all(epsilon, E, nu)
            except ValueError as e:
                messagebox.showerror("Błąd danych wejściowych", str(e))
                return

            result_box.delete("1.0", tk.END)

            result_box.insert(tk.END, "WYNIKI OBLICZEŃ:\n")
            result_box.insert(tk.END, f"odkształcenie średnie εm = {format_sci(results['epsilon_m'])}\n")
            result_box.insert(tk.END, f"moduł objętościowy K = {format_sci(results['K'])} Pa\n")
            result_box.insert(tk.END, f"moduł Kirchoffa μ = {format_sci(results['mu'])} Pa\n")
            result_box.insert(tk.END, f"naprężenie średnie σm = {format_sci(results['sigma_m'])} Pa\n\n")

            result_box.insert(tk.END, "Tensor dewiatorowy ε':\n")
            result_box.insert(tk.END, format_matrix(results ["epsilon_dev"]))
            result_box.insert(tk.END, "\n\n")

            result_box.insert(tk.END, f"energia objętościowa Φv = {format_sci(results['phi_v'])} J/m³\n")
            result_box.insert(tk.END, f"energia postaciowa Φs = {format_sci(results['phi_s'])} J/m³\n")
            result_box.insert(tk.END, f"energia całkowita Φ  = {format_sci(results['phi'])} J/m³\n")

            result_box.insert(tk.END, "\nINTERPRETACJA WYNIKÓW:\n")
            result_box.insert(tk.END, interpret_results(results))
            result_box.insert(tk.END, "\n")

            # wykres
            
            current_fig = create_plot(results["K"], results["mu"], epsilon)

            for widget in canvas_frame.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(current_fig, master=canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

            # plt.close(current_fig)

        except Exception as e:
            result_box.delete("1.0", tk.END)
            result_box.insert(tk.END, f"Błąd danych wejściowych: {e}")

    buttons_frame = tk.Frame(root)
    buttons_frame.grid(row=7, column=0, columnspan=3, pady=8)

    tk.Button(buttons_frame, text="Oblicz", width=15, command=calculate).pack(
        side="left", padx=10
    )

    tk.Button(buttons_frame, text="Zapisz wykres", width=15, command=save_plot).pack(
        side="left", padx=10
    )

    frame_results.grid(row=8, column=0, columnspan=3, padx=5, pady=5)
    canvas_frame.grid(row=9, column=0, columnspan=3, padx=5, pady=5)


    root.mainloop()


if __name__ == "__main__":
    run_gui()