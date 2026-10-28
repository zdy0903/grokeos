# grokeos

铝的可查询状态方程表。热力学量来自 FEOS 16.7 的 3717 号铝，打开了 Maxwell 汽液平衡构造和软球冷曲线。表内低于真空参考压力的格点，压力已改成该参考压力。

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
