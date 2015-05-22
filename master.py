import zmq

def master(p_range, q_range):
    # Setup ZMQ.
    context = zmq.Context()
    sock = context.socket(zmq.REP)
    sock.bind("tcp://0.0.0.0:5557")

    # Generate the json messages for all computations.
    works = generate_works(p_range, q_range)

    # How many calculations are expected?
    n_total = len(p_range) * len(q_range)

    # Loop until all results arrived.
    results = []
    while len(results) < n_total:
        # Receive;
        j = sock.recv_json()

        # First case: worker says "I'm available". Send him some work.
        if j['msg'] == "available":
            send_next_work(sock, works)

        # Second case: worker says "Here's your result". Store it, say thanks.
        elif j['msg'] == "result":
            r = j['result']
            results.append(r)
            send_thanks(sock)

    # Results are all in.
    print "=== Results ==="
    for r in results:
        print r

def generate_works(p_range, q_range):
    # We want to span all (p, q) combinations.
    for p in p_range:
        for q in q_range:
            work = { 'p' : p, 'q': q };
            print "sending work p=%f, q=%f..." % (p, q)
            yield work

def send_next_work(sock, works):
    try:
        work = works.next()
        sock.send_json(work)
    except StopIteration:
        # If no more work is available, we still have to reply something.
        sock.send_json({})

def send_thanks(sock):
    sock.send("") # Nothing more to say actually

if __name__ == "__main__":
    p_range = [pow(10, n) for n in xrange(-6, 6)] # All values for the first parameter
    q_range = [pow(10, n) for n in xrange(-6, 6)] # All values for the second parameter

    master(p_range, q_range)
