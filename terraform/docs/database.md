Cloud SQL
=============

### Benchmarks

50 clients, 2 threads, running for 60 seconds, only INSERT (progress every 10sec):

```bash
pgbench -h 35.240.57.101  -p 5432 -U him -c 50 -j 2 -P 10 -T 60 -n -f <(echo 'INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (2, 3, 4, 1000, CURRENT_TIMESTAMP)') benchmark

# OUTPUT:
pgbench (14.5 (Ubuntu 14.5-0ubuntu0.22.04.1), server 14.4)
progress: 10.0 s, 2965.1 tps, lat 13.770 ms stddev 34.036
progress: 20.0 s, 4036.1 tps, lat 12.326 ms stddev 26.955
progress: 30.0 s, 4324.3 tps, lat 11.580 ms stddev 23.839
progress: 40.0 s, 3958.1 tps, lat 12.589 ms stddev 30.076
progress: 50.0 s, 4356.4 tps, lat 11.486 ms stddev 20.375
progress: 60.0 s, 3870.7 tps, lat 12.895 ms stddev 31.398
transaction type: /dev/fd/63
scaling factor: 1
query mode: simple
number of clients: 50
number of threads: 2
duration: 60 s
number of transactions actually processed: 235157
latency average = 12.353 ms
latency stddev = 27.700 ms
initial connection time = 1794.170 ms
tps = 4038.209269 (without initial connection time)
```

1 client, 1 thread, running for 60 seconds, only INSERT (progress every 10sec):

```bash
pgbench -h 35.240.57.101  -p 5432 -U him -c 1 -j 1 -P 60 -T 60 -n -f <(echo 'INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (2, 3, 4, 1000, CURRENT_TIMESTAMP)') benchmark

# OUTPUT:

pgbench (14.5 (Ubuntu 14.5-0ubuntu0.22.04.1), server 14.4)
progress: 10.0 s, 122.0 tps, lat 8.140 ms stddev 0.549
progress: 20.0 s, 122.5 tps, lat 8.161 ms stddev 0.547
progress: 30.0 s, 121.6 tps, lat 8.227 ms stddev 0.792
progress: 40.0 s, 121.7 tps, lat 8.210 ms stddev 0.611
progress: 50.0 s, 120.7 tps, lat 8.286 ms stddev 0.906
progress: 60.0 s, 119.7 tps, lat 8.357 ms stddev 0.830
transaction type: /dev/fd/63
scaling factor: 1
query mode: simple
number of clients: 1
number of threads: 1
duration: 60 s
number of transactions actually processed: 7283
latency average = 8.230 ms
latency stddev = 0.723 ms
initial connection time = 66.096 ms
tps = 121.506991 (without initial connection time)
```

**CONCLUSION:** the [him Python Worker](https://hyperion.qairos.net/ph/him-worker) with 200 insert/sec for table `book` is just doing fine. I could speed things up by using multi threading, but [SQLAlchemy is not thread safe](https://docs.sqlalchemy.org/en/13/orm/session_basics.html#is-the-session-thread-safe) like verything else in Python (i.e [GIL](https://wiki.python.org/moin/GlobalInterpreterLock)).