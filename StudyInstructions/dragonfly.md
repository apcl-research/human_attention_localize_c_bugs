# dragonfly - curl[curl fdfc2bb]


 ## Project Synopsis:  										
 	Curl: Curl is a command-line tool for transferring data specified with URL syntax.						
## -----------------------------------------------------------------------------------------------------

#####################################---CALIBRATION REQUIRED---####################################
## -----------------------------------------------------------------------------------------------------
## Note: Start a new tracking session.
## -----------------------------------------------------------------------------------------------------


#####################################---START OF BUG REPORT---####################################
## Title: Memory leak in Curl_pin_peer_pubkey function
There is a memory leak in lib\vtls\vtls.c function: Curl_pin_peer_pubkey

### I expected the following
No memory leak.

## curl/libcurl version
[curl -V output]

### operating system

#####################################---END OF BUG REPORT---####################################
	
	
