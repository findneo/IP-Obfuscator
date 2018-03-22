# coding:utf8
# by https://findneo.github.io/
# ref: https://linux.die.net/man/3/inet_aton
#      https://tools.ietf.org/html/draft-main-ipaddr-text-rep-02
#      https://tools.ietf.org/html/rfc3986
#      http://www.linuxsa.org.au/pipermail/linuxsa/2007-September/088131.html

import itertools as it
import random,sys

def hex2oct(x):
    """ arbitrary length is supported
    """
    # moreZero = random.choice(range(10))
    moreZero = 0
    return oct(int(x, 16)).zfill(moreZero + len(oct(int(x, 16)))).strip('L')


def hex2int(x): return str(int(x, 16))


def hex2hex(x):
    # moreZero = random.choice(range(10))
    moreZero = 0
    return '0x' + '0' * moreZero + x

def any2int(x):
    return int(x,16) if x.startswith('0x') else int(x,8) if x.startswith('0') else int(x)

def ip2int(ip):
    dotint = '.'.join([str(any2int(part)) for part in ip.split('.')])
    # print dotint,6666
    ip_parts=dotint.split('.')
    if len(ip_parts)==4:
        intip=dotint
    if len(ip_parts)==3:
        intip="%s.%s.%s.%s"%(ip_parts[0],ip_parts[1],str(int(ip_parts[2])/(2**8)),str(int(ip_parts[2])%(2**8)))
    if len(ip_parts)==2:
        ipp0,ipp1=ip_parts[0],ip_parts[1]
        intip="%s.%s.%s.%s"%(ipp0,str(int(ipp1)%(2**24)/(2**16)),str(int(ipp1)%(2**16)/(2**8)),str(int(ipp1)%(2**8)))
    if len(ip_parts)==1:
        ipp=int(ip_parts[0])
        intip='%s.%s.%s.%s'%(str(ipp/(2**24)),str(ipp%(2**24)/(2**16)),str(ipp%(2**16)/(2**8)),str(ipp%(2**8)))
    return intip


# int to hex
def f(x):
    return hex(int(x))[2:].zfill(2)

def convert(ip):
    i=ip.split('.')
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
    p = [hex2int, hex2hex, hex2oct]
    res = []
    form= []
    # "a.b.c.d"
    # Each of the four numeric parts specifies a byte of the address;
    # the bytes are assigned in left-to-right order to produce the binary address.
    res.extend(['.'.join([i[0](hi[0]), i[1](hi[1]), i[2](hi[2]), i[3](hi[3])]) for i in it.product(p, p, p, p)])
    form.append("(%s|\t%s|\t%s).\n(%s|\t%s|\t%s).\n(%s|\t%s|\t%s).\n(%s|\t%s|\t%s)"%(
        p[0](hi[0]),p[1](hi[0]),p[2](hi[0]),
        p[0](hi[1]),p[1](hi[1]),p[2](hi[1]),
        p[0](hi[2]),p[1](hi[2]),p[2](hi[2]),
        p[0](hi[3]),p[1](hi[3]),p[2](hi[3]),
        ))

    # "a.b.c"
    # Parts a and b specify the first two bytes of the binary address.
    # Part c is interpreted as a 16-bit value that defines the rightmost two bytes of the binary address.
    res.extend(['.'.join([i[0](hi[0]), i[1](hi[1]), i[2](hi[4])]) for i in it.product(p, p, p)])
    form.append("(%s|\t%s|\t%s).\n(%s|\t%s|\t%s).\n(%s|\t%s|\t%s)"%(
        p[0](hi[0]),p[1](hi[0]),p[2](hi[0]),
        p[0](hi[1]),p[1](hi[1]),p[2](hi[1]),
        p[0](hi[4]),p[1](hi[4]),p[2](hi[4]),
        ))

    # "a.b"
    # Part a specifies the first byte of the binary address.
    # Part b is interpreted as a 24-bit value that defines the rightmost three bytes of the binary address.
    res.extend(['.'.join([i[0](hi[0]), i[1](hi[5])]) for i in it.product(p, p)])
    form.append("(%s|\t%s|\t%s) . (%s|\t%s|\t%s)"%(
        p[0](hi[0]),p[1](hi[0]),p[2](hi[0]),
        p[0](hi[5]),p[1](hi[5]),p[2](hi[5]),
        ))


    # "a"
    # The value a is interpreted as a 32-bit value that is stored directly into the binary address without any byte rearrangement.
    res.extend(['.'.join([i[0](hi[6])]) for i in it.product(p)])
    form.append("(%s|\t%s|\t%s)"%(p[0](hi[6]),p[1](hi[6]),p[2](hi[6])))
    return [res,form]

# -------------------------------------------------------------------------------
# test
import os

except_ip = []


def test_notation(ip_notation,ip):
    global except_ip
    x = os.popen('ping -n 1 -w 0.5 ' + ip_notation).readlines()
    answer = x[0] if len(x) == 1 else x[1]
    if ip not in answer:
        except_ip.append(ip_notation)
    return answer.decode('gbk').strip()


def check(ip_after,ip):
    res=ip_after
    print "\nchecking. . .",
    for i in xrange(len(res)):
        # print "[%d] %s\t\t\t%s" % (i, res[i], test_notation(res[i]))
        test_notation(res[i],ip)
        print '.' ,  # ip2int(res[i])

    print "\n\ntotally %d notations of ip checked ,all are equivalent to %s" % (len(res), ip)
    if len(except_ip):
        print "except for notations following:\n", except_ip

def usage():
    print "usage: python obscureIP.python 192.168.1.1\n"
def main():
    try:
        # ip = '192.168.66.233' 
        ip=sys.argv[1]
        ip=ip2int(ip)
        [res,form]=convert(ip)
        print "1st class:\n%s\n\n2nd class:\n%s\n\n3rd class:\n%s\n\n4th class:\n%s\n"%(form[0],form[1],form[2],form[3])
        for i in xrange(len(res)):
            print "[%d]\t%s" % (i, res[i])
        check(res,ip)
    except Exception as e:
        usage()

main()