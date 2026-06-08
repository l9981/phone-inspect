"""
生成 iPhone 8-17 全系列验机知识数据
"""
import json

def make_model(name, screen_desc, camera_desc, bio_desc, bio_type, speaker_desc, call_desc, battery_desc, checklist_extra=""):
    """生成标准化验机项列表"""
    # 屏幕
    screen = (
        "正常：" + screen_desc + "\n"
        "故障：屏幕有划痕/坏点/亮点、原彩显示缺失（换屏特征）、倾斜45度彩虹纹（压盖板屏）、触摸断触/跳屏、漏光或偏色\n"
        "压盖板屏识别：①强光下前置摄像头区域有气泡或灰尘；②手指滑动边缘刮手；③原彩显示丢失或异常；④倾斜45度有彩虹纹"
    )
    screen_note = ("检查「设置-通用-关于本机-部件和服务历史记录」（iOS 15.2+）。"
                   "原装屏必有原彩显示开关。拖动App图标满屏滑动检查断触。压盖板屏价值折损500-1000元。")

    # 摄像头
    camera_note = ("检查步骤：①所有焦段拍照测试切换是否卡顿；②拍白色墙面检查黑斑（镜头进灰）；"
                   "③录像10秒同时说话测试收音和防抖；④前置摄像头自拍检查")

    # 生物识别
    if bio_type == "face":
        bio = ("正常：" + bio_desc + "面容ID设置和录入顺利，支持暗光/戴眼镜解锁。\n"
               "故障：无法录入或提示「面容ID不可用」、解锁频繁失败、原深感摄像头区域遮挡")
        bio_note = ("面容ID维修成本极高（官方报价1500-2500元）。"
                    "重设面容ID测试完整录入和解锁。注意：面容ID模组包含前置摄像头，坏了通常前置也有问题。")
    else:
        bio = ("正常：" + bio_desc + "Touch ID指纹录入顺利，解锁快速准确，支持App Store/Apple Pay指纹支付。\n"
               "故障：无法录入或解锁失败、Home键松动/塌陷、无振动反馈（Taptic Engine异常）")
        bio_note = ("Touch ID与主板绑定（不能单独更换）。"
                    "如果Touch ID坏了说明主板被修过或换过。Home键不可机械按压（通过Taptic Engine模拟），按压没感觉不代表坏。")

    # 扬声器
    speaker_note = "播放立体声测试音频检查左右声道均衡。最大音量播放重低音音乐检查破音。拨打运营商客服测试听筒。语音备忘录录音回放测试麦克风。"

    # 通话
    call_note = ("国行iPhone系统不支持通话录音（隐私法规），这是正常现象。"
                 "检查方法：拨打运营商客服测试通话音质和麦克风；语音备忘录录音回放；FaceTime音视频通话测试。")

    # 电池
    battery_note = ("「设置-电池-电池健康」查看最大容量。通过快捷指令「电池分析」查看循环次数（需先开启共享iPhone分析）。"
                    "二手建议健康度85%以上。低于80%建议换电池或砍价200-400元。")

    # IMEI
    imei = ("正常：*#06#显示的IMEI与卡托/「设置-通用-关于本机」一致，序列号可在Apple官网（checkcoverage.apple.com）查询到有效保修信息。\n"
            "故障：IMEI不一致（拼装机/翻新机）、官网查询不到、显示「运营商锁」（SIM卡已锁）、序列号为已更换状态")
    imei_note = ("*#06#截图->取出卡托核对IMEI->Apple官网查序列号->确认型号号码首字母M(零售)/N(官换)/F(官翻)/3(演示)，"
                 "末尾CH/A(国行)/LL/A(美版)。GSX查询是终极手段。")

    # 爱思
    aisi = ("正常：连接电脑爱思助手（3uTools），验机报告全绿，评分100分，所有部件序列号与出厂一致。\n"
            "故障：屏幕/电池/摄像头标红（换过部件）、硬盘标红（扩容机）、验机评分<100。"
            "注：爱思全绿可能被篡改（改底层数据），建议配合沙漏验机交叉验证和GSX查询。")
    aisi_note = ("强烈建议带电脑去交易现场！连接爱思助手->点击「验机报告」->逐项检查是否全绿。"
                 "注意：部分高仿屏和改底层数据的机器可能「爱思全绿但实际换过件」，需结合外观判断。")

    # 验机清单
    bio_item = "面容ID录入和解锁（含戴口罩）" if bio_type == "face" else "Touch ID录入和解锁"
    checklist = (
        "** 第一阶段：收货准备 **\n"
        "  1. 全程拍摄开箱/验机无间断视频（维权证据）\n"
        "  2. 电脑提前安装爱思助手\n"
        "\n"
        "** 第二阶段：基础核对 **\n"
        "  3. 核对配置：关于本机中确认型号/存储/颜色与卖家描述一致\n"
        "  4. 外观：屏幕/边框/背板/摄像头有无划痕磕碰\n"
        "  5. 按键：电源键/音量键回弹有力无松动\n"
        "  6. 充电口：有无严重灰尘或锈蚀\n"
        "  7. 三码合一：包装盒(如有)/SIM卡托IMEI/关于本机序列号一致\n"
        '  8. 官网查序列号：应显示"请激活"或保修期与描述一致\n'
        "  9. 型号号码：首字母M(零售)/N(官换)/F(官翻)/3(演示)\n"
        "\n"
        "** 第三阶段：系统排查(最关键) **\n"
        "  10. 检查隐藏ID：设置顶部有无陌生Apple ID\n"
        "  11. 【抹掉所有内容和设置】- 重启后应出现Hello欢迎界面\n"
        "  12. 激活时绝不要弹出要求输入陌生Apple ID密码的窗口\n"
        "  13. 检查监管锁：设置-通用-VPN与设备管理\n"
        '  14. 查看部件与服务历史(iOS 15.2+)：有无"未知部件"\n'
        "\n"
        "** 第四阶段：核心功能测试 **\n"
        "  15. 屏幕断触：长按App图标满屏拖拽，边缘重点检查\n"
        "  16. 原彩显示：开启/关闭看色温变化(无此选项=非原装屏)\n"
        "  17. " + bio_item + "\n"
        "  18. 相机：所有焦段拍照->拍白墙查黑斑->录像10秒\n"
        "  19. 电池健康：最大容量与卖家描述一致\n"
        "  20. 语音备忘录录音并播放\n"
        "  21. WiFi/蓝牙/GPS/指南针\n"
        "  22. 振动/按键/静音拨片\n"
        "  23. 气压计：指南针中上下晃动看海拔变化(6s后机型)\n"
        "\n"
        "** 第五阶段：深度排查 **\n"
        "  24. 爱思助手/沙漏验机连接电脑，验机报告应全绿\n"
        "  25. 分析数据：设置-隐私-分析-分析数据，搜panic(一票否决)\n"
        "  26. GSX查询(终极手段)：淘宝花几块钱查GSX激活策略\n"
        "  27. 再次抹掉所有内容和设置，重新激活确认正常\n"
        "\n"
        "** 额外检查 **\n"
        + checklist_extra + "\n"
        '  28. 卖家当面关闭"查找我的iPhone"并退出iCloud\n'
        "  29. 索要电子发票或购买凭证\n"
        "  30. 保存IMEI和序列号截图作为交易凭证\n"
        "\n"
        "💡 全程约40-50分钟。卖家催你或找借口=直接放弃交易！建议打印本清单逐项打勾。"
    )

    img_seed = name.lower().replace(" ", "").replace("/", "-")
    check_points = [
        {"category": "屏幕原装检测（含压盖板判别）", "description": screen, "special_note": screen_note, "compare_img": f"https://picsum.photos/seed/{img_seed}-screen/200/150"},
        {"category": "摄像头检测", "description": camera_desc, "special_note": camera_note, "compare_img": f"https://picsum.photos/seed/{img_seed}-camera/200/150"},
        {"category": "面容ID/Touch ID检测", "description": bio, "special_note": bio_note, "compare_img": f"https://picsum.photos/seed/{img_seed}-bio/200/150"},
        {"category": "听筒与外放音质", "description": speaker_desc, "special_note": speaker_note, "compare_img": f"https://picsum.photos/seed/{img_seed}-speaker/200/150"},
        {"category": "通话与录音功能", "description": call_desc, "special_note": call_note, "compare_img": f"https://picsum.photos/seed/{img_seed}-call/200/150"},
        {"category": "电池健康与充电速度", "description": battery_desc, "special_note": battery_note, "compare_img": f"https://picsum.photos/seed/{img_seed}-battery/200/150"},
        {"category": "机身编码与IMEI核对", "description": imei, "special_note": imei_note, "compare_img": f"https://picsum.photos/seed/{img_seed}-imei/200/150"},
        {"category": "爱思助手全机检测（Apple专有）", "description": aisi, "special_note": aisi_note, "compare_img": f"https://picsum.photos/seed/{img_seed}-3utools/200/150"},
        {"category": "验机建议顺序", "description": checklist, "special_note": "建议打印本清单带到交易现场逐项打勾，全程约40-50分钟。", "compare_img": "https://picsum.photos/seed/iphone-checklist/200/150"}
    ]
    return {"name": name, "check_points": check_points}


