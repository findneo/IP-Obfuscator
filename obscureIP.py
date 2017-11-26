# coding:utf8
# by https://findneo.github.io/
# ref: https://linux.die.net/man/3/inet_aton
#      https://tools.ietf.org/html/draft-main-ipaddr-text-rep-02
#      https://tools.ietf.org/html/rfc3986
#      http://www.linuxsa.org.au/pipermail/linuxsa/2007-September/088131.html
import itertools as it
import random
ip = '192.168.66.233'
i = ip.split('.')


def f(x):
    return hex(int(x))[2:].zfill(2)


hi = [f(i[0]),
      f(i[1]),
      f(i[2]),
      f(i[3]),
      # hi[4]:part c of "a.b.c"
      f(i[2]) + f(i[3]),
      # hi[5]:part b of "a.b"
      f(i[1]) + f(i[2]) + f(i[3]),
      # hi[6]:'a'
      f(i[0]) + f(i[1]) + f(i[2]) + f(i[3]),
      ]


def hex2oct(x):
    """ arbitrary length is supported
    """
    moreZero = random.choice(range(10))
    return oct(int(x, 16)).zfill(moreZero + len(oct(int(x, 16)))).strip('L')


def hex2int(x): return str(int(x, 16))


def hex2hex(x):
    moreZero = random.choice(range(10))
    return '0x' + '0' * moreZero + x


p = [hex2hex, hex2int, hex2oct]
res = []
# "a.b.c.d"
# Each of the four numeric parts specifies a byte of the address;
# the bytes are assigned in left-to-right order to produce the binary address.
res.extend(['.'.join([i[0](hi[0]), i[1](hi[1]), i[2](hi[2]), i[3](hi[3])]) for i in it.product(p, p, p, p)])

# "a.b.c"
# Parts a and b specify the first two bytes of the binary address.
# Part c is interpreted as a 16-bit value that defines the rightmost two bytes of the binary address.
res.extend(['.'.join([i[0](hi[0]), i[1](hi[1]), i[2](hi[4])]) for i in it.product(p, p, p)])

# "a.b"
# Part a specifies the first byte of the binary address.
# Part b is interpreted as a 24-bit value that defines the rightmost three bytes of the binary address.
res.extend(['.'.join([i[0](hi[0]), i[1](hi[5])]) for i in it.product(p, p)])

# "a"
# The value a is interpreted as a 32-bit value that is stored directly into the binary address without any byte rearrangement.
res.extend(['.'.join([i[0](hi[6])]) for i in it.product(p)])
for i in xrange(len(res)):
    print "[%d]\t%s" % (i, res[i])

# -------------------------------------------------------------------------------
# test
import os

except_ip = []


def test_notation(ip_notation):
    global except_ip
    x = os.popen('ping -n 1 -w 0.5 ' + ip_notation).readlines()
    answer = x[0] if len(x) == 1 else x[1]
    if ip not in answer:
        except_ip.append(ip_notation)
    return answer.decode('gbk').strip()


print "\nchecking. . .",
for i in xrange(len(res)):
    # print "[%d] %s\t\t\t%s" % (i, res[i], test_notation(res[i]))
    test_notation(res[i])
    print '.',

print "\n\ntotally %d notations of ip checked ,all are equivalent to %s" % (len(res), ip)
if len(except_ip):
    print "except for notations following:\n", except_ip
