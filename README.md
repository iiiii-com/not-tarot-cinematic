# NOT TAROT — 45s 交互电影（ANTIQUE PLATE 版）

一支「反塔罗」的品牌短片：不预测命运，只交还解释权。全片只有一个墨点，从落地写成心电图，破成心脏，散成符号，收成一张牌，最后落成一个词。

- **在线观看**：<https://iiiii-com.github.io/not-tarot-cinematic/>（GitHub Pages，浏览器直接播放）
- **交互电影单文件**：[`07_final/NOT_TAROT_45s_cinematic.html`](07_final/NOT_TAROT_45s_cinematic.html)（3.87 MB，离线可播，内嵌 14 款字体与 150 张蚀刻图标）
- **成片**：[16:9 主片](07_final/master_16x9.mp4) · [9:16 社媒版](07_final/social_9x16.mp4)

## 这是什么

旧版播放器被整体拆除重写为「古籍图版 / 博物馆藏版」语言：程序生成的纸张纤维与油墨压痕、24fps 胶片颗粒、持续图版框架（双线框、四角套准十字、页眉页脚、图号、斜体图注、页码）。七张图版组成叙事：

| 图版 | 场景 |
|---|---|
| I · 心（HEART） | 一滴墨落地 → 心电图 → 解剖心脏 |
| II · 符号（THE SIGNS） | 心裂 → 浑天仪符号环 |
| III · 世界（THE WORLD） | 手绘蚀刻巨眼（瞳孔跟随指针、眨眼） |
| IV · 牌（THE DECK） | 唯一的黑场：墨洪 → 撕口 → 盲压印卡 |
| V · 抽牌（SIX CARDS） | 六张牌依次抽出，每张一句英文牌义 |
| VI · 印记（THE TOTEM） | 金环 totem → 曼陀罗 morph |
| VII · 名（THE NAME） | NOT TAROT + 意义，由你自己给。 |

## 装饰层（2026-10 decor pass）

在七图版之外新增独立装饰层 `decor.css` / `decor.js`（不改场景结构，只做加法，全部由时间决定、抽帧可复现）：

- **全局版画装置**：四角花饰（明暗幕自动反转）+ 右上圆形 plate-stamp 版画印章（每图版开始 1.55s 内浮现）。
- **逐幕增补**：I 轨道圈/飞溅墨点/「THE FALL」卡尺 · II 雕版校准网格 + 心跳脉冲环 + 72 BPM 卡尺 · III 外虚线圈 + 18 枚罗马数字 + SCALE 卡尺 · IV 黑版骨色角饰 + 卡面套准十字 · V 双轨道圈 + INDEX 卡片导航 · VI 12 辐条 + 罗马数字 · VII 24 花瓣环 + 反向旋转虚线环 · VIII 花饰 cartouche + COLOPHON + EDITION 版记。
- **符号释义浮签**：III / VI / VII 三幕符号悬停显示 `SIGN · 罗马数字 / 拉丁名 / 英文释义`。

## 文字系统（2026-10 textfx pass）

- **纯英文排印**：全片只有英文——`NOT TAROT` 字标、拉丁学名（COR、PAPILIO…）、图号 `FIG.`、版次与数字。所有中文（花体小注、牌义中文句、符号中文释义、帮助与提示文案）已在 2026-10 的 english pass 中全部移除。
- **错版墨色**：每个标题在正字下面再印两遍同字——绯色与金色，各偏 2–4 px，用 `-webkit-text-stroke` 勾成空心轮廓。远看是印刷错位的彩色边缘，近看是三层独立的字。
- **变色**：页脚注每 2.4 秒换一种墨；标题错版轮廓每 2.7 秒交换两色；品牌字每 3.4 秒换一组；卡片名按当前牌换墨。全部由电影时间驱动，抽帧确定可复现。
- **3D 偏色**：指针移动时三层字按深度差反向位移；悬停时两遍错版向外拉开并加粗轮廓；点击有一次压印回弹。
- **3D 立体**：双层 `text-shadow` 浮雕压在纸面上，标题所在文字栏整列跟随指针做 perspective 微旋转。

## 动态系统（2026-10 motion pass）

- **元素微动**：角饰/边注/卡尺呼吸，墨点漂浮，印章自旋，曼陀罗花瓣环与反向虚线环转动，符号轻微浮动（只动画 translate/rotate/scale 独立属性）。
- **3D 动态**：整张版画框随指针做 perspective 3D 视差与位移，换版有「压版」脉冲；场景画层 ±1° 微倾 + 慢漂移；印章 3D 摆动；标本格悬停成玻璃片。
- **色彩错插**：图版双线框、三幕大圆环、印章与花饰框以「绯 + 金」两层 drop-shadow 错版分离，偏移由指针 + 时间起伏 + 换版脉冲驱动（静止 1–3 px，换版瞬间 6–9 px）。
- **开关**：`X` 一键关闭/开启动态与错插；`prefers-reduced-motion` 自动降级；抽帧用负 animation-delay 定格，任意 t 可复现。

## 冷开场钩子 v4「OCULUS · 单行」（2026-10 english pass · 取代 v3）

前 3.78 秒独立冷开场层 `hook.css` + `hook.js`（挂在舞台最上层，不改动七图版场景源），全部由电影时间 t 计算，`?capture=1` 抽帧可复现。
三案融合：**D 满幅雕版巨眼** + **C 纸的撕裂** + **A 第一拍心电脉冲**。v3 在 1.3 秒里塞了四组文案导致英文互相叠压，v4 只留**一行**大字，并把节奏拉长到 3.78 秒做成五段式。

