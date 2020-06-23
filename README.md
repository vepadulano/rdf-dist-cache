# Distributed caching of input datasets in an RDataFrame analysis

`reftree`: Code to recreate the reference `root` file with one single tree and 5 branches.

`tfileprefetch`: Tests with the `TFilePrefetch` ROOT class.

`xrootd`: Tests with an XRootD proxy plugin.

## Preliminary Results

The following table shows 5 consecutive executions of the `mean.cpp` test for the two mechanisms. `n == 0` includes
caching, while the following iterations access the cache and compute the mean. So far it seems that TFilePrefetch has
an advantage. Still need to play around with the `pfc.blocksize` option in XRootD. Execution times are in seconds.

| n | TFilePrefetch | XRootD |
|---|---------------|--------|
| 0 | 83            | 140    |
| 1 | 33            | 29     |
| 2 | 33            | 30     |
| 3 | 33            | 35     |
| 4 | 30            | 30     |