import redvypr
import time


r = redvypr.redvypr()
dlist = r.add_device('test_device')
dev = dlist[0]['device']
dev.thread_start()
time.sleep(1)
dlist = r.add_device('iored')
dev = dlist[0]['device']
dev.thread_start()


