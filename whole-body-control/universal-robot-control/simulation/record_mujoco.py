
import os
os.environ["MUJOCO_GL"] = "osmesa"

from pathlib import Path

import imageio.v2 as imageio
import mujoco
import numpy as np


URDF = Path("models/arm6/arm6.urdf")
OUTPUT = Path("simulation/output/arm6_simulation.mp4")

FPS = 30
DURATION = 10.0
DT = 0.002

if not URDF.exists():
    raise FileNotFoundError(f"Cannot find {URDF}")

model = mujoco.MjModel.from_xml_path(str(URDF))
model.opt.timestep = DT
data = mujoco.MjData(model)

if model.nq != 6 or model.nv != 6:
    raise RuntimeError(
        f"Expected fixed-base 6-DOF arm, got nq={model.nq}, nv={model.nv}"
    )

print("Robot loaded:", model.nbody, "bodies")

# The URDF must contain valid link visual geometry.
# Otherwise MuJoCo may render only a sparse scene.
mujoco.mj_forward(model, data)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

renderer = mujoco.Renderer(model, height=480, width=640)

camera = mujoco.MjvCamera()
camera.type = mujoco.mjtCamera.mjCAMERA_FREE
camera.lookat[:] = [0.0, 0.0, 0.35]
camera.distance = 2.0
camera.azimuth = 135
camera.elevation = -20

kp = 40.0
kd = 8.0

with imageio.get_writer(
    str(OUTPUT),
    fps=FPS,
    codec="libx264",
    quality=8,
) as writer:

    total_frames = int(DURATION * FPS)
    steps_per_frame = int(round(1.0 / (FPS * DT)))

    for frame in range(total_frames):
        for _ in range(steps_per_frame):
            t = data.time

            q_des = 0.3 * np.sin(
                0.7 * t + np.arange(6) * 0.3
            )
            dq_des = 0.21 * np.cos(
                0.7 * t + np.arange(6) * 0.3
            )

            mujoco.mj_forward(model, data)

            # Simple PD + bias-force compensation.
            tau = (
                kp * (q_des - data.qpos)
                + kd * (dq_des - data.qvel)
                + data.qfrc_bias
            )

            # Direct generalized-force control.
            data.qfrc_applied[:] = tau
            mujoco.mj_step(model, data)

        renderer.update_scene(data, camera=camera)
        frame_rgb = renderer.render()
        writer.append_data(frame_rgb)

        if frame % 30 == 0:
            print(f"Recorded {frame}/{total_frames} frames")

renderer.close()

print(f"\nVideo saved to: {OUTPUT.resolve()}")
