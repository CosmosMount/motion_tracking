import pickle
import numpy as np
import sys
import os

def fix_motion_pkl(input_path, output_path=None):
    """
    修复motion PKL文件，填充缺失的 local_body_pos 和 link_body_list
    """
    
    if not os.path.exists(input_path):
        print(f"错误: 文件不存在 {input_path}")
        return
    
    # 如果没有指定输出路径，使用 _fixed 后缀
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_fixed{ext}"
    
    print(f"读取文件: {input_path}")
    
    with open(input_path, 'rb') as f:
        data = pickle.load(f)
    
    if not isinstance(data, dict):
        print("错误: PKL文件不是字典格式")
        return
    
    # 检查必需的键
    required_keys = ['fps', 'root_pos', 'root_rot', 'dof_pos']
    missing_keys = [k for k in required_keys if k not in data]
    if missing_keys:
        print(f"错误: 缺少必需的键: {missing_keys}")
        return
    
    print("\n原始数据:")
    print(f"  fps: {data['fps']}")
    print(f"  帧数: {data['root_pos'].shape[0]}")
    print(f"  DOF数量: {data['dof_pos'].shape[1]}")
    print(f"  local_body_pos: {data.get('local_body_pos', 'missing')}")
    print(f"  link_body_list: {data.get('link_body_list', 'missing')}")
    
    # 获取帧数
    num_frames = data['root_pos'].shape[0]
    
    # 修复 local_body_pos
    if 'local_body_pos' not in data or data['local_body_pos'].size == 0:
        print("\n⚠️  local_body_pos 为空，将从 root_pos 创建...")
        # 使用 root_pos 作为 local_body_pos 的基础
        # 对于 G1 机器人，通常需要包含关键身体部位的位置
        # 这里我们创建一个简单的版本，只包含根位置
        data['local_body_pos'] = data['root_pos'].copy()
        print(f"✓ 创建 local_body_pos: shape={data['local_body_pos'].shape}")
    
    # 修复 link_body_list  
    if 'link_body_list' not in data or len(data['link_body_list']) == 0:
        print("\n⚠️  link_body_list 为空，将创建默认列表...")
        # 对于 G1 机器人的标准身体链接
        # 这是一个基本的身体层次结构
        data['link_body_list'] = ['pelvis']  # 至少包含根链接
        print(f"✓ 创建 link_body_list: {data['link_body_list']}")
    
    # 保存修复后的文件
    print(f"\n保存到: {output_path}")
    with open(output_path, 'wb') as f:
        pickle.dump(data, f)
    
    print("\n✓ 修复完成!")
    print(f"\n测试命令:")
    print(f"  python view_pkl.py {output_path}")
    print(f"\n或者更新 run_motion_server.sh 中的路径:")
    print(f'  motion_file="${{script_dir}}/assets/example_motions/{os.path.basename(output_path)}"')


def create_full_motion_data(input_path, output_path=None):
    """
    创建完整的motion数据，包括所有必需字段
    使用G1机器人的标准配置
    """
    
    if not os.path.exists(input_path):
        print(f"错误: 文件不存在 {input_path}")
        return
    
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_full{ext}"
    
    print(f"读取文件: {input_path}")
    
    with open(input_path, 'rb') as f:
        data = pickle.load(f)
    
    num_frames = data['root_pos'].shape[0]
    num_dofs = data['dof_pos'].shape[1]
    
    # G1机器人的关键身体链接
    g1_body_links = [
        'pelvis',           # 0: 骨盆（根）
        'torso_link',       # 1: 躯干
        'left_hip_pitch_link',   # 2: 左髋
        'left_knee_link',        # 3: 左膝
        'left_ankle_pitch_link', # 4: 左踝
        'right_hip_pitch_link',  # 5: 右髋
        'right_knee_link',       # 6: 右膝
        'right_ankle_pitch_link',# 7: 右踝
        'left_shoulder_pitch_link',  # 8: 左肩
        'left_elbow_link',           # 9: 左肘
        'right_shoulder_pitch_link', # 10: 右肩
        'right_elbow_link',          # 11: 右肘
    ]
    
    # 创建 local_body_pos (相对于根的局部位置)
    # 形状: (num_frames, num_bodies, 3)
    num_bodies = len(g1_body_links)
    local_body_pos = np.zeros((num_frames, num_bodies, 3))
    
    # 第一个身体（骨盆）始终在原点
    local_body_pos[:, 0, :] = 0.0
    
    # 为其他身体设置近似的相对位置
    # 这些是G1机器人的近似身体位置
    body_offsets = {
        1: [0.0, 0.0, 0.3],      # 躯干在骨盆上方
        2: [0.0, 0.1, -0.1],     # 左髋
        3: [0.0, 0.1, -0.4],     # 左膝
        4: [0.0, 0.1, -0.75],    # 左踝
        5: [0.0, -0.1, -0.1],    # 右髋
        6: [0.0, -0.1, -0.4],    # 右膝
        7: [0.0, -0.1, -0.75],   # 右踝
        8: [0.0, 0.2, 0.5],      # 左肩
        9: [0.0, 0.2, 0.25],     # 左肘
        10: [0.0, -0.2, 0.5],    # 右肩
        11: [0.0, -0.2, 0.25],   # 右肘
    }
    
    for body_idx, offset in body_offsets.items():
        local_body_pos[:, body_idx, :] = offset
    
    data['local_body_pos'] = local_body_pos
    data['link_body_list'] = g1_body_links
    
    print("\n创建的数据:")
    print(f"  local_body_pos shape: {local_body_pos.shape}")
    print(f"  link_body_list: {len(g1_body_links)} 个身体部位")
    print(f"  身体部位: {g1_body_links}")
    
    # 保存
    print(f"\n保存到: {output_path}")
    with open(output_path, 'wb') as f:
        pickle.dump(data, f)
    
    print("\n✓ 创建完成!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  简单修复: python fix_pkl.py <input.pkl> [output.pkl]")
        print("  完整创建: python fix_pkl.py <input.pkl> --full [output.pkl]")
        print("\n示例:")
        print("  python fix_pkl.py TWIST2/assets/example_motions/xrobot_retargeting_20260209_194533.pkl")
        print("  python fix_pkl.py input.pkl --full output_full.pkl")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if '--full' in sys.argv:
        # 完整模式
        full_idx = sys.argv.index('--full')
        output_file = sys.argv[full_idx + 1] if full_idx + 1 < len(sys.argv) else None
        create_full_motion_data(input_file, output_file)
    else:
        # 简单修复模式
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        fix_motion_pkl(input_file, output_file)