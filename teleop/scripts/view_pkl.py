import pickle
import numpy as np
import sys
import os

def view_pkl(pkl_path):
    """查看PKL文件的详细内容"""
    
    if not os.path.exists(pkl_path):
        print(f"错误: 文件不存在 {pkl_path}")
        return
    
    print(f"\n{'='*60}")
    print(f"PKL文件路径: {pkl_path}")
    print(f"{'='*60}\n")
    
    # 加载PKL文件
    with open(pkl_path, 'rb') as f:
        data = pickle.load(f)
    
    # 显示基本信息
    print("文件类型:", type(data))
    print()
    
    if isinstance(data, dict):
        print("字典键值:")
        print("-" * 60)
        for key in data.keys():
            print(f"  - {key}")
        print()
        
        # 检查TWIST2 motion格式
        print("TWIST2 Motion格式检查:")
        print("-" * 60)
        required_keys = ['fps', 'root_pos', 'root_rot', 'dof_pos']
        for key in required_keys:
            status = "✓" if key in data else "✗"
            print(f"{status} {key}")
        
        # 检查帧数一致性
        if all(k in data for k in required_keys):
            print("\n帧数一致性检查:")
            shapes = {}
            for key in ['root_pos', 'root_rot', 'dof_pos']:
                if isinstance(data[key], np.ndarray):
                    shapes[key] = data[key].shape[0]
                    print(f"  {key}: {data[key].shape[0]} 帧")
            
            if len(set(shapes.values())) == 1:
                print("  ✓ 所有数据帧数一致")
            else:
                print("  ✗ 帧数不一致！")
        print()
        
        # 详细信息
        print("详细内容:")
        print("-" * 60)
        for key, value in data.items():
            print(f"\n[{key}]")
            print(f"  类型: {type(value)}")
            
            if isinstance(value, np.ndarray):
                print(f"  形状: {value.shape}")
                print(f"  数据类型: {value.dtype}")
                
                # 检查是否为空数组
                if value.size == 0:
                    print(f"  ⚠️  警告: 空数组!")
                else:
                    print(f"  范围: [{value.min():.4f}, {value.max():.4f}]")
                    print(f"  均值: {value.mean():.4f}")
                    
                    # 检查是否有NaN或Inf
                    if np.isnan(value).any():
                        print(f"  ⚠️  警告: 包含NaN值!")
                    if np.isinf(value).any():
                        print(f"  ⚠️  警告: 包含Inf值!")
                    
                    if len(value.shape) <= 2 and value.shape[0] <= 5:
                        print(f"  前几个值:\n{value}")
                    else:
                        print(f"  前3个值:\n{value[:min(3, len(value))]}")
            
            elif isinstance(value, (list, tuple)):
                print(f"  长度: {len(value)}")
                if len(value) == 0:
                    print(f"  ⚠️  警告: 空列表!")
                elif len(value) <= 10:
                    print(f"  内容: {value}")
                else:
                    print(f"  前10个元素: {value[:10]}")
            
            elif isinstance(value, (int, float)):
                print(f"  值: {value}")
            
            elif isinstance(value, str):
                print(f"  值: '{value}'")
            
            else:
                print(f"  值: {value}")
        
        # 额外的motion文件诊断
        print("\n" + "="*60)
        print("Motion文件诊断:")
        print("-" * 60)
        
        if 'dof_pos' in data and isinstance(data['dof_pos'], np.ndarray):
            dof_pos = data['dof_pos']
            if dof_pos.size > 0:
                print(f"DOF数量: {dof_pos.shape[-1] if len(dof_pos.shape) > 1 else 1}")
                print(f"总帧数: {dof_pos.shape[0] if len(dof_pos.shape) > 0 else 0}")
                if 'fps' in data:
                    duration = dof_pos.shape[0] / data['fps']
                    print(f"动作时长: {duration:.2f}秒")
            else:
                print("⚠️  dof_pos 是空数组!")
        
        if 'root_rot' in data and isinstance(data['root_rot'], np.ndarray):
            root_rot = data['root_rot']
            if root_rot.size > 0:
                # 检查四元数归一化
                norms = np.linalg.norm(root_rot, axis=-1)
                if not np.allclose(norms, 1.0, atol=0.01):
                    print(f"⚠️  root_rot 四元数未归一化! 范围: [{norms.min():.4f}, {norms.max():.4f}]")
                else:
                    print("✓ root_rot 四元数已正确归一化")
    
    elif isinstance(data, np.ndarray):
        print("NumPy数组信息:")
        print("-" * 60)
        print(f"形状: {data.shape}")
        print(f"数据类型: {data.dtype}")
        if data.size > 0:
            print(f"范围: [{data.min():.4f}, {data.max():.4f}]")
            print(f"前几个值:\n{data[:min(5, len(data))]}")
        else:
            print("⚠️  空数组!")
    
    elif isinstance(data, (list, tuple)):
        print(f"列表/元组信息 (长度: {len(data)}):")
        print("-" * 60)
        for i, item in enumerate(data[:5]):
            print(f"[{i}]: {type(item)} - {item}")
        if len(data) > 5:
            print(f"... (还有 {len(data)-5} 个元素)")
    
    else:
        print("数据内容:")
        print("-" * 60)
        print(data)
    
    print(f"\n{'='*60}\n")


def compare_pkl_files(pkl_path1, pkl_path2):
    """比较两个PKL文件"""
    
    print(f"\n{'='*60}")
    print("比较两个PKL文件")
    print(f"{'='*60}\n")
    
    with open(pkl_path1, 'rb') as f:
        data1 = pickle.load(f)
    
    with open(pkl_path2, 'rb') as f:
        data2 = pickle.load(f)
    
    if isinstance(data1, dict) and isinstance(data2, dict):
        keys1 = set(data1.keys())
        keys2 = set(data2.keys())
        
        print("共同的键:", keys1 & keys2)
        print("仅在文件1中:", keys1 - keys2)
        print("仅在文件2中:", keys2 - keys1)
        
        print("\n形状比较:")
        print("-" * 60)
        for key in sorted(keys1 & keys2):
            val1, val2 = data1[key], data2[key]
            if isinstance(val1, np.ndarray) and isinstance(val2, np.ndarray):
                match = "✓" if val1.shape == val2.shape else "✗"
                print(f"{match} {key}: {val1.shape} vs {val2.shape}")
    
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  查看单个文件: python view_pkl.py <pkl_file>")
        print("  比较两个文件: python view_pkl.py <pkl_file1> <pkl_file2>")
        print("\n示例:")
        print("  python view_pkl.py TWIST2/assets/example_motions/xrobot_retargeting_20260209_194533.pkl")
        print("  python view_pkl.py file1.pkl file2.pkl")
        sys.exit(1)
    
    if len(sys.argv) == 2:
        view_pkl(sys.argv[1])
    elif len(sys.argv) == 3:
        view_pkl(sys.argv[1])
        view_pkl(sys.argv[2])
        compare_pkl_files(sys.argv[1], sys.argv[2])