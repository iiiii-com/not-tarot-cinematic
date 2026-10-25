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
| `NOT_TAROT_45s_cinematic.html` | 交互电影播放器（自包含：17 款内嵌 woff2（含 Noto Serif SC 400/600 与花体马善政 Ma Shan Zheng 子集）+ 150 张蚀刻图标 + 5 幅大尺幅蚀刻底纹 + 程序生成纸纹/颗粒/晕影/墨迹 + 外部装饰层 + 错版墨色文字层 + 图案填充文字层 + 动态层 + 转场层 + **冷开场钩子层 v3「OCULUS · 巨眼」**） | 4.26 MB · 1920×1080 舞台自适应缩放 · 2026-10 hook v3 |
| `NOT_TAROT_45s_cinematic_hook2.html` | 上一版（冷开场 hook v2「校样 · PROOF」，已弃用，仅存档对比） | 2.75 MB · 2026-10 |
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

## 冷开场钩子 v3「OCULUS · 巨眼」（hook pass · 2026-10 · 取代 v2）

用户判定 v2「校样 · PROOF」比 v1 更土，改为 **D+C+A 三案融合**（D 满幅雕版巨眼 / C 纸的撕裂 / A 第一拍心电脉冲），
英文展示衬线主导、字面带冲击力 + 色差 + 3D、中文只作极少量对应翻译，节奏做「一吸一停一断」。整层是独立 DOM
`hook.css` + `hook.js`（挂在舞台上层的 `#hook`），不动七图版场景源，全部由电影时间 t 计算，`?capture=1` 可复现。

- **0.00–0.36s 第一拍**：黑场低频先响，一道绯色心电图从左向右**描出**（`stroke-dasharray` 逐帧画出，2.4px + 发光），
  另有一层莓色 1px 副本做重影；三次心跳点（0.36 / 0.44 / 0.86）各带一次闪光与整层机械震动（`jolt` 位移）。
- **0.16–0.74s 纸升 / 眼入**：整张纸自下**升起**（`translate3d(0,106%,0) → 0`）覆盖黑场，同时满幅巨型雕版眼
  （`motif_eng_eye_wide_bone`，1060×1140，origin 48.5%/51.6% 对齐虹膜）从 1.15× 缩小定位，虹膜四层环（绯 / 墨 / 内环 / 实心瞳孔）
  依次亮起并带 ±1.6% 呼吸。
- **0.48–0.94s 英文排印**：`DO NOT`（Playfair Display 700 · 132px）/ `SCROLL AWAY`（Cormorant italic 148px）
  两行分行入场，带模糊与纵向位移；下方细线 + 40px 花体中文「别 划 走」；每个字都有**两层错版重影**（绯 .50 multiply +
  金 .38 multiply，偏移由 `--hk-abx/--hk-aby` 驱动，随心跳抖到 3–4 px）。
- **0.62–0.96s 撕裂**：`.hk-sheet` 用 13 点撕裂多边形 `clip-path` 自右上向左下**撕开**，撕裂线下整层消失 → 直接露出
  已在运行的图版 I（S1 从 t=0 就在下层跑，故撕裂即交接、无需淡化）；撕口上方有骨色细描边 + 绯色虚线复线。
- **0.74–1.06s 下壳层**：被撕开的下半张是**黑纸**（`.hk-under`，lamp 底 + 骨色巨眼 motif screen 混合 .16 + 96px 网格），
  上面压 `THIS IS NOT TAROT`（Playfair 600 · 74px 骨白，屏幕混合双层错版：绯 .85 + 金 .52）+ 花体中文「这 不是塔罗」+
  一行小字 `keep going — the last card is yours`。
- **1.06–1.30s 收束**：下壳层上移淡出，撕口线上抬，整层淡出，干净交还图版 I。
- **音效 12 cue**（0.03–1.62s）：低频闷响 / 13 条 whoosh / 三次心跳 thump（44 / 52 / 38 Hz）/ 压印 / 三次铃（196 / 392 Hz），
  全部与画面 beat 对齐。
- **技术**：`clipFor(open)` 与 `underClipFor(open)` 是互补多边形；`.hk-sheet` 只保留撕口以上，`.hk-under` 只保留撕口以下，
  故撕裂处永远严丝合缝；巨眼的 motif 走 `build_motifs()` 内嵌（5 幅 1.3 MB）。

## 双语排版（bilingual pass · 2026-10）

用户要求「以英文为主，中文为辅，在英文旁边部分标注对应的小中文，以花体的形式」：

