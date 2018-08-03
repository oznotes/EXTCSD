# EXTCSD Decoder



------------

#### Decoding using JEDEC's Datasheet.

------------



### [](#header-3)How to use


*   save your extcsd.bin
*   run the script.


### [](#header-3) Screen shot :


EXTCSD Decoder

========================================

Device density : 3,696 MB.

Boot Partition Size : 2048 kB.

RPMB Size : 2048 kB.

Boot 1 with ACK enabled [0x48]

CSD version No. 1.2

CSD Spec  : [ 4.1, 4.2, 4.3, 4.4, 4.41, 4.5, 4.51, 5.0, 5.01, 5.1 ]

Revision 1.5 (for MMC v4.41)

GPP1 : 0 kB. GPP2 : 0 kB. GPP3 : 0 kB. GPP4 : 0 kB.

PARTITIONING_SUPPORT [160] :

        n/a.

        Device can have enhanced technological features in partitions and user data area

        Device supports partitioning features

USER_WP [171] :

        Password protection features are enabled.

        Host is permitted to set PERM_WP_PROTECT .

        Permanent write protection is ON.

BOOT_BUS_CONDITIONS [177] :

        Use single data rate + backward compatible timings in boot operation (default).

        Reset bus width to x1, single data rate and backward compatible

         timings after boot operation (default)

        X1 (sdr) or x4 (ddr) bus width in boot operation mode (default)

BOOT_INFO [228] :

        Device supports high speed timing during boot.

        Device supports dual data rate during boot.

        Device supports alternative boot method.

         [+] Device must show [1] since this is mandatory in v4.4 standard

SEC_FEATURE_SUPPORT [231] :

        Device supports the sanitize operation.

        Device supports the secure and insecure trim operations.

        Device supports the automatic erase operation on retired

          defective portions of the array.

        Secure purge operations are not supported on the device.

PRE_EOL_INFO [267] :

        STATUS = Not Defined
