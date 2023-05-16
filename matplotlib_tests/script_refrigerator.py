from ..simulation import Simulation
import matplotlib.pyplot as plt

sim = Simulation()
sim.reset_controller(10, 1, 1, 1)
sim.start()
t, temp, heat, work, e = sim.get_display_results()

# Plotting output
fig, ax = plt.subplots(2, 2, figsize=(8, 10))
 
# Plot Speed value
ax[0, 0].plot(t, work)
ax[0, 0].axhline(y=40, c="red", linewidth=0.5, linestyle='dashed')
ax[0, 0].set_title('Work change in time')
ax[0, 0].set_xlabel('Time [s]')
ax[0, 0].set_ylabel('Work [J]')
ax[0, 0].grid(True)



# Plot Error value
ax[0, 1].plot(t, e)
ax[0, 1].set_title('Error E change in time')
ax[0, 1].set_xlabel('Time [s]')
ax[0, 1].set_ylabel('Error [m/s]')
ax[0, 1].grid(True)
 
# Plot Position value
ax[1, 0].plot(t, heat)
ax[1, 0].set_title('Heat transfer change in time')
ax[1, 0].set_xlabel('Time [s]')
ax[1, 0].set_ylabel('Heat [J/kg/C]')
ax[1, 0].grid(True)
 
# Plot Control Signal value
ax[1, 1].plot(t, temp)
ax[1, 1].set_title('Temperature change in time')
ax[1, 1].set_xlabel('Time [s]')
ax[1, 1].set_ylabel('Temperature [C]')
ax[1, 1].grid(True)
 
plt.tight_layout()
plt.show()
