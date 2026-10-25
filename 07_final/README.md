# 07_final — 45s 概念片（v6 · MAGAZINE / STICKER 版 · 细节修复）

## 文件
| 文件 | 内容 | 规格 |
|---|---|---|
| `NOT_TAROT_45s_v6.html` | 单文件交互电影播放器（离线可播） | 1.35 MB；11 页杂志排版 + 模切贴纸；图标为参考卡原像素提取（保留蚀刻排线）+ 矢量眼；内嵌 Cormorant Garamond / Jost 字体 |
| `master_16x9.mp4` | 主成片（横版） | 1920×1080 · 24fps · 45.000s · 1080 帧 · H.264 High@4.2 CRF16 · 8.24 MB · AAC 192k/48k |
| `social_9x16.mp4` | 社媒竖版 | 1080×1920 · 24fps · 45.000s · 1080 帧 · 7.19 MB · 独立竖版杂志排版 |

## 11 页结构
01 COVER 封面（冷开场）→ 02 CONTENTS 目录 → 03 FEATURE / THE HEART 特稿 → 04 THE INDEX 符号索引（4×4·16 个不同符号）→ 05 PULL QUOTE 大引文 → 06 THE STICKER SHEET 贴纸页（撕贴动画）→ 07 INTERLUDE 黑色插页 → 08 THE SEAL 金环曼陀罗 → 09 COLOPHON 版权页 → 10 BACK COVER 封底 → 11 END 尾页

## 播放器操作
- 双击 `NOT_TAROT_45s_v6.html`（Edge/Chrome）→ 点封面 "CLICK TO BEGIN · 点击开始"。
- `Space` 播放/暂停；`←`/`→` 前后 1 秒；底部 `01–11` 章节跳转；`SOUND ON/OFF` 环境声开关；`REPLAY` 重播。
- 窗口竖长时自动切换 9:16 版式；`?t=秒数` 可定位（如 `?t=23`）。

## v6 相对 v5 的修复
| 用户反馈 | v6 做法 |
|---|---|
| 图案模糊 / 图标糊成块 | 弃用 vtracer 矢量化图标；改为参考卡逐像素 alpha 提取的栅格图标（保留内部排线与蚀刻细节），仅做最小清洗与四色染色；超大「眼」改手绘矢量 SVG；渲染 DPR2 → Lanczos 下采样 |
| 特效错误 | 修复 barcode 只剩一根条；删除黑场文字频闪与孤立红点；修复印章页标题重叠；修图标居中 |
| 各内容糊在一起 | 取消双向 0.12s 交叉淡化，改「纸页擦除」转场（新页从上往下揭示 0.30s），上一页保持到被覆盖 |
| 排版松 / 字号小 | 封面改冷开场（标题 p=0 即全显）；目录加罗马数字+页标题+描述句；索引改 4×4 十六个不同符号、图标 128px、名称 12.5px；全片页脚 10px、kicker 12px |

## 制作链（可完全重跑）
1. `python _tools/make_icon_pack_v6.py` — 从 `03_assets/symbols/sprites/` 生成四色栅格图标到 `03_assets/symbols/sprites6/`。
2. `python _tools/patch_v6.py`（及 patch_v6b/c/d/e）— 由 v5 模板生成 `_tools/magazine_v6_template.html` 并就地修补。
3. `python _tools/build_v6_film.py` — 内嵌 96 个资源（栅格图标四色变体 + 矢量眼 + 手绘剪刀/花 + 字体 + 纸纹）→ `NOT_TAROT_45s_v6.html`。
4. `python _tools/review_v6.py` — Playwright/Edge 抽 20 帧目检 + contact sheet。
5. `python _tools/capture_v6.py both` — DPR2 逐帧截图（3840×2160 / 2160×3840，1080 帧/画幅）。
6. `python _tools/encode_v6.py` — ffmpeg Lanczos 降到 1080p + AAC → 两条 MP4。

## 文字系统（textfx pass · 2026-10）

