#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建测试目录结构脚本

用于构建符合 BSH 文档管理规范的测试目录结构，包含：
- 01_BCG
- 02_Policy (02_GPS, 03_EPS)
- 03_Reg_WI (02_in working Reg WI)

每个目录下都会创建 00_Publish 文件夹和测试文件
"""

import os
from pathlib import Path
from datetime import datetime


def create_test_file(file_path: Path, content: str = None):
    """创建测试文件"""
    if content is None:
        content = f"""测试文档
创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
文件路径: {file_path}

这是一个用于测试飞书上传工具的示例文档。
"""
    
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ 创建文件: {file_path}")


def create_directory_structure(base_dir: str = "test_data"):
    """
    创建完整的测试目录结构
    
    Args:
        base_dir: 基础目录名称，默认为 "test_data"
    """
    base_path = Path(base_dir).resolve()
    
    print(f"\n开始创建测试目录结构: {base_path}\n")
    print("=" * 60)
    
    # ========================================
    # 0. 创建其他不需要扫描的目录（干扰项）
    # ========================================
    print("\n[0/4] 创建其他目录（干扰项，不应被扫描）...")
    
    other_top_dirs = [
        "00_Process management",
        "04_Forms and Template_ylx",
        "05_E-Workflow",
        "06_SDC management",
        "07_PM team",
        "08_Process Communication",
        "09_ISO audit",
        "10_Process Efficiency Analysis",
        "11_IC report and measure list"
    ]
    
    for dir_name in other_top_dirs:
        dir_path = base_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ 创建目录: {dir_name}")
    
    # ========================================
    # 1. 创建 01_BCG 结构
    # ========================================
    print("\n[1/4] 创建 01_BCG 结构...")
    
    bcg_publish = base_path / "01_BCG" / "00_Publish"
    bcg_publish.mkdir(parents=True, exist_ok=True)
    
    # 创建多个 BCG 项目目录（使用简短名称）
    bcg_projects = ["Str", "Ana", "Prs", "Rsh", "Imp", "Mkt", "Cmp", "Fin", "Ops"]
    
    file_types = ["docx", "pdf", "xlsx", "pptx"]
    
    for project in bcg_projects:
        # 每个项目创建多个文件，直接放在 bcg_publish 下
        for i in range(1, 4):
            for ext in file_types:
                create_test_file(
                    bcg_publish / f"BCG_{project}_v{i}.{ext}",
                    f"BCG {project} v{i}"
                )
    
    print(f"✓ 01_BCG 结构创建完成")
    
    # ========================================
    # 2. 创建 02_Policy 结构
    # ========================================
    print("\n[2/4] 创建 02_Policy 结构...")
    
    # 2.1 创建其他目录（不应被扫描）
    other_dirs = ["01_List Report", "04_Shared info"]
    for dir_name in other_dirs:
        other_path = base_path / "02_Policy" / dir_name
        other_path.mkdir(parents=True, exist_ok=True)
        fake_publish = other_path / "00_Publish"
        fake_publish.mkdir(parents=True, exist_ok=True)
        create_test_file(
            fake_publish / "should_not_be_scanned.txt",
            "⚠️ 这个文件不应该被扫描到！"
        )
    
    # 2.2 创建 02_GPS 结构（应被扫描）- 15 个项目（简短名称）
    gps_projects = [
        "GPS_01", "GPS_02", "GPS_03", "GPS_04", "GPS_05",
        "GPS_06", "GPS_07", "GPS_08", "GPS_09", "GPS_10",
        "GPS_11", "GPS_12", "GPS_13", "GPS_14", "GPS_15"
    ]
    
    for project in gps_projects:
        gps_publish = base_path / "02_Policy" / "02_GPS" / project / "00_Publish"
        gps_publish.mkdir(parents=True, exist_ok=True)
        
        # 每个项目创建多个版本的文件
        for version in range(1, 6):
            for ext in ["docx", "pdf", "xlsx", "pptx"]:
                create_test_file(
                    gps_publish / f"{project}_v{version}.{ext}",
                    f"GPS v{version}"
                )
        
        # 添加附件（直接放目录下）
        for i in range(1, 3):
            create_test_file(
                gps_publish / f"{project}_Att_{i}.pdf",
                f"Att {i}"
            )
    
    # 2.3 创建 03_EPS 结构（应被扫描）- 10 个项目
    eps_projects = [
        "EPS_01", "EPS_02", "EPS_03", "EPS_04", "EPS_05",
        "EPS_06", "EPS_07", "EPS_08", "EPS_09", "EPS_10"
    ]
    
    for project in eps_projects:
        eps_publish = base_path / "02_Policy" / "03_EPS" / project / "00_Publish"
        eps_publish.mkdir(parents=True, exist_ok=True)
        
        for version in range(1, 5):
            for ext in ["docx", "pdf", "xlsx"]:
                create_test_file(
                    eps_publish / f"{project}_v{version}.{ext}",
                    f"EPS v{version}"
                )
        
        # 创建相关文件（直接放目录下）
        for sub in ["Img", "Tpl", "Rpt"]:
            for i in range(1, 2):
                create_test_file(
                    eps_publish / f"{project}_{sub}_{i}.pdf",
                    f"{sub} {i}"
                )
    
    print(f"✓ 02_Policy 结构创建完成")
    
    # ========================================
    # 3. 创建 03_Reg_WI 结构
    # ========================================
    print("\n[3/4] 创建 03_Reg_WI 结构...")
    
    # 3.1 创建其他目录（不应被扫描）
    other_reg_dirs = ["01_List Report", "03_Deleted Reg WI", "04_Shared info"]
    for dir_name in other_reg_dirs:
        other_path = base_path / "03_Reg_WI" / dir_name
        other_path.mkdir(parents=True, exist_ok=True)
        fake_publish = other_path / "00_Publish"
        fake_publish.mkdir(parents=True, exist_ok=True)
        create_test_file(
            fake_publish / "should_not_be_scanned.txt",
            "⚠️ 这个文件不应该被扫描到！"
        )
    
    # 3.2 创建 02_in working Reg WI 结构（应被扫描）- 大量项目
    working_base = base_path / "03_Reg_WI" / "02_in working Reg WI"
    
    # DS1 项目组 - 10 个项目（使用简短名称）
    ds1_base = "DS1_Marketing"
    ds1_projects = [
        "HQ_R_451",
        "HQ_R_452",
        "HQ_R_453",
        "HQ_R_454",
        "CN_R_455",
        "CN_R_456",
        "AP_R_457",
        "EU_R_458",
        "NA_R_459",
        "LA_R_460"
    ]
    
    for project_name in ds1_projects:
        project_publish = working_base / ds1_base / project_name / "00_Publish"
        project_publish.mkdir(parents=True, exist_ok=True)
        
        for version in range(1, 6):
            for ext in ["docx", "pdf", "xlsx", "pptx"]:
                create_test_file(
                    project_publish / f"{project_name}_v{version}.{ext}",
                    f"DS1\n\nProject: {project_name}\nVersion: {version}.0"
                )
        
        # 添加模板和表单（直接放目录下）
        for sub in ["Tpl", "Form", "Rpt"]:
            for i in range(1, 2):
                create_test_file(
                    project_publish / f"{project_name}_{sub}_{i}.xlsx",
                    f"{sub} file {i}"
                )
    
    # DS2 项目组 - 8 个项目
    ds2_base = "DS2_Sales"
    ds2_projects = [
        "CN_R_481",
        "CN_R_482",
        "CN_R_483",
        "HQ_R_484",
        "AP_R_485",
        "EU_R_486",
        "NA_R_487",
        "LA_R_488"
    ]
    
    for project_name in ds2_projects:
        project_publish = working_base / ds2_base / project_name / "00_Publish"
        project_publish.mkdir(parents=True, exist_ok=True)
        
        for version in range(1, 5):
            for ext in ["docx", "pdf", "xlsx"]:
                create_test_file(
                    project_publish / f"{project_name}_v{version}.{ext}",
                    f"DS2\n\nProject: {project_name}\nVersion: {version}.0"
                )
        
        for sub in ["Tpl", "Ctr"]:
            for i in range(1, 2):
                create_test_file(
                    project_publish / f"{project_name}_{sub}_{i}.docx",
                    f"{sub} file {i}"
                )
    
    # DS3 项目组 - 10 个项目
    ds3_base = "DS3_Service"
    ds3_projects = [
        "CN_R_746",
        "CN_R_747",
        "CN_R_748",
        "HQ_R_749",
        "HQ_R_750",
        "AP_R_751",
        "EU_R_752",
        "NA_R_753",
        "LA_R_754",
        "GL_R_755"
    ]
    
    for project_name in ds3_projects:
        project_publish = working_base / ds3_base / project_name / "00_Publish"
        project_publish.mkdir(parents=True, exist_ok=True)
        
        for version in range(1, 5):
            for ext in ["docx", "pdf", "xlsx", "pptx"]:
                create_test_file(
                    project_publish / f"{project_name}_v{version}.{ext}",
                    f"DS3\n\nProject: {project_name}\nVersion: {version}.0"
                )
        
        for sub in ["FAQ", "Trn", "Gdn"]:
            for i in range(1, 2):
                create_test_file(
                    project_publish / f"{project_name}_{sub}_{i}.pdf",
                    f"{sub} file {i}"
                )
    
    print(f"✓ 03_Reg_WI 结构创建完成")
    
    # ========================================
    # 统计信息
    # ========================================
    print("\n[4/4] 统计信息...")
    print("\n" + "=" * 60)
    print("✅ 测试目录结构创建完成！\n")
    
    # 统计 00_Publish 目录数量
    publish_count = len(list(base_path.rglob("00_Publish")))
    file_count = len(list(base_path.rglob("*.*")))
    top_dir_count = len([d for d in base_path.iterdir() if d.is_dir()])
    
    print(f"📊 统计信息:")
    print(f"  • 总共创建了 {top_dir_count} 个一级目录")
    print(f"  • 总共创建了 {publish_count} 个 00_Publish 目录")
    print(f"  • 总共创建了 {file_count} 个测试文件")
    print(f"  • 根目录: {base_path}")
    
    print("\n📁 一级目录结构:")
    print("  ❌ 00_Process management         (干扰项，不扫描)")
    print("  ✅ 01_BCG                        (扫描)")
    print("  ✅ 02_Policy                     (扫描 02_GPS, 03_EPS)")
    print("  ✅ 03_Reg_WI                     (扫描 02_in working Reg WI)")
    print("  ❌ 04_Forms and Template_ylx     (干扰项，不扫描)")
    print("  ❌ 05_E-Workflow                 (干扰项，不扫描)")
    print("  ❌ 06_SDC management             (干扰项，不扫描)")
    print("  ❌ 07_PM team                    (干扰项，不扫描)")
    print("  ❌ 08_Process Communication      (干扰项，不扫描)")
    print("  ❌ 09_ISO audit                  (干扰项，不扫描)")
    print("  ❌ 10_Process Efficiency Analysis(干扰项，不扫描)")
    print("  ❌ 11_IC report and measure list (干扰项，不扫描)")
    
    print("\n📝 预期扫描结果:")
    print("  ✓ 应该扫描到的 00_Publish 目录:")
    print("    - 01_BCG/00_Publish (1个)")
    print("    - 02_Policy/02_GPS/*/00_Publish (15个)")
    print("    - 02_Policy/03_EPS/*/00_Publish (10个)")
    print("    - 03_Reg_WI/02_in working Reg WI/DS1/* (10个)")
    print("    - 03_Reg_WI/02_in working Reg WI/DS2/* (8个)")
    print("    - 03_Reg_WI/02_in working Reg WI/DS3/* (10个)")
    print(f"    总计: 54 个目录")
    
    print("\n  ✗ 不应该扫描到的 00_Publish 目录:")
    print("    - 02_Policy/01_List Report/00_Publish")
    print("    - 02_Policy/04_Shared info/00_Publish")
    print("    - 03_Reg_WI/01_List Report/00_Publish")
    print("    - 03_Reg_WI/03_Deleted Reg WI/00_Publish")
    print("    - 03_Reg_WI/04_Shared info/00_Publish")
    print("    总计: 5 个目录（应被忽略）")
    
    print("\n💡 使用方法:")
    print(f"  python feishu_uploader.py \"{base_path}\" --dry-run")
    print("=" * 60 + "\n")
    
    return base_path


if __name__ == "__main__":
    import sys
    
    # 支持自定义目录名称
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        base_dir = "test_data"
    
    try:
        result_path = create_directory_structure(base_dir)
        print(f"✅ 成功！测试数据已创建在: {result_path}")
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)
