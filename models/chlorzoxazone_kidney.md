# Model for the renal excretion of 6-hydroxychlorzoxazone-O-glucuronide

Model `chlorzoxazone_kidney`, SBML Level 3 Version 2, read from chlorzoxazone\_kidney.xml, written by sbmlode 0.3.0.

Model for the renal excretion of 6-hydroxychlorzoxazone-O-glucuronide

Model for the renal excretion of 6-hydroxychlorzoxazone-O-glucuronide encoded in SBML format.

Import and secretion are not modeled explicitly but a lumped excretion reaction relative to the GFR is used to describe the urinary elimination of the glucuronide.

58-64 % of a 250 mg dose are recovered as 6-hydroxychlorzoxazone (free and glucuronide) in the urine (Frye1998, Burckart1998, Vesell1995)

71-74 % of a 750 mg dose (Desiraju1983, Kharasch1993)

the renal clearance of total 6-hydroxychlorzoxazone is 464-506 ml/min (Frye1998), above the GFR: a tubular secretion

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
| $\mathrm{Vki}$ | `Vki` | kidney | $1.5$ | l | ✓ |
| $\mathrm{Vurine}$ | `Vurine` | urine | $1$ | l | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{czxoglu}_{\mathrm{ext}}$ | `czxoglu_ext` | 6-hydroxychlorzoxazone-O-glucuronide (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{czxoglu}_{\mathrm{urine}}$ | `czxoglu_urine` | 6-hydroxychlorzoxazone-O-glucuronide (urine) | $\mathrm{Vurine}$ |  | mmol | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $f_{\mathrm{renal\_function}}$ | `f_renal_function` | renal function | $1$ | \- | ✓ |
| $\mathrm{GFR}_{\mathrm{base}}$ | `GFR_base` | glomerular filtration rate (healthy) | $101$ | ml/min | ✓ |
| $\mathrm{CZXOGLU}_{\mathrm{EX\_f}}$ | `CZXOGLU_EX_f` | renal clearance of the glucuronide relative to the GFR | $14.6084423962984$ | \- | ✓ |
| $\mathrm{GFR}$ | `GFR` | glomerular filtration rate |  | ml/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{czxoglu}_{\mathrm{urine}} &= 0 \cdot \mathrm{Vurine}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{GFR} &= f_{\mathrm{renal\_function}} \cdot \mathrm{GFR}_{\mathrm{base}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{CZXOGLU\_EX}}$ | `CZXOGLU_EX` | excretion 6-hydroxychlorzoxazone-O-glucuronide | $\mathrm{czxoglu}_{\mathrm{ext}} \longrightarrow \mathrm{czxoglu}_{\mathrm{urine}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{CZXOGLU\_EX}} &= \mathrm{GFR} \cdot 0.001 \cdot \mathrm{CZXOGLU}_{\mathrm{EX\_f}} \cdot \mathrm{czxoglu}_{\mathrm{ext}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{czxoglu}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{CZXOGLU\_EX}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{czxoglu}_{\mathrm{urine}}}{\mathrm{d} t} &= v_{\mathrm{CZXOGLU\_EX}}
\end{aligned}
$$
