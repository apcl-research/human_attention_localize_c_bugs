# silverfish redis[redis 6.2.6 4930d19]

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
## Title: A memory leak in the example module "hello cluster"
### Describe the bug

When running the following, there is a memory leak during the ping callback. 

1. Create the clusters.
Utilized the script create-cluster provided in utils.
```
$ ./utils/create-cluster/create-cluster start
$ ./utils/create-cluster/create-cluster create
```

2. Load the module.
Utilized redis-cli. Using MODULE LOAD to load the module.
```
$ ./src/redis-cli -p 30001
127.0.0.1:30001> MOUDLE LOAD ./src/modules/hellocluster.so
OK
$ ./src/redis-cli -p 30002
127.0.0.1:30001> MOUDLE LOAD ./src/modules/hellocluster.so
OK
```

3. Trigger the callback.
```
$ ./src/redis-cli -p 30001
127.0.0.1:30001> hellocluster.pingall
OK
```
Then the cluster 30002 will trigger the call back.


During these steps automatic memory management 
(enabled by calling RedisModule_AutoMemory at the 
beginning of a command) is NOT enabled. 

## -------------------------END OF BUG REPORT-------------------------
	
### Hint: Many of the `RedisModule*` function definitions are in `module.c` 
