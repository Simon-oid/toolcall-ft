## hand7-test_hand7: ft-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 36 | 5 | 47 | 4/15 (0.019), 1/7 (0.07), 0/25 (6e-08) |
| abstain | 30 | 3 | 1 | 0/1 (1), 1/0 (1), 2/0 (0.5) |
| grounded | 27 | 15 | 6 | 5/4 (1), 5/2 (0.45), 5/0 (0.062) |
| episode | 30 | 3 | 15 | 1/4 (0.38), 2/3 (1), 0/8 (0.0078) |

## hand6-test_hand6: ft-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 42 | 2 | 53 | 1/16 (0.00027), 1/10 (0.012), 0/27 (1.5e-08) |
| abstain | 32 | 5 | 2 | 0/1 (1), 1/1 (1), 4/0 (0.12) |
| grounded | 30 | 20 | 9 | 6/3 (0.51), 5/6 (1), 9/0 (0.0039) |
| episode | 32 | 3 | 18 | 0/6 (0.031), 1/5 (0.22), 2/7 (0.18) |

## mtg-mt_test_ood_g: ft-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 5 | 371 | 3/89 (5.2e-23), 2/57 (6.1e-15), 0/225 (3.7e-68) |
| abstain | 200 | 0 | 7 | 0/7 (0.016), 0/0 (1), 0/0 (1) |
| grounded | 160 | 188 | 10 | 67/6 (3.9e-14), 61/2 (4.4e-16), 60/2 (8.5e-16) |
| episode | 200 | 40 | 133 | 8/29 (0.00075), 32/23 (0.28), 0/81 (8.3e-25) |

## mt-mt_test_ood: ft-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 5 | 369 | 3/89 (5.2e-23), 2/57 (6.1e-15), 0/223 (1.5e-67) |
| abstain | 200 | 0 | 7 | 0/7 (0.016), 0/0 (1), 0/0 (1) |
| grounded | 160 | 0 | 18 | 0/7 (0.016), 0/2 (0.5), 0/9 (0.0039) |
| episode | 200 | 2 | 267 | 1/81 (3.4e-23), 1/48 (1.8e-13), 0/138 (5.7e-42) |

## test_ood: ft-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 189 | 1 | 228 | 1/69 (1.2e-19), 0/31 (9.3e-10), 0/128 (5.9e-39) |
| abstain | 105 | 1 | 6 | 0/6 (0.031), 0/0 (1), 1/0 (1) |

## test_id: ft-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 120 | 0 | 132 | 0/40 (1.8e-12), 0/15 (6.1e-05), 0/77 (1.3e-23) |
| abstain | 60 | 1 | 7 | 0/6 (0.031), 0/1 (1), 1/0 (1) |

## hand7-test_hand7: ft-1.5b-v6 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 36 | 7 | 44 | 4/16 (0.012), 3/6 (0.51), 0/22 (4.8e-07) |
| abstain | 30 | 6 | 1 | 3/1 (0.62), 1/0 (1), 2/0 (0.5) |
| grounded | 27 | 9 | 7 | 6/4 (0.75), 1/3 (0.62), 2/0 (0.5) |
| episode | 30 | 7 | 17 | 4/6 (0.75), 3/3 (1), 0/8 (0.0078) |

## hand6-test_hand6: ft-1.5b-v6 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 42 | 3 | 54 | 2/16 (0.0013), 1/11 (0.0063), 0/27 (1.5e-08) |
| abstain | 32 | 6 | 2 | 2/1 (1), 1/1 (1), 3/0 (0.25) |
| grounded | 30 | 10 | 8 | 5/1 (0.22), 1/5 (0.22), 4/2 (0.69) |
| episode | 32 | 4 | 24 | 2/6 (0.29), 1/8 (0.039), 1/10 (0.012) |

## mtg-mt_test_ood_g: ft-1.5b-v6 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 12 | 349 | 7/73 (5.8e-15), 5/54 (1.9e-11), 0/222 (3e-67) |
| abstain | 200 | 0 | 6 | 0/6 (0.031), 0/0 (1), 0/0 (1) |
| grounded | 160 | 1 | 55 | 0/16 (3.1e-05), 1/19 (4e-05), 0/20 (1.9e-06) |
| episode | 200 | 2 | 262 | 1/70 (6.1e-20), 1/57 (4.1e-16), 0/135 (4.6e-41) |

## mt-mt_test_ood: ft-1.5b-v6 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 12 | 351 | 7/75 (1.7e-15), 5/54 (1.9e-11), 0/222 (3e-67) |
| abstain | 200 | 0 | 5 | 0/5 (0.062), 0/0 (1), 0/0 (1) |
| grounded | 160 | 2 | 16 | 1/5 (0.22), 1/2 (1), 0/9 (0.0039) |
| episode | 200 | 2 | 245 | 1/63 (7e-18), 1/47 (3.5e-13), 0/135 (4.6e-41) |

## test_ood: ft-1.5b-v6 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 189 | 5 | 233 | 1/73 (7.9e-21), 2/36 (5.4e-09), 2/124 (1.9e-34) |
| abstain | 105 | 7 | 6 | 1/6 (0.12), 3/0 (0.25), 3/0 (0.25) |

## test_id: ft-1.5b-v6 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 120 | 0 | 128 | 0/38 (7.3e-12), 0/15 (6.1e-05), 0/75 (5.3e-23) |
| abstain | 60 | 2 | 6 | 0/6 (0.031), 0/0 (1), 2/0 (0.5) |

