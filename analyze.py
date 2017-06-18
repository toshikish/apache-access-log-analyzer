import argparse
import datetime
import re
import sys

hour = [0] * 24
host = {}

parser = argparse.ArgumentParser(description='Analyze Apache access_logs and calculate them.')
parser.add_argument('files', nargs='*', type=argparse.FileType('r'), default=sys.stdin, help='acess_log file(s) path(s)')
parser.add_argument('-f', '--fromDate', help='From when; format=YYYYMMDD')
parser.add_argument('-u', '--untilDate', help='Until when; format=YYYYMMDD')
args = parser.parse_args()

if args.fromDate:
    fdt = datetime.datetime.strptime(args.fromDate, '%Y%m%d')
    fd = datetime.date(fdt.year, fdt.month, fdt.day)
if args.untilDate:
    udt = datetime.datetime.strptime(args.untilDate, '%Y%m%d')
    ud = datetime.date(udt.year, udt.month, udt.day)

for f in args.files:
    line = f.readline()
    while line:
        tstr = re.search('[0-9]{2}/[A-Z]{1}[a-z]{2}/[0-9]{4}:[0-9]{2}:[0-9]{2}:[0-9]{2} [+-]{1}[0-9]{4}', line).group()
        t = datetime.datetime.strptime(tstr, '%d/%b/%Y:%H:%M:%S %z')
        td = datetime.date(t.year, t.month, t.day)
        if not (args.fromDate and td < fd) and not (args.untilDate and ud < td):
            hour[t.hour] = hour[t.hour] + 1
            h = re.search('^[0-9a-zA-Z.-]+', line).group()
            host[h] = host[h] + 1 if h in host else 1
        line = f.readline()
    f.close()

print('Number of hits in every hour:')
for i in range(24):
    print("{0:02d}:00-: {1:4d}".format(i, hour[i]))

print('Number of hits of each remote host:')
for rh in sorted(host.items(), key=lambda x: x[1], reverse=True):
    print("{0:>30}: {1:4d}".format(rh[0], rh[1]))
