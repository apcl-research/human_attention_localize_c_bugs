# praying_mantis redis[redis 522760f]

## Project Synopsis:  										
Redis is often referred to as a data structures server. 
What this means is that Redis provides access to mutable data structures 
via a set of commands, which are sent using a server-client model with 
TCP sockets and a simple protocol. So different processes can query and 
modify the same data structures in a shared way.		

----------------------------------------------------------------------------------------------------------------

| Please make sure you have CALIBRATED and STARTED TRACKING before starting!  |
|-----------------------------------------------------------------------------|


## -------------------------START OF BUG REPORT-------------------------
## Title: Heap Buffer Overflow

```
./src/redis-server
5630:C 12 Dec 01:08:14.910 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
5630:C 12 Dec 01:08:14.911 # Redis version=999.999.999, bits=64, commit=522760fa, modified=1, pid=5630, just started
5630:C 12 Dec 01:08:14.911 # Warning: no config file specified, using the default config. In order to specify a config file use ./src/redis-server /path/to/redis.conf
5630:M 12 Dec 01:08:14.914 * Increased maximum number of open files to 10032 (it was originally set to 7168).
                _._
           _.-``__ ''-._
      _.-``    `.  `_.  ''-._           Redis 999.999.999 (522760fa/1) 64 bit
  .-`` .-```.  ```\/    _.,_ ''-._
 (    '      ,       .-`  | `,    )     Running in standalone mode
 |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
 |    `-._   `._    /     _.-'    |     PID: 5630
  `-._    `-._  `-./  _.-'    _.-'
 |`-._`-._    `-.__.-'    _.-'_.-'|
 |    `-._`-._        _.-'_.-'    |           http://redis.io
  `-._    `-._`-.__.-'_.-'    _.-'
 |`-._`-._    `-.__.-'    _.-'_.-'|
 |    `-._`-._        _.-'_.-'    |
  `-._    `-._`-.__.-'_.-'    _.-'
      `-._    `-.__.-'    _.-'
          `-._        _.-'
              `-.__.-'

5630:M 12 Dec 01:08:14.918 # Server initialized
5630:M 12 Dec 01:08:14.918 * DB loaded from disk: 0.000 seconds
5630:M 12 Dec 01:08:14.918 * Ready to accept connections
=================================================================
==5630==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x603000009ec6 at pc 0x000104feaaf4 bp 0x7ffeeac7d180 sp 0x7ffeeac7d178
READ of size 1 at 0x603000009ec6 thread T0
    #0 0x104feaaf3 in stringmatchlen util.c
    #1 0x104ffb812 in keysCommand db.c:521
    #2 0x104fa82ec in call server.c:2242
    #3 0x104fa9f90 in processCommand server.c:2524
    #4 0x104fe4ead in processInputBuffer networking.c:1363
    #5 0x104f8f5fa in aeProcessEvents ae.c:421
    #6 0x104f90290 in aeMain ae.c:464
    #7 0x104fb2328 in main server.c:3912
    #8 0x7fff626ca144 in start (libdyld.dylib:x86_64+0x1144)

0x603000009ec6 is located 0 bytes to the right of 22-byte region [0x603000009eb0,0x603000009ec6)
allocated by thread T0 here:
    #0 0x10540ba83 in wrap_malloc (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0x56a83)
    #1 0x104fc107e in zmalloc zmalloc.c:98
    #2 0x104fedd81 in createStringObject object.c:85
    #3 0x104fe3bfa in processMultibulkBuffer networking.c:1302
    #4 0x104fe4e71 in processInputBuffer networking.c:1353
    #5 0x104f8f5fa in aeProcessEvents ae.c:421
    #6 0x104f90290 in aeMain ae.c:464
    #7 0x104fb2328 in main server.c:3912
    #8 0x7fff626ca144 in start (libdyld.dylib:x86_64+0x1144)

SUMMARY: AddressSanitizer: heap-buffer-overflow util.c in stringmatchlen
Shadow bytes around the buggy address:
  0x1c0600001380: fa fa fd fd fd fa fa fa fd fd fd fa fa fa fd fd
  0x1c0600001390: fd fa fa fa fd fd fd fa fa fa fd fd fd fa fa fa
  0x1c06000013a0: fd fd fd fa fa fa fd fd fd fa fa fa fd fd fd fa
  0x1c06000013b0: fa fa fd fd fd fa fa fa fd fd fd fa fa fa fd fd
  0x1c06000013c0: fd fa fa fa fd fd fd fa fa fa fd fd fd fa fa fa
=>0x1c06000013d0: 00 00 00 fa fa fa 00 00[06]fa fa fa 00 00 00 fa
  0x1c06000013e0: fa fa 00 00 00 fa fa fa fa fa fa fa fa fa fa fa
  0x1c06000013f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c0600001400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c0600001410: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1c0600001420: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==5630==ABORTING
[1]    5630 abort      ./src/redis-server
```

## -------------------------END OF BUG REPORT-------------------------
	
	
