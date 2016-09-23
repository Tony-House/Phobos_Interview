# Project Title

Phobos Interview Server

## Installing

Download phobos_server.py.

### Requirements

Windows/Linux, ping, Python3, Flask, bash (for tests).

## Running

```
python phobos_server.py
```

## API

Root request returns this documentation file or information on usage in text/plain.
API includes 3 methods:

### Prime Number

Returns a N-th prime number in HTTP-response body.
N must be integer and >= 1. Max N is **10000000** (can be changed via variable *def_prime_limit* in *phobos_server.py*) or a first line in prime numbers file.
```
**Example:** curl -X GET http://localhost:5000/api/prime/%N%
```

### Factoring

Returns a prime decomposition of a number N in HTTP-response body.
N must be integer and >= 2.
```
**Example:** curl -X GET http://localhost:5000/api/factoring/%N%
```

### Ping

Pings a specified in HTTP-request body server N times. Returns full ping output in HTTP-response body.
N must be integer and >= 1. Max N is **10** (can be changed via variable *def_ping_limit* in *phobos_server.py*).
```
**Example:** curl -X POST -d "127.0.0.1" http://localhost:5000/api/ping/%N%
```

## Files

```
[phobos_server.py](phobos_server.py) - Main program.
[phobos_test.sh](phobos_test.sh) - Test script.
ping_tmp-%% - Temporary files for ping output (can be changed via variable *ping_file* in *phobos_server.py*).
[prime_file.txt](prime_file.txt) - List of prime numbers, first line contains count of prime numbers in file (can be changed via variable *prime_file* in *phobos_server.py*).
[README.md](README.md) - Documentation (can be changed via variable *doc_file* in *phobos_server.py*).
```

## Tests

You can use manual testing (with curl for localhost:5000, for example) or automated with script.

### Automated Testing

Test script for phobos_server.py. Emulates multiple clients with multiple random requests with curl.
**Usage:** phobos_test.sh arg1 arg2 arg3
    arg1 - amount of clients per test, >= 1, <= 50.
    arg2 - amount of requests per client, >= 1, <= 50.
    arg3 - log file(s) with test commands and output.
```
**Example:** ./phobos_test.sh 10 10 phobos_test_log
```

### Compare Results

```
[Prime Number](https://primes.utm.edu/nthprime/index.php)
[Factoring](http://www.calculatorsoup.com/calculators/math/prime-factors.php)
[Ping](http://ping.eu/ping/)
```

## Improvements

Some ideas, maybe worth implementing.
1 - Use pickle for prime_file (requires more RAM to load list).
2 - Buff numbers with 0 and use *seek* for prime_file (larger file, but faster loading).
3 - Use database for prime_file (more code, but probably faster).
4 - Generate prime numbers every time (very slow and memory-consumable, but no max limit).
5 - Use subprocess instead of os.system (remove ping_tmp files, but ping will not be compatible with Windows).
6 - Return True/False or something else instead of full ping output (remove ping_tmp files).

## License

This project is licensed under the GNU GPLv3.
