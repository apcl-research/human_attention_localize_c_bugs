# grasshopper - mbedtls[mbedtls 179f33a]

 ## Project Synopsis:  										
 	Mbed TLS is a C library that implements cryptographic primitives, X.509 certificate manipulation and the SSL/TLS and DTLS protocols.
 	Its small code footprint makes it suitable for embedded systems.						
## -----------------------------------------------------------------------------------------------------

#####################################---CALIBRATION REQUIRED---####################################
## -----------------------------------------------------------------------------------------------------
## Note: Start a new tracking session.
## -----------------------------------------------------------------------------------------------------


#####################################---START OF BUG REPORT---####################################
## Title: mbedtls_x509_set_extension(..) leads to a segementation fault
### Summary
When calling the function `mbedtls_x509_set_extension(..)` with the value `0xFFFFFFFF` 
for the parameter `val_len`, there is a segmentation fault.

### System information
Mbed TLS version (number or commit id): `4aad0ff` (current development branch)  
Operating system and version: Ubuntu 22.04.3 LTS  
Configuration (if not default, please attach `mbedtls_config.h`): default  
Compiler and options (if you used a pre-built binary, please indicate how you obtained it): see "Steps to reproduce"  
Additional environment information: -  

### Expected behavior
Return error (e.g. `MBEDTLS_ERR_X509_BAD_INPUT_DATA`).

### Actual behavior
Segmentation fault

### Steps to reproduce
Call `mbedtls_x509_set_extension(..)` with the value `0xFFFFFFFF` for the parameter `val_len`.

Example `programs/x509/set_ext.c`:

```
#include "mbedtls/x509_csr.h"
#include "mbedtls/oid.h"
#include <stdio.h>

#define EXT_KEY_USAGE_TMP_BUF_MAX_LENGTH 12

int x509_set_extension_length_check(int val_len)
{
    int ret = 0;

    mbedtls_x509write_csr ctx;
    mbedtls_x509write_csr_init(&ctx);
    unsigned char buf[EXT_KEY_USAGE_TMP_BUF_MAX_LENGTH] = { 0 };
    unsigned char *p = buf + sizeof(buf);

    ret = mbedtls_x509_set_extension(&(ctx.MBEDTLS_PRIVATE(extensions)),
                                        MBEDTLS_OID_EXTENDED_KEY_USAGE,
                                        MBEDTLS_OID_SIZE(MBEDTLS_OID_EXTENDED_KEY_USAGE),
                                        0,
                                        p,
                                        val_len);

    return ret;
}

int main(void){
    int ret = 0;
    
    ret = x509_set_extension_length_check(0xFFFFFFFE);      // -0x2880 == MBEDTLS_ERR_X509_ALLOC_FAILED
    printf("val_len: 0xFFFFFFFE -> ret: -0x%04x\n", -ret); 

    ret = x509_set_extension_length_check(0xFFFFFFFF);      // Segementation fault
    printf("val_len: 0xFFFFFFFF -> ret: -0x%04x\n", -ret);
}
```

Build command:

```
cc -Wall -Wextra -Wformat=2 -Wno-format-nonliteral -I../tests/include -I../include -D_FILE_OFFSET_BITS=64 -I../3rdparty/everest/include -I../3rdparty/everest/include/everest -I../3rdparty/everest/include/everest/kremlib -I../3rdparty/p256-m/p256-m/include -I../3rdparty/p256-m/p256-m/include/p256-m -I../3rdparty/p256-m/p256-m_driver_interface -O2 x509/set_ext.c    ../tests/src/asn1_helpers.o ../tests/src/bignum_helpers.o ../tests/src/certs.o ../tests/src/fake_external_rng_for_test.o ../tests/src/helpers.o ../tests/src/psa_crypto_helpers.o ../tests/src/psa_exercise_key.o ../tests/src/random.o ../tests/src/threading_helpers.o ../tests/src/drivers/hash.o ../tests/src/drivers/platform_builtin_keys.o ../tests/src/drivers/test_driver_aead.o ../tests/src/drivers/test_driver_asymmetric_encryption.o ../tests/src/drivers/test_driver_cipher.o ../tests/src/drivers/test_driver_key_agreement.o ../tests/src/drivers/test_driver_key_management.o ../tests/src/drivers/test_driver_mac.o ../tests/src/drivers/test_driver_pake.o ../tests/src/drivers/test_driver_signature.o ../tests/src/test_helpers/ssl_helpers.o -L../library -lmbedtls -lmbedx509 -lmbedcrypto  -o x509/set_ext
```

Execution and Output:
```
./x509/set_ext 
val_len: 0xFFFFFFFE -> ret: -0x2880
zsh: segmentation fault  ./x509/set_ext
```

#####################################---END OF BUG REPORT---####################################
	
	
