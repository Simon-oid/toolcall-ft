## hand7-test_hand7: ft-1.5b-v5 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 36 | 8 | 9 | 4/3 (1), 3/5 (0.73), 1/1 (1) |
| abstain | 30 | 0 | 24 | 0/12 (0.00049), 0/9 (0.0039), 0/3 (0.25) |
| grounded | 27 | 9 | 15 | 4/8 (0.39), 4/6 (0.75), 1/1 (1) |
| episode | 30 | 3 | 18 | 2/8 (0.11), 1/8 (0.039), 0/2 (0.5) |

## hand6-test_hand6: ft-1.5b-v5 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 42 | 6 | 8 | 2/5 (0.45), 3/2 (1), 1/1 (1) |
| abstain | 32 | 0 | 23 | 0/16 (3.1e-05), 0/7 (0.016), 0/0 (1) |
| grounded | 30 | 14 | 19 | 4/10 (0.18), 5/9 (0.42), 5/0 (0.062) |
| episode | 32 | 7 | 18 | 1/10 (0.012), 3/8 (0.23), 3/0 (0.25) |

## mtg-mt_test_ood_g: ft-1.5b-v5 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 22 | 28 | 4/11 (0.12), 15/17 (0.86), 3/0 (0.25) |
| abstain | 200 | 0 | 97 | 0/49 (3.6e-15), 0/37 (1.5e-11), 0/11 (0.00098) |
| grounded | 160 | 135 | 29 | 59/21 (2.5e-05), 58/8 (1.8e-10), 18/0 (7.6e-06) |
| episode | 200 | 119 | 93 | 48/42 (0.6), 56/40 (0.13), 15/11 (0.56) |

## mt-mt_test_ood: ft-1.5b-v5 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 24 | 28 | 4/11 (0.12), 15/17 (0.86), 5/0 (0.062) |
| abstain | 200 | 0 | 97 | 0/49 (3.6e-15), 0/37 (1.5e-11), 0/11 (0.00098) |
| grounded | 160 | 0 | 46 | 0/32 (4.7e-10), 0/9 (0.0039), 0/5 (0.062) |
| episode | 200 | 18 | 114 | 3/56 (1.2e-13), 10/44 (3.4e-06), 5/14 (0.064) |

## test_ood: ft-1.5b-v5 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 189 | 11 | 40 | 8/13 (0.38), 2/22 (3.6e-05), 1/5 (0.22) |
| abstain | 105 | 0 | 220 | 0/99 (3.2e-30), 0/103 (2e-31), 0/18 (7.6e-06) |

## test_id: ft-1.5b-v5 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 120 | 1 | 22 | 1/3 (0.62), 0/19 (3.8e-06), 0/0 (1) |
| abstain | 60 | 0 | 123 | 0/54 (1.1e-16), 0/60 (1.7e-18), 0/9 (0.0039) |

## hand7-test_hand7: ft-1.5b-v6 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 36 | 12 | 8 | 3/3 (1), 5/4 (1), 4/1 (0.38) |
| abstain | 30 | 0 | 21 | 0/9 (0.0039), 0/9 (0.0039), 0/3 (0.25) |
| grounded | 27 | 3 | 16 | 2/5 (0.45), 0/7 (0.016), 1/4 (0.38) |
| episode | 30 | 3 | 16 | 1/6 (0.12), 1/7 (0.07), 1/3 (0.62) |

## hand6-test_hand6: ft-1.5b-v6 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 42 | 7 | 9 | 2/4 (0.69), 2/2 (1), 3/3 (1) |
| abstain | 32 | 0 | 22 | 0/14 (0.00012), 0/7 (0.016), 0/1 (1) |
| grounded | 30 | 5 | 19 | 2/7 (0.18), 1/8 (0.039), 2/4 (0.69) |
| episode | 32 | 3 | 19 | 0/7 (0.016), 1/9 (0.021), 2/3 (1) |

## mtg-mt_test_ood_g: ft-1.5b-v6 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 55 | 32 | 21/8 (0.024), 19/15 (0.61), 15/9 (0.31) |
| abstain | 200 | 0 | 96 | 0/48 (7.1e-15), 0/37 (1.5e-11), 0/11 (0.00098) |
| grounded | 160 | 1 | 127 | 0/39 (3.6e-12), 1/28 (1.1e-07), 0/60 (1.7e-18) |
| episode | 200 | 35 | 176 | 17/59 (1.4e-06), 8/57 (3.2e-10), 10/60 (8e-10) |

