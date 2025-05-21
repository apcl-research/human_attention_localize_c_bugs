# cricket - openssl[openssl b6144bb] 

## Project Synopsis:  										
OpenSSL:  OpenSSL is a robust, commercial-grade, full-featured Open Source Toolkit for the TLS 
(formerly SSL), DTLS and QUIC (currently client side only) protocols.		

----------------------------------------------------------------------------------------------------------------

| Please make sure you have CALIBRATED and STARTED TRACKING before starting!  |
|-----------------------------------------------------------------------------|

## -------------------------START OF BUG REPORT-------------------------
## Title: Array index out of bounds with OPENSSL_TRACE=ALL
When environment variable OPENSSL_TRACE is set to ALL, the openssl command fails with an array index overflow:

```
# export OPENSSL_TRACE=ALL
# openssl
TRACE[00:00:03:FF:AE:2E:C7:D0]:TRACE: Attach channel 0x60d000000450 to category 'TRACE' (with callback)
TRACE[00:00:03:FF:AE:2E:C7:D0]:TRACE: Attach channel 0x60d0000006c0 to category 'INIT' (with callback)
TRACE[00:00:03:FF:AE:2E:C7:D0]:TRACE: Attach channel 0x60d000000930 to category 'TLS' (with callback)
TRACE[00:00:03:FF:AE:2E:C7:D0]:TRACE: Attach channel 0x60d000000ba0 to category 'TLS_CIPHER' (with callback)
TRACE[00:00:03:FF:AE:2E:C7:D0]:TRACE: Attach channel 0x60d000000e10 to category 'CONF' (with callback)
TRACE[00:00:03:FF:AE:2E:C7:D0]:TRACE: Attach channel 0x60d000001080 to category 'ENGINE_TABLE' (with callback)
TRACE[00:00:03:FF:AE:2E:C7:D0]:TRACE: Attach channel 0x60d0000012f0 to category 'ENGINE_REF_COUNT' (with callback)
TRACE[00:00:03:FF:AE:2E:C7:D0]:TRACE: Attach channel 0x60d000001560 to category 'PKCS5V2' (with callback)
TRACE[00:00:03:FF:AE:2E:C7:D0]:TRACE: Attach channel 0x60d0000017d0 to category 'PKCS12_KEYGEN' (with callback)
TRACE[00:00:03:FF:AE:2E:C7:D0]:TRACE: Attach channel 0x60d000001a40 to category 'PKCS12_DECRYPT' (with callback)
TRACE[00:00:03:FF:AE:2E:C7:D0]:TRACE: Attach channel 0x60d000001cb0 to category 'X509V3_POLICY' (with callback)
TRACE[00:00:03:FF:AE:2E:C7:D0]:TRACE: Attach channel 0x60d000001f20 to category 'BN_CTX' (with callback)
TRACE[00:00:03:FF:AE:2E:C7:D0]:TRACE: Attach channel 0x60d000002190 to category 'STORE' (with callback)
TRACE[00:00:03:FF:AE:2E:C7:D0]:TRACE: Attach channel 0x60d000002400 to category 'DECODER' (with callback)
TRACE[00:00:03:FF:AE:2E:C7:D0]:TRACE: Attach channel 0x60d000002670 to category 'ENCODER' (with callback)
TRACE[00:00:03:FF:AE:2E:C7:D0]:TRACE: Attach channel 0x60d0000028e0 to category 'REF_COUNT' (with callback)
crypto/trace.c:362:9: runtime error: index 17 out of bounds for type 'trace_category_st [17]'
```
I guess this is reported by the address sanitizer.

## -------------------------END OF BUG REPORT-------------------------
	
	
