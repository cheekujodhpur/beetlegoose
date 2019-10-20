
def wait_on(q, msg):
    while True:
        print("Waiting on %s" % msg)
        rcvd = q.get()
        if msg == rcvd:
            return
        else:
            print("got: %s" % rcvd)
