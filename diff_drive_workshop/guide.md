# 🤖 Differential Drive Robot — Hands-On Workshop Guide

> **Setup:** Open a terminal and `cd` into the workshop folder before every step.
> ```bash
> cd ~/Desktop/diff_drive_workshop
> source /opt/ros/humble/setup.bash
> ```

---

## Part 1 — Visualise the Chassis

Open `urdf/01_chassis.urdf.xml` and read through it. Notice:
- `base_footprint` is a virtual link at ground level (no geometry)
- `base_link` is the chassis box: 0.30 × 0.20 × 0.05 m
- The chassis centre sits **0.075 m** above the ground (wheel radius 0.05 + half chassis height 0.025)

Launch the visualiser:

```bash
ros2 launch launch/workshop_rviz.launch.py urdf:=urdf/01_chassis.urdf.xml
```

✅ **Check:** You should see a grey box. In the TF panel confirm `base_footprint → base_link`.

Close all terminals before the next part.

---

## Part 2 — Study the Wheel and Caster Files

Open and read `urdf/02_wheels.urdf.xml` and `urdf/03_caster.urdf.xml`. Focus on:

| File | Key concept |
|------|------------|
| `02_wheels.urdf.xml` | Cylinders rotated 90° around X to align with the Y-axis wheel axis. `continuous` joint has no rotation limits. |
| `03_caster.urdf.xml` | Two-part caster (bracket + sphere). `fixed` joints because friction is zeroed in Gazebo — the physics engine handles sliding. |

No terminal commands needed here.

---

## Part 3 — Complete the Assembly File

Open `urdf/04_robot_assembly.urdf.xml`. Find the four `<!-- PASTE ... HERE -->` markers and fill each one in order.

---

### Placeholder 1 — Left wheel joint

Find: `<!-- PASTE YOUR LEFT WHEEL JOINT HERE -->`

Replace it with:

```xml
<joint name="left_wheel_joint" type="continuous">
  <parent link="base_link"/>
  <child  link="left_wheel_link"/>
  <origin xyz="0.0 0.1125 -0.025" rpy="0.0 0.0 0.0"/>
  <axis xyz="0.0 1.0 0.0"/>
  <dynamics damping="0.1" friction="0.1"/>
</joint>
```

> **Why `y = +0.1125`?** Half chassis width (0.10) + half wheel thickness (0.0125) = 0.1125 m.
> **Why `z = -0.025`?** Wheel centre is at ground + 0.05 m; chassis centre is at ground + 0.075 m → offset = −0.025 m.

---

### Placeholder 2 — Right wheel joint

Find: `<!-- PASTE YOUR RIGHT WHEEL JOINT HERE -->`

Same as the left joint but with `y = -0.1125`:

```xml
<joint name="right_wheel_joint" type="continuous">
  <parent link="base_link"/>
  <child  link="right_wheel_link"/>
  <origin xyz="0.0 -0.1125 -0.025" rpy="0.0 0.0 0.0"/>
  <axis xyz="0.0 1.0 0.0"/>
  <dynamics damping="0.1" friction="0.1"/>
</joint>
```

---

### Placeholder 3 — Caster friction (Gazebo)

Find: `<!-- ### PASTE CASTER FRICTION BLOCK HERE ### -->`

Replace it with:

```xml
<gazebo reference="caster_wheel_link">
  <mu1>0.0</mu1>
  <mu2>0.0</mu2>
  <kp>1000000.0</kp>
  <kd>100.0</kd>
  <minDepth>0.001</minDepth>
</gazebo>
```

> `mu1` / `mu2` are friction coefficients. Setting them to **0.0** lets the caster slide freely so it doesn't resist turning.

---

### Placeholder 4 — Differential drive plugin

Find: `<!-- ### PASTE DIFF DRIVE PLUGIN HERE ### -->`

Replace it with:

```xml
<gazebo>
  <plugin
      filename="ignition-gazebo-diff-drive-system"
      name="ignition::gazebo::systems::DiffDrive">
    <left_joint>left_wheel_joint</left_joint>
    <right_joint>right_wheel_joint</right_joint>
    <wheel_separation>0.225</wheel_separation>
    <wheel_radius>0.05</wheel_radius>
    <topic>/cmd_vel</topic>
    <odom_topic>/odom</odom_topic>
    <frame_id>odom</frame_id>
    <child_frame_id>base_footprint</child_frame_id>
    <odom_publish_frequency>50</odom_publish_frequency>
  </plugin>
</gazebo>
```

> `wheel_separation` = 2 × 0.1125 = **0.225 m** (centre-to-centre distance between wheels).
> `wheel_radius` = **0.05 m**.

---

## Part 4 — Validate Your URDF

```bash
check_urdf urdf/04_robot_assembly.urdf.xml
```

Expected output:
```
robot name is: diff_drive_robot
---------- Successfully Parsed XML ---------------
root Link: base_footprint has 1 child(ren)
    child(1):  base_link
        child(1):  caster_bracket_link
            child(1):  caster_wheel_link
        child(2):  left_wheel_link
        child(3):  right_wheel_link
```

If you see `Two root links found` or `Multiple roots found`, a joint's `<parent>` or `<child>` link name has a typo — check your wheel joint names carefully.

---

## Part 5 — Visualise the Complete Robot in RViz2

```bash
ros2 launch launch/workshop_rviz.launch.py
```

Use the **Joint State Publisher GUI** sliders to spin the wheels and confirm the joints are working. Close all terminals when done.

---

## Part 6 — Spawn in Gazebo and Drive!

```bash
ros2 launch launch/gazebo.launch.py
```

Wait for Gazebo to fully open and the robot to appear. Then in a **new terminal**:

```bash
source /opt/ros/humble/setup.bash
cd ~/Desktop/diff_drive_workshop
```

Drive forward:
```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.2}}" --once
```

Turn in place:
```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{angular: {z: 0.8}}" --once
```

Stop:
```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{}" --once
```

✅ **You're done!** You've built a complete differential drive robot URDF from scratch and driven it in simulation.

---

## Discussion Questions

1. Why does `base_footprint` have no geometry?
2. What is the difference between `fixed`, `continuous`, and `revolute` joint types?
3. If you increase the wheel separation, how does it affect turning radius?
4. Why is the caster sphere friction set to zero in Gazebo?
5. What does the `wheel_separation` parameter in the diff_drive plugin correspond to on the physical robot?
