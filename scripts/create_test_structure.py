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
    # 1. 创建 01_BCG 结构
    # ========================================
    print("\n[1/3] 创建 01_BCG 结构...")
    
    bcg_publish = base_path / "01_BCG" / "00_Publish"
    bcg_publish.mkdir(parents=True, exist_ok=True)
    
    # 创建 BCG 测试文件
    create_test_file(
        bcg_publish / "BCG_Strategy_2024.docx",
        "BCG 战略文档 2024\n\n这是 BCG 咨询项目的核心战略文档。"
    )
    create_test_file(
        bcg_publish / "BCG_Analysis_Report.pdf",
        "BCG 分析报告\n\n市场分析和竞争态势研究。"
    )
    create_test_file(
        bcg_publish / "BCG_Presentation.pptx",
        "BCG 演示文稿\n\n高层汇报材料。"
    )
    
    # 创建子目录
    bcg_sub = bcg_publish / "Appendix"
    create_test_file(
        bcg_sub / "BCG_Data_Tables.xlsx",
        "BCG 数据表格\n\n附录数据。"
    )
    
    print(f"✓ 01_BCG 结构创建完成")
    
    # ========================================
    # 2. 创建 02_Policy 结构
    # ========================================
    print("\n[2/3] 创建 02_Policy 结构...")
    
    # 2.1 创建其他目录（不应被扫描）
    other_dirs = ["01_List Report", "04_Shared info"]
    for dir_name in other_dirs:
        other_path = base_path / "02_Policy" / dir_name
        other_path.mkdir(parents=True, exist_ok=True)
        # 故意在这些目录下也创建 00_Publish，但不应被扫描到
        fake_publish = other_path / "00_Publish"
        fake_publish.mkdir(parents=True, exist_ok=True)
        create_test_file(
            fake_publish / "should_not_be_scanned.txt",
            "⚠️ 这个文件不应该被扫描到！\n\n如果看到这个文件被上传，说明扫描逻辑有问题。"
        )
    
    # 2.2 创建 02_GPS 结构（应被扫描）
    gps_projects = [
        "GPS_1_Policy Management and Governance Ownership",
        "GPS_2_Risk Assessment Framework",
        "GPS_3_Compliance Monitoring"
    ]
    
    for project in gps_projects:
        gps_publish = base_path / "02_Policy" / "02_GPS" / project / "00_Publish"
        gps_publish.mkdir(parents=True, exist_ok=True)
        
        create_test_file(
            gps_publish / f"{project}_Policy.docx",
            f"GPS 政策文档\n\n项目: {project}\n版本: 1.0"
        )
        create_test_file(
            gps_publish / f"{project}_Guidelines.pdf",
            f"GPS 指南\n\n项目: {project}"
        )
    
    # 2.3 创建 03_EPS 结构（应被扫描）
    eps_projects = [
        "EPS_1_Environmental_Policy",
        "EPS_2_Sustainability_Standards"
    ]
    
    for project in eps_projects:
        eps_publish = base_path / "02_Policy" / "03_EPS" / project / "00_Publish"
        eps_publish.mkdir(parents=True, exist_ok=True)
        
        create_test_file(
            eps_publish / f"{project}_Document.docx",
            f"EPS 环境政策文档\n\n项目: {project}\n版本: 2.0"
        )
        
        # 创建多层子目录
        sub_folder = eps_publish / "Attachments" / "Images"
        create_test_file(
            sub_folder / "diagram.png",
            "PNG 图片占位符"
        )
    
    print(f"✓ 02_Policy 结构创建完成")
    
    # ========================================
    # 3. 创建 03_Reg_WI 结构
    # ========================================
    print("\n[3/3] 创建 03_Reg_WI 结构...")
    
    # 3.1 创建其他目录（不应被扫描）
    other_reg_dirs = ["01_List Report", "03_Deleted Reg WI", "04_Shared info"]
    for dir_name in other_reg_dirs:
        other_path = base_path / "03_Reg_WI" / dir_name
        other_path.mkdir(parents=True, exist_ok=True)
        # 故意创建 00_Publish，但不应被扫描
        fake_publish = other_path / "00_Publish"
        fake_publish.mkdir(parents=True, exist_ok=True)
        create_test_file(
            fake_publish / "should_not_be_scanned.txt",
            "⚠️ 这个文件不应该被扫描到！"
        )
    
    # 3.2 创建 02_in working Reg WI 结构（应被扫描）
    working_base = base_path / "03_Reg_WI" / "02_in working Reg WI"
    
    # DS1 项目
    ds1_projects = [
        "DS1 ItB Market&consumer Insights to Branded marting performance/HQ_R_451_Marketing Touchpoint",
        "DS1 ItB Market&consumer Insights to Branded marting performance/HQ_R_452_Brand Strategy"
    ]
    
    for project_path in ds1_projects:
        project_publish = working_base / project_path / "00_Publish"
        project_publish.mkdir(parents=True, exist_ok=True)
        
        project_name = project_path.split('/')[-1]
        create_test_file(
            project_publish / f"{project_name}_Procedure.docx",
            f"工作指令文档\n\n项目: {project_name}\n状态: 工作中"
        )
        create_test_file(
            project_publish / f"{project_name}_Flowchart.pdf",
            f"流程图\n\n项目: {project_name}"
        )
    
    # DS2 项目
    ds2_project = "DS2 LtO lead to Sales Order/China_R_481_BSH第三方平台官方旗舰店业务流程"
    ds2_publish = working_base / ds2_project / "00_Publish"
    ds2_publish.mkdir(parents=True, exist_ok=True)
    
    create_test_file(
        ds2_publish / "China_R_481_业务流程.docx",
        "中国区第三方平台业务流程\n\n适用范围: 天猫、京东等官方旗舰店"
    )
    create_test_file(
        ds2_publish / "China_R_481_操作手册.pdf",
        "操作手册\n\n详细步骤说明"
    )
    
    # 创建多层嵌套
    ds2_sub = ds2_publish / "Templates" / "Forms"
    create_test_file(
        ds2_sub / "Application_Form.xlsx",
        "申请表模板"
    )
    
    # DS3 项目
    ds3_project = "DS3 CtL Consumer care to consumer satisfaction and loyalty/China_R_746_网点技术员与网点信息员账号申请"
    ds3_publish = working_base / ds3_project / "00_Publish"
    ds3_publish.mkdir(parents=True, exist_ok=True)
    
    create_test_file(
        ds3_publish / "China_R_746_账号申请流程.docx",
        "网点技术员与信息员账号申请流程\n\n版本: 3.0\n更新日期: 2024-01-15"
    )
    create_test_file(
        ds3_publish / "China_R_746_FAQ.pdf",
        "常见问题解答"
    )
    create_test_file(
        ds3_publish / "China_R_746_权限说明.xlsx",
        "权限矩阵说明"
    )
    
    print(f"✓ 03_Reg_WI 结构创建完成")
    
    # ========================================
    # 统计信息
    # ========================================
    print("\n" + "=" * 60)
    print("✅ 测试目录结构创建完成！\n")
    
    # 统计 00_Publish 目录数量
    publish_count = len(list(base_path.rglob("00_Publish")))
    file_count = len(list(base_path.rglob("*.*")))
    
    print(f"📊 统计信息:")
    print(f"  • 总共创建了 {publish_count} 个 00_Publish 目录")
    print(f"  • 总共创建了 {file_count} 个测试文件")
    print(f"  • 根目录: {base_path}")
    
    print("\n📝 预期扫描结果:")
    print("  ✓ 应该扫描到的 00_Publish 目录:")
    print("    - 01_BCG/00_Publish (1个)")
    print("    - 02_Policy/02_GPS/*/00_Publish (3个)")
    print("    - 02_Policy/03_EPS/*/00_Publish (2个)")
    print("    - 03_Reg_WI/02_in working Reg WI/*/00_Publish (4个)")
    print("    总计: 10 个目录")
    
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
