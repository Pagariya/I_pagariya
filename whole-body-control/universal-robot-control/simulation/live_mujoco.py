
import os
import time
from pathlib import Path

import mujoco
import meshcat
import meshcat.geometry as g
import numpy as np
import meshcat.servers.zmqserver as zmqserver



# --------------------------------------------------
# Configuration
# --------------------------------------------------

URDF_PATH = Path("models/arm6/arm6.urdf")

SIM_DT = 0.002       # MuJoCo physics: 500 Hz
VIS_DT = 0.033       # Browser visualization: ~30 FPS

KP = 40.0
KD = 8.0


# --------------------------------------------------
# Load MuJoCo model
# --------------------------------------------------

if not URDF_PATH.exists():
    raise FileNotFoundError(
        f"Robot model not found: {URDF_PATH}"
    )

model = mujoco.MjModel.from_xml_path(str(URDF_PATH))
data = mujoco.MjData(model)

print("Robot loaded")
print("nq:", model.nq)
print("nv:", model.nv)
print("nu:", model.nu)

if model.nq != 6 or model.nv != 6:
    raise RuntimeError(
        "This demo expects a fixed-base 6-DOF robot."
    )

# --------------------------------------------------
# Start MeshCat
# --------------------------------------------------

vis = meshcat.Visualizer()
# print("Open MeshCat at:", vis.url())

print("MeshCat URL:", vis.url())

# --------------------------------------------------
# Build visualization from MuJoCo bodies
# --------------------------------------------------

body_nodes = {}

for body_id in range(1, model.nbody):
    body_name = mujoco.mj_id2name(
        model,
        mujoco.mjtObj.mjOBJ_BODY,
        body_id
    )

    node = vis[f"robot/{body_name}"]

    # Simple visual marker for each body.
    # Replace with actual URDF meshes later.
    node.set_object(
        g.Box([0.08, 0.08, 0.08])
    )

    body_nodes[body_id] = node


def update_visualization():
    for body_id, node in body_nodes.items():
        transform = np.eye(4)

        transform[:3, :3] = data.xmat[
            body_id
        ].reshape(3, 3)

        transform[:3, 3] = data.xpos[body_id]

        node.set_transform(transform)


# --------------------------------------------------
# Controller
# --------------------------------------------------

def compute_torque(t):
    q = data.qpos.copy()
    dq = data.qvel.copy()

    phase = np.arange(6) * 0.3

    q_des = 0.35 * np.sin(
        0.7 * t + phase
    )

    dq_des = 0.35 * 0.7 * np.cos(
        0.7 * t + phase
    )

    # PD feedback
    tau_pd = (
        KP * (q_des - q)
        + KD * (dq_des - dq)
    )

    # MuJoCo gravity compensation
    mujoco.mj_forward(model, data)
    tau_gravity = data.qfrc_bias.copy()

    return tau_pd + tau_gravity


# --------------------------------------------------
# Simulation loop
# --------------------------------------------------

mujoco.mj_forward(model, data)
update_visualization()

print("Simulation started.")

last_visualization = time.monotonic()

while True:
    start = time.monotonic()

    t = data.time

    tau = compute_torque(t)

    # Apply generalized torques directly.
    # This assumes 6 independent hinge joints.
    data.qfrc_applied[:6] = tau

    mujoco.mj_step(model, data)

    now = time.monotonic()

    if now - last_visualization >= VIS_DT:
        update_visualization()
        last_visualization = now

    elapsed = time.monotonic() - start

    time.sleep(max(0.0, SIM_DT - elapsed))
