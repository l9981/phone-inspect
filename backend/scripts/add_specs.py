"""
为所有机型添加第一项"手机参数"：处理器/内存/存储/屏幕/电池/摄像头
"""
import json

# ========== Apple 全系参数 ==========
APPLE_SPECS = {
    "iPhone 8 / 8 Plus": {
        "iPhone 8": "A11 Bionic | 2GB RAM | 64/256GB | 4.7英寸LCD 1334x750 | 1821mAh | 单摄1200万",
        "iPhone 8 Plus": "A11 Bionic | 3GB RAM | 64/256GB | 5.5英寸LCD 1920x1080 | 2691mAh | 双摄1200万+1200万"
    },
    "iPhone X": "A11 Bionic | 3GB RAM | 64/256GB | 5.8英寸OLED 2436x1125 | 2716mAh | 双摄1200万+1200万",
    "iPhone XS / XS Max": {
        "iPhone XS": "A12 Bionic | 4GB RAM | 64/256/512GB | 5.8英寸OLED 2436x1125 | 2658mAh | 双摄1200万+1200万",
        "iPhone XS Max": "A12 Bionic | 4GB RAM | 64/256/512GB | 6.5英寸OLED 2688x1242 | 3174mAh | 双摄1200万+1200万"
    },
    "iPhone XR": "A12 Bionic | 3GB RAM | 64/128/256GB | 6.1英寸LCD 1792x828 | 2942mAh | 单摄1200万",
    "iPhone 11": "A13 Bionic | 4GB RAM | 64/128/256GB | 6.1英寸LCD 1792x828 | 3110mAh | 双摄1200万+1200万",
    "iPhone 11 Pro / 11 Pro Max": {
        "iPhone 11 Pro": "A13 Bionic | 4GB RAM | 64/256/512GB | 5.8英寸OLED 2436x1125 | 3046mAh | 三摄1200万+1200万+1200万",
        "iPhone 11 Pro Max": "A13 Bionic | 4GB RAM | 64/256/512GB | 6.5英寸OLED 2688x1242 | 3969mAh | 三摄1200万+1200万+1200万"
    },
    "iPhone SE 2": "A13 Bionic | 3GB RAM | 64/128/256GB | 4.7英寸LCD 1334x750 | 1821mAh | 单摄1200万",
    "iPhone 12 / 12 mini": {
        "iPhone 12 mini": "A14 Bionic | 4GB RAM | 64/128/256GB | 5.4英寸OLED 2340x1080 | 2227mAh | 双摄1200万+1200万",
        "iPhone 12": "A14 Bionic | 4GB RAM | 64/128/256GB | 6.1英寸OLED 2532x1170 | 2815mAh | 双摄1200万+1200万"
    },
    "iPhone 12 Pro / 12 Pro Max": {
        "iPhone 12 Pro": "A14 Bionic | 6GB RAM | 128/256/512GB | 6.1英寸OLED 2532x1170 | 2815mAh | 三摄1200万+1200万+1200万+LiDAR",
        "iPhone 12 Pro Max": "A14 Bionic | 6GB RAM | 128/256/512GB | 6.7英寸OLED 2778x1284 | 3687mAh | 三摄1200万+1200万+1200万+LiDAR"
    },
    "iPhone 13 / 13 mini": {
        "iPhone 13 mini": "A15 Bionic | 4GB RAM | 128/256/512GB | 5.4英寸OLED 2340x1080 | 2406mAh | 双摄1200万+1200万",
        "iPhone 13": "A15 Bionic | 4GB RAM | 128/256/512GB | 6.1英寸OLED 2532x1170 | 3227mAh | 双摄1200万+1200万"
    },
    "iPhone 13 Pro / 13 Pro Max": {
        "iPhone 13 Pro": "A15 Bionic | 6GB RAM | 128/256/512GB/1TB | 6.1英寸OLED 2532x1170(120Hz) | 3095mAh | 三摄1200万+1200万+1200万+LiDAR",
        "iPhone 13 Pro Max": "A15 Bionic | 6GB RAM | 128/256/512GB/1TB | 6.7英寸OLED 2778x1284(120Hz) | 4352mAh | 三摄1200万+1200万+1200万+LiDAR"
    },
    "iPhone SE 3": "A15 Bionic | 4GB RAM | 64/128/256GB | 4.7英寸LCD 1334x750 | 2018mAh | 单摄1200万",
    "iPhone 14 / 14 Plus": {
        "iPhone 14": "A15 Bionic | 6GB RAM | 128/256/512GB | 6.1英寸OLED 2532x1170 | 3279mAh | 双摄1200万+1200万",
        "iPhone 14 Plus": "A15 Bionic | 6GB RAM | 128/256/512GB | 6.7英寸OLED 2778x1284 | 4325mAh | 双摄1200万+1200万"
    },
    "iPhone 14 Pro / 14 Pro Max": {
        "iPhone 14 Pro": "A16 Bionic | 6GB RAM | 128/256/512GB/1TB | 6.1英寸OLED 2556x1179(120Hz)灵动岛 | 3200mAh | 三摄4800万+1200万+1200万+LiDAR",
        "iPhone 14 Pro Max": "A16 Bionic | 6GB RAM | 128/256/512GB/1TB | 6.7英寸OLED 2796x1290(120Hz)灵动岛 | 4323mAh | 三摄4800万+1200万+1200万+LiDAR"
    },
    "iPhone 15 / 15 Plus": {
        "iPhone 15": "A16 Bionic | 6GB RAM | 128/256/512GB | 6.1英寸OLED 2556x1179灵动岛 | 3349mAh | 双摄4800万+1200万",
        "iPhone 15 Plus": "A16 Bionic | 6GB RAM | 128/256/512GB | 6.7英寸OLED 2796x1290灵动岛 | 4383mAh | 双摄4800万+1200万"
    },
    "iPhone 15 Pro / 15 Pro Max": {
        "iPhone 15 Pro": "A17 Pro(3nm) | 8GB RAM | 128/256/512GB/1TB | 6.1英寸OLED 2556x1179(120Hz)钛金属 | 3274mAh | 三摄4800万+4800万+1200万3x+LiDAR",
        "iPhone 15 Pro Max": "A17 Pro(3nm) | 8GB RAM | 256/512GB/1TB | 6.7英寸OLED 2796x1290(120Hz)钛金属 | 4422mAh | 三摄4800万+4800万+1200万5x潜望+LiDAR"
    },
    "iPhone 16 / 16 Plus": {
        "iPhone 16": "A18(3nm) | 8GB RAM | 128/256/512GB | 6.1英寸OLED 2556x1179 | 3561mAh | 双摄4800万+1200万",
        "iPhone 16 Plus": "A18(3nm) | 8GB RAM | 128/256/512GB | 6.7英寸OLED 2796x1290 | 4674mAh | 双摄4800万+1200万"
    },
    "iPhone 16 Pro / 16 Pro Max": {
        "iPhone 16 Pro": "A18 Pro(3nm) | 8GB RAM | 128/256/512GB/1TB | 6.3英寸OLED 2622x1206(120Hz) | 3582mAh | 三摄4800万+4800万+1200万5x+LiDAR",
        "iPhone 16 Pro Max": "A18 Pro(3nm) | 8GB RAM | 256/512GB/1TB | 6.9英寸OLED 2868x1320(120Hz) | 4685mAh | 三摄4800万+4800万+1200万5x+LiDAR"
    },
    "iPhone 17 / 17 Plus": {
        "iPhone 17": "A19(3nm) | 8GB RAM | 128/256/512GB | 6.1英寸OLED(120Hz LTPO) | 约3800mAh | 双摄4800万+1200万",
        "iPhone 17 Plus": "A19(3nm) | 8GB RAM | 128/256/512GB | 6.7英寸OLED(120Hz LTPO) | 约4800mAh | 双摄4800万+1200万"
    },
    "iPhone 17 Pro / 17 Pro Max": {
        "iPhone 17 Pro": "A19 Pro(3nm) | 10GB RAM | 256/512GB/1TB | 6.3英寸OLED(120Hz LTPO)屏下Face ID | 约3800mAh | 三摄4800万+4800万+4800万5x+LiDAR",
        "iPhone 17 Pro Max": "A19 Pro(3nm) | 10GB RAM | 256/512GB/1TB/2TB | 6.9英寸OLED(120Hz LTPO)屏下Face ID | 约4900mAh | 三摄4800万+4800万+4800万5x+LiDAR"
    },
}

