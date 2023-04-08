from simulation import Simulation
import matplotlib.pyplot as plt

sim = Simulation()
sim.reset_regulator(80)
sim.start()
t, v, x, u, e = sim.get_display_results()

# Plotting output
fig, ax = plt.subplots(2, 2, figsize=(8, 10))
 
# Plot Speed value
ax[0, 0].plot(t, v)
ax[0, 0].axhline(y=40, c="red", linewidth=0.5, linestyle='dashed')
ax[0, 0].set_title('Speed V change in time')
ax[0, 0].set_xlabel('Time [s]')
ax[0, 0].set_ylabel('Speed [m/s]')
ax[0, 0].grid(True)

# Plot Error value
ax[0, 1].plot(t, e)
ax[0, 1].set_title('Error E change in time')
ax[0, 1].set_xlabel('Time [s]')
ax[0, 1].set_ylabel('Error [m/s]')
ax[0, 1].grid(True)
 
# Plot Position value
ax[1, 0].plot(t, x)
ax[1, 0].set_title('Position X change in time')
ax[1, 0].set_xlabel('Time [s]')
ax[1, 0].set_ylabel('Position [m]')
ax[1, 0].grid(True)
 
# Plot Control Signal value
ax[1, 1].plot(t, u)
ax[1, 1].set_title('Control U change in time')
ax[1, 1].set_xlabel('Time [s]')
ax[1, 1].set_ylabel('Voltage [V]')
ax[1, 1].grid(True)
 
plt.tight_layout()
plt.show()
