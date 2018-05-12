# 6.437 Project
This is the repository for MIT 6.437 Project I and II in Spring 2018.

## Content
```
.
├── data
│   └── plaintext
│       ├── feynman.txt
│       ├── paradiselost.txt
│       ├── russell.txt
│       └── warandpeace.txt
├── main
│   ├── data
│   │   ├── ngrams
│   │   │   ├── lp1.npy
│   │   │   ├── lp2.npy
│   │   │   └── lp3.npy
│   │   └── word
│   │       └── wlp.pickle
│   ├── decode.py
│   ├── Demo.ipynb
│   ├── _hungarian.py
│   ├── solver.py
│   └── util.py
├── report
├── test
```
 - data: plain text sources
 - main: code: entry point: decode in decode.py
 - report: latex and pdf for report I and II
 - test: a test suite for the code running on MIT Athena
 
 ## Algorithm
 MCMC-based sampling for maximum likelihood estimator for substitution deciphering with 4 improvements:
  - fast ensemble MCMC
  - refined language model
  - linear assignment initialization
  - majority voting and mapping fixing