# ========== Android 全系参数 ==========
ANDROID_SPECS = {
    # ------ Xiaomi ------
    "Xiaomi 15 Pro": "骁龙8 Elite(3nm) | 12/16GB LPDDR5X | 256/512GB/1TB UFS4.0 | 6.73英寸LTPO AMOLED等深四曲屏3200x1440 1-120Hz | 6100mAh+90W | 徕卡三摄5000万+5000万+5000万5倍潜望",
    "Xiaomi 15 Ultra": "骁龙8 Elite(3nm) | 16GB LPDDR5X | 512GB/1TB UFS4.0 | 6.73英寸LTPO AMOLED等深四曲屏3200x1440 1-120Hz | 6000mAh+90W | 徕卡四摄1英寸5000万+5000万+5000万3倍+5000万5倍",
    "Xiaomi 14 Pro": "骁龙8 Gen3(4nm) | 12/16GB LPDDR5X | 256/512GB/1TB UFS4.0 | 6.73英寸LTPO AMOLED微曲屏3200x1440 1-120Hz | 4880mAh+120W | 徕卡三摄5000万+5000万+5000万3.2倍",
    "Xiaomi 14 Ultra": "骁龙8 Gen3(4nm) | 16GB LPDDR5X | 512GB/1TB UFS4.0 | 6.73英寸LTPO AMOLED微曲屏3200x1440 1-120Hz | 5300mAh+90W | 徕卡四摄1英寸LYT-900+5000万+5000万3.2倍+5000万5倍",
    "Xiaomi 13 Pro": "骁龙8 Gen2(4nm) | 8/12GB LPDDR5X | 128/256/512GB UFS4.0 | 6.73英寸LTPO AMOLED微曲屏3200x1440 1-120Hz | 4820mAh+120W | 徕卡三摄5000万+5000万+5000万3.2倍",
    "Xiaomi 13 Ultra": "骁龙8 Gen2(4nm) | 12/16GB LPDDR5X | 256/512GB/1TB UFS4.0 | 6.73英寸LTPO AMOLED微曲屏3200x1440 1-120Hz | 5000mAh+90W | 徕卡四摄1英寸IMX989+5000万+5000万3.2倍+5000万5倍",
    "Xiaomi 12 Pro": "骁龙8 Gen1(4nm) | 8/12GB LPDDR5 | 128/256GB UFS3.1 | 6.73英寸LTPO AMOLED微曲屏3200x1440 1-120Hz | 4600mAh+120W | 三摄5000万+5000万+5000万2倍",
    "Xiaomi 12S Ultra": "骁龙8+ Gen1(4nm) | 8/12GB LPDDR5 | 256/512GB UFS3.1 | 6.73英寸LTPO AMOLED微曲屏3200x1440 1-120Hz | 4860mAh+67W | 徕卡三摄1英寸IMX989+4800万+4800万5倍",
    "Redmi K80 Pro": "骁龙8 Gen3(4nm) | 12/16GB LPDDR5X | 256/512GB UFS4.0 | 6.67英寸OLED直屏3200x1440 120Hz | 6000mAh+120W | 三摄5000万+800万+200万",
    "Redmi K70 Pro": "骁龙8 Gen3(4nm) | 12/16/24GB LPDDR5X | 256/512GB/1TB UFS4.0 | 6.67英寸OLED直屏3200x1440 120Hz | 5000mAh+120W | 三摄5000万+1200万+5000万2倍",
    "Redmi K60 Ultra": "天玑9200+(4nm) | 12/16GB LPDDR5X | 256/512GB/1TB UFS4.0 | 6.67英寸OLED直屏2712x1220 144Hz | 5000mAh+120W | 三摄5000万+800万+200万",
    "Redmi Note 14 Pro+": "天玑7350(4nm) | 8/12GB LPDDR4X | 256/512GB UFS2.2 | 6.67英寸OLED微曲屏2712x1220 120Hz | 5000mAh+120W | 三摄2亿+800万+200万",
    "Redmi Note 13 Pro+": "天玑7200 Ultra(4nm) | 8/12GB LPDDR5 | 256/512GB UFS3.1 | 6.67英寸OLED微曲屏2712x1220 120Hz | 5000mAh+120W | 三摄2亿HP3+800万+200万",
    "Redmi Note 12 Turbo": "骁龙7+ Gen2(4nm) | 8/12/16GB LPDDR5 | 256/512GB/1TB UFS3.1 | 6.67英寸OLED直屏2400x1080 120Hz | 5000mAh+67W | 三摄6400万+800万+200万",
    "Xiaomi 17 Pro": "骁龙8 Elite 2(3nm) | 16GB LPDDR5X | 256/512GB/1TB UFS4.1 | 6.73英寸LTPO AMOLED等深四曲屏3200x1440 1-144Hz | 6500mAh+100W | 徕卡三摄5000万+5000万+5000万5倍",
    "Xiaomi 17 Ultra": "骁龙8 Elite 2(3nm) | 16GB LPDDR5X | 512GB/1TB UFS4.1 | 6.73英寸LTPO AMOLED等深四曲屏3200x1440 1-144Hz | 6500mAh+100W | 徕卡四摄1英寸+5000万+5000万3倍+5000万5倍",

    # ------ Samsung ------
    "Samsung Galaxy S25 Ultra": "骁龙8 Elite for Galaxy(3nm) | 12/16GB LPDDR5X | 256/512GB/1TB | 6.9英寸Dynamic AMOLED 2X直屏3120x1440 1-120Hz | 5000mAh+45W | 四摄2亿+5000万+5000万3倍+5000万5倍+S Pen",
    "Samsung Galaxy S25+": "骁龙8 Elite for Galaxy(3nm) | 12GB LPDDR5X | 256/512GB | 6.7英寸Dynamic AMOLED 2X直屏3120x1440 1-120Hz | 4900mAh+45W | 三摄5000万+1200万+1000万3倍",
    "Samsung Galaxy S24 Ultra": "骁龙8 Gen3 for Galaxy(4nm) | 12GB LPDDR5X | 256/512GB/1TB | 6.8英寸Dynamic AMOLED 2X直屏3120x1440 1-120Hz | 5000mAh+45W | 四摄2亿HP2+1200万+1000万3倍+5000万5倍+S Pen",
    "Samsung Galaxy S24+": "骁龙8 Gen3 for Galaxy(4nm) | 12GB LPDDR5X | 256/512GB | 6.7英寸Dynamic AMOLED 2X直屏3120x1440 1-120Hz | 4900mAh+45W | 三摄5000万+1200万+1000万3倍",
    "Samsung Galaxy S23 Ultra": "骁龙8 Gen2 for Galaxy(4nm) | 8/12GB LPDDR5X | 256/512GB/1TB | 6.8英寸Dynamic AMOLED 2X微曲屏3088x1440 1-120Hz | 5000mAh+45W | 四摄2亿HP2+1200万+1000万3倍+1000万10倍+S Pen",
    "Samsung Galaxy S23+": "骁龙8 Gen2 for Galaxy(4nm) | 8GB LPDDR5X | 256/512GB | 6.6英寸Dynamic AMOLED 2X直屏2340x1080 120Hz | 4700mAh+45W | 三摄5000万+1200万+1000万3倍",
    "Samsung Galaxy S22 Ultra": "骁龙8 Gen1(4nm) | 8/12GB LPDDR5 | 128/256/512GB/1TB | 6.8英寸Dynamic AMOLED 2X微曲屏3088x1440 1-120Hz | 5000mAh+45W | 四摄1.08亿+1200万+1000万3倍+1000万10倍+S Pen",
    "Samsung Galaxy S22+": "骁龙8 Gen1(4nm) | 8GB LPDDR5 | 128/256GB | 6.6英寸Dynamic AMOLED 2X直屏2340x1080 120Hz | 4500mAh+45W | 三摄5000万+1200万+1000万3倍",
    "Samsung Galaxy Z Fold6": "骁龙8 Gen3 for Galaxy(4nm) | 12GB LPDDR5X | 256/512GB/1TB | 7.6英寸内屏2160x1856 120Hz + 6.3英寸外屏 | 4400mAh+25W | 三摄5000万+1200万+1000万3倍",
    "Samsung Galaxy Z Flip6": "骁龙8 Gen3 for Galaxy(4nm) | 12GB LPDDR5X | 256/512GB | 6.7英寸内屏2640x1080 120Hz + 3.4英寸外屏 | 4000mAh+25W | 双摄5000万+1200万",
    "Samsung Galaxy A55": "Exynos 1480(4nm) | 8GB LPDDR5 | 128/256GB | 6.6英寸Super AMOLED直屏2340x1080 120Hz | 5000mAh+25W | 三摄5000万+1200万+500万",

    # ------ Huawei ------
    "Huawei Pura 80 Ultra": "麒麟9010(7nm) | 16GB | 512GB/1TB | 6.8英寸LTPO OLED等深四曲屏2844x1260 1-120Hz | 5400mAh+100W | 四摄5000万+5000万+5000万3.5倍+5000万10倍潜望",
    "Huawei Pura 70 Ultra": "麒麟9010(7nm) | 16GB | 512GB/1TB | 6.8英寸LTPO OLED等深四曲屏2844x1260 1-120Hz | 5200mAh+100W | 伸缩主摄5000万1英寸+4000万+5000万3.5倍潜望",
    "Huawei Pura 70 Pro": "麒麟9010(7nm) | 12/16GB | 256/512GB/1TB | 6.8英寸LTPO OLED等深四曲屏2844x1260 1-120Hz | 5050mAh+100W | 三摄5000万+1250万+4800万3.5倍潜望",
    "Huawei Mate 70 Pro": "麒麟9100(7nm) | 16GB | 256/512GB/1TB | 6.9英寸LTPO OLED等深四曲屏2832x1316 1-120Hz | 5500mAh+100W | 四摄5000万+4000万+5000万3.5倍+5000万5倍",
    "Huawei Mate 60 Pro": "麒麟9000S(7nm) | 12GB | 256/512GB/1TB | 6.82英寸LTPO OLED等深四曲屏2720x1260 1-120Hz | 5000mAh+88W | 三摄5000万+1200万+4800万3.5倍潜望",
    "Huawei Mate 60 RS Ultimate": "麒麟9000S(7nm) | 16GB | 512GB/1TB | 6.82英寸LTPO OLED等深四曲屏2720x1260 1-120Hz陶瓷机身 | 5000mAh+88W | 三摄4800万+4000万+4800万3.5倍潜望",
    "Huawei P60 Pro": "骁龙8+ Gen1(4nm) | 8/12GB | 256/512GB | 6.67英寸LTPO OLED微曲屏2700x1220 1-120Hz昆仑玻璃 | 4815mAh+88W | 三摄4800万+1300万+4800万3.5倍潜望",
    "Huawei Mate 50 Pro": "骁龙8+ Gen1(4nm) | 8GB | 256/512GB | 6.74英寸OLED微曲屏2616x1212 120Hz昆仑玻璃刘海屏 | 4700mAh+66W | 三摄5000万+1300万+6400万3.5倍潜望",
    "Huawei Nova 12 Ultra": "麒麟9000SL(7nm) | 12GB | 512GB/1TB | 6.76英寸OLED等深四曲屏2776x1224 120Hz昆仑玻璃 | 4600mAh+100W | 双摄5000万+800万+前置6000万+800万",

    # ------ Vivo ------
    "Vivo X200 Pro": "天玑9400(3nm) | 12/16GB LPDDR5X | 256/512GB/1TB UFS4.0 | 6.78英寸LTPO AMOLED等深四曲屏2800x1260 1-120Hz | 6000mAh+90W | 三摄5000万+5000万+2亿像素蔡司APO长焦",
    "Vivo X200 Ultra": "骁龙8 Elite(3nm) | 16GB LPDDR5X | 512GB/1TB UFS4.0 | 6.78英寸LTPO AMOLED等深四曲屏2K 1-120Hz | 6000mAh+90W | 三摄5000万+5000万+2亿像素蔡司长焦+V5芯片",
    "Vivo X100 Pro": "天玑9300(4nm) | 12/16GB LPDDR5X | 256/512GB/1TB UFS4.0 | 6.78英寸LTPO AMOLED微曲屏2800x1260 1-120Hz | 5400mAh+100W | 三摄5000万+5000万+5000万4.3倍潜望+V3芯片",
    "Vivo X90 Pro+": "骁龙8 Gen2(4nm) | 12GB LPDDR5X | 256/512GB UFS4.0 | 6.78英寸LTPO AMOLED微曲屏3200x1440 1-120Hz | 4700mAh+80W | 四摄5000万+4800万+5000万2倍+6400万3.5倍+V2芯片",
    "Vivo X80 Pro": "天玑9000(4nm) | 8/12GB LPDDR5 | 256/512GB UFS3.1 | 6.78英寸LTPO AMOLED微曲屏3200x1440 1-120Hz | 4700mAh+80W | 四摄5000万+4800万+1200万2倍+800万5倍+V1+芯片",
    "iQOO 14": "骁龙8 Elite 2(3nm) | 12/16GB LPDDR5X | 256/512GB/1TB UFS4.1 | 6.82英寸LTPO AMOLED直屏2K 1-144Hz | 6200mAh+120W | 三摄5000万+5000万+5000万3倍潜望+Q5芯片",
    "iQOO 13": "骁龙8 Elite(3nm) | 12/16GB LPDDR5X | 256/512GB/1TB UFS4.0 | 6.82英寸LTPO AMOLED直屏2K 1-144Hz | 6150mAh+120W | 三摄5000万+5000万+5000万2倍+Q4芯片",
    "iQOO 12": "骁龙8 Gen3(4nm) | 12/16GB LPDDR5X | 256/512GB/1TB UFS4.0 | 6.78英寸LTPO AMOLED直屏2800x1260 144Hz | 5000mAh+120W | 三摄5000万+5000万+6400万3倍潜望+Q1芯片",
    "Vivo S20 Pro": "天玑9300+(4nm) | 8/12/16GB LPDDR5X | 256/512GB UFS4.0 | 6.67英寸AMOLED微曲屏2800x1260 120Hz | 5500mAh+90W | 三摄5000万+5000万+5000万2倍+前置5000万双柔光",
    "Vivo S19 Pro": "天玑9200+(4nm) | 8/12GB LPDDR5X | 256/512GB UFS3.1 | 6.78英寸AMOLED微曲屏2800x1260 120Hz | 5500mAh+80W | 三摄5000万+800万+5000万2倍+前置5000万柔光",

    # ------ Oppo ------
    "Oppo Find X9 Pro": "骁龙8 Elite 2(3nm) | 16GB LPDDR5X | 256/512GB/1TB UFS4.1 | 6.78英寸LTPO AMOLED等深四曲屏2K 1-120Hz | 6000mAh+100W | 四摄5000万+5000万+5000万3倍+5000万6倍潜望+V5芯片",
    "Oppo Find X8 Pro": "天玑9400(3nm) | 12/16GB LPDDR5X | 256/512GB/1TB UFS4.0 | 6.78英寸LTPO AMOLED等深四曲屏2780x1264 1-120Hz | 5910mAh+80W | 四摄5000万+5000万+5000万3倍+5000万6倍潜望",
    "Oppo Find X8 Ultra": "骁龙8 Elite(3nm) | 16GB LPDDR5X | 256/512GB/1TB UFS4.0 | 6.82英寸LTPO AMOLED等深四曲屏2K 1-120Hz | 6000mAh+100W | 四摄5000万+5000万+5000万3倍+5000万6倍潜望",
    "Oppo Find X7 Ultra": "骁龙8 Gen3(4nm) | 12/16GB LPDDR5X | 256/512GB/1TB UFS4.0 | 6.82英寸LTPO AMOLED微曲屏3168x1440 1-120Hz | 5000mAh+100W | 四摄5000万+5000万+5000万3倍+5000万6倍潜望+V3芯片",
    "Oppo Find X6 Pro": "骁龙8 Gen2(4nm) | 12/16GB LPDDR5X | 256/512GB UFS4.0 | 6.82英寸LTPO AMOLED微曲屏3168x1440 1-120Hz | 5000mAh+100W | 三摄5000万+5000万+5000万3倍潜望+马里亚纳X芯片",
    "Oppo Reno 13 Pro": "天玑8350(4nm) | 12/16GB LPDDR5X | 256/512GB UFS3.1 | 6.83英寸AMOLED等深四曲屏2800x1272 120Hz | 5800mAh+80W | 三摄5000万+800万+5000万2倍+前置5000万",
    "Oppo Reno 12 Pro": "天玑9200+ Star(4nm) | 12/16GB LPDDR5X | 256/512GB UFS3.1 | 6.7英寸AMOLED微曲屏2412x1080 120Hz | 4700mAh+80W | 三摄5000万+800万+5000万2倍+前置5000万",
    "OnePlus 13": "骁龙8 Elite(3nm) | 12/16/24GB LPDDR5X | 256/512GB/1TB UFS4.0 | 6.82英寸LTPO AMOLED等深四曲屏3168x1440 1-120Hz | 6000mAh+100W | 三摄5000万+5000万+5000万3倍潜望+哈苏",
    "OnePlus 12": "骁龙8 Gen3(4nm) | 12/16/24GB LPDDR5X | 256/512GB/1TB UFS4.0 | 6.82英寸LTPO AMOLED微曲屏3168x1440 1-120Hz | 5400mAh+100W | 三摄5000万+4800万+6400万3倍潜望+哈苏",
    "OnePlus Open": "骁龙8 Gen3(4nm) | 16GB LPDDR5X | 512GB UFS4.0 | 7.82英寸内屏2268x2440 120Hz + 6.31英寸外屏 | 4805mAh+67W | 三摄4800万+4800万+6400万3倍潜望+哈苏",
}