- **全部文案改回英文主导**：七个图版的标题/图注/口号、25 个符号的释义、六张卡的牌名与义句、海报/抽卡/帮助/提示，
  全部英文；`NOT TAROT`、拉丁学名（COR / PAPILIO…）、`FIG.`、罗马数字、版次保留拉丁。
- **花体中文小注**：用 Google Fonts **马善政 Ma Shan Zheng** 按全片实际用字裁切的子集（145 KB / 349 字，构建时内嵌），
  以 `<i class="hz">` 行内小注（.56em、金色、−1.7° 倾斜）、`.hz.hzb` 标题下小注（.30em、莓色）、`.hz.hzw` 段落小译三层呈现；
  标题的小注改为**与标题同一行**内联，避免压到图注或越过版框。
- 中文注在悬停符号时会**实时换成该符号的中文名**（`.hz-live`），是文字层与图案层互动的第一处。

## 图案填充文字（patfx pass · 2026-10）

`patfx.css` + `patfx.js`：把 12 处主标题（S1 大标 / S2 三行 / S3 标题 / S4 大标 / S5 标题 / S6 大标 / 卡名 / S8 / S9 / S10 / S11 / 海报标题）
克隆出一层 `.pat-layer`，用 `background-clip:text` 把**蚀刻图案本身**填进字里（默认 opacity .13 呼吸，悬停抬到 .34）：

- 悬停 III / VI / VII 的任一符号（或 V 的 5×5 标本格）→ 当前幕主标题的图案填充**换成该符号的版画**（绯色），
  同时标题旁的中文小注换成该符号中文名——文字真的「穿上」了图案。
- 卡名（`.c-name`）跟着当前抽出的牌换图案；S9 `BECOME.` 每 0.55s 换一个符号（蝶→花→心→冠→眼）；S11 字标每 1.6s 换（冠→心→眼）。
- 全部由 t 与指针决定，`?capture=1` 下 transition 关闭、结果可复现。

## 转场层（trans pass · 2026-10）

`trans.css` + `trans.js`：11 个幕切点各配一种**因果式**转场手势（不是整场透明度交叉淡化），全部由 t 计算：

- 切点表 `MARKS = [0, 8.0, 14.0, 17.5, 22.0, 24.5, 33.5, 36.0, 40.0, 42.0]`，每处 `LEAD = 1.55s` 起效、`HALF = .9s` 达峰。
- 五种手势：`shut`（上下纸帘对合）/ `bloom`（莓色径向晕开，金色变体用于曼陀罗）/ `rule`（发丝线横扫 + 细切）/ `ink`（墨淌自下缘升起）/ `motes`（16 粒确定性浮尘穿场）/ `dip`（22.0s 专用：先去色入黑，换幕在黑里完成再放亮）。
- 另有全程晕影 `.tr-vig`（切点前后加深 0.86 强度）把两次画面在视觉上「压」到一起。
- 每处都做过 0.1s 步长的密度抽帧验证：`dMean` 平滑、`dInk` 无突变（早期 17.5 / 42.0 的全屏闪黑已修，22.0 的硬切改用 `dip` 后消失）。

## 交互（L3）
- 封面：拖墨滴或点任意处开始；拖拽幅度决定开场文案。
- 开场 0–1.30s：冷开场「OCULUS」自动播放（黑场心电第一拍 → 纸升 + 巨眼入 → DO NOT SCROLL AWAY 双行排印 + 花体「别 划 走」→ 撕裂露出黑纸下壳层 + THIS IS NOT TAROT → 淡出交还图版 I），可 seek 重播。
- 全片：`Space` 播放/暂停，`←`/`→` ±2s，`Home` 回首帧，`M` 静音，`F` 全屏，`?` 帮助，`Esc` 关闭浮层，`1`–`7` 直达图版，`X` 开关动态（3D 视差 / 色彩错插 / 元素微动）。
- 时间轴：底部可拖 scrubber（悬停显示时间/图版名）+ 右侧 7 个章节墨点（悬停提示/点击跳转）；闲置 3.2s 自动隐藏 HUD。
- 卡牌：点击当前卡 3D 翻面（背义句），鼠标悬停有倾斜；滚轮在「黑版」阶段把牌抽出→自动进入第一张；左侧 INDEX 导航点任意行 → 跳至该卡并继续播放。
- 符号：III/VI/VII 幕符号悬停出现释义浮签（SIGN · 罗马数字 / 拉丁名 / 英文描述 + 花体中文）；同时把当幕主标题的图案填充换成该符号版画、标题旁中文小注换成该符号中文名。
- 瞳孔跟随指针；5×5 标本格悬停显示符号名；纸面任意点击留下墨晕（ink ping）；指针视差 + 微镜头浮动。
- 长按纸面 220ms 进入「呼吸」0.34× 慢放（右下角环形进度），松开恢复。
- 42s 后点击画面抽「你自己的牌」（随机符号 + 义句），可 DRAW AGAIN / SAVE THE CARD（导出 900×1280 PNG）/ CLOSE。
- 音效为 WebAudio 合成（心跳、翻纸、落墨、铃）；首次交互后启动，遵循 `prefers-reduced-motion`。
- URL：`?t=秒` 定位、`?capture=1` 纯画面（抽帧用）、`?vertical=1` 竖屏框。

