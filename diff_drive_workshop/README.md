# 🤖 Differential Drive Robot — URDF Workshop
### ROS 2 Humble · Gazebo Ignition Fortress

---

## Workshop Overview

In this workshop you will build a complete URDF (Unified Robot Description Format) model of a differential drive robot **from scratch**, piece by piece.  By the end you will have a robot you can visualise in **RViz2** and drive around in **Gazebo**.

```
diff_drive_workshop/
├── urdf/
│   ├── 01_chassis.urdf.xml              ← Part 1 — chassis only
│   ├── 02_wheels.urdf.xml               ← Part 2 — wheels (study only)
│   ├── 03_caster.urdf.xml               ← Part 3 — caster (study only)
│   ├── 04_robot_assembly.urdf.xml       ← Part 4 — YOUR WORKING FILE ★
│   └── 05_robot_assembly_SOLUTION.urdf.xml  ← Instructor reference
├── launch/
│   ├── workshop_rviz.launch.py          ← Visualise in RViz2
│   └── gazebo.launch.py                 ← Run in Gazebo
└── rviz/
    └── robot_view.rviz                  ← Pre-configured RViz2 layout
```

---

## Prerequisites

```bash
sudo apt install -y \
  ros-humble-robot-state-publisher \
  ros-humble-joint-state-publisher-gui \
  ros-humble-rviz2 \
  ros-humble-xacro \
  ros-ign-bridge \
  ros-ign-gazebo
```

---

## Step-by-Step Workshop Guide

### ① Visualise the chassis alone

Open `urdf/01_chassis.urdf.xml` and read through it.  Then visualise it:

```bash
# Terminal 1
ros2 run robot_state_publisher robot_state_publisher \
  --ros-args -p robot_description:="$(cat urdf/01_chassis.urdf.xml)"

# Terminal 2
ros2 run joint_state_publisher_gui joint_state_publisher_gui

# Terminal 3
rviz2 -d rviz/robot_view.rviz
```

> **Check:** You should see a grey box.  In the TF panel, confirm
> `base_footprint → base_link` is shown.

---

### ② Study the wheel and caster files

Read `02_wheels.urdf.xml` and `03_caster.urdf.xml`.  Pay attention to:
- How cylinders are rotated to align with the wheel axis
- Why drive wheels use `continuous` joints
- Why the caster uses `fixed` joints

---

### ③ Complete the assembly file

Open `urdf/04_robot_assembly.urdf.xml`.  You will find **4 placeholders** marked with `### PASTE ... HERE ###`.

#### Placeholder 1 — Left wheel joint

```xml
<joint name="left_wheel_joint" type="continuous">
  <parent link="base_link"/>
  <child  link="left_wheel_link"/>
  <origin xyz="0.0 0.1125 -0.025" rpy="0.0 0.0 0.0"/>
  <axis xyz="0.0 1.0 0.0"/>
  <dynamics damping="0.1" friction="0.1"/>
</joint>
```

#### Placeholder 2 — Right wheel joint

Same as the left wheel joint but with `y = -0.1125`:

```xml
<joint name="right_wheel_joint" type="continuous">
  <parent link="base_link"/>
  <child  link="right_wheel_link"/>
  <origin xyz="0.0 -0.1125 -0.025" rpy="0.0 0.0 0.0"/>
  <axis xyz="0.0 1.0 0.0"/>
  <dynamics damping="0.1" friction="0.1"/>
</joint>
```

#### Placeholder 3 — Caster friction (Gazebo)

```xml
<gazebo reference="caster_wheel_link">
  <mu1>0.0</mu1>
  <mu2>0.0</mu2>
  <kp>1000000.0</kp>
  <kd>100.0</kd>
  <minDepth>0.001</minDepth>
</gazebo>
```

#### Placeholder 4 — Differential drive plugin

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

---

### ④ Validate your URDF

```bash
# Check syntax
check_urdf urdf/04_robot_assembly.urdf.xml

# Visualise the TF tree as a PDF
urdf_to_graphviz urdf/04_robot_assembly.urdf.xml
evince diff_drive_robot.pdf
```

Expected output from `check_urdf`:
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

---

### ⑤ Visualise the complete robot in RViz2

```bash
ros2 launch launch/workshop_rviz.launch.py
```

Use the **Joint State Publisher GUI** sliders to spin the wheels and confirm
the joints are working correctly.

---

### ⑥ Spawn in Gazebo and drive it!

```bash
ros2 launch launch/gazebo.launch.py
```

Drive forward:
```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.2}}" --once
```

Turn in place:
```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{angular: {z: 0.8}}" --once
```

Stop:
```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{}" --once
```

---

## Robot Dimensions Reference

| Parameter | Value |
|-----------|-------|
| Chassis (L × W × H) | 0.30 × 0.20 × 0.05 m |
| Chassis mass | 2.0 kg |
| Wheel radius | 0.05 m |
| Wheel width | 0.025 m |
| Wheel mass | 0.3 kg |
| Wheel separation (centre-to-centre) | 0.225 m |
| Caster sphere radius | 0.02 m |
| Robot ground clearance | 0.0 m (wheels touch ground) |
| Chassis height above ground | 0.075 m |

---

## Discussion Questions

1. Why does the `base_footprint` link have no geometry?
2. What is the difference between `fixed`, `continuous`, and `revolute` joint types?
3. If you increase the wheel separation, how does it affect turning radius?
4. Why is the caster sphere friction set to zero in Gazebo?
5. What does the `wheel_separation` parameter in the diff_drive plugin correspond to on the physical robot?

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Multiple roots found` | A joint's parent/child link name has a typo | Check all joint `<parent>` and `<child>` link names |
| Robot floating above ground in Gazebo | Wheel radius / chassis z-offset mismatch | Recalculate `base_footprint_joint` z-offset |
| Wheels spin but robot doesn't move | Caster mu1/mu2 too high | Set caster mu1 and mu2 to 0.0 |
| `check_urdf: file not found` | Wrong working directory | Run from the `diff_drive_workshop/` folder |

---

*Happy building! 🚗*
