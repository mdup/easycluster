import zmq
import subprocess

def worker():
    # Setup ZMQ sockets.
    context = zmq.Context()
    sock_in = context.socket(zmq.PULL)
    sock_in.connect("tcp://192.168.196.1:5557") # IP of master
    sock_out = context.socket(zmq.PUSH)
    sock_out.connect("tcp://192.168.196.1:5558") # IP of master

    while True:
        work = sock_in.recv_json()
        p = work['p']
        q = work['q']
        print "running computation p=%d, q=%d" % (p, q)
        result = run_computation(p, q)
        sock_out.send(result)

# Delegate the hard work to the C++ binary, and retrieve its results.
def run_computation(p, q):
    return subprocess.check_output(["./think", str(p), str(q)])
