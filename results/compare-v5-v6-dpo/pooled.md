## hand7-test_hand7: ft-1.5b-v5 -> ft-1.5b-v6

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 36 | 3 | 8 | 2/1 (1), 1/4 (0.38), 0/3 (0.25) |
| abstain | 30 | 0 | 3 | 0/3 (0.25), 0/0 (1), 0/0 (1) |
| grounded | 27 | 12 | 5 | 3/4 (1), 5/0 (0.062), 4/1 (0.38) |
| episode | 30 | 5 | 7 | 3/4 (1), 1/2 (1), 1/1 (1) |

## hand6-test_hand6: ft-1.5b-v5 -> ft-1.5b-v6

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 42 | 5 | 5 | 1/2 (1), 1/0 (1), 3/3 (1) |
| abstain | 32 | 1 | 2 | 0/2 (0.5), 0/0 (1), 1/0 (1) |
| grounded | 30 | 16 | 7 | 4/5 (1), 5/2 (0.45), 7/0 (0.016) |
| episode | 32 | 11 | 6 | 2/4 (0.69), 4/1 (0.38), 5/1 (0.22) |

## mtg-mt_test_ood_g: ft-1.5b-v5 -> ft-1.5b-v6

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 17 | 46 | 2/22 (3.6e-05), 3/9 (0.15), 12/15 (0.7) |
| abstain | 200 | 0 | 1 | 0/1 (1), 0/0 (1), 0/0 (1) |
| grounded | 160 | 234 | 2 | 78/1 (2.6e-22), 78/1 (2.6e-22), 78/0 (6.6e-24) |
| episode | 200 | 191 | 24 | 60/12 (8.1e-09), 69/4 (2.4e-16), 62/8 (1.8e-11) |

## mt-mt_test_ood: ft-1.5b-v5 -> ft-1.5b-v6

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 18 | 43 | 2/20 (0.00012), 3/9 (0.15), 13/14 (1) |
| abstain | 200 | 0 | 2 | 0/2 (0.5), 0/0 (1), 0/0 (1) |
| grounded | 160 | 0 | 4 | 0/3 (0.25), 0/1 (1), 0/0 (1) |
| episode | 200 | 15 | 37 | 1/19 (4e-05), 3/4 (1), 11/14 (0.69) |

## test_ood: ft-1.5b-v5 -> ft-1.5b-v6

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 189 | 11 | 10 | 6/2 (0.29), 5/2 (0.45), 0/6 (0.031) |
| abstain | 105 | 0 | 6 | 0/1 (1), 0/3 (0.25), 0/2 (0.5) |

## test_id: ft-1.5b-v5 -> ft-1.5b-v6

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 120 | 0 | 4 | 0/2 (0.5), 0/0 (1), 0/2 (0.5) |
| abstain | 60 | 0 | 2 | 0/0 (1), 0/1 (1), 0/1 (1) |

## hand7-test_hand7: ft-1.5b-v5 -> dpo-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 36 | 3 | 8 | 0/5 (0.062), 1/1 (1), 2/2 (1) |
| abstain | 30 | 2 | 1 | 1/0 (1), 1/0 (1), 0/1 (1) |
| grounded | 27 | 12 | 1 | 4/1 (0.38), 5/0 (0.062), 3/0 (0.25) |
| episode | 30 | 7 | 4 | 1/1 (1), 3/1 (0.62), 3/2 (1) |

## hand6-test_hand6: ft-1.5b-v5 -> dpo-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 42 | 2 | 6 | 1/5 (0.22), 0/1 (1), 1/0 (1) |
| abstain | 32 | 2 | 0 | 0/0 (1), 1/0 (1), 1/0 (1) |
| grounded | 30 | 22 | 5 | 6/2 (0.29), 6/2 (0.29), 10/1 (0.012) |
| episode | 32 | 9 | 3 | 1/1 (1), 2/1 (1), 6/1 (0.12) |

## mtg-mt_test_ood_g: ft-1.5b-v5 -> dpo-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 3 | 59 | 0/29 (3.7e-09), 0/17 (1.5e-05), 3/13 (0.021) |
| abstain | 200 | 0 | 0 | 0/0 (1), 0/0 (1), 0/0 (1) |
| grounded | 160 | 168 | 4 | 60/0 (1.7e-18), 60/0 (1.7e-18), 48/4 (1.3e-10) |
| episode | 200 | 116 | 28 | 40/11 (5.7e-05), 42/8 (1.2e-06), 34/9 (0.00017) |