## hand7-test_hand7: dpo-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 36 | 6 | 43 | 4/10 (0.18), 2/8 (0.11), 0/25 (6e-08) |
| abstain | 30 | 3 | 2 | 0/2 (0.5), 0/0 (1), 3/0 (0.25) |
| grounded | 27 | 5 | 7 | 1/3 (0.62), 2/4 (0.69), 2/0 (0.5) |
| episode | 30 | 5 | 20 | 1/4 (0.38), 3/6 (0.51), 1/10 (0.012) |

## hand6-test_hand6: dpo-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 42 | 3 | 50 | 2/13 (0.0074), 1/9 (0.021), 0/28 (7.5e-09) |
| abstain | 32 | 4 | 3 | 0/1 (1), 1/2 (1), 3/0 (0.25) |
| grounded | 30 | 3 | 9 | 2/3 (1), 0/5 (0.062), 1/1 (1) |
| episode | 32 | 1 | 22 | 0/6 (0.031), 1/6 (0.12), 0/10 (0.002) |

## mtg-mt_test_ood_g: dpo-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 26 | 336 | 16/73 (7.2e-10), 10/48 (4.5e-07), 0/215 (3.8e-65) |
| abstain | 200 | 0 | 7 | 0/7 (0.016), 0/0 (1), 0/0 (1) |
| grounded | 160 | 24 | 10 | 7/6 (1), 1/2 (1), 16/2 (0.0013) |
| episode | 200 | 20 | 201 | 11/61 (1.5e-09), 9/34 (0.00017), 0/106 (2.5e-32) |

## mt-mt_test_ood: dpo-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 26 | 336 | 16/73 (7.2e-10), 10/48 (4.5e-07), 0/215 (3.8e-65) |
| abstain | 200 | 0 | 7 | 0/7 (0.016), 0/0 (1), 0/0 (1) |
| grounded | 160 | 6 | 10 | 2/6 (0.29), 0/2 (0.5), 4/2 (0.69) |
| episode | 200 | 15 | 228 | 7/63 (2.3e-12), 8/41 (2e-06), 0/124 (9.4e-38) |

## test_ood: dpo-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 189 | 11 | 224 | 3/63 (1.3e-15), 8/35 (4.2e-05), 0/126 (2.4e-38) |
| abstain | 105 | 1 | 6 | 1/6 (0.12), 0/0 (1), 0/0 (1) |

## test_id: dpo-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 120 | 7 | 129 | 0/38 (7.3e-12), 7/15 (0.13), 0/76 (2.6e-23) |
| abstain | 60 | 0 | 8 | 0/7 (0.016), 0/1 (1), 0/0 (1) |

## hand7-test_hand7: dpo2-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 36 | 4 | 45 | 3/15 (0.0075), 1/5 (0.22), 0/25 (6e-08) |
| abstain | 30 | 26 | 0 | 11/0 (0.00098), 10/0 (0.002), 5/0 (0.062) |
| grounded | 27 | 16 | 1 | 6/1 (0.12), 5/0 (0.062), 5/0 (0.062) |
| episode | 30 | 16 | 13 | 7/4 (0.55), 7/1 (0.07), 2/8 (0.11) |

## hand6-test_hand6: dpo2-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 42 | 1 | 50 | 1/13 (0.0018), 0/10 (0.002), 0/27 (1.5e-08) |
| abstain | 32 | 26 | 0 | 15/0 (6.1e-05), 7/0 (0.016), 4/0 (0.12) |
| grounded | 30 | 17 | 1 | 9/0 (0.0039), 3/0 (0.25), 5/1 (0.22) |
| episode | 32 | 9 | 13 | 5/2 (0.45), 3/2 (1), 1/9 (0.021) |

## mtg-mt_test_ood_g: dpo2-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 15 | 375 | 3/82 (5.3e-21), 12/65 (5.9e-10), 0/228 (4.6e-69) |
| abstain | 200 | 90 | 0 | 42/0 (4.5e-13), 37/0 (1.5e-11), 11/0 (0.00098) |
| grounded | 160 | 76 | 4 | 23/0 (2.4e-07), 11/2 (0.022), 42/2 (1.1e-10) |
| episode | 200 | 80 | 199 | 35/62 (0.008), 34/41 (0.49), 11/96 (4.3e-18) |

## mt-mt_test_ood: dpo2-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 15 | 375 | 3/82 (5.3e-21), 12/65 (5.9e-10), 0/228 (4.6e-69) |
| abstain | 200 | 90 | 0 | 42/0 (4.5e-13), 37/0 (1.5e-11), 11/0 (0.00098) |
| grounded | 160 | 34 | 6 | 25/0 (6e-08), 9/2 (0.065), 0/4 (0.12) |
| episode | 200 | 79 | 248 | 35/62 (0.008), 33/46 (0.18), 11/140 (1.2e-29) |

## test_ood: dpo2-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 189 | 16 | 214 | 5/68 (3.4e-15), 11/22 (0.08), 0/124 (9.4e-38) |
| abstain | 105 | 215 | 0 | 93/0 (2e-28), 103/0 (2e-31), 19/0 (3.8e-06) |

## test_id: dpo2-1.5b-v5 -> dpo3-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 120 | 16 | 127 | 0/38 (7.3e-12), 16/12 (0.57), 0/77 (1.3e-23) |
| abstain | 60 | 117 | 0 | 48/0 (7.1e-15), 59/0 (3.5e-18), 10/0 (0.002) |

