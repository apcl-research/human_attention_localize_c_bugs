# hornet - sway[sway 77587ee]

## Project Synopsis:  										
sway is an i3-compatible Wayland compositor		

----------------------------------------------------------------------------------------------------------------

| Please make sure you have CALIBRATED and STARTED TRACKING before starting!  |
|-----------------------------------------------------------------------------|

## -------------------------START OF BUG REPORT-------------------------
## Title: Abort due to double free via workspace command

Using this in a config:

```
workspace "x" gaps "x" "x"
```

causes Sway to output:
```
free(): double free detected in tcache 2
Aborted (core dumped)
```

However, this works:
```
workspace "x" gaps "x" "1"
```

The user should be told to enter a numeric value for the fourth parameter.

Hint: Look in `hornet/hornet_sway_sway/commands`
## -------------------------END OF BUG REPORT-------------------------
	
	
