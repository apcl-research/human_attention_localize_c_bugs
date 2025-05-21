# weevil - openssl[openssl 0c9646e] 

## Project Synopsis:  										
OpenSSL:  OpenSSL is a robust, commercial-grade, full-featured Open Source Toolkit for the TLS 
(formerly SSL), DTLS and QUIC (currently client side only) protocols.		

----------------------------------------------------------------------------------------------------------------

| Please make sure you have CALIBRATED and STARTED TRACKING before starting!  |
|-----------------------------------------------------------------------------|


## -------------------------START OF BUG REPORT-------------------------
## Title: A double free bug in crypto/http/http_client.c

File: crypto/http/http_client.c
Bug Function: BIO *OSSL_HTTP_get

## -------------------------END OF BUG REPORT-------------------------

