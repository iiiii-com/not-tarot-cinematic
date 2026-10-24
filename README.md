# NOT TAROT — 45s 交互电影（ANTIQUE PLATE 版）

一支「反塔罗」的品牌短片：不预测命运，只交还解释权。全片只有一个墨点，从落地写成心电图，破成心脏，散成符号，收成一张牌，最后落成一个词。

- **在线观看**：<https://iiiii-com.github.io/not-tarot-cinematic/>（GitHub Pages，浏览器直接播放）
- **交互电影单文件**：[`07_final/NOT_TAROT_45s_cinematic.html`](07_final/NOT_TAROT_45s_cinematic.html)（2.73 MB，离线可播，内嵌 16 款字体（含中文子集）与 150 张蚀刻图标）
- **成片**：[16:9 主片](07_final/master_16x9.mp4) · [9:16 社媒版](07_final/social_9x16.mp4)

## 这是什么

旧版播放器被整体拆除重写为「古籍图版 / 博物馆藏版」语言：程序生成的纸张纤维与油墨压痕、24fps 胶片颗粒、持续图版框架（双线框、四角套准十字、页眉页脚、图号、斜体图注、页码）。七张图版组成叙事：

| 图版 | 场景 |
|---|---|
| I · 心（HEART） | 一滴墨落地 → 心电图 → 解剖心脏 |
| II · 符号（THE SIGNS） | 心裂 → 浑天仪符号环 |
| III · 世界（THE WORLD） | 手绘蚀刻巨眼（瞳孔跟随指针、眨眼） |
| IV · 牌（THE DECK） | 唯一的黑场：墨洪 → 撕口 → 盲压印卡 |
| V · 抽牌（SIX CARDS） | 六张牌依次抽出，中文义句为主、英文义句为辅 |
| VI · 印记（THE TOTEM） | 金环 totem → 曼陀罗 morph |
| VII · 名（THE NAME） | NOT TAROT + 意义，由你自己给。 |

## 装饰层（2026-10 decor pass）

在七图版之外新增独立装饰层 `decor.css` / `decor.js`（不改场景结构，只做加法，全部由时间决定、抽帧可复现）：

- **全局版画装置**：四角花饰（明暗幕自动反转）+ 右上圆形 plate-stamp 版画印章（每图版开始 1.55s 内浮现）。
- **逐幕增补**：I 轨道圈/飞溅墨点/「THE FALL」卡尺 · II 雕版校准网格 + 心跳脉冲环 + 72 BPM 卡尺 · III 外虚线圈 + 18 枚罗马数字 + SCALE 卡尺 · IV 黑版骨色角饰 + 卡面套准十字 · V 双轨道圈 + INDEX 卡片导航 · VI 12 辐条 + 罗马数字 · VII 24 花瓣环 + 反向旋转虚线环 · VIII 花饰 cartouche + COLOPHON + EDITION 版记。
- **符号释义浮签**：III / VI / VII 三幕符号悬停显示 `SIGN · 罗马数字 / 拉丁名 / 英文释义`。

## 文字系统（2026-10 textfx pass）

- **中文为主、英文为辅**：标题/正文/说明全部中文；`NOT TAROT` 品牌字标、拉丁学名（COR、PAPILIO…）、图号 `FIG.`、版次与数字保留拉丁。中文为构建时内嵌的 Noto Serif SC 子集（400/600，按全片 368 字裁切，共 ~137 KB），不依赖读者系统字体。
- **错版墨色**：每个标题在正字下面再印两遍同字——绯色与金色，各偏 2–4 px，用 `-webkit-text-stroke` 勾成空心轮廓。远看是印刷错位的彩色边缘，近看是三层独立的字。
- **变色**：页脚注每 2.4 秒换一种墨；标题错版轮廓每 2.7 秒交换两色；品牌字每 3.4 秒换一组；卡片名按当前牌换墨。全部由电影时间驱动，抽帧确定可复现。
- **3D 偏色**：指针移动时三层字按深度差反向位移；悬停时两遍错版向外拉开并加粗轮廓；点击有一次压印回弹。
- **3D 立体**：双层 `text-shadow` 浮雕压在纸面上，标题所在文字栏整列跟随指针做 perspective 微旋转。

