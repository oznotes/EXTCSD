import binascii
import sys
import os


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


def is_not_empty(s):  # if string is empty or not
    """
    :param s: String
    :return: Bool value given the string if empty will return True
    """
    return bool(s and s.strip())


if __name__ == '__main__':

    PARTITION_CONFIG_KEY = \
        {
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
            '0x9': 'Reserved for future ',
            '0x8': 'Reserved for future ',
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
            '0x9': 'Reserved for future ',
            '0x8': 'Reserved for future ',
            '0x7': 'Reserved for future ',
            '0x6': 'Reserved for future ',
            '0x5': 'Reserved for future ',
            '0x4': 'Reserved for future ',
            '0x3': 'Reserved for future ',
            '0x2': 'CSD version No. 1.2  \n'
                   'CSD Spec  : [ 4.1, 4.2, 4.3, 4.4, 4.41, 4.5, 4.51, 5.0, 5.01, 5.1 ] ',
            '0x1': 'CSD version No. 1.1 [ Allocated by MMCA ] ',
            '0x0': 'CSD version No. 1.0 [ Allocated by MMCA ] '
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
    CSD_rev = "0x{:x}".format(ecsd[194])
    EXT_CSD_rev = "0x{:x}".format(ecsd[192])
    partition_config = "0x{:x}".format(ecsd[179])
    boot_size = int(ecsd[226]) * 128  # BOOT_SIZE_MULT [226] Boot Partition size = 128K bytes * BOOT_SIZE_MULT
    rpmb_size = int(ecsd[168]) * 128  # RPMB_SIZE_MULT [168] RPMB partition size = 128kB * RPMB_SIZE_MULT
    print "Boot Partition Size : " + str(boot_size) + " KB"
    print "RPMB Size : " + str(rpmb_size) + " KB"
    print PARTITION_CONFIG_KEY[partition_config]
    print CSD_REVISION[CSD_rev]
    print EXTCSD_REVISION[EXT_CSD_rev]
