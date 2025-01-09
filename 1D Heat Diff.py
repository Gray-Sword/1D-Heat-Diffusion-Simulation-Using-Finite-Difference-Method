import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, StringVar, IntVar

def run_simulation(L, T_max, Nx, Nt, alpha, T_left, T_right, T_initial):
    dx = L / (Nx - 1)
    dt = T_max / Nt

    if alpha * dt / dx**2 > 0.5:
        print("Warning: Stability condition violated. Consider reducing dt or increasing dx.")

    T = np.copy(T_initial)

    def plot_temperature(T, time_step):
        plt.plot(np.linspace(0, L, Nx), T, label=f"t = {time_step * dt:.2f} s")
        plt.xlabel('Position along the rod (m)')
        plt.ylabel('Temperature (°C)')
        plt.title('1D Heat Diffusion')
        plt.legend(loc='upper right')

    for t in range(1, Nt):
        T_new = np.copy(T)
        for i in range(1, Nx - 1):
            T_new[i] = T[i] + alpha * dt / dx**2 * (T[i - 1] - 2 * T[i] + T[i + 1])
        T_new[0] = T_left
        T_new[-1] = T_right
        T = np.copy(T_new)
        if t % 100 == 0:
            plt.clf()
            plot_temperature(T, t)
            plt.pause(0.01)
    plt.show()

def start_menu():
    window = Tk()
    window.title("1D Heat Diffusion Simulation")
    
    L_var = StringVar(value="10.0")
    T_max_var = StringVar(value="100.0")
    Nx_var = IntVar(value=100)
    Nt_var = IntVar(value=2000)
    alpha_var = StringVar(value="0.01")
    
    Label(window, text="Length of rod (L):").grid(row=0, column=0)
    Entry(window, textvariable=L_var).grid(row=0, column=1)
    Label(window, text="Total simulation time (T_max):").grid(row=1, column=0)
    Entry(window, textvariable=T_max_var).grid(row=1, column=1)
    Label(window, text="Number of spatial points (Nx):").grid(row=2, column=0)
    Entry(window, textvariable=Nx_var).grid(row=2, column=1)
    Label(window, text="Number of time steps (Nt):").grid(row=3, column=0)
    Entry(window, textvariable=Nt_var).grid(row=3, column=1)
    Label(window, text="Thermal diffusivity (alpha):").grid(row=4, column=0)
    Entry(window, textvariable=alpha_var).grid(row=4, column=1)

    def initial_condition(Nx):
        T_initial = np.zeros(Nx)
        T_initial[Nx // 3:2 * Nx // 3] = 100
        return T_initial

    def start_simulation():
        try:
            L = float(L_var.get())
            T_max = float(T_max_var.get())
            Nx = Nx_var.get()
            Nt = Nt_var.get()
            alpha = float(alpha_var.get())
            T_left = 0.0
            T_right = 0.0
            T_initial = initial_condition(Nx)
            window.quit()
            run_simulation(L, T_max, Nx, Nt, alpha, T_left, T_right, T_initial)
        except ValueError:
            print("Please enter valid numeric values for all fields.")

    Button(window, text="Start Simulation", command=start_simulation).grid(row=5, column=0, columnspan=2)
    window.mainloop()

start_menu()
