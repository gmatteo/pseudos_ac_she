
```
85_At: OK: Delta=0.5, Delta'=1.58
87_Fr: OK: Delta=0.13, Delta'=1.80
88_Ra: OK: Delta=0.48, Delta'=2.74
       NB: Ra-5spd does not include extra projector for f unlike _Ra_with_f.in
       I believe that _Ra_with_f.in should perform much better in oxides although the df is 0.82
89_Ac: OK: Delta=0.77, Delta'=2.20. my version with projector for empty f makes a huge difference wrt origin.
90_Th: OK: Delta=0.6, Delta'=0.96.
91_Pa: OK: Delta=0.15, Delta'=0.18
           Promoting 1e from 5f to 6d gave the best df.
           Pseudo with atomic GS as reference is also provided.
92_U:  OK. Delta=0.37, Delta'=0.43
93_Np: OK: Delta=0.43,  Delta'=0.49
94_Pu: OK Delta=0.41, Delta'=1.35
95_Am: OK Delta=0.14, Delta'=0.48
       Much better if smaller core radii (FR is problematic to generate)
96_Cm: OK-REASONABLE: Delta=1.27, Delta'=3.61
       NB: very bad if FR wo SOC
97_Bk: OK: Delta=0.24, Delta'=0.43
       NB: excellent agreement with new AE results if NM configuration is used
98_Cf: OK: Delta=0.14, Delta'=0.48
       NB Had to use AE results with magnetic configuration
99_Es: OK: Delta=0.51, Delta'=2.20
       NB: using AE NOMAG as reference. 
100_Fm: OK: AE EOS now looks OK, pseudo is not optimal but df 2.54
        NB: Fm-5spdf-armageddon is the best one to be used.
101_Md: OK Delta=1.81, Delta'=12.25
        NB: I tried different version, this is quite hard (106 Ha) but it's the best I managed 
        to get in terms of delta and convergence profile.
102_No: OK: Delta=0.03, Delta'=0.14
103_Lr: OK: Delta=0.43, Delta'=1.03

=========
Begin_SHE
=========
104_Rf: OK: Delta=1.47, Delta'=1.98
        NB: AE points deviate from the fit
105_Db: OK: Delta=3.43, Delta'=2.8
106_Sg: OK: Delta=1.41, Delta'=0.98
107_Bh: OK: Delta=1.49, Delta'=0.75
108_Hs: OK: Delta=0.65, Delta'=0.31
109_Mt: OK: Delta=2.80, Delta'=1.44
110_Ds: OK: Delta=0.97, Delta'=0.65
111_Rg: OK: Delta=1.87, Delta'=2.16
        NB: AE points deviate from the fit
112_Cn: OK: Delta=0.18, Delta'=4.55
        NB: The best one is the Cn origin_new_new to be sued.
113_Nh: OK: Delta=0.43, Delta'=1.10
        NB: Using new AE NOMAG as reference. Nh_origin.psp8 gives df 1.18
114_Fl: OK: Delta=0.43, Delta'=1.10
        NB: Take my version with f-projector (0.43 vs 1.25)
115_Mc: OK: Delta=1.56, Delta'=2.78
        NB: Take my version with f-projector (1.56 vs 3.08 origin)
        NB: AE points deviate from the fit
116_Lv: OK-REASONABLE: Delta=2.28, Delta'=3.75

117_Ts: OK: Delta=2.15, Delta'=5.42
        NB: AE EOS looks ok, version 6spd is the best one.
 
=========================================
THESE PSEUDOS ARE EXCLUDED FROM THE PAPER
=========================================
    118_Og: FIXME: Can't manage to get decent pseudo for this!
            running with nsppol 2 and spinat (0 0 8). No significant change
            Now using AE NOMAG as reference, best df ~ 0.84 but PS EOS is completely off (small b0 here)
            RERUNNING WITH NEW DATA
=========================================

119_Uue: OK: Delta=0.44, Delta'=5.02
120_Ubn: OK: Delta=0.29, Delta'=2.29
```

# AE results

All AE are fine and the EOS looks perfect and were obtained with TZ2P

# pseudos_ac_she

118 non si ottiene niente di buono Matteo e Christian hanno provato di tutto.

