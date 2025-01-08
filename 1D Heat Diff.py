import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, StringVar, IntVar

# Define the simulation function
def run_simulation(L, T_max, Nx, Nt, alpha, T_left, T_right, T_initial):
    dx = L / (Nx - 1)  # Spatial step size
    dt = T_max / Nt  # Time step size

    # Stability condition (CFL condition)
    if alpha * dt / dx**2 > 0.5:
        print("Warning: Stability condition violated. Consider reducing dt or increasing dx.")

    T = np.copy(T_initial)

    # Plotting function to visualize the temperature distribution at each time step
    def plot_temperature(T, time_step):
        plt.plot(np.linspace(0, L, Nx), T, label=f"t = {time_step * dt:.2f} s")
        plt.xlabel('Position along the rod (m)')
        plt.ylabel('Temperature (°C)')
        plt.title('1D Heat Diffusion')
        plt.legend(loc='upper right')

    # Perform the time-stepping simulation
    for t in range(1, Nt):
        T_new = np.copy(T)

        # Apply the finite difference method for heat diffusion
        for i in range(1, Nx - 1):
            T_new[i] = T[i] + alpha * dt / dx**2 * (T[i - 1] - 2 * T[i] + T[i + 1])

        # Apply boundary conditions (fixed temperature)
        T_new[0] = T_left
        T_new[-1] = T_right

        # Update temperature array
        T = np.copy(T_new)

        # Plot temperature every 100 time steps to visualize the evolution
        if t % 100 == 0:
            plt.clf()  # Clear the previous plot
            plot_temperature(T, t)
            plt.pause(0.01)

    # Display final temperature distribution
    plt.show()

# Define the start menu function
def start_menu():
    # Create a new window for the start menu
    window = Tk()
    window.title("1D Heat Diffusion Simulation")
    
    # Define variables for user input
    L_var = StringVar(value="10.0")  # Length of the rod (m)
    T_max_var = StringVar(value="100.0")  # Total simulation time (s)
    Nx_var = IntVar(value=100)  # Number of spatial points
    Nt_var = IntVar(value=2000)  # Number of time steps
    alpha_var = StringVar(value="0.01")  # Thermal diffusivity (m^2/s)
    
    # Add input fields for parameters
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

    # Default initial condition (a hot middle section of the rod)
    def initial_condition(Nx):
        T_initial = np.zeros(Nx)
        T_initial[Nx // 3:2 * Nx // 3] = 100  # Heating the middle section
        return T_initial

    # Function to start the simulation based on user input
    def start_simulation():
        try:
            L = float(L_var.get())  # Length of rod
            T_max = float(T_max_var.get())  # Total time
            Nx = Nx_var.get()  # Number of spatial points
            Nt = Nt_var.get()  # Number of time steps
            alpha = float(alpha_var.get())  # Thermal diffusivity

            T_left = 0.0  # Temperature at left end (0°C)
            T_right = 0.0 # Temperature at right end (0°C)
            
            # Initial temperature distribution
            T_initial = initial_condition(Nx)
            
            # Run the simulation
            window.quit()  # Close the start menu
            run_simulation(L, T_max, Nx, Nt, alpha, T_left, T_right, T_initial)

        except ValueError:
            print("Please enter valid numeric values for all fields.")

    # Button to start the simulation
    Button(window, text="Start Simulation", command=start_simulation).grid(row=5, column=0, columnspan=2)

    # Start the Tkinter main loop
    window.mainloop()

# Run the start menu
start_menu()