def main():
    models = []

    # 1. iPhone 8 / 8 Plus
    models.append(make_model("iPhone 8 / 8 Plus",
        "4.7英寸/5.5英寸LCD Retina HD，1334x750/1920x1080分辨率，625尼特亮度，True Tone原彩显示，3D Touch（最后支持3D Touch的机型）。",
        "后置单摄1200万f/1.8（iPhone 8）/后置双摄1200万广角+长焦f/1.8+f/2.8（iPhone 8 Plus），OIS光学防抖，人像模式（8Plus），4K 60fps录像。前置700万。",
        "", "touch",
        "立体声双扬声器，支持杜比全景声播放，音量充沛无破音。",
        "通话音质清晰，VoLTE支持，麦克风收音正常。",
        "1821mAh/2691mAh电池，18W PD快充（需USB-C to Lightning线），7.5W Qi无线充电（iPhone 8系列首次支持无线充电）。",
        "- 无线充电测试（iPhone 8起支持）\n- 3D Touch测试（设置-通用-辅助功能-3D Touch调节灵敏度）"
    ))

    # 2. iPhone X
    models.append(make_model("iPhone X",
        "5.8英寸OLED Super Retina，2436x1125分辨率，458ppi，HDR10/杜比视界，True Tone原彩显示。首款全面屏iPhone，无Home键。",
        "后置双摄1200万广角f/1.8+长焦f/2.4，双OIS，人像模式/人像光效，4K 60fps。前置700万原深感摄像头（首款支持Face ID和Animoji）。",
        "", "face",
        "立体声双扬声器，杜比全景声，空间音频。",
        "通话音质清晰，VoLTE支持。",
        "2716mAh电池，18W PD快充，7.5W Qi无线充电。电池老化问题较普遍（2017年机型二手健康度普遍<80%）。",
        "- 无线充电测试\n- OLED烧屏检查（纯白/纯灰背景检查状态栏区域有无烙印）\n- Face ID横屏解锁测试"
    ))

    # 3. iPhone XS / XS Max
    models.append(make_model("iPhone XS / XS Max",
        "5.8英寸/6.5英寸OLED Super Retina，2436x1125/2688x1242分辨率，458ppi，HDR10，True Tone，120Hz触控采样率。",
        "后置双摄1200万广角f/1.8+长焦f/2.4，双OIS，智能HDR，人像模式支持后期调焦（Depth Control）。前置700万原深感摄像头。",
        "", "face",
        "立体声双扬声器，杜比全景声，外放动态范围较iPhone X提升。",
        "通话音质清晰，4麦克风设计收音更佳。",
        "2658mAh/3174mAh电池，18W PD快充，7.5W Qi无线充电。",
        "- IP68防水检查（SIM卡托防水胶圈是否完整）\n- 无线充电测试"
    ))

    # 4. iPhone XR
    models.append(make_model("iPhone XR",
        "6.1英寸LCD Liquid Retina，1792x828分辨率，326ppi，1400:1对比度，True Tone，Haptic Touch（取代3D Touch）。",
        "后置单摄1200万f/1.8，OIS光学防抖，智能HDR，人像模式（算法模拟仅支持人脸）。前置700万原深感摄像头。",
        "", "face",
        "立体声双扬声器，杜比全景声，音量充沛。",
        "通话音质清晰。",
        "2942mAh电池（续航优于iPhone 8 Plus），18W PD快充，7.5W Qi无线充电。",
        "- 无线充电测试\n- Haptic Touch测试（长按图标看是否弹出菜单）"
    ))

    # 5. iPhone 11
    models.append(make_model("iPhone 11",
        "6.1英寸LCD Liquid Retina，1792x828分辨率，625尼特亮度，True Tone，Haptic Touch。",
        "后置双摄1200万广角f/1.8+1200万超广角f/2.4（120度视野），夜间模式，人像模式支持宠物检测。前置1200万TrueDepth（升级至1200万）。",
        "", "face",
        "立体声双扬声器，杜比全景声，空间音频。",
        "通话音质清晰。",
        "3110mAh电池，18W PD快充，7.5W Qi无线充电。续航较XR提升1小时。",
        "- 无线充电测试\n- 夜间模式测试（暗光下相机自动触发）\n- 超广角与主摄色彩一致性检查"
    ))

    # 6. iPhone 11 Pro / 11 Pro Max
    models.append(make_model("iPhone 11 Pro / 11 Pro Max",
        "5.8英寸/6.5英寸OLED Super Retina XDR，2436x1125/2688x1242分辨率，800/1200尼特亮度（HDR），True Tone。Pro系列首次搭载OLED。",
        "后置三摄1200万广角f/1.8+1200万超广角f/2.4+1200万长焦f/2.0，夜间模式，Deep Fusion，智能HDR，4K 60fps。首款三摄iPhone。前置1200万TrueDepth。",
        "", "face",
        "立体声双扬声器，杜比全景声，空间音频。",
        "通话音质清晰。",
        "3046mAh/3969mAh电池，18W PD快充（标配18W充电器），7.5W Qi无线充电。",
        "- 无线充电测试\n- OLED烧屏检查\n- 三摄色彩一致性测试（0.5x/1x/2x拍同一物体看色彩是否一致）"
    ))

    # 7. iPhone SE 2
    models.append(make_model("iPhone SE 2",
        "4.7英寸LCD Retina HD，1334x750分辨率，625尼特亮度，True Tone，Haptic Touch。与iPhone 8同款屏幕设计。",
        "后置单摄1200万f/1.8，OIS光学防抖，人像模式（算法模拟），智能HDR，4K 60fps。前置700万。",
        "", "touch",
        "立体声双扬声器，杜比全景声。",
        "通话音质清晰。",
        "1821mAh电池，18W PD快充，7.5W Qi无线充电。续航偏短（与iPhone 8相同电池容量但A13芯片更高效）。",
        "- 无线充电测试\n- Home键按压和Touch ID灵敏度测试"
    ))

    # 8. iPhone 12 / 12 mini
    models.append(make_model("iPhone 12 / 12 mini",
        "6.1英寸/5.4英寸OLED Super Retina XDR，2532x1170/2340x1080分辨率，625/1200尼特亮度（HDR），True Tone。首款OLED的普通版iPhone。",
        "后置双摄1200万广角f/1.6+1200万超广角f/2.4，夜间模式全焦段，Deep Fusion，智能HDR 3，夜间人像模式。前置1200万TrueDepth。",
        "", "face",
        "立体声双扬声器，杜比全景声，空间音频。",
        "通话音质清晰，5G VoNR（首款5G iPhone）。",
        "2815mAh/2227mAh电池，20W PD快充，15W MagSafe无线充电（首款MagSafe）。12 mini续航偏短。",
        "- MagSafe磁吸无线充电测试\n- 5G网络测试（插入5G卡测试网速）\n- 12 mini续航实测"
    ))

    # 9. iPhone 12 Pro / 12 Pro Max
    models.append(make_model("iPhone 12 Pro / 12 Pro Max",
        "6.1英寸/6.7英寸OLED Super Retina XDR，2532x1170/2778x1284分辨率，800/1200尼特亮度，True Tone。",
        "后置三摄1200万广角+超广角+长焦+LiDAR，12 Pro Max长焦2.5x/12 Pro长焦2x，Apple ProRAW，夜间人像模式（LiDAR辅助），4K HDR 60fps Dolby Vision。前置1200万。",
        "", "face",
        "立体声双扬声器，杜比全景声，空间音频。",
        "通话音质清晰，5G VoNR。",
        "2815mAh/3687mAh电池，20W PD快充，15W MagSafe。12 Pro Max续航优秀。",
        "- MagSafe测试\n- LiDAR测距（打开「测距仪」App测试AR测量精度）\n- 5G测试\n- Apple ProRAW拍照测试"
    ))

    # 10. iPhone 13 / 13 mini
    models.append(make_model("iPhone 13 / 13 mini",
        "6.1英寸/5.4英寸OLED Super Retina XDR，2532x1170/2340x1080分辨率，800/1200尼特亮度，True Tone。刘海缩小20%。",
        "后置双摄1200万广角f/1.6（传感器位移式OIS）+1200万超广角f/2.4，对角线排列。电影效果模式（1080p 30fps），智能HDR 4，摄影风格。前置1200万。",
        "", "face",
        "立体声双扬声器，杜比全景声，空间音频。支持通话降噪（语音突显）。",
        "通话音质清晰，5G VoNR。",
        "3227mAh/2406mAh电池，20W PD快充，15W MagSafe。13系列续航较12系列提升1.5-2.5小时。",
        "- MagSafe测试\n- 电影效果模式测试（相机-电影效果，拍摄人物看自动对焦切换）\n- 传感器位移OIS防抖测试"
    ))

    # 11. iPhone 13 Pro / 13 Pro Max
    models.append(make_model("iPhone 13 Pro / 13 Pro Max",
        "6.1英寸/6.7英寸OLED Super Retina XDR，2532x1170/2778x1284分辨率，1000/1200尼特亮度，ProMotion 120Hz LTPO自适应刷新率（首款ProMotion Pro），True Tone。",
        "后置三摄1200万广角+超广角+长焦3x+LiDAR，Apple ProRAW，ProRes 4K 30fps，全焦段夜间模式，微距摄影（超广角首款支持微距的iPhone）。前置1200万。",
        "", "face",
        "立体声双扬声器，杜比全景声，空间音频。",
        "通话音质清晰，5G VoNR。",
        "3095mAh/4352mAh电池，20W PD快充，15W MagSafe。13 Pro Max续航最强之一。",
        "- MagSafe测试\n- ProMotion 120Hz测试\n- 微距摄影测试（相机自动切换到超广角微距模式）\n- ProRes录影"
    ))

    # 12. iPhone SE 3
    models.append(make_model("iPhone SE 3",
        "4.7英寸LCD Retina HD，1334x750分辨率，625尼特亮度，True Tone原彩显示，Haptic Touch。与iPhone 8同款屏幕。",
        "后置单摄1200万f/1.8，OIS光学防抖，智能HDR 4，摄影风格，4K 60fps。A15芯片驱动计算摄影。前置700万。",
        "", "touch",
        "立体声双扬声器，杜比全景声。",
        "通话音质清晰，5G VoNR（SE 3首次支持5G）。",
        "2018mAh电池，20W PD快充，7.5W Qi无线充电。A15能效使续航较SE 2略有改善。",
        "- 无线充电测试\n- 5G网络测试\n- Home键Touch ID测试"
    ))

    # 13. iPhone 14 / 14 Plus
    models.append(make_model("iPhone 14 / 14 Plus",
        "6.1英寸/6.7英寸OLED Super Retina XDR，2532x1170/2778x1284分辨率，800/1200尼特亮度，True Tone。14 Plus是首款大屏非Pro机型。",
        "后置双摄1200万广角f/1.5（传感器位移OIS）+1200万超广角f/2.4。光像引擎，夜间模式，运动模式防抖。前置1200万TrueDepth（首次支持自动对焦）。",
        "", "face",
        "立体声双扬声器，杜比全景声，空间音频。",
        "通话音质清晰，5G VoNR。支持车祸检测和卫星SOS（iPhone 14系列新增）。",
        "3279mAh/4325mAh电池，20W PD快充，15W MagSafe。14 Plus续航为iPhone史上最强之一。",
        "- MagSafe测试\n- 卫星SOS测试界面验证\n- 运动模式录像测试（相机-录像-运动模式）"
    ))

    # 14. iPhone 14 Pro / 14 Pro Max
    models.append(make_model("iPhone 14 Pro / 14 Pro Max",
        "6.1英寸/6.7英寸OLED Super Retina XDR，2556x1179/2796x1290分辨率，1000/1600/2000尼特亮度，ProMotion 120Hz LTPO，灵动岛设计，全天候显示（Always-On Display首款支持）。",
        "后置三摄4800万主摄f/1.78（四合一输出1200万）+1200万超广角+1200万长焦3x+LiDAR。首款4800万像素iPhone，ProRAW 4800万像素，光像引擎，运动模式，4K HDR电影模式。",
        "", "face",
        "立体声双扬声器，杜比全景声，空间音频。",
        "通话音质清晰，5G VoNR。车祸检测+卫星SOS。",
        "3200mAh/4323mAh电池，20W PD快充（支持27W），15W MagSafe。",
        "- 全天候显示测试（设置-显示与亮度-全天候显示）\n- 灵动岛交互测试\n- 4800万ProRAW测试\n- 运动模式录像测试"
    ))

    # 15. iPhone 15 / 15 Plus
    models.append(make_model("iPhone 15 / 15 Plus",
        "6.1英寸/6.7英寸OLED Super Retina XDR，2556x1179/2796x1290分辨率，1000/1600/2000尼特亮度，True Tone，Haptic Touch。灵动岛设计（15系列标配）。",
        "后置双摄4800万主摄f/1.6（四合一输出2400万默认）+1200万超广角f/2.4。2x光学变焦（裁切4800万）。新一代人像模式（自动检测人物/宠物）。USB-C接口首现。前置1200万。",
        "", "face",
        "立体声双扬声器，杜比全景声，空间音频。",
        "通话音质清晰，5G VoNR。卫星SOS+车祸检测。",
        "3349mAh/4383mAh电池，20W PD快充（USB-C），15W MagSafe，15W Qi2无线充电。",
        "- USB-C充电和数据传输测试\n- Qi2无线充电测试\n- 2400万像素默认拍照测试\n- 新一代人像模式测试"
    ))

    # 16. iPhone 15 Pro / 15 Pro Max
    models.append(make_model("iPhone 15 Pro / 15 Pro Max",
        "6.1英寸/6.7英寸OLED Super Retina XDR，2556x1179/2796x1290分辨率，1000/1600/2000尼特亮度，ProMotion 120Hz LTPO，True Tone，全天候显示。钛金属边框（首款钛金属iPhone）。",
        "后置三摄4800万主摄+4800万超广角+1200万长焦3x（Pro）/5x潜望（Pro Max）+LiDAR。5倍光学变焦（Pro Max首款潜望长焦）。USB-C 3.0 10Gbps。Log编码。前置1200万。",
        "", "face",
        "立体声双扬声器，杜比全景声，空间音频。",
        "通话音质清晰，5G VoNR。操作按钮（Action Button）取代静音拨片。",
        "3274mAh/4422mAh电池，20W PD快充（支持27W），15W MagSafe，15W Qi2。",
        "- 操作按钮测试分别设置为静音/相机/手电筒测试\n- 5x潜望长焦测试（仅Pro Max拍远处文字检查清晰度）\n- USB-C 3.0传输速度测试\n- Log编码录像测试"
    ))

    # 17. iPhone 16 / 16 Plus
    models.append(make_model("iPhone 16 / 16 Plus",
        "6.1英寸/6.7英寸OLED Super Retina XDR，2556x1179/2796x1290分辨率，1000/1600/2000尼特亮度，True Tone，Haptic Touch。灵动岛设计。",
        "后置双摄4800万主摄f/1.6+1200万超广角f/2.4。第二代传感器位移OIS。空间视频拍摄（配合Vision Pro）。相机控制按钮（Camera Control）。前置1200万。",
        "", "face",
        "立体声双扬声器，杜比全景声，空间音频。",
        "通话音质清晰，5G VoNR。卫星SOS+车祸检测+卫星信息。",
        "电池容量较15增加，20W+PD快充（最高约27W），15W MagSafe，15W Qi2。",
        "- 相机控制按钮测试（半按对焦-全按拍照-滑动变焦）\n- 空间视频拍摄\n- Apple Intelligence功能检查"
    ))

    # 18. iPhone 16 Pro / 16 Pro Max
    models.append(make_model("iPhone 16 Pro / 16 Pro Max",
        "6.3英寸/6.9英寸OLED Super Retina XDR，2622x1206/2868x1320分辨率，1000/1600/2000尼特亮度，ProMotion 120Hz LTPO，全天候显示。屏幕尺寸较15 Pro增大。",
        "后置三摄4800万主摄+4800万超广角+1200万长焦5x（Pro Max）/3x（Pro）+LiDAR。超广角升级至4800万。相机控制按钮。空间视频。前置1200万。",
        "", "face",
        "立体声双扬声器，杜比全景声，空间音频。",
        "通话音质清晰，5G VoNR。",
        "电池容量增大，20W+PD快充（最高约40W），15W MagSafe/Qi2。",
        "- 相机控制按钮测试\n- 4800万超广角拍照测试\n- 空间视频拍摄\n- Apple Intelligence功能\n- 散热测试（原神30分钟看发热）"
    ))

    # 19. iPhone 17 / 17 Plus
    models.append(make_model("iPhone 17 / 17 Plus",
        "6.1英寸/6.7英寸OLED Super Retina XDR，亮度2500尼特，True Tone，Haptic Touch。灵动岛设计。全系列标配LTPO（非Pro也支持1-120Hz自适应）。",
        "后置双摄4800万主摄f/1.6+1200万超广角f/2.4。传感器位移OIS。相机控制按钮。Apple Intelligence深度集成。前置1200万。",
        "", "face",
        "立体声双扬声器，杜比全景声，空间音频。",
        "通话音质清晰，5G VoNR。卫星SOS+卫星信息。",
        "电池容量继续增加，30W PD快充（标配），15W MagSafe/Qi2。",
        "- 120Hz LTPO测试（非Pro首款高刷，滑动桌面检查流畅度）\n- 相机控制按钮测试\n- Apple Intelligence功能测试"
    ))

    # 20. iPhone 17 Pro / 17 Pro Max
    models.append(make_model("iPhone 17 Pro / 17 Pro Max",
        "6.3英寸/6.9英寸OLED Super Retina XDR，峰值亮度3000尼特，ProMotion 120Hz LTPO，全天候显示。可能屏下Face ID（灵动岛缩小或取消）。",
        "后置三摄4800万主摄+4800万超广角+4800万长焦5x+LiDAR。全焦段4800万。8K 60fps ProRes（首款）。相机控制按钮。前置4800万（升级）。",
        "", "face",
        "立体声双扬声器，杜比全景声，空间音频，自适应音频算法。",
        "通话音质清晰，5G VoNR。卫星通话（部分版本支持）。",
        "电池容量大幅增加，35W+PD快充，15W MagSafe/Qi2，7.5W反向无线充电。",
        "- 屏下Face ID测试（不同光线条件下录入和解锁）\n- 8K录像测试（相机-格式-8K 60fps ProRes）\n- 全焦段4800万拍照测试\n- 反向无线充电测试"
    ))

    # 构建完整数据
    apple_brand = {"name": "Apple", "models": models}

    with open('data/knowledge.json', 'r', encoding='utf-8') as f:
        old = json.load(f)
    non_apple = [b for b in old['brands'] if b['name'] != 'Apple']

    new_brands = [apple_brand] + non_apple
    output = {"brands": new_brands}

    with open('data/knowledge.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    total_models = len(models)
    total_checks = sum(len(m['check_points']) for m in models)
    all_checks = sum(len(m['check_points']) for b in new_brands for m in b['models'])
    print(f"Apple models: {total_models}")
    for m in models:
        print(f"  {m['name']}: {len(m['check_points'])} items")
    print(f"Non-Apple brands: {[b['name'] for b in non_apple]}")
    print(f"Total in file: {all_checks} check points")
    print("Done!")


if __name__ == "__main__":
    main()