## mt-mt_test_ood: ft-1.5b-v5 -> dpo-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 4 | 58 | 0/29 (3.7e-09), 0/17 (1.5e-05), 4/12 (0.077) |
| abstain | 200 | 0 | 0 | 0/0 (1), 0/0 (1), 0/0 (1) |
| grounded | 160 | 0 | 14 | 0/3 (0.25), 0/0 (1), 0/11 (0.00098) |
| episode | 200 | 4 | 56 | 0/24 (1.2e-07), 0/14 (0.00012), 4/18 (0.0043) |

## test_ood: ft-1.5b-v5 -> dpo-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 189 | 8 | 22 | 1/9 (0.021), 7/11 (0.48), 0/2 (0.5) |
| abstain | 105 | 1 | 1 | 0/1 (1), 0/0 (1), 1/0 (1) |

## test_id: ft-1.5b-v5 -> dpo-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 120 | 0 | 10 | 0/2 (0.5), 0/7 (0.016), 0/1 (1) |
| abstain | 60 | 2 | 0 | 1/0 (1), 0/0 (1), 1/0 (1) |

## hand7-test_hand7: ft-1.5b-v6 -> dpo-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 36 | 9 | 9 | 1/7 (0.07), 4/1 (0.38), 4/1 (0.38) |
| abstain | 30 | 5 | 1 | 4/0 (0.12), 1/0 (1), 0/1 (1) |
| grounded | 27 | 7 | 3 | 5/1 (0.22), 1/1 (1), 1/1 (1) |
| episode | 30 | 11 | 6 | 5/4 (1), 4/1 (0.38), 2/1 (1) |

## hand6-test_hand6: ft-1.5b-v6 -> dpo-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 42 | 4 | 8 | 1/4 (0.38), 0/2 (0.5), 3/2 (1) |
| abstain | 32 | 4 | 1 | 2/0 (0.5), 1/0 (1), 1/1 (1) |
| grounded | 30 | 11 | 3 | 5/0 (0.062), 2/1 (1), 4/2 (0.69) |
| episode | 32 | 8 | 7 | 3/1 (0.62), 1/3 (0.62), 4/3 (1) |

## mtg-mt_test_ood_g: ft-1.5b-v6 -> dpo-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 25 | 52 | 13/22 (0.18), 2/13 (0.0074), 10/17 (0.25) |
| abstain | 200 | 1 | 0 | 1/0 (1), 0/0 (1), 0/0 (1) |
| grounded | 160 | 2 | 70 | 1/18 (7.6e-05), 1/18 (7.6e-05), 0/34 (1.2e-10) |
| episode | 200 | 23 | 102 | 13/32 (0.0066), 0/31 (9.3e-10), 10/39 (3.8e-05) |

## mt-mt_test_ood: ft-1.5b-v6 -> dpo-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 252 | 23 | 52 | 11/22 (0.08), 2/13 (0.0074), 10/17 (0.25) |
| abstain | 200 | 2 | 0 | 2/0 (0.5), 0/0 (1), 0/0 (1) |
| grounded | 160 | 4 | 14 | 3/3 (1), 1/0 (1), 0/11 (0.00098) |
| episode | 200 | 21 | 51 | 11/17 (0.34), 0/13 (0.00024), 10/21 (0.071) |

## test_ood: ft-1.5b-v6 -> dpo-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 189 | 14 | 29 | 2/14 (0.0042), 7/14 (0.19), 5/1 (0.22) |
| abstain | 105 | 6 | 0 | 0/0 (1), 3/0 (0.25), 3/0 (0.25) |

## test_id: ft-1.5b-v6 -> dpo-1.5b-v5

| metric | n per seed | fixed | broken | per seed fixed/broken (McNemar p) |
|---|---|---|---|---|
| call right | 120 | 1 | 7 | 0/0 (1), 0/7 (0.016), 1/0 (1) |
| abstain | 60 | 4 | 0 | 1/0 (1), 1/0 (1), 2/0 (0.5) |

