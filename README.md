# motion_tracking
TWIST2 with BeyondMimic lowlevel
Motion retargeting from [GMR](https://github.com/YanjieZe/GMR)
Teleoperation from [TWIST2](https://github.com/amazon-far/TWIST2)
Training strategy from [TWIST2](https://github.com/amazon-far/TWIST2) and [BeyondMimic](https://github.com/HybridRobotics/whole_body_tracking)
## Teleop
### sim
1. 将VR和PC连接到同个局域网下，启动VR端服务，选择到可以进行全身控制标定
2. 启动电脑XRoboToolkit
3. 启动xrobot.sh
4. 启动to_sim.sh
### real
1. 本地配置sdk
2. 网线连接机器人，机器人进调试模式
3. 启动xrobot.sh
4. 启动to_real.sh