## mt-mt_test_ood: ft-1.5b-v6 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 54 | 33 | 20/9 (0.061), 19/15 (0.61), 15/9 (0.31) |
| abstain | 200 | 0 | 95 | 0/47 (1.4e-14), 0/37 (1.5e-11), 0/11 (0.00098) |
| grounded | 160 | 1 | 43 | 0/29 (3.7e-09), 1/9 (0.021), 0/5 (0.062) |
| episode | 200 | 39 | 113 | 16/51 (2.2e-05), 8/41 (2e-06), 15/21 (0.41) |

## test_ood: ft-1.5b-v6 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 189 | 14 | 44 | 4/13 (0.049), 3/26 (1.5e-05), 7/5 (0.77) |
| abstain | 105 | 0 | 214 | 0/98 (6.3e-30), 0/100 (1.6e-30), 0/16 (3.1e-05) |

## test_id: ft-1.5b-v6 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 120 | 5 | 22 | 3/3 (1), 0/19 (3.8e-06), 2/0 (0.5) |
| abstain | 60 | 0 | 121 | 0/54 (1.1e-16), 0/59 (3.5e-18), 0/8 (0.0078) |

## hand7-test_hand7: dpo-1.5b-v5 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 36 | 15 | 11 | 9/3 (0.15), 4/6 (0.75), 2/2 (1) |
| abstain | 30 | 0 | 25 | 0/13 (0.00024), 0/10 (0.002), 0/2 (0.5) |
| grounded | 27 | 1 | 18 | 0/7 (0.016), 1/8 (0.039), 0/3 (0.25) |
| episode | 30 | 5 | 23 | 3/9 (0.15), 1/10 (0.012), 1/4 (0.38) |

## hand6-test_hand6: dpo-1.5b-v5 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 42 | 9 | 7 | 5/4 (1), 4/2 (0.69), 0/1 (1) |
| abstain | 32 | 0 | 25 | 0/16 (3.1e-05), 0/8 (0.0078), 0/1 (1) |
| grounded | 30 | 3 | 25 | 1/11 (0.0063), 0/8 (0.0078), 2/6 (0.29) |
| episode | 32 | 4 | 21 | 0/9 (0.0039), 2/8 (0.11), 2/4 (0.69) |

## mtg-mt_test_ood_g: dpo-1.5b-v5 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 71 | 21 | 28/6 (0.0002), 30/15 (0.036), 13/0 (0.00024) |
| abstain | 200 | 0 | 97 | 0/49 (3.6e-15), 0/37 (1.5e-11), 0/11 (0.00098) |
| grounded | 160 | 7 | 65 | 0/22 (4.8e-07), 0/10 (0.002), 7/33 (4.2e-05) |
| episode | 200 | 46 | 108 | 14/37 (0.0018), 19/37 (0.022), 13/34 (0.0031) |

## mt-mt_test_ood: dpo-1.5b-v5 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 71 | 21 | 28/6 (0.0002), 30/15 (0.036), 13/0 (0.00024) |
| abstain | 200 | 0 | 97 | 0/49 (3.6e-15), 0/37 (1.5e-11), 0/11 (0.00098) |
| grounded | 160 | 7 | 39 | 1/30 (3e-08), 0/9 (0.0039), 6/0 (0.031) |
| episode | 200 | 50 | 94 | 15/44 (0.0002), 19/39 (0.012), 16/11 (0.44) |

## test_ood: dpo-1.5b-v5 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 189 | 31 | 46 | 16/13 (0.71), 12/28 (0.017), 3/5 (0.73) |
| abstain | 105 | 0 | 220 | 0/98 (6.3e-30), 0/103 (2e-31), 0/19 (3.8e-06) |

## test_id: dpo-1.5b-v5 -> dpo2-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 120 | 11 | 22 | 3/3 (1), 7/19 (0.029), 1/0 (1) |
| abstain | 60 | 0 | 125 | 0/55 (5.6e-17), 0/60 (1.7e-18), 0/10 (0.002) |

