# Model for chlorzoxazone elimination in the liver

Model `chlorzoxazone_liver`, SBML Level 3 Version 2, read from chlorzoxazone\_liver.xml, written by sbmlode 0.3.0.

Model for chlorzoxazone elimination in the liver

Model for the hepatic metabolism of chlorzoxazone via CYP2E1 and a second, CYP2E1 independent pathway, the glucuronidation of 6-hydroxychlorzoxazone, the elimination of ethanol and the turnover of CYP2E1 encoded in SBML format.

The content of this model has been carefully created in a manual research effort.

Terms of use

Copyright © 2026 Matthias König.

This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.

Redistribution and use of any part of this model, with or without modification, are permitted provided that the following conditions are met:

Redistributions of this SBML file must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in a different form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

This model is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

## Units

| Time | Substance | Extent | Volume | Area | Length |
| --- | --- | --- | --- | --- | --- |
| min | mmol | mmol | l | m<sup>2</sup> | m |

## Compartments

| Symbol | Id | Name | Size | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{Vext}$ | `Vext` | plasma | $4$ | l | ✓ |
| $\mathrm{Vli}$ | `Vli` | liver | $1.5$ | l | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{czx}_{\mathrm{ext}}$ | `czx_ext` | chlorzoxazone (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{czx}$ | `czx` | chlorzoxazone (liver) | $\mathrm{Vli}$ | $0$ | mmol/l | concentration |
| $\mathrm{czx6oh}$ | `czx6oh` | 6-hydroxychlorzoxazone (liver) | $\mathrm{Vli}$ | $0$ | mmol/l | concentration |
| $\mathrm{czx6oh}_{\mathrm{ext}}$ | `czx6oh_ext` | 6-hydroxychlorzoxazone (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{czxoglu}$ | `czxoglu` | 6-hydroxychlorzoxazone-O-glucuronide (liver) | $\mathrm{Vli}$ | $0$ | mmol/l | concentration |
| $\mathrm{czxoglu}_{\mathrm{ext}}$ | `czxoglu_ext` | 6-hydroxychlorzoxazone-O-glucuronide (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{ethanol}$ | `ethanol` | ethanol (liver) | $\mathrm{Vli}$ | $0$ | mmol/l | concentration |
| $\mathrm{ethanol}_{\mathrm{ext}}$ | `ethanol_ext` | ethanol (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{cyp2e1}$ | `cyp2e1` | CYP2E1 | $\mathrm{Vli}$ | $1$ | \- | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{BW}$ | `BW` | body weight \[kg\] | $75$ | kg | ✓ |
| $\mathrm{cf}_{\mathrm{units\_per\_mmole}}$ | `cf_units_per_mmole` | conversion factor for dimensionless species | $1$ | 1/mmol | ✓ |
| $\mathrm{cyp2e1}_{\mathrm{thalf}}$ | `cyp2e1_thalf` | CYP2E1 half life | $2592$ | min | ✓ |
| $\mathrm{CZX}_{\mathrm{k\_IM}}$ | `CZX_k_IM` | rate constant for chlorzoxazone import into the liver | $100$ | 1/min | ✓ |
| $\mathrm{CZX}_{\mathrm{F\_EX}}$ | `CZX_F_EX` | liver partition of chlorzoxazone (inverse) | $1.59$ | \- | ✓ |
| $\mathrm{CZX6OH}_{\mathrm{k\_EX}}$ | `CZX6OH_k_EX` | rate constant for 6-hydroxychlorzoxazone export | $100$ | 1/min | ✓ |
| $\mathrm{CZX6OH}_{\mathrm{F\_IM}}$ | `CZX6OH_F_IM` | liver to plasma ratio of 6-hydroxychlorzoxazone | $0.221$ | \- | ✓ |
| $\mathrm{CZXOGLU}_{\mathrm{k\_EX}}$ | `CZXOGLU_k_EX` | rate constant for 6-hydroxychlorzoxazone-O-glucuronide export | $100$ | 1/min | ✓ |
| $\mathrm{CZXOGLU}_{\mathrm{F\_IM}}$ | `CZXOGLU_F_IM` | liver to plasma ratio of 6-hydroxychlorzoxazone-O-glucuronide | $1$ | \- | ✓ |
| $f_{\mathrm{cyp2e1}}$ | `f_cyp2e1` | CYP2E1 activity | $1$ | \- | ✓ |
| $f_{\mathrm{cyp2e1\_Km}}$ | `f_cyp2e1_Km` | factor of the Km of CYP2E1 | $1$ | \- | ✓ |
| $\mathrm{CZXOX}_{\mathrm{Vmax}}$ | `CZXOX_Vmax` | Vmax of the chlorzoxazone 6-hydroxylation | $0.0071748083525124$ | mmol/min/l | ✓ |
| $\mathrm{CZXOX}_{\mathrm{Km}}$ | `CZXOX_Km` | Km of the chlorzoxazone 6-hydroxylation | $0.00990140603641784$ | mmol/l | ✓ |
| $f_{\mathrm{czxother}}$ | `f_czxother` | activity of the CYP2E1 independent elimination | $1$ | \- | ✓ |
| $\mathrm{CZXOTHER}_{\mathrm{k}}$ | `CZXOTHER_k` | rate constant of the CYP2E1 independent elimination | $0.263160773946114$ | 1/min | ✓ |
| $\mathrm{CZXOGLU}_{\mathrm{k}}$ | `CZXOGLU_k` | rate constant of the glucuronidation of 6-hydroxychlorzoxazone | $42.7782424502833$ | 1/min | ✓ |
| $f_{\mathrm{GLU}}$ | `f_GLU` | UGT activity (6-hydroxychlorzoxazone glucuronidation) | $1$ | \- | ✓ |
| $\mathrm{ETH}_{\mathrm{k\_IM}}$ | `ETH_k_IM` | rate constant for ethanol import into the liver | $100$ | 1/min | ✓ |
| $\mathrm{ETHEL}_{\mathrm{VMAX}}$ | `ETHEL_VMAX` | rate of ethanol elimination | $0.0485245432051771$ | mmol/min/kg | ✓ |
| $\mathrm{ETHEL}_{\mathrm{KM}}$ | `ETHEL_KM` | Km of the ethanol elimination | $2.17$ | mmol/l | ✓ |
| $k_{\mathrm{cyp2e1\_prod}}$ | `k_cyp2e1_prod` | rate constant for CYP2E1 production |  | mmol/min/l |  |
| $k_{\mathrm{cyp2e1\_deg}}$ | `k_cyp2e1_deg` | rate constant for CYP2E1 degradation |  | mmol/min/l |  |
| $\mathrm{Ki}_{\mathrm{cyp2e1\_deg\_ethanol}}$ | `Ki_cyp2e1_deg_ethanol` | stabilization constant (inhibition degradation) | $10^{-5}$ | mmol/l | ✓ |
| $\mathrm{kd}_{\mathrm{cyp2e1}}$ | `kd_cyp2e1` |  |  | mmol/min/l |  |

## Initial assignments and assignment rules

The assignment rules hold at every time $t$:

$$
\begin{aligned}
k_{\mathrm{cyp2e1\_deg}} &= \frac{\frac{1 \cdot 0.693}{\mathrm{cyp2e1}_{\mathrm{thalf}}}}{\mathrm{Vli}} \\[1ex]
\mathrm{kd}_{\mathrm{cyp2e1}} &= \frac{k_{\mathrm{cyp2e1\_deg}}}{1 + \frac{\mathrm{ethanol}}{\mathrm{Ki}_{\mathrm{cyp2e1\_deg\_ethanol}}}} \\[1ex]
k_{\mathrm{cyp2e1\_prod}} &= k_{\mathrm{cyp2e1\_deg}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation | Modifiers |
| --- | --- | --- | --- | --- |
| $v_{\mathrm{CZXIM}}$ | `CZXIM` | chlorzoxazone import | $\mathrm{czx}_{\mathrm{ext}} \rightleftharpoons \mathrm{czx}$ |  |
| $v_{\mathrm{CZX6OHEX}}$ | `CZX6OHEX` | 6-hydroxychlorzoxazone export | $\mathrm{czx6oh} \rightleftharpoons \mathrm{czx6oh}_{\mathrm{ext}}$ |  |
| $v_{\mathrm{CZXOGLU\_EX}}$ | `CZXOGLU_EX` | 6-hydroxychlorzoxazone-O-glucuronide export | $\mathrm{czxoglu} \rightleftharpoons \mathrm{czxoglu}_{\mathrm{ext}}$ |  |
| $v_{\mathrm{CZXOX}}$ | `CZXOX` | chlorzoxazone 6-hydroxylation (CYP2E1) | $\mathrm{czx} \longrightarrow \mathrm{czx6oh}$ | $\mathrm{cyp2e1}$ |
| $v_{\mathrm{CZXOTHER}}$ | `CZXOTHER` | chlorzoxazone elimination (CYP2E1 independent) | $\mathrm{czx} \longrightarrow \varnothing$ |  |
| $v_{\mathrm{CZXOGLU}}$ | `CZXOGLU` | 6-hydroxychlorzoxazone glucuronidation (UGT) | $\mathrm{czx6oh} \longrightarrow \mathrm{czxoglu}$ |  |
| $v_{\mathrm{ETHIM}}$ | `ETHIM` | ethanol import | $\mathrm{ethanol}_{\mathrm{ext}} \rightleftharpoons \mathrm{ethanol}$ |  |
| $v_{\mathrm{ETH\_ELIMINATION}}$ | `ETH_ELIMINATION` | ethanol elimination (ALD) | $\mathrm{ethanol} \longrightarrow \varnothing$ |  |
| $v_{\mathrm{CYP2E1\_PROD}}$ | `CYP2E1_PROD` | CYP2E1 production | $\varnothing \longrightarrow \mathrm{cyp2e1}$ |  |
| $v_{\mathrm{CYP2E1\_DEG}}$ | `CYP2E1_DEG` | CYP2E1 degradation | $\mathrm{cyp2e1} \longrightarrow \varnothing$ | $\mathrm{ethanol}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{CZXIM}} &= \mathrm{CZX}_{\mathrm{k\_IM}} \cdot \mathrm{Vli} \cdot \mathopen{}\left(\mathrm{czx}_{\mathrm{ext}} - \mathrm{CZX}_{\mathrm{F\_EX}} \cdot \mathrm{czx}\right) \\[1ex]
v_{\mathrm{CZX6OHEX}} &= \mathrm{CZX6OH}_{\mathrm{k\_EX}} \cdot \mathrm{Vli} \cdot \mathopen{}\left(\mathrm{czx6oh} - \mathrm{CZX6OH}_{\mathrm{F\_IM}} \cdot \mathrm{czx6oh}_{\mathrm{ext}}\right) \\[1ex]
v_{\mathrm{CZXOGLU\_EX}} &= \mathrm{CZXOGLU}_{\mathrm{k\_EX}} \cdot \mathrm{Vli} \cdot \mathopen{}\left(\mathrm{czxoglu} - \mathrm{CZXOGLU}_{\mathrm{F\_IM}} \cdot \mathrm{czxoglu}_{\mathrm{ext}}\right) \\[1ex]
v_{\mathrm{CZXOX}} &= \frac{f_{\mathrm{cyp2e1}} \cdot \mathrm{cyp2e1} \cdot \mathrm{CZXOX}_{\mathrm{Vmax}} \cdot \mathrm{Vli} \cdot \mathrm{czx}}{\mathrm{czx} + \mathrm{CZXOX}_{\mathrm{Km}} \cdot f_{\mathrm{cyp2e1\_Km}}} \\[1ex]
v_{\mathrm{CZXOTHER}} &= f_{\mathrm{czxother}} \cdot \mathrm{CZXOTHER}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot \mathrm{czx} \\[1ex]
v_{\mathrm{CZXOGLU}} &= f_{\mathrm{GLU}} \cdot \mathrm{CZXOGLU}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot \mathrm{czx6oh} \\[1ex]
v_{\mathrm{ETHIM}} &= \mathrm{ETH}_{\mathrm{k\_IM}} \cdot \mathrm{Vli} \cdot \mathopen{}\left(\mathrm{ethanol}_{\mathrm{ext}} - \mathrm{ethanol}\right) \\[1ex]
v_{\mathrm{ETH\_ELIMINATION}} &= \frac{\mathrm{ETHEL}_{\mathrm{VMAX}} \cdot \mathrm{BW} \cdot \mathrm{ethanol}}{\mathrm{ethanol} + \mathrm{ETHEL}_{\mathrm{KM}}} \\[1ex]
v_{\mathrm{CYP2E1\_PROD}} &= \mathrm{Vli} \cdot k_{\mathrm{cyp2e1\_prod}} \\[1ex]
v_{\mathrm{CYP2E1\_DEG}} &= \mathrm{Vli} \cdot \mathrm{kd}_{\mathrm{cyp2e1}} \cdot \mathrm{cyp2e1}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{czx}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{CZXIM}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{czx}}{\mathrm{d} t} &= \frac{v_{\mathrm{CZXIM}} - v_{\mathrm{CZXOX}} - v_{\mathrm{CZXOTHER}}}{\mathrm{Vli}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{czx6oh}}{\mathrm{d} t} &= \frac{-v_{\mathrm{CZX6OHEX}} + v_{\mathrm{CZXOX}} - v_{\mathrm{CZXOGLU}}}{\mathrm{Vli}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{czx6oh}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{v_{\mathrm{CZX6OHEX}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{czxoglu}}{\mathrm{d} t} &= \frac{-v_{\mathrm{CZXOGLU\_EX}} + v_{\mathrm{CZXOGLU}}}{\mathrm{Vli}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{czxoglu}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{v_{\mathrm{CZXOGLU\_EX}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{ethanol}}{\mathrm{d} t} &= \frac{v_{\mathrm{ETHIM}} - v_{\mathrm{ETH\_ELIMINATION}}}{\mathrm{Vli}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{ethanol}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{ETHIM}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{cyp2e1}}{\mathrm{d} t} &= \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{CYP2E1\_PROD}} - \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{CYP2E1\_DEG}}
\end{aligned}
$$
