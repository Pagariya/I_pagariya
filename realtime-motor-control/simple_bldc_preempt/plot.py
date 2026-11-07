import csv
import matplotlib.pyplot as plt
with open('telemetry.csv', newline='') as f:
    rows=list(csv.DictReader(f))
def col(name): return [float(r[name]) for r in rows]
t=col('time_s')
plt.figure();plt.plot(t,col('target_rad_s'),label='Target');plt.plot(t,col('ramped_rad_s'),label='Ramp');plt.plot(t,col('speed_rad_s'),label='Motor');plt.xlabel('Time (s)');plt.ylabel('Speed (rad/s)');plt.legend();plt.tight_layout();plt.savefig('speed.png')
plt.figure();plt.plot(t,col('wakeup_lateness_us'),label='Wake-up lateness');plt.plot(t,col('period_jitter_us'),label='Period jitter',alpha=.7);plt.xlabel('Time (s)');plt.ylabel('Microseconds');plt.legend();plt.tight_layout();plt.savefig('timing.png')
print('Saved speed.png and timing.png')