## 重跑
1. 源文件：`_tools/v4src/`（shell.html + base/ui/acts/fx/decor/zh/textfx/motion/hook/**trans**/**patfx**.css + core/effects/decor/textfx/motion/hook/scenes_a/scenes_b/interact/**trans**/**patfx**/boot.js，共 24 个源文件）。
2. `python _tools/build_cinematic_v4.py` → `07_final/NOT_TAROT_45s_cinematic.html`（`--out` 可改输出、`--force-textures` 重生成纸纹）。
3. 依赖：`03_assets/symbols/sprites/`（25 个原始蚀刻图标）、`03_assets/fonts/`（17 款 woff2，含 Noto Serif SC 400/600 与马善政花体子集，已自包含）、`03_assets/concept_v3/motifs2/`（5 幅满幅蚀刻底纹，构建时 `build_motifs()` 内嵌）；纸纹/颗粒/晕影/墨迹为构建时 PIL 程序生成，不依赖外部贴图。
4. 抽帧：`_tools/shot_server.py` + `_tools/shot_client.py`（Playwright/Edge，状态化交互截图）；`03_assets/keyframes/cinematic_v4/hook_pass_v2/` 存开场 17 帧（含首帧 / 墨涌 / 印章 / 受光退场 / 留人线）+ 全片抽检 7 帧 + 拼图 + 3 张放大复核（`hook_pass/` 为 v1 存档，`motion_pass/` 为上一版）。

## 已知边界
- 交互为「电影放映 + 注释层」，不是游戏；音效为合成占位，正式配乐替换 `effects.js` 内 WebAudio cue 即可。
- 竖屏 `?vertical=1` 目前为 16:9 居中放映框，正式 9:16 成片仍用 `social_9x16.mp4` 流水线。
- 冷开场巨眼用的是 `motifs2/eng_eye_wide_bone.png`（615×655 放大到 1060×1140），近距离看颗粒略粗；如需大银幕，替换为更高分辨率底纹即可。
- 旧版播放器（1.10 MB）已被本文件替换；如需回收，参考 git/`_archive/`。

## 排版收口（type-fix pass · 2026-10）

冷开场与转场定稿后，又针对「标题 / 花体小注 / 图版说明」三层文字做了两处收口：

- **图版 III**：说明行 `.s3-sub` 原在标题上滑动画期间就淡入，两层文字有约 0.4 s 交叠；现改为标题完全落位后才淡入（`scenes_a.js` 中 `wt(local, 3.3, 3.95)`），并把说明行抬到 940px、花体注压到 `.80em` 行内，实测 title 891–930 / 花体注 943–963 / 说明 975–978+1004–1016（框线）互不相交。
- **图版 IX**：`BECOME.` 126px 字形在 968px 处会压到说明行（实测重叠约 47px，且花体注换行）；现给 `.s9-word` 加 `white-space:nowrap`、花体注收紧到 `.26em / .08em` 行内，并把字标从 846px 上提到 **812px** —— 实测字 821–980 / 说明 983–1010，完全分离，仍在图版内框（1016）之上。

**交付件**：`NOT_TAROT_45s_cinematic.html` **4,264,283 B**，SHA256 `E33BAC6DEABFF3BBA1F32F965C0A34374A6386316AF0DEE0B99DA91471025804`。

**抽帧存档**：`03_assets/keyframes/cinematic_v4/typefix_pass/`（20 张 16:9 全分辨率 + 6 张 1080×1080 竖版 + 两张联络板）。

**验收脚本**（可选重跑）：

```powershell
python -X utf8 _tools/build_cinematic_v4.py --out 07_final/NOT_TAROT_45s_cinematic.html
python -X utf8 E:\deepseek\review_out\shot.py E:\deepseek\review_out\plan_final.json
python -X utf8 E:\deepseek\review_out\shot.py E:\deepseek\review_out\plan_finalchk.json
```

