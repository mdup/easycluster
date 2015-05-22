import zmq
import sys

def ventilator(p_range, q_range):
    # Setup ZMQ socket
    context = zmq.Context()
    sock = context.socket(zmq.PUSH)
    sock.bind("tcp://0.0.0.0:5557")

    # Iterate over the grid, send each piece of computation to a worker.
    for p in p_range:
        for q in [0.01, 0.1, 1, 10]:
            work = { 'p' : p, 'q': q };
            print "sending work p=%d, q=%d..." % (p, q)
            sock.send_json(work)

def sink(p_range, q_range):
    # Total number of computations.
    n_total = len(p_range) * len(q_range)

    # Setup ZMQ socket.
    context = zmq.Context()
    sock = context.socket(zmq.PULL)
    sock.bind("tcp://0.0.0.0:5558")

    # Accumulate the results until we know all computations are done.
    results = []
    n_processed = 0
    while n_processed < n_total:
        r = sock.recv()
        results.append(r)
        n_processed += 1
    for r in results:
        print r

if __name__ == "__main__":
    p_range = [pow(10, n) for n in xrange(-6, 6)] # All values for the first parameter
    q_range = [pow(10, n) for n in xrange(-6, 6)] # All values for the second parameter

    if len(sys.argv) < 2:
        print "usage: %s (ventilator | sink)" % sys.argv[0]
    elif sys.argv[1] == 'ventilator':
        ventilator(p_range, q_range)
    elif sys.argv[1] == 'sink':
        sink(p_range, q_range)
    else:
        print "usage: %s (ventilator | sink)" % sys.argv[0]
