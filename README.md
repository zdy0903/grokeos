# grokeos

## 最新表（2026-10-29，FLASH 直接读取）

`tables/Al_FEOS_metastable_rhomin1e-7_20261029.dat`

这是当前最新的铝 EOS。格式仍是 `FEOS_PECOVER_1T_V1`：250 个温度节点 × 1349 个密度节点，密度 \(1\times10^{-7}\)–\(3\,\mathrm{g/cm^3}\)，温度约 300 K–1000 eV。原子量 26.9815，内能偏移 \(1.0246534692181387\times10^{9}\,\mathrm{erg/g}\)。

两相区以外与 Maxwell 平衡表相同。液相旋节线到液相双节线之间的 64056 个格点改成 Maxwell 关闭时的均匀态，也就是过热、拉伸液相；这些格点的压力、内能、比熵和电离度一起替换。每条等密度线上内能随温度升高。密度或温度超出表格范围时，现有读取程序会报错，不外推。

SHA256：`5203770b424438479302049ccb2743d897b72ceb258536961f808d5afd85634e`

`tables/Al_FEOS_metastable_bands_20261029.dat` 给出每条等温线上三个从 1 开始的密度节点序号：两相区起点、亚稳带起点、单相液体起点。没有汽液穹顶的等温线写成 `0 0 0`。FLASH 只读主表，不读这个索引。`tables/metastable_summary.json` 是抽样核对记录。

另一台电脑把主表放到算例目录，把 `eos_ionmixFile` 指到这个文件名即可。

## 2026-10-28 的 Python 查询包

铝的可查询状态方程表。热力学量来自 FEOS 16.7 的 3717 号铝，打开了 Maxwell 汽液平衡构造和软球冷曲线。表内低于真空参考压力的格点，压力已改成该参考压力。这张 250×250 表带真空压力底，不是上面那张 FLASH 主表。

另一台电脑只需要 Python 3.9+ 和 numpy，不需要编译 FEOS。

## 表

| 项目 | 值 |
|---|---|
| 密度 | 1e-7–3 g/cm³，250 点 |
| 温度 | 300 K–1000 eV，250 点 |
| 真空参考态 | 1e-7 g/cm³，1000 K |
| 真空压力 | 30.7943063 Pa |
| 被抬高的格点 | 62500 个中的 22856 个 |

压力单位是 Pa，内能单位是 J/g。内能没有因为压力底而改动。密度或温度超出表格时会报错，不外推。

## 用法

在本目录执行：

```bash
python -c "import sys; sys.path.insert(0,'.'); from grokeos import pressure, state; print(pressure(2.7, 300)); print(state(2.7, 2000))"
```

也可以安装后导入：

```bash
pip install .
```

```python
from grokeos import pressure, energy, state

pressure(2.7, 300)    # Pa；300 K 的低压平台已被抬到真空压力
energy(2.7, 2000)     # J/g
state(1.0, 5200)
```

`state` 还返回 `two_phase` 和 `pressure_floored`。

## 来源

表格由未改动的 FEOS 16.7 在材料 3717 上采样得到，Maxwell 和软球开关都是打开的。FEOS 本身以 GNU GPL-3.0 发布，许可证原文在 `FEOS-GPL-3.0.txt`。本目录里的查询程序和真空压力底是 2026-10-28 在采样结果上追加的，不是 FEOS 原程序的一部分。

`data/binodal.npz` 保存采样时的汽液共存边界，供对照，不参与 `pressure` 插值。