| 时间 | 动作 |
|---|---|
| 0.00 | 黑场静置（低频先响） |
| 0.34 | 四角框线与十字准星生长 |
| 0.52–1.90 | 绯色心电线自左向右描绘（2.2px + 发光，另一层莓色重影） |
| 1.00 / 1.34 | 两记心跳（画面 jolt + 色差抖动） |
| 1.90–2.18 | 线收走，回到黑场，留一口气 |
| 2.16–2.86 | 纸面自下升起（`translateY 104% → 0`） |
| 2.34–3.02 | 满幅雕版巨眼显影，虹膜四层环与瞳孔分层入场 |
| 2.88–3.12 | 唯一一行大字 `THIS IS NOT TAROT` 落位（Playfair 700 · 118px） |
| 3.02 | 第三记心跳（这一次在纸上） |
| 3.12–3.46 | 完全静止的呼吸段 |
| 3.46–3.78 | 撕裂揭示：上壳层沿 13 点折线撕开，露出已运行的图版 I |
| 3.78 | 图版 I 接管 |

- **撕裂即交接**：`clipFor(open)` 生成 13 点 `polygon()`，上壳层只保留撕线上方，撕开就直接露出下一层，不做淡化。撕口带 74px 模糊黑影 + 骨色 1.2px + 莓色 2.0px 双描边。
- **单行不叠字**：kick 行 `A FILM IN SEVEN PLATES ◆ ONE QUESTION` 独占 top 188，大字独占 top 300，两者垂直间隔 90px 以上；旧版的 `SCROLL AWAY`、花体「别划走」、下壳层 `THIS IS NOT TAROT` 三组文案整体删除。
- **音效 11 cue**：框线 tick / 描线 whoosh / 三次心跳 thump（46·54·42 Hz）/ 纸升 whoosh / 压印 / 撕裂 whoosh / 铃（196 Hz），与画面 beat 对齐。

## 全片去中文（2026-10 english pass）

- 删除 **108 处** `<i class="hz">` 花体中文小注、`SIGN_ZH` 中文映射、`NAMES` 第三项中文释义、`CARDS` 的 `zh` 字段、`PLATES` 的 `zh`/`capZh`、`STAMPS` 第四字段，以及 poster / drawer / help / toast / 导出卡片 canvas 里的全部中文。
- `zh.css` 退场，Google Fonts 的 `Ma Shan Zheng` 与 `Noto Serif SC` 两种字体移出构建：字体 17 → **14 款**，体积 4.26 MB → **3.87 MB**。
- 构建产物扫描确认 **0 个 CJK 字符**。

## 图案填充文字（2026-10 patfx pass）

- **文字穿上图案**：12 处主标题克隆出 `.pat-layer`，用 `background-clip:text` 把蚀刻图案填进字里（默认 .13 呼吸、悬停 .34）。悬停任一符号 → 当幕主标题的图案填充换成该符号版画；卡名跟牌换图案，`BECOME.` 每 0.55s 换一个符号。
- 全部由 t 与指针决定，抽帧可复现。

## 转场层（2026-10 trans pass）

11 个幕切点各配一种因果式手势（**不是**整场透明度交叉淡化）：`shut` 纸帘对合 / `bloom` 莓色径向晕开（金色变体用于曼陀罗）/ `rule` 发丝线横扫 / `ink` 墨淌自下缘升起 / `motes` 16 粒确定性浮尘 / `dip`（22.0s 专用：先入黑，换幕在黑里完成再放亮）。外加全程晕影在切点前后加深。每处都做过 0.1s 步长密度抽帧验证：`dMean` 平滑、`dInk` 无突变。

## 交互

拖墨滴开场 · `Space` 播放/暂停 · `←/→` ±2s · `Home` 首帧 · `M` 静音 · `F` 全屏 · `?` 帮助 · `Esc` 关闭浮层 · `1`–`7` 直达图版
可拖时间轴 + 7 个章节墨点 · 卡牌点击 3D 翻面、悬停倾斜、滚轮抽牌 · 左侧 INDEX 导航点任意行跳至该卡 · 符号悬停释义 · 长按 220ms 呼吸慢放（0.34×） · 指针视差 · 纸面点击墨晕 · 42s 后可抽「你自己的牌」并导出 900×1280 PNG · 双击标题重印一次 · `[`/`]` 调错版强度 · `C` 开关错版色彩 · `X` 开关动态（3D 视差 / 色彩错插 / 元素微动）。

开场 0–3.78s 冷开场钩子自动播放（黑场 → 心电描线 → 纸升眼现 → 一行字 → 撕裂揭示图版 I），任意 seek 回 0–3.78s 会重播，首帧可作封面。

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
  v4src/                  源文件（shell.html + css + js，含 decor 装饰层 / 错版文字层 textfx / motion 动态层 / 冷开场 hook 层 / trans 转场层 / patfx 图案填充层）
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
- 字体：Cormorant Garamond / EB Garamond / Playfair Display / Jost / IM Fell English SC / Pinyon Script，均来自 Google Fonts，遵循各自开源许可。

### 排版收口（type-fix）

- 图版 III 说明行改为标题落位后才淡入，避免与标题交叠。
- 图版 IX `BECOME.` 字标上提至 812px、花体注收紧行内，说明行完全分离。

### 英文版交付（english pass）

- 冷开场 3.78 秒五段式，只留一行 `THIS IS NOT TAROT`，不再叠字。
- 全片 0 个中文字符，14 款内嵌字体，构建 3.87 MB。
- 交付件 `07_final/NOT_TAROT_45s_cinematic.html` **3,869,780 B**，抽帧存于
  `03_assets/keyframes/cinematic_v4/english_oculus/`（18 帧 + 联排图）。