- **中文为主、英文为辅**：标题/正文/说明全部中文；品牌字标 `NOT TAROT`、拉丁学名（COR、PAPILIO…）、图号 `FIG.`、版次与数字保留拉丁。中文用构建时内嵌的 Noto Serif SC 子集（400/600，按全片字符集裁切，共 ~137 KB），不依赖读者系统字体。
- **错版墨色（misregistration）**：每个标题在正字下方再印两遍同字——绯色与金色，各偏 2–4 px，用 `-webkit-text-stroke` 勾出空心轮廓。远看是印刷错位的彩色边缘，近看是三层独立的字。
- **变色**：页脚注 `#capT` 每 2.4 秒换一种墨（plum/berry/crimson/gold）；标题错版轮廓每 2.7 秒交换两色；品牌字每 3.4 秒换一组；卡片名按当前牌换墨。全部由电影时间驱动，抽帧结果确定。
- **3D 偏色**：指针移动时三层字按深度差反向位移（--mx/--my），桌面端形成轻微立体偏色；悬停时两遍错版向外拉开并加粗轮廓；点击有一次「压印回弹」。
- **3D 立体**：`text-shadow` 双层 emboss（金 + 绯）压在纸面上；标题所在文字栏整列跟随指针做 `perspective` 微旋转。
- **交互**：双击标题「重印」一次（REPRINT toast）；`[` / `]` 调错版强度 0.35×–2.4×；`C` 关闭/开启错版色彩；帮助面板（`?`）里列出这三项。
- 已知取舍：彩色墨字（绯/莓）的错版轮廓会稍柔，这是为了避免红字+红边糊成一团；深墨字轮廓更锐。

## 动态系统（motion pass · 2026-10）

在场景源与文字层之外再新增独立 `motion.css` + `motion.js`「动态层」，只做加法、全部由电影时间与指针决定（抽帧可复现）：
- **元素活起来**：装饰角饰/边注/卡尺呼吸，墨点飞溅漂浮，印章缓慢自旋，曼陀罗花瓣环与反向虚线环转动，六幕符号轻微上下浮动——只动画 `translate/rotate/scale` 独立属性，不与场景自带的 `transform` 打架。
- **3D 动态**：整个版画框 `#chrome` 成为一张有厚度的纸——指针移动时以 perspective 做 rotateX/rotateY 视差 + 位移，图版切换时有短促的「压版」脉冲；场景画层同时做 ±1° 级 3D 微倾与慢漂移；版画印章自带 3D 摆动；5×5 标本格悬停变成带透视的玻璃片。
- **色彩错插（chromatic misregistration）**：图版双线框、三幕大圆环、印章与花饰框都以「绯 + 金」两层 drop-shadow 做错版分离，偏移量由指针位置 + 缓慢起伏 + 换版脉冲共同驱动（换版瞬间可达 6–9 px，静止时 1–3 px），模拟三色印刷没对齐的物理感。
- **交互**：`X` 一键开关全部动态（`body.motion-off`，含 3D 与色彩错插，toast「动态已关闭 · STILL PLATE」）；`prefers-reduced-motion` 自动降级。
- **确定性**：capture 模式下所有循环动画暂停并用负 `animation-delay = -t` 把相位定格到影片时间，因此任意 t 的抽帧仍可复现。

## 已知边界（诚实清单）
- 这是 **高保真动态杂志（motion magazine）**，用于锁时长、节奏、构图、转场、声音；**不是最终 CG 成片**。正式发布前按 `04_prompts/` 生成正式素材替换。
- 声音是 numpy 合成的临时混音（心跳/翻页/撕纸/低频/铃），不是最终配乐。
- 卡片中文义句与文案为排版占位，最终以品牌文案为准。
- 逐帧渲染依赖本机 Edge + Playwright；重渲约 6–8 分钟。
- 旧版本归档于 `_archive/`（v5 的 HTML 与两条 MP4；v4 亦在）。


---

# NOT_TAROT_45s_cinematic.html — v2 重制版 · ANTIQUE PLATE（45s 交互电影 · hook pass）

单文件、离线可播的 45 秒交互电影（拆除 v2 旧播放器，重写为「古籍图版 / 博物馆藏版」语言）。

## 文件
| 文件 | 内容 | 规格 |
|---|---|---|
| `NOT_TAROT_45s_cinematic.html` | 交互电影播放器（自包含：16 款内嵌 woff2（含 Noto Serif SC 中文子集）+ 150 张蚀刻图标 + 程序生成纸纹/颗粒/晕影/墨迹 + 外部装饰层 + 错版墨色文字层 + 动态层 + 冷开场钩子层 v2「校样 · PROOF」） | 2.75 MB · 1920×1080 舞台自适应缩放 · 2026-10 hook v2 |
| `NOT_TAROT_45s_cinematic_hook1.html` | 上一版（冷开场 hook v1：黑场大字 + 对开；已弃用，仅存档对比） | 2.74 MB · 2026-10 |
| `NOT_TAROT_45s_cinematic_motion.html` | 上一版（中文 + 错版字效 + 动态层，无冷开场钩子） | 2.73 MB · 2026-10 |
| `NOT_TAROT_45s_cinematic_textfx.html` | 更早一版（中文 + 错版字效 pass，无动态层） | 2.71 MB · 2026-10 |
| `NOT_TAROT_45s_cinematic_decor.html` | 更早一版（装饰层 pass，无中文/错版文字层） | 2.50 MB · 2026-10 |

