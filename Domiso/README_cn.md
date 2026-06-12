# DoMiSo Yihuan

这个目录是 `异环 / Neverness To Everness` 定制版 DoMiSo，保留新版播放控制和 UI 工作流，同时切换目标游戏和键位模型。

## 目标环境
- 游戏：`Neverness To Everness`
- 主进程：`HTGame.exe`
- 备用进程：`NTEGame.exe`
- 游戏目录：`D:\Neverness To Everness`
- 项目目录：`D:\domiso\DoMiSo-yihuan`

## 已做修改
- 把程序品牌切成 Yihuan / 异环。
- 游戏进程检测改为优先 `HTGame.exe`，找不到时再检测 `NTEGame.exe`。
- 保留新版播放功能：进度条、暂停后原位置继续播放、播放快捷键。
- 可弹键位模型改成异环 36 键钢琴：21 个自然音 + 15 个半音。
- 保留 DoMiSo 升降音语法：`#` 表示升半音，`b` 表示降半音，例如 `1#`、`3b`、`+5#`。
- 主界面颜色改成异环独立的砂金/墨绿风格。
- 托盘菜单改为直接打开异环游戏目录。

## 使用方式
1. 先启动 `Neverness To Everness`，进入钢琴演奏界面。
2. 运行 `DoMiSo.ahk` 或编译后的可执行文件。
3. 在编辑框粘贴 DoMiSo 谱，或用 `File` 打开 `txt / dms` 文件。
4. `Listen` 用于 MIDI 试听。
5. `Play` 用于向游戏自动演奏。
6. 快捷键：`F7` 暂停，`F8` 停止并复位，`F9` 从头开始，`F10` 从暂停位置继续。

## 异环 36 键键位
- 自然音键位：
  - 高音：`Q W E R T Y U`
  - 中音：`A S D F G H J`
  - 低音：`Z X C V B N M`
- 半音规则：
  - `Shift + 键位` 演奏游戏 UI 标出的高半音。
  - `Ctrl + 键位` 演奏游戏 UI 标出的低半音。
- 这个版本支持的 DoMiSo 音域是 MIDI `48-83`，也就是三组八度内的 `-1` 到 `+7`，并支持范围内的升降音。

## 说明
- 这个版本是本地定制分支。
- 当前默认不自动更新，避免拉取原神版发布包。
- 如果要充分利用 36 键半音，谱子需要包含 DoMiSo 的 `# / b` 升降音。

