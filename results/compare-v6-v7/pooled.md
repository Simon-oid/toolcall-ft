## hand8-test_hand8: ft-1.5b-v6 -> ft-1.5b-v7

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 47 | 16 | 4 | 7/1 (0.07), 5/1 (0.22), 4/2 (0.69) |
| abstain | 43 | 16 | 5 | 8/2 (0.11), 4/2 (0.69), 4/1 (0.38) |
| grounded | 35 | 16 | 9 | 9/3 (0.15), 4/3 (1), 3/3 (1) |
| episode | 43 | 25 | 7 | 12/2 (0.013), 8/3 (0.23), 5/2 (0.45) |

## mt7-mt7_test_ood: ft-1.5b-v6 -> ft-1.5b-v7

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 318 | 455 | 16 | 147/7 (3.3e-35), 144/4 (1.1e-37), 164/5 (3e-42) |
| abstain | 240 | 191 | 0 | 69/0 (3.4e-21), 62/0 (4.3e-19), 60/0 (1.7e-18) |
| grounded | 240 | 305 | 3 | 114/1 (5.6e-33), 95/0 (5e-29), 96/2 (3.1e-26) |
| episode | 240 | 463 | 4 | 156/0 (2.2e-47), 148/0 (5.6e-45), 159/4 (5e-42) |

## hand7-test_hand7: ft-1.5b-v6 -> ft-1.5b-v7

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 36 | 14 | 7 | 4/3 (1), 5/2 (0.45), 5/2 (0.45) |
| abstain | 30 | 6 | 1 | 4/0 (0.12), 1/1 (1), 1/0 (1) |
| grounded | 27 | 10 | 1 | 7/0 (0.016), 1/0 (1), 2/1 (1) |
| episode | 30 | 14 | 4 | 7/2 (0.18), 3/1 (0.62), 4/1 (0.38) |

## hand6-test_hand6: ft-1.5b-v6 -> ft-1.5b-v7

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 42 | 15 | 3 | 5/1 (0.22), 4/0 (0.12), 6/2 (0.29) |
| abstain | 32 | 8 | 2 | 4/1 (0.38), 2/1 (1), 2/0 (0.5) |
| grounded | 30 | 19 | 6 | 8/1 (0.039), 6/4 (0.75), 5/1 (0.22) |
| episode | 32 | 20 | 6 | 6/1 (0.12), 7/4 (0.55), 7/1 (0.07) |

## mtg-mt_test_ood_g: ft-1.5b-v6 -> ft-1.5b-v7

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 42 | 49 | 17/29 (0.1), 13/6 (0.17), 12/14 (0.85) |
| abstain | 200 | 1 | 0 | 1/0 (1), 0/0 (1), 0/0 (1) |
| grounded | 160 | 1 | 6 | 1/4 (0.38), 0/1 (1), 0/1 (1) |
| episode | 200 | 38 | 48 | 17/29 (0.1), 11/6 (0.33), 10/13 (0.68) |

## mt-mt_test_ood: ft-1.5b-v6 -> ft-1.5b-v7

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 40 | 49 | 15/29 (0.049), 13/6 (0.17), 12/14 (0.85) |
| abstain | 200 | 2 | 0 | 2/0 (0.5), 0/0 (1), 0/0 (1) |
| grounded | 160 | 3 | 1 | 3/0 (0.25), 0/0 (1), 0/1 (1) |
| episode | 200 | 36 | 45 | 15/26 (0.12), 11/6 (0.33), 10/13 (0.68) |

## test_ood: ft-1.5b-v6 -> ft-1.5b-v7

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 189 | 16 | 6 | 3/2 (1), 6/1 (0.12), 7/3 (0.34) |
| abstain | 105 | 1 | 6 | 1/3 (0.62), 0/2 (0.5), 0/1 (1) |

## test_id: ft-1.5b-v6 -> ft-1.5b-v7

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 120 | 5 | 0 | 3/0 (0.25), 0/0 (1), 2/0 (0.5) |
| abstain | 60 | 2 | 4 | 1/1 (1), 0/1 (1), 1/2 (1) |

