# Simple BLDC Speed Control + PREEMPT_RT

A teaching simulation: speed ramp, PI controller, simplified motor response, and Linux periodic scheduling. **Not FOC**, not phase commutation, and not suitable for controlling a physical BLDC motor. Motor simulation uses a fixed step and does not incorporate scheduling jitter into physics.

## Ubuntu setup

```bash
sudo apt update
sudo apt install -y build-essential cmake python3-matplotlib
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
./build/simple_bldc --seconds 8 --hz 1000
mv telemetry.csv normal.csv
sudo ./build/simple_bldc --fifo --seconds 8 --hz 1000
python3 plot.py
```

Verify the running kernel with `uname -r` and `cat /sys/kernel/realtime` (1 indicates active RT kernel when exposed). For a fair comparison, save the output from each run, and compare the same scheduler on generic vs RT kernels. `--fifo` needs appropriate permissions. Logging is buffered in memory and written after the loop. No memory locking or CPU pinning in this introductory version. Running in VirtualBox cannot establish hard-real-time guarantees.