---

## 冷开场钩子 v4「OCULUS · 单行」＋ 全片去中文（2026-10-25）

本轮按反馈做了三件事：**删掉全部中文**、**修掉冷开场里叠在一起的英文**、**重做冷开场的呼吸节奏**。

### 1. 全片去中文

花体中文小注（`<i class="hz">`，共 108 处）、`SIGN_ZH` 中文映射、`NAMES` 第三项中文释义、
`CARDS` 的 `zh` 字段、`PLATES` 的 `zh`/`capZh`、`STAMPS` 第四字段、poster/drawer/help/toast 的中文、
save-card canvas 里的中文全部删除；`zh.css` 退场、`Ma Shan Zheng` 与 `Noto Serif SC` 三种字体移出构建。
构建产物扫描：**0 个 CJK 字符**，内嵌字体 14 款（原 17 款），体积 4.26 MB → **3.87 MB**。

### 2. 冷开场英文不再叠字

旧版在 1.3 s 内塞了 `DO NOT` / `SCROLL AWAY` / `别划走` / `THIS IS NOT TAROT` 四组文案，
时间窗几乎同时、版面也在同一竖向区间。现在只保留**一行**大字 `THIS IS NOT TAROT`
（`.hk-big1`，Playfair 700 / 118px / top 300），另外两行与中文行整体删除；
kick 行 `A FILM IN SEVEN PLATES ◆ ONE QUESTION` 单独占 top 188，两者垂直间隔 90px 以上，任一时刻不重叠。

### 3. 冷开场重做为 3.78 s 五段式（呼吸感）

| 时间 | 动作 |
|---|---|
| 0.00 | 黑场静置 |
| 0.34 | 四角框线与十字准星生长 |
| 0.52–1.90 | 绯色心电线从左向右描绘，三次 QRS 峰 |
| 1.00 / 1.34 | 两记心跳（画面轻微 jolt + 色差抖动） |
| 1.90–2.18 | 线收走，回到黑场（留一口气） |
| 2.16–2.86 | 纸面自下升起（`translateY 104% → 0`） |
| 2.34–3.02 | 雕版巨眼显影 + 虹膜/瞳孔分层入场 |
| 2.88–3.12 | 一行字落位 |
| 3.02 | 第三记心跳（在纸上） |
| 3.12–3.46 | 完全静止（呼吸段） |
| 3.46–3.78 | 撕裂揭示：上壳层沿 13 点折线撕开，露出已运行的 plate I |
| 3.78 | plate I 接管 |

`hook.js` 时间轴常量：`END = 3.78`、`REVEAL = 3.46`；撕裂用 `clipFor(open)` 生成 13 点 `polygon()`，
上壳层只保留撕裂线上方，撕裂即揭示下一幕，无需淡出淡入。撕口带 74px 模糊黑影 + 骨色 1.2px + 莓色 2.0px 双描边。

### 4. 时间轴与音效同步

- `core.js` `T` 首段 `[0, 5.00]`，`scenes_a.js` `S1 = scene(0, 5.00, …)`、`S2 = scene(5.00, 8.0, …)`。
- `S1.upd` 内 `const local = Math.max(0, olocal - 1.85)`：冷开场占前 1.85 s，plate I 自己的墨滴动作从 `local=0` 起算。
- `S2.upd` 内 `const local = olocal * (5.4 / Math.max(0.8, dur))`：plate II 原按 5.4 s 编排，3.0 s 窗口需要内部提速。
- `effects.js` 冷开场 cue 重排为 0.34 / 0.52 / 1.00 / 1.34 / 1.90 / 2.16 / 2.20 / 2.88 / 3.02 / 3.46 / 3.78，
  plate II 心跳改为 `[5.72, 6.21, 6.70, 7.19]`。

### 5. 验证数据

- 构建 3,869,780 B，`node --check` rc=0，0 CJK，14 fonts。
- 抽帧 18 帧（`03_assets/keyframes/cinematic_v4/english_oculus/`）像素统计：
  0.6 s mean 23.9（黑场 100%）、2.5 s mean 110.4（纸升起）、3.2 s mean 203.4（眼+字）、
  4.4 s 起 plate I 225.8、S3 黑幕 23.4 s mean 16.8（99.5% dark）、其余幕 204–230。
- 行带检查：3.2 s 左侧文字区只有 3 条独立墨带（193–202 kick / 239–247 细线 / 340–412 大字），无叠字。
