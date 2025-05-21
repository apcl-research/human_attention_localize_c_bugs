# firefly - openssl[openssl 6fa9a84] 

## Project Synopsis:  										
OpenSSL:  OpenSSL is a robust, commercial-grade, full-featured Open Source Toolkit for the TLS 
(formerly SSL), DTLS and QUIC (currently client side only) protocols.		

----------------------------------------------------------------------------------------------------------------

| Please make sure you have CALIBRATED and STARTED TRACKING before starting!  |
|-----------------------------------------------------------------------------|


## -------------------------START OF BUG REPORT-------------------------
## Title: LeakSanitizer: detected memory leaks
I am using OpenSSL version 3.0.9 and observed a memory leak error when running the following command on the arm platform.
LD_PRELOAD=/usr/lib64/libasan.so.6 ./openssl_3/bin/openssl dgst -list
Use the built-in libasan of the system to sterilize addresses.

The command output is as follows:
```
Supported digests:
-blake2b512                -blake2s256                -md4
-md5                       -md5-sha1                  -mdc2
-ripemd                    -ripemd160                 -rmd160
-sha1                      -sha224                    -sha256
-sha3-224                  -sha3-256                  -sha3-384
-sha3-512                  -sha384                    -sha512
-sha512-224                -sha512-256                -shake128
-shake256                  -sm3                       -ssl3-md5
-ssl3-sha1                 -whirlpool

=================================================================
==645655==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 4560 byte(s) in 19 object(s) allocated from:
    #0 0xffffb7beee10 in __interceptor_malloc ../../../../libsanitizer/asan/asan_malloc_linux.cpp:149
    #1 0xffffb77cc760 in CRYPTO_malloc crypto/mem.c:190
    #2 0xffffb77cc78c in CRYPTO_zalloc crypto/mem.c:197
    #3 0xffffb7781a40 in evp_md_new crypto/evp/digest.c:863
    #4 0xffffb7781d78 in evp_md_from_algorithm crypto/evp/digest.c:943
    #5 0xffffb7797004 in construct_evp_method crypto/evp/evp_fetch.c:239
    #6 0xffffb77c77ec in ossl_method_construct_this crypto/core_fetch.c:109
    #7 0xffffb77c70c4 in algorithm_do_map crypto/core_algorithm.c:77
    #8 0xffffb77c7200 in algorithm_do_this crypto/core_algorithm.c:122
    #9 0xffffb77db8a0 in ossl_provider_doall_activated crypto/provider_core.c:1431
    #10 0xffffb77c7300 in ossl_algorithm_do_all crypto/core_algorithm.c:162
    #11 0xffffb77c7918 in ossl_method_construct crypto/core_fetch.c:153
    #12 0xffffb77973b8 in inner_evp_generic_fetch crypto/evp/evp_fetch.c:344
    #13 0xffffb77975b0 in evp_generic_fetch crypto/evp/evp_fetch.c:396
    #14 0xffffb7782380 in EVP_MD_fetch crypto/evp/digest.c:1073
    #15 0x4335e4 in show_digests (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4335e4)
    #16 0xffffb77f0668 in OBJ_NAME_do_all_sorted crypto/objects/o_names.c:346
    #17 0x4343c8 in dgst_main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4343c8)
    #18 0x4422e8 in do_cmd (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4422e8)
    #19 0x421e70 in main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421e70)
    #20 0xffffb7405ffc in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #21 0xffffb74060d4 in __libc_start_main_impl ../csu/libc-start.c:409
    #22 0x421fac in _start (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421fac)

Indirect leak of 1064 byte(s) in 19 object(s) allocated from:
    #0 0xffffb7beee10 in __interceptor_malloc ../../../../libsanitizer/asan/asan_malloc_linux.cpp:149
    #1 0xffffb77cc760 in CRYPTO_malloc crypto/mem.c:190
    #2 0xffffb77cc78c in CRYPTO_zalloc crypto/mem.c:197
    #3 0xffffb77de248 in CRYPTO_THREAD_lock_new crypto/threads_pthread.c:50
    #4 0xffffb7781a54 in evp_md_new crypto/evp/digest.c:866
    #5 0xffffb7781d78 in evp_md_from_algorithm crypto/evp/digest.c:943
    #6 0xffffb7797004 in construct_evp_method crypto/evp/evp_fetch.c:239
    #7 0xffffb77c77ec in ossl_method_construct_this crypto/core_fetch.c:109
    #8 0xffffb77c70c4 in algorithm_do_map crypto/core_algorithm.c:77
    #9 0xffffb77c7200 in algorithm_do_this crypto/core_algorithm.c:122
    #10 0xffffb77db8a0 in ossl_provider_doall_activated crypto/provider_core.c:1431
    #11 0xffffb77c7300 in ossl_algorithm_do_all crypto/core_algorithm.c:162
    #12 0xffffb77c7918 in ossl_method_construct crypto/core_fetch.c:153
    #13 0xffffb77973b8 in inner_evp_generic_fetch crypto/evp/evp_fetch.c:344
    #14 0xffffb77975b0 in evp_generic_fetch crypto/evp/evp_fetch.c:396
    #15 0xffffb7782380 in EVP_MD_fetch crypto/evp/digest.c:1073
    #16 0x4335e4 in show_digests (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4335e4)
    #17 0xffffb77f0668 in OBJ_NAME_do_all_sorted crypto/objects/o_names.c:346
    #18 0x4343c8 in dgst_main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4343c8)
    #19 0x4422e8 in do_cmd (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4422e8)
    #20 0x421e70 in main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421e70)
    #21 0xffffb7405ffc in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #22 0xffffb74060d4 in __libc_start_main_impl ../csu/libc-start.c:409
    #23 0x421fac in _start (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421fac)

Indirect leak of 224 byte(s) in 1 object(s) allocated from:
    #0 0xffffb7beee10 in __interceptor_malloc ../../../../libsanitizer/asan/asan_malloc_linux.cpp:149
    #1 0xffffb77cc760 in CRYPTO_malloc crypto/mem.c:190
    #2 0xffffb77cc78c in CRYPTO_zalloc crypto/mem.c:197
    #3 0xffffb77d9968 in provider_new crypto/provider_core.c:459
    #4 0xffffb77db590 in provider_activate_fallbacks crypto/provider_core.c:1315
    #5 0xffffb77db6f4 in ossl_provider_doall_activated crypto/provider_core.c:1370
    #6 0xffffb77c7300 in ossl_algorithm_do_all crypto/core_algorithm.c:162
    #7 0xffffb77c7918 in ossl_method_construct crypto/core_fetch.c:153
    #8 0xffffb77973b8 in inner_evp_generic_fetch crypto/evp/evp_fetch.c:344
    #9 0xffffb77975b0 in evp_generic_fetch crypto/evp/evp_fetch.c:396
    #10 0xffffb7782380 in EVP_MD_fetch crypto/evp/digest.c:1073
    #11 0x4335e4 in show_digests (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4335e4)
    #12 0xffffb77f0668 in OBJ_NAME_do_all_sorted crypto/objects/o_names.c:346
    #13 0x4343c8 in dgst_main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4343c8)
    #14 0x4422e8 in do_cmd (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4422e8)
    #15 0x421e70 in main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421e70)
    #16 0xffffb7405ffc in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #17 0xffffb74060d4 in __libc_start_main_impl ../csu/libc-start.c:409
    #18 0x421fac in _start (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421fac)

Indirect leak of 175 byte(s) in 19 object(s) allocated from:
    #0 0xffffb7beee10 in __interceptor_malloc ../../../../libsanitizer/asan/asan_malloc_linux.cpp:149
    #1 0xffffb77cc760 in CRYPTO_malloc crypto/mem.c:190
    #2 0xffffb77cebe8 in CRYPTO_strndup crypto/o_str.c:43
    #3 0xffffb77c7418 in ossl_algorithm_get1_first_name crypto/core_algorithm.c:195
    #4 0xffffb7781e50 in evp_md_from_algorithm crypto/evp/digest.c:959
    #5 0xffffb7797004 in construct_evp_method crypto/evp/evp_fetch.c:239
    #6 0xffffb77c77ec in ossl_method_construct_this crypto/core_fetch.c:109
    #7 0xffffb77c70c4 in algorithm_do_map crypto/core_algorithm.c:77
    #8 0xffffb77c7200 in algorithm_do_this crypto/core_algorithm.c:122
    #9 0xffffb77db8a0 in ossl_provider_doall_activated crypto/provider_core.c:1431
    #10 0xffffb77c7300 in ossl_algorithm_do_all crypto/core_algorithm.c:162
    #11 0xffffb77c7918 in ossl_method_construct crypto/core_fetch.c:153
    #12 0xffffb77973b8 in inner_evp_generic_fetch crypto/evp/evp_fetch.c:344
    #13 0xffffb77975b0 in evp_generic_fetch crypto/evp/evp_fetch.c:396
    #14 0xffffb7782380 in EVP_MD_fetch crypto/evp/digest.c:1073
    #15 0x4335e4 in show_digests (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4335e4)
    #16 0xffffb77f0668 in OBJ_NAME_do_all_sorted crypto/objects/o_names.c:346
    #17 0x4343c8 in dgst_main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4343c8)
    #18 0x4422e8 in do_cmd (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4422e8)
    #19 0x421e70 in main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421e70)
    #20 0xffffb7405ffc in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #21 0xffffb74060d4 in __libc_start_main_impl ../csu/libc-start.c:409
    #22 0x421fac in _start (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421fac)

Indirect leak of 96 byte(s) in 1 object(s) allocated from:
    #0 0xffffb7beee10 in __interceptor_malloc ../../../../libsanitizer/asan/asan_malloc_linux.cpp:149
    #1 0xffffb77cc760 in CRYPTO_malloc crypto/mem.c:190
    #2 0xffffb77cc78c in CRYPTO_zalloc crypto/mem.c:197
    #3 0xffffb7675d8c in BIO_meth_new crypto/bio/bio_meth.c:38
    #4 0xffffb78a2ec0 in ossl_bio_prov_init_bio_method providers/common/bio_prov.c:210
    #5 0xffffb78a2314 in ossl_default_provider_init providers/defltprov.c:582
    #6 0xffffb77da9a8 in provider_init crypto/provider_core.c:930
    #7 0xffffb77dafa8 in provider_activate crypto/provider_core.c:1128
    #8 0xffffb77db5d0 in provider_activate_fallbacks crypto/provider_core.c:1329
    #9 0xffffb77db6f4 in ossl_provider_doall_activated crypto/provider_core.c:1370
    #10 0xffffb77c7300 in ossl_algorithm_do_all crypto/core_algorithm.c:162
    #11 0xffffb77c7918 in ossl_method_construct crypto/core_fetch.c:153
    #12 0xffffb77973b8 in inner_evp_generic_fetch crypto/evp/evp_fetch.c:344
    #13 0xffffb77975b0 in evp_generic_fetch crypto/evp/evp_fetch.c:396
    #14 0xffffb7782380 in EVP_MD_fetch crypto/evp/digest.c:1073
    #15 0x4335e4 in show_digests (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4335e4)
    #16 0xffffb77f0668 in OBJ_NAME_do_all_sorted crypto/objects/o_names.c:346
    #17 0x4343c8 in dgst_main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4343c8)
    #18 0x4422e8 in do_cmd (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4422e8)
    #19 0x421e70 in main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421e70)
    #20 0xffffb7405ffc in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #21 0xffffb74060d4 in __libc_start_main_impl ../csu/libc-start.c:409
    #22 0x421fac in _start (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421fac)

Indirect leak of 56 byte(s) in 1 object(s) allocated from:
    #0 0xffffb7beee10 in __interceptor_malloc ../../../../libsanitizer/asan/asan_malloc_linux.cpp:149
    #1 0xffffb77cc760 in CRYPTO_malloc crypto/mem.c:190
    #2 0xffffb77cc78c in CRYPTO_zalloc crypto/mem.c:197
    #3 0xffffb77de248 in CRYPTO_THREAD_lock_new crypto/threads_pthread.c:50
    #4 0xffffb77d99e0 in provider_new crypto/provider_core.c:471
    #5 0xffffb77db590 in provider_activate_fallbacks crypto/provider_core.c:1315
    #6 0xffffb77db6f4 in ossl_provider_doall_activated crypto/provider_core.c:1370
    #7 0xffffb77c7300 in ossl_algorithm_do_all crypto/core_algorithm.c:162
    #8 0xffffb77c7918 in ossl_method_construct crypto/core_fetch.c:153
    #9 0xffffb77973b8 in inner_evp_generic_fetch crypto/evp/evp_fetch.c:344
    #10 0xffffb77975b0 in evp_generic_fetch crypto/evp/evp_fetch.c:396
    #11 0xffffb7782380 in EVP_MD_fetch crypto/evp/digest.c:1073
    #12 0x4335e4 in show_digests (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4335e4)
    #13 0xffffb77f0668 in OBJ_NAME_do_all_sorted crypto/objects/o_names.c:346
    #14 0x4343c8 in dgst_main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4343c8)
    #15 0x4422e8 in do_cmd (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4422e8)
    #16 0x421e70 in main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421e70)
    #17 0xffffb7405ffc in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #18 0xffffb74060d4 in __libc_start_main_impl ../csu/libc-start.c:409
    #19 0x421fac in _start (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421fac)

Indirect leak of 56 byte(s) in 1 object(s) allocated from:
    #0 0xffffb7beee10 in __interceptor_malloc ../../../../libsanitizer/asan/asan_malloc_linux.cpp:149
    #1 0xffffb77cc760 in CRYPTO_malloc crypto/mem.c:190
    #2 0xffffb77cc78c in CRYPTO_zalloc crypto/mem.c:197
    #3 0xffffb77de248 in CRYPTO_THREAD_lock_new crypto/threads_pthread.c:50
    #4 0xffffb77d9a00 in provider_new crypto/provider_core.c:472
    #5 0xffffb77db590 in provider_activate_fallbacks crypto/provider_core.c:1315
    #6 0xffffb77db6f4 in ossl_provider_doall_activated crypto/provider_core.c:1370
    #7 0xffffb77c7300 in ossl_algorithm_do_all crypto/core_algorithm.c:162
    #8 0xffffb77c7918 in ossl_method_construct crypto/core_fetch.c:153
    #9 0xffffb77973b8 in inner_evp_generic_fetch crypto/evp/evp_fetch.c:344
    #10 0xffffb77975b0 in evp_generic_fetch crypto/evp/evp_fetch.c:396
    #11 0xffffb7782380 in EVP_MD_fetch crypto/evp/digest.c:1073
    #12 0x4335e4 in show_digests (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4335e4)
    #13 0xffffb77f0668 in OBJ_NAME_do_all_sorted crypto/objects/o_names.c:346
    #14 0x4343c8 in dgst_main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4343c8)
    #15 0x4422e8 in do_cmd (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4422e8)
    #16 0x421e70 in main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421e70)
    #17 0xffffb7405ffc in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #18 0xffffb74060d4 in __libc_start_main_impl ../csu/libc-start.c:409
    #19 0x421fac in _start (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421fac)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0xffffb7beee10 in __interceptor_malloc ../../../../libsanitizer/asan/asan_malloc_linux.cpp:149
    #1 0xffffb77cc760 in CRYPTO_malloc crypto/mem.c:190
    #2 0xffffb784eac4 in OPENSSL_sk_deep_copy crypto/stack/stack.c:87
    #3 0xffffb77d8e00 in sk_INFOPAIR_deep_copy crypto/provider_local.h:16
    #4 0xffffb77d9a64 in provider_new crypto/provider_core.c:474
    #5 0xffffb77db590 in provider_activate_fallbacks crypto/provider_core.c:1315
    #6 0xffffb77db6f4 in ossl_provider_doall_activated crypto/provider_core.c:1370
    #7 0xffffb77c7300 in ossl_algorithm_do_all crypto/core_algorithm.c:162
    #8 0xffffb77c7918 in ossl_method_construct crypto/core_fetch.c:153
    #9 0xffffb77973b8 in inner_evp_generic_fetch crypto/evp/evp_fetch.c:344
    #10 0xffffb77975b0 in evp_generic_fetch crypto/evp/evp_fetch.c:396
    #11 0xffffb7782380 in EVP_MD_fetch crypto/evp/digest.c:1073
    #12 0x4335e4 in show_digests (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4335e4)
    #13 0xffffb77f0668 in OBJ_NAME_do_all_sorted crypto/objects/o_names.c:346
    #14 0x4343c8 in dgst_main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4343c8)
    #15 0x4422e8 in do_cmd (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4422e8)
    #16 0x421e70 in main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421e70)
    #17 0xffffb7405ffc in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #18 0xffffb74060d4 in __libc_start_main_impl ../csu/libc-start.c:409
    #19 0x421fac in _start (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421fac)

Indirect leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0xffffb7beee10 in __interceptor_malloc ../../../../libsanitizer/asan/asan_malloc_linux.cpp:149
    #1 0xffffb77cc760 in CRYPTO_malloc crypto/mem.c:190
    #2 0xffffb77cc78c in CRYPTO_zalloc crypto/mem.c:197
    #3 0xffffb790174c in ossl_prov_ctx_new providers/common/provider_ctx.c:16
    #4 0xffffb78a22f4 in ossl_default_provider_init providers/defltprov.c:581
    #5 0xffffb77da9a8 in provider_init crypto/provider_core.c:930
    #6 0xffffb77dafa8 in provider_activate crypto/provider_core.c:1128
    #7 0xffffb77db5d0 in provider_activate_fallbacks crypto/provider_core.c:1329
    #8 0xffffb77db6f4 in ossl_provider_doall_activated crypto/provider_core.c:1370
    #9 0xffffb77c7300 in ossl_algorithm_do_all crypto/core_algorithm.c:162
    #10 0xffffb77c7918 in ossl_method_construct crypto/core_fetch.c:153
    #11 0xffffb77973b8 in inner_evp_generic_fetch crypto/evp/evp_fetch.c:344
    #12 0xffffb77975b0 in evp_generic_fetch crypto/evp/evp_fetch.c:396
    #13 0xffffb7782380 in EVP_MD_fetch crypto/evp/digest.c:1073
    #14 0x4335e4 in show_digests (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4335e4)
    #15 0xffffb77f0668 in OBJ_NAME_do_all_sorted crypto/objects/o_names.c:346
    #16 0x4343c8 in dgst_main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4343c8)
    #17 0x4422e8 in do_cmd (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4422e8)
    #18 0x421e70 in main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421e70)
    #19 0xffffb7405ffc in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #20 0xffffb74060d4 in __libc_start_main_impl ../csu/libc-start.c:409
    #21 0x421fac in _start (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421fac)

Indirect leak of 19 byte(s) in 1 object(s) allocated from:
    #0 0xffffb7beee10 in __interceptor_malloc ../../../../libsanitizer/asan/asan_malloc_linux.cpp:149
    #1 0xffffb77cc760 in CRYPTO_malloc crypto/mem.c:190
    #2 0xffffb77ceb70 in CRYPTO_strdup crypto/o_str.c:27
    #3 0xffffb7675db0 in BIO_meth_new crypto/bio/bio_meth.c:41
    #4 0xffffb78a2ec0 in ossl_bio_prov_init_bio_method providers/common/bio_prov.c:210
    #5 0xffffb78a2314 in ossl_default_provider_init providers/defltprov.c:582
    #6 0xffffb77da9a8 in provider_init crypto/provider_core.c:930
    #7 0xffffb77dafa8 in provider_activate crypto/provider_core.c:1128
    #8 0xffffb77db5d0 in provider_activate_fallbacks crypto/provider_core.c:1329
    #9 0xffffb77db6f4 in ossl_provider_doall_activated crypto/provider_core.c:1370
    #10 0xffffb77c7300 in ossl_algorithm_do_all crypto/core_algorithm.c:162
    #11 0xffffb77c7918 in ossl_method_construct crypto/core_fetch.c:153
    #12 0xffffb77973b8 in inner_evp_generic_fetch crypto/evp/evp_fetch.c:344
    #13 0xffffb77975b0 in evp_generic_fetch crypto/evp/evp_fetch.c:396
    #14 0xffffb7782380 in EVP_MD_fetch crypto/evp/digest.c:1073
    #15 0x4335e4 in show_digests (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4335e4)
    #16 0xffffb77f0668 in OBJ_NAME_do_all_sorted crypto/objects/o_names.c:346
    #17 0x4343c8 in dgst_main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4343c8)
    #18 0x4422e8 in do_cmd (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4422e8)
    #19 0x421e70 in main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421e70)
    #20 0xffffb7405ffc in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #21 0xffffb74060d4 in __libc_start_main_impl ../csu/libc-start.c:409
    #22 0x421fac in _start (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421fac)

Indirect leak of 8 byte(s) in 1 object(s) allocated from:
    #0 0xffffb7beee10 in __interceptor_malloc ../../../../libsanitizer/asan/asan_malloc_linux.cpp:149
    #1 0xffffb77cc760 in CRYPTO_malloc crypto/mem.c:190
    #2 0xffffb77ceb70 in CRYPTO_strdup crypto/o_str.c:27
    #3 0xffffb77d9a30 in provider_new crypto/provider_core.c:473
    #4 0xffffb77db590 in provider_activate_fallbacks crypto/provider_core.c:1315
    #5 0xffffb77db6f4 in ossl_provider_doall_activated crypto/provider_core.c:1370
    #6 0xffffb77c7300 in ossl_algorithm_do_all crypto/core_algorithm.c:162
    #7 0xffffb77c7918 in ossl_method_construct crypto/core_fetch.c:153
    #8 0xffffb77973b8 in inner_evp_generic_fetch crypto/evp/evp_fetch.c:344
    #9 0xffffb77975b0 in evp_generic_fetch crypto/evp/evp_fetch.c:396
    #10 0xffffb7782380 in EVP_MD_fetch crypto/evp/digest.c:1073
    #11 0x4335e4 in show_digests (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4335e4)
    #12 0xffffb77f0668 in OBJ_NAME_do_all_sorted crypto/objects/o_names.c:346
    #13 0x4343c8 in dgst_main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4343c8)
    #14 0x4422e8 in do_cmd (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4422e8)
    #15 0x421e70 in main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421e70)
    #16 0xffffb7405ffc in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #17 0xffffb74060d4 in __libc_start_main_impl ../csu/libc-start.c:409
    #18 0x421fac in _start (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421fac)

Indirect leak of 1 byte(s) in 1 object(s) allocated from:
    #0 0xffffb7beee10 in __interceptor_malloc ../../../../libsanitizer/asan/asan_malloc_linux.cpp:149
    #1 0xffffb77cc760 in CRYPTO_malloc crypto/mem.c:190
    #2 0xffffb77cc82c in CRYPTO_realloc crypto/mem.c:213
    #3 0xffffb77dbe40 in ossl_provider_set_operation_bit crypto/provider_core.c:1627
    #4 0xffffb77c7788 in ossl_method_construct_postcondition crypto/core_fetch.c:99
    #5 0xffffb77c7128 in algorithm_do_map crypto/core_algorithm.c:84
    #6 0xffffb77c7200 in algorithm_do_this crypto/core_algorithm.c:122
    #7 0xffffb77db8a0 in ossl_provider_doall_activated crypto/provider_core.c:1431
    #8 0xffffb77c7300 in ossl_algorithm_do_all crypto/core_algorithm.c:162
    #9 0xffffb77c7918 in ossl_method_construct crypto/core_fetch.c:153
    #10 0xffffb77973b8 in inner_evp_generic_fetch crypto/evp/evp_fetch.c:344
    #11 0xffffb77975b0 in evp_generic_fetch crypto/evp/evp_fetch.c:396
    #12 0xffffb7782380 in EVP_MD_fetch crypto/evp/digest.c:1073
    #13 0x4335e4 in show_digests (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4335e4)
    #14 0xffffb77f0668 in OBJ_NAME_do_all_sorted crypto/objects/o_names.c:346
    #15 0x4343c8 in dgst_main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4343c8)
    #16 0x4422e8 in do_cmd (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x4422e8)
    #17 0x421e70 in main (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421e70)
    #18 0xffffb7405ffc in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #19 0xffffb74060d4 in __libc_start_main_impl ../csu/libc-start.c:409
    #20 0x421fac in _start (/home/test1/sse_test/KunpengTrunk/st_install_dir/openssl_3/bin/openssl+0x421fac)

SUMMARY: AddressSanitizer: 6315 byte(s) leaked in 66 allocation(s).
```
## -------------------------END OF BUG REPORT-------------------------

