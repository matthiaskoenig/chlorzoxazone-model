# Model for chlorzoxazone absorption in the small intestine

Model `chlorzoxazone_intestine`, SBML Level 3 Version 2, read from chlorzoxazone\_intestine.xml, written by sbmlode 0.3.0.

Model for chlorzoxazone absorption in the small intestine

Absorption of chlorzoxazone from the intestinal lumen into the portal plasma and absorption of oral ethanol. Chlorzoxazone is not metabolized in the intestine: CYP2E1 is low in the enterocytes, the first pass is the saturable hepatic CYP2E1.

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
| $\mathrm{Vext}$ | `Vext` | plasma | $1$ | l | ✓ |
| $\mathrm{Vgu}$ | `Vgu` | intestine | $1.2825$ | l | ✓ |
| $\mathrm{Vlumen}$ | `Vlumen` | intestinal lumen (inner part of intestine) | $1.15425$ | l |  |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{czx}_{\mathrm{lumen}}$ | `czx_lumen` | chlorzoxazone (intestinal volume) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{czx}_{\mathrm{ext}}$ | `czx_ext` | chlorzoxazone (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{czx}_{\mathrm{feces}}$ | `czx_feces` | chlorzoxazone (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{ethanol}_{\mathrm{ext}}$ | `ethanol_ext` | ethanol (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{PODOSE}_{\mathrm{ethanol}}$ | `PODOSE_ethanol` | oral ethanol dose \[mg\] | $0$ | mg |  |
| $F_{\mathrm{czx\_abs}}$ | `F_czx_abs` | fraction absorbed chlorzoxazone | $1$ | \- | ✓ |
| $\mathrm{Ka}_{\mathrm{abs\_czx}}$ | `Ka_abs_czx` | absorption rate chlorzoxazone | $1.17342368845129$ | 1/hr | ✓ |
| $f_{\mathrm{Ka\_czx}}$ | `f_Ka_czx` | scaling factor of the absorption rate of chlorzoxazone | $1$ | \- | ✓ |
| $\mathrm{Ka}_{\mathrm{abs\_eth}}$ | `Ka_abs_eth` | absorption rate ethanol | $2.47394678419484$ | 1/hr | ✓ |
| $\mathrm{Mr}_{\mathrm{ethanol}}$ | `Mr_ethanol` | Molecular weight ethanol \[g/mole\] | $46.07$ | g/mol | ✓ |
| $\mathrm{absorption}$ | `absorption` | transport of chlorzoxazone out of the lumen |  | mmol/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{czx}_{\mathrm{feces}} &= 0 \cdot \mathrm{Vfeces}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{absorption} &= \frac{f_{\mathrm{Ka\_czx}} \cdot \mathrm{Ka}_{\mathrm{abs\_czx}}}{60} \cdot \mathrm{Vgu} \cdot \mathrm{czx}_{\mathrm{lumen}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{CZXABS}}$ | `CZXABS` | absorption chlorzoxazone | $\mathrm{czx}_{\mathrm{lumen}} \longrightarrow \mathrm{czx}_{\mathrm{ext}}$ |
| $v_{\mathrm{ETHABS}}$ | `ETHABS` | absorption ethanol | $\varnothing \longrightarrow \mathrm{ethanol}_{\mathrm{ext}}$ |
| $v_{\mathrm{CZXEXC}}$ | `CZXEXC` | excretion chlorzoxazone (feces) | $\mathrm{czx}_{\mathrm{lumen}} \longrightarrow \mathrm{czx}_{\mathrm{feces}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{CZXABS}} &= F_{\mathrm{czx\_abs}} \cdot \mathrm{absorption} \\[1ex]
v_{\mathrm{ETHABS}} &= \frac{\frac{\mathrm{Ka}_{\mathrm{abs\_eth}}}{60} \cdot \mathrm{PODOSE}_{\mathrm{ethanol}}}{\mathrm{Mr}_{\mathrm{ethanol}}} \\[1ex]
v_{\mathrm{CZXEXC}} &= \mathopen{}\left(1 - F_{\mathrm{czx\_abs}}\right) \cdot \mathrm{absorption}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{czx}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{CZXABS}} - v_{\mathrm{CZXEXC}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{czx}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{v_{\mathrm{CZXABS}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{czx}_{\mathrm{feces}}}{\mathrm{d} t} &= v_{\mathrm{CZXEXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{ethanol}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{v_{\mathrm{ETHABS}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{PODOSE}_{\mathrm{ethanol}}}{\mathrm{d} t} &= -v_{\mathrm{ETHABS}} \cdot \mathrm{Mr}_{\mathrm{ethanol}} \qquad \text{(rate rule)}
\end{aligned}
$$
