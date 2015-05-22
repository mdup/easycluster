import zmq
import subprocess

def slave():
    # Setup ZMQ.
    context = zmq.Context()
    sock = context.socket(zmq.REQ)
    sock.connect("tcp://192.168.196.1:5557") # IP of master

    while True:
        # Say we're available.
        sock.send_json({ "msg": "available" })

        # Retrieve work and run the computation.
        work = sock.recv_json()
        if work == {}:
            continue
        p = work['p']
        q = work['q']
        print "running computation p=%d, q=%d" % (p, q)
        result = run_computation(p, q)

        # We have a result, let's inform the master about that, and receive the
        # "thanks".
        sock.send_json({ "msg": "result", "result": result})
        sock.recv()

# Delegate the hard work to the C++ binary and retrieve its results from the
# standard output.
def run_computation(p, q):
    return subprocess.check_output(["./think", str(p), str(q)])

if __name__ == "__main__":
    slave()
