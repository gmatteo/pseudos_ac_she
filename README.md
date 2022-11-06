# Finalized

85_At: OK: At-spd. May try At-d
87_Fr: OK Take Fr.psp8. Smoother convergence 
88_Ra: OK-Reasonable: Ra_origin ?
89_Ac: OK. my version with projector for empty f makes a huge difference wrt origin.
90_Th: OK. Take my version. Much better
91_Pa: FIXME: AE EOS looks OK but best pseudo has 5.44 df. Running Pa_5f_new: Does not improve XXX
92_U:  FIXME: Running U_5f_new: Does not improve XXX
93_Np: FIXME: AE EOS looks OK but best pseudo has 15.50 df! Running new pseudo
94_Pu: OK: Take my version. Much better.
95_Am: OK-Reasonable. Take Am_5f_origin?
96_Cm: OK Take my version. Harder but more accurate.
97_Bk: FIXME AE EOS looks suspicious. New results are needed.
98_Cf: OK: take Cf_5f.psp8, slightly better than Cf_origin_5f.psp8
99_Es:  FIXME: AE EOS is completely wrong!
100_Fm: FIXME: AE EOS now looks good but pseudos are not!
101_Md: FIXME: AE EOS is suspicious
102_No: OK: All pseudos are good, should find compromise btw accuracy and convergence ratio
103_Lr: OK-TODO: Take: Lr_5f_origin
104_Rf: OK-TODO: Take Rf.psp8 algthugh convergence in ecut can be improved
105_Db: OK: Take Db.psp8
106_Sg: OK: Take Sg_origin.psp8
107_Bh: OK-TODO Take Bh.psp8 Perhaps, one can accelerate a bit the convergence.
108_Hs: OK-TODO: Take Hs.psp8: Perhaps, one can accelerate a bit the convergence.
109_Mt: OK-TODO: Take Mt.psp8, Perhaps, one can accelerate a bit the convergence.
110_Ds: OK: Take my version with smoother MCC and 0.93 vs 2.79 from origin

111_Rg: TODO: RUNNING Rg.in
112_Rg: TODO: Slow ecut conv, df good but there are discrepancies wrt AE. Cn_new.in is the best so far.

113_Nh: Requires extra work
114_Fl: OK: Take my Fl.psp8 with f-projector (0.42 vs 1.25)
115_Mc: OK: Take Mc_new.psp8 with f-projector (1.56 vs 3.08 origin)
116_Lv: Requires extra work
117_Ts: Requires extra work, use Ts.in as starting point
118_Og: ???


# AE results

Weird results for AE EOS of 100_Fm  ------> REDONE AND UPDATED #CT

# pseudos_ac_she

5f 91-92 rifare 

118-119 rifare

no5f da 90 a 102 guardare attentamente

no 5f 103 fare 

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


Fr: Add two projectos for f to improve logder.  Minor adjustment in qcut values. Ecut now ~35

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

