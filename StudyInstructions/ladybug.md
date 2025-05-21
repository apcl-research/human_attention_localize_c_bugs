# ladybug - sway[sway d6f2799]

## Project Synopsis:  										
sway is an i3-compatible Wayland compositor		

----------------------------------------------------------------------------------------------------------------

| Please make sure you have CALIBRATED and STARTED TRACKING before starting!  |
|-----------------------------------------------------------------------------|

## -------------------------START OF BUG REPORT-------------------------
## Title: sway_switch is never destroyed
```
Direct leak of 280 byte(s) in 7 object(s) allocated from:
    #0 0x7f18aa588fb9 in __interceptor_calloc /usr/src/debug/gcc/libsanitizer/asan/asan_malloc_linux.cpp:154
    #1 0x5562660d724c in sway_switch_create ../sway/sway/input/switch.c:9
    #2 0x5562660d724c in seat_configure_switch ../sway/sway/input/seat.c:815
    #3 0x5562660d724c in seat_configure_device ../sway/sway/input/seat.c:881
```

`sway_switch` devices are created but never destroyed on teardown.

## -------------------------END OF BUG REPORT-------------------------
	
	