# ========== 执行更新 ==========
with open('data/knowledge.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

added = 0
for brand in data['brands']:
    for model in brand['models']:
        name = model['name']
        # 确定参数文本
        spec = None
        raw_spec = None
        if brand['name'] == 'Apple':
            if name in APPLE_SPECS:
                raw_spec = APPLE_SPECS[name]
            else:
                for key, val in APPLE_SPECS.items():
                    if name.startswith(key[:6]) or key.startswith(name[:6]):
                        raw_spec = val
                        break
        else:
            if name in ANDROID_SPECS:
                raw_spec = ANDROID_SPECS[name]

        if raw_spec:
            # 格式化为每行一个参数
            if isinstance(raw_spec, dict):
                lines = []
                for variant_name, variant_spec in raw_spec.items():
                    parts = [p.strip() for p in variant_spec.split('|')]
                    labels = ['处理器', '内存', '存储', '屏幕', '电池+充电', '摄像头']
                    lines.append(f'**{variant_name}**')
                    for i, part in enumerate(parts):
                        lbl = labels[i] if i < len(labels) else f'参数{i+1}'
                        lines.append(f'{lbl}：{part}')
                    lines.append('')
                spec_text = '\n'.join(lines).strip()
            else:
                parts = [p.strip() for p in raw_spec.split('|')]
                labels = ['处理器', '内存', '存储', '屏幕', '电池+充电', '摄像头']
                spec_text = ''
                for i, part in enumerate(parts):
                    lbl = labels[i] if i < len(labels) else f'参数{i+1}'
                    spec_text += f'{lbl}：{part}\n'
                spec_text = spec_text.strip()

            spec_item = {
                "category": "手机参数",
                "description": spec_text,
                "special_note": "请核对以上参数与卖家描述是否一致。存储容量和颜色版本会影响二手价格。",
                "compare_img": ""
            }
            model['check_points'].insert(0, spec_item)
            added += 1
            print(f'  OK: {brand["name"]} {name}')
        else:
            print(f'  MISSING: {brand["name"]} {name}')

with open('data/knowledge.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nTotal: {added} models updated with specs')
