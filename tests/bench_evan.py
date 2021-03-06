# From http://www.evanjones.ca/memoryallocator/
# Improving Python's Memory Allocator
# Evan Jones

import gc, time

if 1:
    import tracemalloc

    tracemalloc.start()

    def dump_memory(what):
        print("***** %s *****" % what)
        size, peak_size = tracemalloc.get_traced_memory()
        print("traced: %.1f KB (peak: %.1f KB)" % (size / 1024., peak_size / 1024.))

else:
    def dump_memory(what):
        print("***** %s *****" % what)
        with open("/proc/self/status") as fp:
            for line in fp:
                if "VmRSS" not in line:
                    continue
                print(line.rstrip())
                break

iterations = 2000000

start = time.time()
l = []
for i in range( iterations ):
        l.append( None )

dump_memory("None (1)")
print()

for i in range( iterations ):
        l[i] = {}

dump_memory("empty dict (1)")
print()

for i in range( iterations ):
        l[i] = None

dump_memory("None (2)")
print()

for i in range( iterations ):
        l[i] = {}


dump_memory("empty dict (2)")
print()

l = None
gc.collect()
dt = time.time() - start

dump_memory("free memory")
print()

print("Total time: %.1f sec" % dt)

