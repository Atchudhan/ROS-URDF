# ✅ Workshop Verification Cheat Sheet

```bash
cd ~/Desktop/diff_drive_workshop
source /opt/ros/humble/setup.bash
```

---

## Step 1 — Chassis in RViz2

```bash
ros2 launch launch/workshop_rviz.launch.py urdf:=urdf/01_chassis.urdf.xml
```
👁 Grey box visible. TF shows `base_footprint → base_link`. Close terminals.

---

## Step 2 — Study Files (no terminal)

Read `urdf/02_wheels.urdf.xml` and `urdf/03_caster.urdf.xml`.

---

## Step 3 — Fill Placeholders in `urdf/04_robot_assembly.urdf.xml`

**Placeholder 1** — Left wheel joint
```xml
<joint name="left_wheel_joint" type="continuous">
  <parent link="base_link"/>
  <child  link="left_wheel_link"/>
  <origin xyz="0.0 0.1125 -0.025" rpy="0.0 0.0 0.0"/>
  <axis xyz="0.0 1.0 0.0"/>
  <dynamics damping="0.1" friction="0.1"/>
</joint>
```

**Placeholder 2** — Right wheel joint
```xml
<joint name="right_wheel_joint" type="continuous">
  <parent link="base_link"/>
  <child  link="right_wheel_link"/>
  <origin xyz="0.0 -0.1125 -0.025" rpy="0.0 0.0 0.0"/>
  <axis xyz="0.0 1.0 0.0"/>
  <dynamics damping="0.1" friction="0.1"/>
</joint>
```

**Placeholder 3** — Caster friction
```xml
<gazebo reference="caster_wheel_link">
  <mu1>0.0</mu1>
  <mu2>0.0</mu2>
  <kp>1000000.0</kp>
  <kd>100.0</kd>
  <minDepth>0.001</minDepth>
</gazebo>
```

**Placeholder 4** — Diff drive plugin
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

## Step 4 — Validate URDF

```bash
check_urdf urdf/04_robot_assembly.urdf.xml
```
✅ Expected:
```
root Link: base_footprint has 1 child(ren)
    child(1):  base_link
        child(1):  caster_bracket_link
            child(1):  caster_wheel_link
        child(2):  left_wheel_link
        child(3):  right_wheel_link
```
❌ `Two root links found` → a wheel joint has a typo in `<parent>` or `<child>`.

---

## Step 5 — Full Robot in RViz2

```bash
ros2 launch launch/workshop_rviz.launch.py urdf:=urdf/04_robot_assembly.urdf.xml
```
👁 Full robot with wheels + caster. Spin sliders to verify joints rotate. Close terminals.

---

## Step 6 — Gazebo + Drive

**Terminal 1:**
```bash
ros2 launch launch/gazebo.launch.py
```
Wait for Gazebo + robot to load.

**Terminal 2:**
```bash
source /opt/ros/humble/setup.bash
# Forward
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.2}}" --once
# Turn
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{angular: {z: 0.8}}" --once
# Stop
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{}" --once
```
👁 Robot moves in Gazebo. ✅ Workshop complete.

---

## ⚠️ Common Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `Unable to parse robot_description as yaml` | `ParameterValue` missing in launch file | Already fixed in provided launch files |
| `No transform from [left_wheel_link] to [base_link]` | Wheel joints not pasted, or URDF is invalid XML | Run `check_urdf`; look for `--` (double-dash) inside XML comments |
| Wheels appear at chassis center | Same — RSP rejected the URDF silently | Fix URDF, relaunch |
| JSPGUI shows no sliders | Same — no joints parsed | Fix URDF, relaunch |
| `Two root links found` in check_urdf | Typo in `<parent>` or `<child>` link name | Check spelling matches exactly |
