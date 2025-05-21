# stonefly redis[redis fe2fdef]

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
## Title: Potential overflow may cause server panic 
When writing data over 2GB, `rdbSaveLzfStringObject` will return a big negative number, but we just cover the situation of n==-1 and n>0.
If `rdbWriteRaw` overflow, the string will be written twice, the first is compressed, the other is plain. The rdb format will
mismatch and cause serverpanic on loading rdb.

Hint: `rdb*` functions are in `stonefly/src/rdb.c` 

## -------------------------END OF BUG REPORT-------------------------