## 设计语言（相对旧 v2）
- 纸：程序生成暖米色纸纤维 + 斑点 + 手撕边，叠加极轻油墨压痕、胶片颗粒（24fps 抖动）、柔和晕影；关闭全部 mix-blend-mode，改为 alpha 正常合成，渲染稳定。
- 版：持续图版框架（双细线框 + 四角套准十字 + 页眉/页脚/图号/斜体图注/页码 + 罗马数字图版编号），全局 closed palette，标题 Cormorant Garamond、字标 Playfair Display、微标签 Jost、图注 EB Garamond Italic、铭文 IM Fell。
- 七图版：I 心跳（滴墨→心电图→解剖心 + EVERYTHING MEANS SOMETHING.）→ II 符号释出（心裂→浑天仪环 18 符号）→ III 世界（巨眼 SVG 手绘蚀刻，瞳孔跟随指针 + 眨眼）→ IV 黑版（墨洪→撕口→盲压印卡 + LII）→ V 六张抽卡（FEARLESS / LET GO / BECOME / SEE CLEARLY / CREATE / GET SHIT DONE，每张配英文义句 + 中文义句）→ VI 印记（金环 totem → 曼陀罗 morph + BECOME.）→ VII 名义（NOT TAROT + MAKE YOUR OWN MEANING. + 印章）。
- 转场全部「因果式」：墨扩散、纸页交替、心跳推镜、卡片抽出、光圈收缩；无整场透明度交叉淡化。

## 装饰层（decor pass · 2026-10 增强）
在场景源之外新增独立 `decor.css` + `decor.js`「外部装饰层」，不改动原七图版结构，只做加法，全部由时间 t 决定（抽帧可复现）：
- **全局版画装置**：chrome 四角花饰（明暗幕自动反转色）、右上圆形 plate-stamp 版画印章（每个图版开始后 1.55s 内浮现，黑版用骨色反色版）。
- **I 心跳**：双轨道圈 + 11 粒墨点飞溅 + 四角准星 + 竖排边注 + 花饰 + 竖向「THE FALL」尺寸卡尺。
- **II 符号**：雕版校准网格（细/粗两级 pattern，104,472→1712×438）+ 三次心跳脉冲环 + 「1 SEC · 72 BPM」卡尺 + 边注。
- **III 世界**：外虚线圈 r360 + 72 细刻度 + 十字准线 + 18 枚罗马数字 r398 + SCALE 卡尺 + 边注。
- **IV 黑版**：四角骨色角饰（镜像旋转）+ 16 粒骨色墨点 + 卡面四角十字套准 + 骨色花饰 + 竖排反色边注。
- **V 抽卡**：双轨道圈 + 左侧 INDEX · SIX CARDS 可点击导航（6 行罗马数字 + 卡名，active 随进度高亮）。
- **VI 印记**：12 辐条 + 外虚线圈 r378 + 12 罗马数字 r386 + 边注；**VII 曼陀罗**：24 花瓣椭圆环 + 12 罗马数字 + 反向旋转虚线环 + 边注。
- **VIII 名义**：花饰 cartouche（1180×588）+ 左侧 COLOPHON + 右上 EDITION 01 版记。
- **符号悬停释义（#symTip）**：III / VI / VII 三幕符号悬停，显示 `SIGN · 罗马数字 / 拉丁名 / 英文释义`（共 25 条词条）。

## 冷开场钩子 v2「校样 · PROOF」（hook pass · 2026-10）

面向短视频平台的前 2.56 秒独立「钩子层」`hook.css` + `hook.js`（挂在舞台最上层的独立 DOM，不改动七个图版场景源），全部由电影时间 t 计算，`?capture=1` 抽帧可复现。v1 的「黑场 + 巨型空心描边字 + 平涂红圆」被评为土、丢质感，v2 整体重做为**与全片一致的古籍校样语言**：