## 动态系统（2026-10 motion pass）

- **元素微动**：角饰/边注/卡尺呼吸，墨点漂浮，印章自旋，曼陀罗花瓣环与反向虚线环转动，符号轻微浮动（只动画 translate/rotate/scale 独立属性）。
- **3D 动态**：整张版画框随指针做 perspective 3D 视差与位移，换版有「压版」脉冲；场景画层 ±1° 微倾 + 慢漂移；印章 3D 摆动；标本格悬停成玻璃片。
- **色彩错插**：图版双线框、三幕大圆环、印章与花饰框以「绯 + 金」两层 drop-shadow 错版分离，偏移由指针 + 时间起伏 + 换版脉冲驱动（静止 1–3 px，换版瞬间 6–9 px）。
- **开关**：`X` 一键关闭/开启动态与错插；`prefers-reduced-motion` 自动降级；抽帧用负 animation-delay 定格，任意 t 可复现。

## 交互

拖墨滴开场 · `Space` 播放/暂停 · `←/→` ±2s · `Home` 首帧 · `M` 静音 · `F` 全屏 · `?` 帮助 · `Esc` 关闭浮层 · `1`–`7` 直达图版
可拖时间轴 + 7 个章节墨点 · 卡牌点击 3D 翻面、悬停倾斜、滚轮抽牌 · 左侧 INDEX 导航点任意行跳至该卡 · 符号悬停释义 · 长按 220ms 呼吸慢放（0.34×） · 指针视差 · 纸面点击墨晕 · 42s 后可抽「你自己的牌」并导出 900×1280 PNG · 双击标题重印一次 · `[`/`]` 调错版强度 · `C` 开关错版色彩 · `X` 开关动态（3D 视差 / 色彩错插 / 元素微动）。

URL 参数：`?t=12.5` 定位到秒 · `?capture=1` 纯画面 · `?vertical=1` 竖屏框。

## 目录

```
07_final/           成片与交互电影（交付物）
03_assets/
  symbols/sprites/  25 个原始蚀刻图标（构建输入）
  fonts/            woff2 字体（构建输入，SIL OFL / Apache 2.0）
  keyframes/        验收静帧 + 海报 + 联排图
01_style_bible/     色板、字号、版式规则（closed palette，V01–V12 硬约束）
02_storyboard/      分镜表与创意方向（ONE INK 概念、转场与交互规范）
_tools/
  build_cinematic_v4.py   构建脚本
  v4src/                  源文件（shell.html + css + js，18 个，含 decor 装饰层 / 中文排版 zh.css / 错版文字层 textfx / motion 动态层）
  shot_server.py / shot_client.py / cdp_shot.mjs   无头浏览器抽帧与交互测试
```

## 重新构建

```bash
python _tools/build_cinematic_v4.py
# → 07_final/NOT_TAROT_45s_cinematic.html
# 依赖：Pillow；可选 --out / --force-textures
# 纸纹、颗粒、晕影、墨迹均在构建时由 PIL 生成，不依赖外部贴图
```

## 说明

- 交互音效为 WebAudio 合成（心跳、翻纸、落墨、铃），首次交互后启动；`prefers-reduced-motion` 下自动降级。
- `?vertical=1` 目前是 16:9 居中放映框；正式 9:16 成片走 `social_9x16.mp4` 流水线。
- 字体：Cormorant Garamond / EB Garamond / Playfair Display / Jost / IM Fell English SC / Pinyon Script / Noto Serif SC（中文子集），均来自 Google Fonts，遵循各自开源许可。
