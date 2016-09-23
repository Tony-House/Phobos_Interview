from flask import Flask, make_response, abort, jsonify, request
from math import floor, sqrt
from platform import system
from threading import get_ident
import os

def_prime_limit = 10000000      # Default max prime number N-th, used if none specified in prime_file
def_ping_limit = 10             # Max count of ping
ping_file = 'ping_tmp'          # Temporary files for ping output
prime_file = 'prime_file.txt'   # List of prime numbers, first line contains count of prime numbers in file
doc_file = 'README.md'          # Documentation
prime_limit = 1                 # Actual max prime number N-th
app = Flask(__name__)           # Flask app


def gen_primes():
    """ Generate an infinite sequence of prime numbers. """
    d = {}
    q = 2
    while True:
        if q not in d:
            yield q
            d[q * q] = [q]
        else:
            for p in d[q]:
                d.setdefault(p + q, []).append(p)
            del d[q]
        q += 1


def factoring(n):
    """
    Prime decomposition of a number.
    :argument n -- number to decompose.
    :return q -- list of prime numbers which when all multiplied together, are equal to number n.
    """
    def step(x): return 1 + (x << 2) - ((x >> 1) << 1)
    maxq = int(floor(sqrt(n)))
    d = 1
    q = n % 2 == 0 and 2 or 3
    while q <= maxq and n % q != 0:
        q = step(d)
        d += 1
    return q <= maxq and [q] + factoring(n // q) or [n]


def cross_ping(count, server):
    """
    Ping a specified server specified amount of times. Cross-platform. Output of ping is written into ping_file.
    :argument count -- count of packets.
    :argument server -- IP address or host name to ping.
    :return True/False -- True if host responds to a ping request, False if not.
    """
    """ Returns True if host responds to a ping request """
    ping_arg = '-n' if system().lower() == 'windows' else '-c'
    return os.system('ping ' + ping_arg + ' ' + str(count) + ' ' + server + ' > ' + ping_file + str(get_ident())) == 0


@app.route('/')
def index():
    """ Index page of a server. Displays, if exists, documentation file or short description of usage. """
    if os.path.isfile(doc_file) and os.path.getsize(doc_file) > 0:
        with open(doc_file, 'r') as fd:
            res = fd.read()
    else:
        res = 'API Usage:\r\n' \
               'Prime Number - GET http://localhost:5000/api/prime/%N%\r\n' \
               'Factoring - GET http://localhost:5000/api/factoring/%N%\r\n' \
               'Ping - POST -d "127.0.0.1" http://localhost:5000/api/ping/%N%'
    response = make_response(res)
    response.headers['Content-Type'] = 'text/plain'
    return response


@app.route('/api/prime/<int:count>', methods=['GET'])
def api_prime(count):
    """
    Returns a N-th prime number in in HTTP-response body.
    N must be integer and >= 1. Max N is def_prime_limit or a first line in prime numbers file.
    :argument count -- N.
    """
    # Check if count is within permitted range
    if count < 1:
        abort(400, 'ERROR: Min available prime number is 1-th!')
    if count > prime_limit:
        abort(400, 'ERROR: Max available prime number is ' + str(prime_limit) + '-th!')
    # Access prime numbers file
    if not (os.path.isfile(prime_file) and os.path.getsize(prime_file) > 0):
        abort(500, 'ERROR: Prime numbers file not found!')
    # Locate required prime number
    with open(prime_file) as fd:
        for num, line in enumerate(fd):
            if num == count:
                res = int(line)
                break
    # Return required prime number as string
    return str(res)


@app.route('/api/factoring/<int:number>', methods=['GET'])
def api_factoring(number):
    """
    Returns a prime decomposition of a number N in HTTP-response body.
    N must be integer and >= 2.
    :argument number -- N.
    """
    # Check if number is within permitted range
    if number <= 1:
        abort(400, 'ERROR: Min possible number for factoring is 2!')
    # Return list of prime multipliers as JSON
    return jsonify(factoring(number))


@app.route('/api/ping/<int:count>', methods=['POST'])
def api_ping(count):
    """
    Pings a specified in HTTP-request body server N times. Returns full ping output in HTTP-response body.
    N must be integer and >= 1. Max N is def_ping_limit.
    :argument count -- N.
    """
    # Check if count is within permitted range
    if count < 1:
        abort(400, 'ERROR: Min count of packets is 1!')
    if count > def_ping_limit:
        abort(400, 'ERROR: Max count of packets is ' + str(def_ping_limit) + '!')
    # Perform ping
    cross_ping(count, str(request.get_data(), 'utf-8'))
    # Access temporary ping output file
    ping_file_full = ping_file + str(get_ident())
    if not (os.path.isfile(ping_file_full) and os.path.getsize(ping_file_full) > 0):
        abort(500, 'ERROR: Temporary ping output file not found!')
    # Read ping output
    with open(ping_file_full, 'r') as fd:
        res = fd.read()
    # Remove temporary ping output file
    os.remove(ping_file_full)
    # Return ping output as plain text
    response = make_response(res)
    response.headers['Content-Type'] = 'text/plain'
    return response


if __name__ == '__main__':
    # Check if prime numbers file exists
    if os.path.isfile(prime_file) and os.path.getsize(prime_file) > 0:
        with open(prime_file) as fd:
            first_line = fd.readline()
        # Set prime max limit from the first line of prime numbers file
        prime_limit = int(first_line)
    else:
        # Populate prime numbers file (might take a while, depending on how big is def_prime_limit)
        fd = open(prime_file, 'w')
        fd.write(str(def_prime_limit) + '\r\n')
        count = 0
        for prime in gen_primes():
            fd.write(str(prime) + '\r\n')
            count += 1
            if count == def_prime_limit:
                break
        fd.close()
        # Set prime max limit as def_prime_limit
        prime_limit = def_prime_limit
    app.run(threaded=True)
