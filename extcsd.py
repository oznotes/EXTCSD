import binascii
import sys
import os

__author__ = "Oz"
__copyright__ = "EXT CSD Decoder"
__credits__ = ["https://gist.github.com/kylemanna/5692543"]


def str2bytearray(s):
    if len(s) % 2:
        s = '0' + s
    reorder = True
    if reorder:
        r = []
        i = 1
        while i <= len(s):
            r.append(s[len(s) - i - 1])
            r.append(s[len(s) - i])
            i += 2
        s = ''.join(r)
    out = bytearray(binascii.unhexlify(s))
    return out


def dec_to_bin(x):
    return int(bin(x)[2:])


def is_not_empty(s):  # if string is empty or not
    """
    :param s: String
    :return: Bool value given the string if empty will return True
    """
    return bool(s and s.strip())


if __name__ == '__main__':
    PARTITION_CONFIG_KEY = \
        {
            '0x0': 'Device not boot enabled (default)',
            '0x00': 'Device not boot enabled (default)',
            '0x8': 'Boot 1 enabled ',
            '0x08': 'Boot 1 enabled ',
            '0x10': 'Boot 2 enabled ',
            '0x38': 'User Area enabled ',
            '0x40': 'Device Not Boot Enabled ',
            '0x48': 'Boot 1 with ACK enabled ',
            '0x50': 'Boot 2 with ACK enabled ',
            '0x78': 'User Area with ACK enabled '
        }
    EXTCSD_REVISION = \
        {
            '0x8': 'Revision 1.8 (for MMC v5.1)',
            '0x7': 'Revision 1.7 (for MMC v5.0, v5.01) ',
            '0x6': 'Revision 1.6 (for MMC v4.5, v4.51) ',
            '0x5': 'Revision 1.5 (for MMC v4.41) ',
            '0x4': 'Revision 1.4 (Obsolete) ',
            '0x3': 'Revision 1.3 (for MMC v4.3) ',
            '0x2': 'Revision 1.2 (for MMC v4.2) ',
            '0x1': 'Revision 1.1 (for MMC v4.1) ',
            '0x0': 'Revision 1.0 (for MMC v4.0) '
        }
    CSD_REVISION = \
        {
            '0x2': 'CSD version No. 1.2  \n' +
            'CSD Spec  : [ 4.1, 4.2, 4.3, 4.4, 4.41, 4.5, 4.51, 5.0, 5.01, 5.1 ] ',
            '0x1': 'CSD version No. 1.1 [ Allocated by MMCA ] ',
            '0x0': 'CSD version No. 1.0 [ Allocated by MMCA ] '
        }
    SEC_FEATURE_SUPPORT_KEY = \
        {   # 0 1 2 3 4 5 6 SEC_FEATURE_SUPPORT_ECSD List
            # 6 5 4 3 2 1 0 from JEDEC Manual
            'SEC_SANITIZE':
                {
                    '0x1': 'Device supports the sanitize operation.',  # 0 digit
                    '0x0': 'Device does not support the sanitizeoperation.',
                },
            'SEC_GB_CL_EN(R)':
                {
                    '0x0': 'Device does not support the secure and insecure trim operations.',  # 2 digit
                    '0x1': 'Device supports the secure and insecure trim operations.'
                },
            'SEC_BD_BLK_EN(R)':
                {
                    '0x0': 'Device does not support the automatic erase operation \n'   # 4 digit
                           '\t  on retired defective portions of the array.',
                    '0x1': 'Device supports the automatic erase operation on retired \n'
                           '\t  defective portions of the array.',
                },
            'SECURE_ER_EN(R)':
                {
                    '0x0': 'Secure purge operations are not supported on the device.',  # 6 digit
                    '0x1': 'Secure purge operations are supported.',
                }
        }
    BOOT_BUS_CONDITIONS = \
        {   # BOOT_BUS_CONDITIONS [177]
            # 0 1 2 |3 4 | 5 6 7 BOOT_BUS_CONDITIONS_ECSD List
            # 7 6 5 |4 3 | 2 1 0 from JEDEC Manual
            'BOOT_MODE':
                {
                    '0x0': 'Use single data rate + backward compatible timings in boot operation (default).',
                    '0x1': 'Use single data rate + High Speed timings in boot operation mode.',
                    '0x2': 'Use dual data rate in boot operation.',
                    '0x3': 'Reserved  NOTE'
                },
            'RESET_BOOT_BUS_CONDITIONS':
                {
                    '0x0': 'Reset bus width to x1, single data rate and backward compatible \n '
                           '\t timings after boot operation (default)',
                    '0x1': 'Retain BOOT_BUS_WIDTH and BOOT_MODE values after boot operation. \n'
                           'This is relevant to Push-pull mode operation only. '
                },
            'BOOT_BUS_WIDTH':
                {
                    '0x0': 'X1 (sdr) or x4 (ddr) bus width in boot operation mode (default)',
                    '0x1': 'X4 (sdr/ddr) bus width in boot operation mode',
                    '0x2': 'X8 (sdr/ddr) bus width in boot operation mode',
                    '0x3': 'Reserved'
                }
        }

    if os.path.isfile("extcsd.bin") is True:
            if os.path.getsize("extcsd.bin") > 512:
                print "File size for extcsd.bin should be 512 bytes"
                sys.exit()
            else:
                f = open("extcsd.bin", "rb")
                file_contents = f.read()
                f.close()
                if is_not_empty(file_contents) is True:
                    ecsd_str = binascii.hexlify(''.join(reversed(file_contents)))
                    ecsd = str2bytearray(ecsd_str)
                    line_len = 16
                    i = 0
                    while i < len(ecsd):
                        sys.stdout.write("{0:04x}:\t".format(i))
                        for j in range(line_len):
                            if i < len(ecsd):
                                sys.stdout.write("{0:=02x}".format(ecsd[i]))
                                i = i + 1
                            else:
                                break
                            if j == (line_len - 1):
                                pass
                            elif i % 4:
                                sys.stdout.write(" ")
                            else:
                                sys.stdout.write("   ")
                        sys.stdout.write("\n")
                else:
                    print "File is empty"
                    sys.exit()
    else:
        print "File not found"
        sys.exit()

    GP1_SIZE_MULT_X_0 = int(ecsd[143])
    GP1_SIZE_MULT_X_1 = int(ecsd[144])
    GP1_SIZE_MULT_X_2 = int(ecsd[145])
    GP2_SIZE_MULT_X_0 = int(ecsd[146])
    GP2_SIZE_MULT_X_1 = int(ecsd[147])
    GP2_SIZE_MULT_X_2 = int(ecsd[148])
    GP3_SIZE_MULT_X_0 = int(ecsd[149])
    GP3_SIZE_MULT_X_1 = int(ecsd[150])
    GP3_SIZE_MULT_X_2 = int(ecsd[151])
    GP4_SIZE_MULT_X_0 = int(ecsd[152])
    GP4_SIZE_MULT_X_1 = int(ecsd[153])
    GP4_SIZE_MULT_X_2 = int(ecsd[154])
    HC_WP_GRP_SIZE_ECSD = int(ecsd[221])
    HC_ERASE_GRP_SIZE_ECSD = int(ecsd[224])
    # ecsd177  =  ('{:08d}'.format(ecsd[177]))
    SEC_FEATURE_SUPPORT_ECSD = list(str(dec_to_bin(ecsd[231])))
    BOOT_BUS_CONDITIONS_ECSD = dec_to_bin(ecsd[177])
    BOOT_BUS_CONDITIONS_ECSD = list(('{:08d}'.format(int(BOOT_BUS_CONDITIONS_ECSD))))
    CSD_rev = "0x{:x}".format(ecsd[194])
    EXT_CSD_rev = "0x{:x}".format(ecsd[192])
    partition_config = "0x{:x}".format(ecsd[179])
    SEC_SANITIZE_K = SEC_FEATURE_SUPPORT_ECSD[0]
    SEC_GB_CL_EN_K = SEC_FEATURE_SUPPORT_ECSD[2]
    SEC_BD_BLK_EN_K = SEC_FEATURE_SUPPORT_ECSD[4]
    SECURE_ER_EN_K = SEC_FEATURE_SUPPORT_ECSD[6]
    BOOT_MODE_K = '0x' + str(int(BOOT_BUS_CONDITIONS_ECSD[3] + BOOT_BUS_CONDITIONS_ECSD[4], 2))
    RESET_BOOT_BUS_CONDITIONS_K = '0x' + str(int(BOOT_BUS_CONDITIONS_ECSD[5]))
    BOOT_BUS_WIDTH_K = '0x' + str(int(BOOT_BUS_CONDITIONS_ECSD[6] + BOOT_BUS_CONDITIONS_ECSD[7], 2))
    boot_size = int(ecsd[226]) * 128  # BOOT_SIZE_MULT [226] Boot Partition size = 128K bytes * BOOT_SIZE_MULT
    rpmb_size = int(ecsd[168]) * 128  # RPMB_SIZE_MULT [168] RPMB partition size = 128kB * RPMB_SIZE_MULT
    HC_WP_GRP_SIZE = 512 * int(ecsd[224]) * int(ecsd[221]) * 1024
    HC_ERASE_GRP_SIZE = 512 * int(ecsd[224]) * 1024

    GPP1_SIZE = (GP1_SIZE_MULT_X_2 * 2**16 + GP1_SIZE_MULT_X_1 * 2**8 + GP1_SIZE_MULT_X_0 * 2**0
                 ) * HC_ERASE_GRP_SIZE_ECSD * HC_WP_GRP_SIZE_ECSD * 512
    GPP2_SIZE = (GP2_SIZE_MULT_X_2 * 2**16 + GP2_SIZE_MULT_X_1 * 2**8 + GP2_SIZE_MULT_X_0 * 2**0
                 ) * HC_ERASE_GRP_SIZE_ECSD * HC_WP_GRP_SIZE_ECSD * 512
    GPP3_SIZE = (GP3_SIZE_MULT_X_2 * 2**16 + GP3_SIZE_MULT_X_1 * 2**8 + GP3_SIZE_MULT_X_0 * 2**0
                 ) * HC_ERASE_GRP_SIZE_ECSD * HC_WP_GRP_SIZE_ECSD * 512
    GPP4_SIZE = (GP4_SIZE_MULT_X_2 * 2**16 + GP4_SIZE_MULT_X_1 * 2**8 + GP4_SIZE_MULT_X_0 * 2**0
                 ) * HC_ERASE_GRP_SIZE_ECSD * HC_WP_GRP_SIZE_ECSD * 512

    print "\n"
    print "EXTCSD Decoder\n"
    print "========================================"
    print "Boot Partition Size : " + str(boot_size) + " kB."
    print "RPMB Size : " + str(rpmb_size) + " kB."
    if PARTITION_CONFIG_KEY.get(partition_config) is None:
        print ("Partition Config 0x{:x}".format(ecsd[179]))
    else:
        print PARTITION_CONFIG_KEY[partition_config] + "[0x{:x}]".format(ecsd[179])
    if CSD_REVISION.get(CSD_rev) is None:
        print ("CSD Revision 0x{:x}".format(ecsd[194]))
    else:
        print CSD_REVISION[CSD_rev]
    if EXTCSD_REVISION.get(EXT_CSD_rev) is None:
        print ("EXT_CSD Revision 0x{:x}".format(ecsd[192]))
    else:
        print EXTCSD_REVISION[EXT_CSD_rev]

    print "GPP1 : " + str(GPP1_SIZE) + " kB. " + \
          "GPP2 : " + str(GPP2_SIZE) + " kB. " + \
          "GPP3 : " + str(GPP3_SIZE) + " kB. " + \
          "GPP4 : " + str(GPP4_SIZE) + " kB. "
    print "\n"
    print "SEC_FEATURE_SUPPORT_[231] :\n"
    print '\t' + SEC_FEATURE_SUPPORT_KEY['SEC_SANITIZE']['0x' + SEC_SANITIZE_K]
    print '\t' + SEC_FEATURE_SUPPORT_KEY['SEC_GB_CL_EN(R)']['0x' + SEC_GB_CL_EN_K]
    print '\t' + SEC_FEATURE_SUPPORT_KEY['SEC_BD_BLK_EN(R)']['0x' + SEC_BD_BLK_EN_K]
    print '\t' + SEC_FEATURE_SUPPORT_KEY['SECURE_ER_EN(R)']['0x' + SECURE_ER_EN_K]
    print "\n"
    print "BOOT_BUS_CONDITIONS_[177] :\n"
    print '\t' + BOOT_BUS_CONDITIONS['BOOT_MODE'][BOOT_MODE_K]
    print '\t' + BOOT_BUS_CONDITIONS['RESET_BOOT_BUS_CONDITIONS'][RESET_BOOT_BUS_CONDITIONS_K]
    print '\t' + BOOT_BUS_CONDITIONS['BOOT_BUS_WIDTH'][BOOT_BUS_WIDTH_K]
    print "\n"
