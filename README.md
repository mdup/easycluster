### Easy cluster parallelization in ZeroMQ

This is meant as a support code for [this blog
post](http://mdup.fr/blog/easy-cluster-parallelization-with-zeromq).

TL;DR: two skeletons to dispatch jobs in a cluster using zeromq. The first, bad
skeleton is "ventilatorsink" + "worker" (PUSH/PULL). It's not good because it
can block if a worker is too long. The good pattern is "master" + "slave"
(REQ/REP).

Marc Dupont [mdup.fr](http://mdup.fr)
