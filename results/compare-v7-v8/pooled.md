## hand9-test_hand9: ft-1.5b-v7 -> ft-1.5b-v8

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 77 | 22 | 6 | 5/3 (0.73), 7/0 (0.016), 10/3 (0.092) |
| abstain | 48 | 2 | 9 | 0/1 (1), 2/4 (0.69), 0/4 (0.12) |
| grounded | 40 | 3 | 4 | 0/0 (1), 3/0 (0.25), 0/4 (0.12) |
| episode | 48 | 16 | 8 | 3/2 (1), 7/1 (0.07), 6/5 (1) |

## mt8-mt8_test_ood: ft-1.5b-v7 -> ft-1.5b-v8

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 334 | 396 | 14 | 130/2 (3.2e-36), 122/4 (2.4e-31), 144/8 (2.2e-33) |
| abstain | 180 | 140 | 2 | 43/0 (2.3e-13), 60/0 (1.7e-18), 37/2 (2.8e-09) |
| grounded | 180 | 175 | 4 | 57/2 (6.1e-15), 64/1 (3.6e-18), 54/1 (3.1e-15) |
| episode | 180 | 423 | 1 | 143/1 (1.3e-41), 140/0 (1.4e-42), 140/0 (1.4e-42) |

## hand8-test_hand8: ft-1.5b-v7 -> ft-1.5b-v8

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 47 | 10 | 6 | 3/2 (1), 4/3 (1), 3/1 (0.62) |
| abstain | 43 | 7 | 10 | 2/3 (1), 3/4 (1), 2/3 (1) |
| grounded | 35 | 14 | 13 | 4/5 (1), 4/4 (1), 6/4 (0.75) |
| episode | 43 | 18 | 14 | 6/5 (1), 6/5 (1), 6/4 (0.75) |

## mt7-mt7_test_ood: ft-1.5b-v7 -> ft-1.5b-v8

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 318 | 27 | 29 | 9/9 (1), 16/6 (0.052), 2/14 (0.0042) |
| abstain | 240 | 0 | 3 | 0/0 (1), 0/1 (1), 0/2 (0.5) |
| grounded | 240 | 11 | 10 | 5/3 (0.73), 1/3 (0.62), 5/4 (1) |
| episode | 240 | 36 | 38 | 14/11 (0.69), 15/9 (0.31), 7/18 (0.043) |

## hand7-test_hand7: ft-1.5b-v7 -> ft-1.5b-v8

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 36 | 9 | 7 | 3/1 (0.62), 2/2 (1), 4/4 (1) |
| abstain | 30 | 1 | 3 | 0/1 (1), 1/1 (1), 0/1 (1) |
| grounded | 27 | 1 | 2 | 0/1 (1), 0/1 (1), 1/0 (1) |
| episode | 30 | 3 | 6 | 1/2 (1), 0/1 (1), 2/3 (1) |

## hand6-test_hand6: ft-1.5b-v7 -> ft-1.5b-v8

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 42 | 2 | 6 | 1/2 (1), 1/3 (0.62), 0/1 (1) |
| abstain | 32 | 0 | 5 | 0/1 (1), 0/2 (0.5), 0/2 (0.5) |
| grounded | 30 | 7 | 4 | 3/1 (0.62), 2/1 (1), 2/2 (1) |
| episode | 32 | 6 | 7 | 3/2 (1), 2/3 (1), 1/2 (1) |

## mtg-mt_test_ood_g: ft-1.5b-v7 -> ft-1.5b-v8

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 31 | 32 | 19/5 (0.0066), 5/15 (0.041), 7/12 (0.36) |
| abstain | 200 | 0 | 1 | 0/0 (1), 0/0 (1), 0/1 (1) |
| grounded | 160 | 4 | 2 | 4/1 (0.38), 0/0 (1), 0/1 (1) |
| episode | 200 | 31 | 30 | 20/5 (0.0041), 4/14 (0.031), 7/11 (0.48) |

## mt-mt_test_ood: ft-1.5b-v7 -> ft-1.5b-v8

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 31 | 32 | 19/5 (0.0066), 5/15 (0.041), 7/12 (0.36) |
| abstain | 200 | 0 | 1 | 0/0 (1), 0/0 (1), 0/1 (1) |
| grounded | 160 | 0 | 2 | 0/1 (1), 0/0 (1), 0/1 (1) |
| episode | 200 | 29 | 30 | 18/5 (0.011), 4/14 (0.031), 7/11 (0.48) |

## test_ood: ft-1.5b-v7 -> ft-1.5b-v8

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 189 | 9 | 6 | 0/2 (0.5), 7/1 (0.07), 2/3 (1) |
| abstain | 105 | 2 | 3 | 1/2 (1), 1/0 (1), 0/1 (1) |

## test_id: ft-1.5b-v7 -> ft-1.5b-v8

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 120 | 0 | 1 | 0/1 (1), 0/0 (1), 0/0 (1) |
| abstain | 60 | 3 | 0 | 0/0 (1), 1/0 (1), 2/0 (0.5) |

