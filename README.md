# Load testing homework:

## To launch run: 
- `docker-compose up --build`
- `siege -f urls.txt -c${CONCURRENCY} -t1m`


## Results Table

### *Concurrency 10*:
```
    Transactions:                   1480 hits
    Availability:                 100.00 %
    Elapsed time:                  60.48 secs
    Data transferred:               2.07 MB
    Response time:                  0.41 secs
    Transaction rate:              24.47 trans/sec
    Throughput:                     0.03 MB/sec
    Concurrency:                    9.95
    Successful transactions:        1480
    Failed transactions:               0
    Longest transaction:            0.73
    Shortest transaction:           0.28

```

### *Concurrency 20*:
```
    Transactions:                   1399 hits
    Availability:                 100.00 %
    Elapsed time:                  60.23 secs
    Data transferred:               1.86 MB
    Response time:                  0.85 secs
    Transaction rate:              23.23 trans/sec
    Throughput:                     0.03 MB/sec
    Concurrency:                   19.78
    Successful transactions:        1399
    Failed transactions:               0
    Longest transaction:            2.37
    Shortest transaction:           0.27

```

### *Concurrency 50*:
```
    Transactions:                   1494 hits
    Availability:                 100.00 %
    Elapsed time:                  60.31 secs
    Data transferred:               2.05 MB
    Response time:                  1.98 secs
    Transaction rate:              24.77 trans/sec
    Throughput:                     0.03 MB/sec
    Concurrency:                   49.09
    Successful transactions:        1494
    Failed transactions:               0
    Longest transaction:            3.62
    Shortest transaction:           0.45
```
### *Concurrency 100*:

```
    Transactions:                   1481 hits
    Availability:                  99.60 %
    Elapsed time:                  60.59 secs
    Data transferred:               1.92 MB
    Response time:                  3.96 secs
    Transaction rate:              24.44 trans/sec
    Throughput:                     0.03 MB/sec
    Concurrency:                   96.68
    Successful transactions:        1481
    Failed transactions:               6
    Longest transaction:            6.91
    Shortest transaction:           2.19

```