- **首帧即暖纸（不再是黑场）**：纸纤维 + 双线框 + 四角套准角标 + 页眉「NOT TAROT — 校样 / 第 Ⅰ 图版 / Ⅶ」+ 页脚「FIG. 0 — GUTTA / MMXXVI」，像一张刚从印版上取下的校样；**首帧本身可直接截作平台封面**。
- **0.00–0.56s「别 划 走」**：236px Noto Serif SC 深墨排印（「划」为莓色作冲突），上下朱红细线 + 菱形端点，缩放进场；0.26s 起**撕边墨洪从右下涌入**，先吞掉第一句。
- **0.56–1.12s「这不是塔罗」**：158px 骨白大字压在墨面上（「塔罗」为纸白），下方 23px cap「一颗心 ◆ 七张图版 ◆ 最后一张，由你决定」；0.74s 绯色圆章「非」压印（双环 + 虚线内环 + 纸纹，−9° 带衰减抖动）。
- **1.14–1.22s 以「纸面受光」退场**：暖白 bloom + 纸纤维盖过溶解过程，观众看到的是纸张被灯照亮的一瞬，而不是灰洗、白闪或黑场对开。
- **1.24s 起无缝交还图版 I**（S1 早已在下层运行）；1.26–2.52s 纸面底部细线 + 留人承诺「看到最后 ◆ 抽一张属于你的牌」，随片头结束淡出。
- **2.56s** `#hook` 完全退场；任何 seek 回到 0–2.56s 自动重播，`?t=` 静态帧同样支持。
- **音效 6 cue**：0.03 低频闷响、0.30 墨涌、0.62 tick、0.80 压印 + 双 tick、1.02 退墨、1.36 轻铃。
- **技术**：墨洪为构建时 PIL 生成的 LA 遮罩（对角墨海 = 右缘实心 band ∪ 多瓣 blob + 细丝前锋 + 卫星墨滴 + 泪滴），CSS `mask-image` 应用；早期踩过的 BOM 破坏 `#hook` 规则、遮罩噪声聚中导致正圆/直边等问题均已修复。

## 交互（L3）
- 封面：拖墨滴或点任意处开始；拖拽幅度决定开场文案。
- 开场 0–2.56s：短视频钩子层自动播放（纸面「别 划 走」→ 撕边墨海「这不是塔罗」+ 非印章 → 纸面受光交还图版 I → 留人承诺），可 seek 重播；首帧可作平台封面。
- 全片：`Space` 播放/暂停，`←`/`→` ±2s，`Home` 回首帧，`M` 静音，`F` 全屏，`?` 帮助，`Esc` 关闭浮层，`1`–`7` 直达图版，`X` 开关动态（3D 视差 / 色彩错插 / 元素微动）。
- 时间轴：底部可拖 scrubber（悬停显示时间/图版名）+ 右侧 7 个章节墨点（悬停提示/点击跳转）；闲置 3.2s 自动隐藏 HUD。
- 卡牌：点击当前卡 3D 翻面（背义句），鼠标悬停有倾斜；滚轮在「黑版」阶段把牌抽出→自动进入第一张；左侧 INDEX 导航点任意行 → 跳至该卡并继续播放。
- 符号：III/VI/VII 幕符号悬停出现释义浮签（SIGN · 罗马数字 / 拉丁名 / 英文描述）。
- 瞳孔跟随指针；5×5 标本格悬停显示符号名；纸面任意点击留下墨晕（ink ping）；指针视差 + 微镜头浮动。
- 长按纸面 220ms 进入「呼吸」0.34× 慢放（右下角环形进度），松开恢复。
- 42s 后点击画面抽「你自己的牌」（随机符号 + 义句），可 DRAW AGAIN / SAVE THE CARD（导出 900×1280 PNG）/ CLOSE。
- 音效为 WebAudio 合成（心跳、翻纸、落墨、铃）；首次交互后启动，遵循 `prefers-reduced-motion`。
- URL：`?t=秒` 定位、`?capture=1` 纯画面（抽帧用）、`?vertical=1` 竖屏框。

## 重跑
1. 源文件：`_tools/v4src/`（shell.html + base/ui/acts/fx/decor/zh/textfx/motion/**hook**.css + core/effects/decor/textfx/motion/**hook**/scenes_a/scenes_b/interact/boot.js，共 20 个源文件）。
2. `python _tools/build_cinematic_v4.py` → `07_final/NOT_TAROT_45s_cinematic.html`（`--out` 可改输出、`--force-textures` 重生成纸纹）。
3. 依赖：`03_assets/symbols/sprites/`（25 个原始蚀刻图标）、`03_assets/fonts/`（16 款 woff2，含 Noto Serif SC 400/600 中文子集，已自包含）；纸纹/颗粒/晕影为构建时 PIL 程序生成，不依赖外部贴图。
4. 抽帧：`_tools/shot_server.py` + `_tools/shot_client.py`（Playwright/Edge，状态化交互截图）；`03_assets/keyframes/cinematic_v4/hook_pass_v2/` 存开场 17 帧（含首帧 / 墨涌 / 印章 / 受光退场 / 留人线）+ 全片抽检 7 帧 + 拼图 + 3 张放大复核（`hook_pass/` 为 v1 存档，`motion_pass/` 为上一版）。

## 已知边界
- 交互为「电影放映 + 注释层」，不是游戏；音效为合成占位，正式配乐替换 `effects.js` 内 WebAudio cue 即可。
- 竖屏 `?vertical=1` 目前为 16:9 居中放映框，正式 9:16 成片仍用 `social_9x16.mp4` 流水线。
- 旧版播放器（1.10 MB）已被本文件替换；如需回收，参考 git/`_archive/`。