# MG CHANGELOG

Ac: Add 1 projector for f to improve logder.

Th_5f.in: Decrease rc for d by 0.5
          NB: This pseudos uses a sligly excited configuration with fractional occupancies.

Pa_5f.in: Optimize qcut, now ecut ~58

U_5f.in: Optimize qcut, decrease core radii, now ecut ~58, previously it was ~68

Np_5f.in: Optimize qcut, decrease core radii, now ecut ~58, previously it was ~62

Pu_5f.in: decrease rc for d by 0.1, no change in qcut values. 
          Already very good and similar to Np_5f.in
 
Am_5f.in: decrease rc for d by 0.2, no change in qcut values. ecut ~70

Cm_5f.in: decrease rc for d by 0.2, minor adjustments in qcut values. ecut ~70

Bk_5f.in: decrease rc for d by 0.2. No change in qcut values. ecut ~72

CF_5f.in: decrease rc for d by 0.2. Important optimization of qcut values: from ~105 to ~72

Es_5f.in: decrease rc for d by 0.2. No change in qcut values. ecut ~75

Fm_5f.in: decrease rc for d by 0.2. Minor adjustment in qcut values. ecut ~73

Md_5f.in: decrease rc for d by 0.2. Minor adjustment in qcut values. ecut ~75

No_5f.in: decrease rc for d by 0.2. Minor adjustment in qcut values. ecut ~78

Lr_5f.in: decrease rc for p by 0.2, d by 0.05. Minor adjustment in qcut values. ecut ~95 due to rc 1.2 for 5f.
          BTW: twpo possible configurations: [Rn]5f147s27p1 or 5f146d17s2

Rf: decrease rc for p and d. Minor adjustment in qcut values. ecut ~95, previous one ~105
Fb: decrease rc for p and d. Minor adjustment in qcut values. ecut ~96, previous one ~105
Sg: decrease rc for p and d. Minor adjustment in qcut values. ecut ~98, previous one ~108
Bh: decrease rc for p and d. Minor adjustment in qcut values. ecut ~100, previous one ~108
Hs: decrease rc for p and d. Minor adjustment in qcut values. ecut ~102, previous one ~108
Mt: decrease rc for p and d. Minor adjustment in qcut values
Ds: decrease rc for p and d. Minor adjustment in qcut values, increase qc for f, ecut 120,  previous one ~140
Ds: decrease rc for p and d. Minor adjustment in qcut values, increase qc for f, ecut 120,  previous one ~140
Cn: decrease rc for p and d. Minor adjustment in qcut values, increase qc for f, ecut 120,  previous one ~160
Ng: Minor adjustment in qcut values, ecut 125,  previous one ~128

Fl: Add projector for f with ep = 0.05 to improve f-logder
Mg: Add projector for f with ep = 0.05 to improve f-logder
Lv: Add projector for f with ep = 0.05 to improve f-logder
Ts: Decrease rcs significantly. Add projector for f with ep = 0.05 to improve f-logder
Og: Decrease rcs significantly e.g from 1.6 to 1.4. Add projector for f with ep = 0.05 to improve f-logder


Fr: Add two prrojectos for f to improve logder.  Minor adjustment in qcut values. Ecut now ~35

At: Decrease core radii using my new Po-spd.in as starting point. Add extra projector for f-channel with ep 0.05


### FCC COMPUTATIONAL DETAILS####

Spin Orbit Coupling	no
Spin Polarization	collinear (Z)
Smearing Fermi-Dirac	0.001 Ha
K-points	15 x 15 x 15

### OXIDES COMPUTATIONAL DETAILS

------- WE DO NOT USE THESE RESULTS FOR THE PAPER  #CT
Spin Orbit Coupling no
Spin Polarization   collinear (Z)
Smearing Fermi-Dirac    0.05 Ha
K-points    5 x 5 x 5

### DATA FOR PAPERS

1) Delta-Gauge (meV) (FCC system)
2) Lattice percentage difference between AE and PW (FCC system)
3) Plot of hints
4) Delta-Gauge (meV) vs hints
5) Difference between V0 B0 and B0' obtained with AE and PW (FCC system)

