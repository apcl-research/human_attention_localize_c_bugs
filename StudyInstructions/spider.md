# spider - sway[sway 8d7ebc2]

## Project Synopsis:  										
sway is an i3-compatible Wayland compositor		

----------------------------------------------------------------------------------------------------------------

| Please make sure you have CALIBRATED and STARTED TRACKING before starting!  |
|-----------------------------------------------------------------------------|

## -------------------------START OF BUG REPORT-------------------------
## Title: swaynag: double-free crash

Sway Version: sway version 1.0-beta.2-39-g1442d4e6 (Dec 17 2018, branch 'master')

Debug Log: N/A

Configuration File: N/A

Running swaynag without any arguments crashes. 

```
jaeger:~ $ gdb `which swaynag`   
GNU gdb (GDB) Fedora 8.2-5.fc29
[... snip .... ]
2018-12-17 13:40:09 - [swaynag/main.c:80] No message passed. Please provide --message/-m
free(): double free detected in tcache 2

Program received signal SIGABRT, Aborted.
0x00007ffff789f53f in raise () from /lib64/libc.so.6
[... snip ...]
(gdb) bt
#0  0x00007ffff789f53f in raise () at /lib64/libc.so.6
#1  0x00007ffff7889895 in abort () at /lib64/libc.so.6
#2  0x00007ffff78e2927 in __libc_message () at /lib64/libc.so.6
#3  0x00007ffff78e925c in  () at /lib64/libc.so.6
#4  0x00007ffff78ead45 in _int_free () at /lib64/libc.so.6
#5  0x0000000000407b73 in swaynag_destroy (swaynag=0x412b60 <swaynag>) at ../swaynag/swaynag.c:419
#6  0x0000000000404db2 in main (argc=1, argv=0x7fffffffdb08) at ../swaynag/main.c:130
```

## -------------------------END OF BUG REPORT-------------------------
	
	
