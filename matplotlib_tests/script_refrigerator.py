from simulation import Simulation
import matplotlib.pyplot as plt

sim = Simulation()
sim.reset(25)
sim.reset_controller(15,25,1.0,1.0,1.0)
sim.start()
t, temp, work, signal, e = sim.get_display_results()

# Plotting output
fig, ax = plt.subplots(2, 2, figsize=(8, 10))
 


# Plot Position value
ax[0, 0].plot(t, signal)
ax[0, 0].set_title('Signal change in time')
ax[0, 0].set_xlabel('Time [s]')
ax[0, 0].set_ylabel('Signal')
ax[0, 0].grid(True)



# Plot Error value
ax[0, 1].plot(t, e)
ax[0, 1].set_title('Error E change in time')
ax[0, 1].set_xlabel('Time [s]')
ax[0, 1].set_ylabel('Error [m/s]')
ax[0, 1].grid(True)
 
# Plot Speed value
ax[1, 0].plot(t, work)
ax[1, 0].set_title('Heat loss change in time')
ax[1, 0].set_xlabel('Time [s]')
ax[1, 0].set_ylabel('Heat loss [J]')
ax[1, 0].grid(True)
 
# Plot Control Signal value
ax[1, 1].plot(t, temp)
ax[1, 1].set_title('Temperature change in time')
ax[1, 1].set_xlabel('Time [s]')
ax[1, 1].set_ylabel('Temperature [C]')
ax[1, 1].grid(True)
 
plt.tight_layout()
plt.show()
