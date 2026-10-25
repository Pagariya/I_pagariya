# Universal Robot Control

**A modular C++20 foundation for model-based robot control, built with Pinocchio and Eigen.**

![Robot control architecture](docs/architecture.svg)

> **Status:** Early development / simulation-oriented prototype. The current demo calculates torque commands; it does **not** execute a physical or simulated motion trajectory.

## What's implemented

| Component | Capability |
|---|---|
| **RobotModel** | Load URDF (fixed or floating base); neutral configuration; forward kinematics; end-effector position; frame Jacobian; mass matrix (CRBA); nonlinear effects; inverse dynamics (RNEA); forward dynamics (ABA) |
| **ComputedTorqueController** | Joint-space desired-acceleration feedforward with proportional–derivative feedback, mapped to torques using inverse dynamics |
| **CartesianImpedanceController** | 3D translational virtual spring–damper at `tool0`; Jacobian-transpose torque mapping with gravity compensation |
| **Demo** | Print robot dimensions, joint state, tool position, mass matrix and torque outputs for both controllers |
| **Build and tests** | CMake + Ninja, Pixi-managed dependencies, existing GoogleTest dynamics suite |

## Controller equations

### Joint-space computed torque

For joint configuration `q` and velocity `v`, the commanded acceleration is

```text
a_cmd = a_des + Kp * (q_des - q) + Kd * (v_des - v)
tau   = inverseDynamics(q, v, a_cmd)
```

For the standard rigid-body model, inverse dynamics evaluates

```text
tau = M(q) * a_cmd + h(q, v)
h(q, v) = C(q, v) * v + g(q)
```

### Cartesian impedance (translation only)

```text
x       = framePosition(q, "tool0")
Jv      = top 3 rows of frameJacobian(q, "tool0")
dx      = Jv * v
F_cmd   = Kp * (x_des - x) + Kd * (dx_des - dx)
tau     = Jv.transpose() * F_cmd + g(q)
```

The Jacobian is expressed in Pinocchio's `LOCAL_WORLD_ALIGNED` convention. Stiffness is in N/m, damping in N·s/m, and `F_cmd` is a **virtual commanded force**, not a measured contact force.

The demo uses a 5 mm X-direction setpoint offset and default Cartesian gains of 300 N/m and 30 N·s/m on each axis. This produces a nominal 1.5 N spring term along X before Jacobian mapping. Actual torque values depend on configuration and URDF parameters.

## Project layout

```text
universal-robot-control/
├── CMakeLists.txt
├── pixi.toml
├── include/urc/
│   ├── robot_model.hpp
│   ├── computed_torque.hpp
│   └── cartesian_impedance.hpp
├── src/
│   ├── robot_model.cpp
│   ├── computed_torque.cpp
│   ├── cartesian_impedance.cpp
│   └── main.cpp
├── models/arm6/arm6.urdf
├── tests/test_dynamics.cpp
└── docs/architecture.svg
```

## Build

From the repository root, with Pixi dependencies already installed:

```bash
cmake -S . -B build \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_CXX_FLAGS_DEBUG="-O0 -g0" \
  -DCMAKE_PREFIX_PATH="$PWD/.pixi/envs/default"

cmake --build build --parallel 1
```

The single-job build is useful in memory-constrained Codespaces environments.

## Run the demo

```bash
./build/urc_demo models/arm6/arm6.urdf
```

The current `src/main.cpp` runs **both** controllers sequentially at the same robot configuration. It prints a clearly labeled computed-torque section, Cartesian impedance section, and torque comparison. The joint-space demo tracks the current pose (gravity compensation), while the Cartesian demo requests a small end-effector offset.

To run the existing dynamics tests when desired:

```bash
ctest --test-dir build --output-on-failure
```

## Roadmap

- [x] URDF-based robot model and rigid-body dynamics
- [x] Joint-space computed-torque controller
- [x] Basic translational Cartesian impedance torque computation
- [ ] Closed-loop simulated motion using forward dynamics and numerical integration
- [ ] Gain tuning and trajectory-response plots
- [ ] Torque saturation, joint-limit handling, watchdogs and contact-safety logic
- [ ] 6D Cartesian impedance with orientation control
- [ ] Damped least-squares inverse kinematics and singularity handling
- [ ] MuJoCo-based compliant / fragile assembly scenario
- [ ] Real-time 1 kHz loop and allocation/jitter benchmarking
- [ ] Floating-base, contact-constrained and whole-body control

## Safety and scope

This repository is an educational/research foundation, **not a certified robot controller**. Current Cartesian impedance code assumes a fixed-base torque-actuated arm and does not enforce actuator torque limits, joint limits, contact-force limits or collision avoidance. Do not deploy it to physical hardware without independent validation and appropriate safety systems.
