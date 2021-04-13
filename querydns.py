#!/usr/bin/env python3

import sys

if (len(sys.argv) == 1):
    help = 'Usage: querydns.py <name> [type] [resolver] [timeout]'
    print(help)
    exit(1)
else:
    name = sys.argv[1]

if (len(sys.argv) >= 3):
    type = sys.argv[2]
    type = type.upper()
else:
    type = 'A'

try:
    import dns.resolver
    dns = dns.resolver.Resolver()
    dns.lifetime = 5
except Exception as e:
    print('ZBXDNSERROR105 No dnspython installed?:' + str(e.args), file=sys.stderr)
    exit(105)

if (len(sys.argv) >= 5):
    try:
        lifetime = int(sys.argv[4])
        dns.lifetime = lifetime
    except Exception as e:
        print("ZBXDNSERROR102: Can't set lifetime (wtf): " + str(e.args), file=sys.stderr)
        exit(102)

#resolver = '192.168.209.2'
#dns.nameservers = [resolver]

if (len(sys.argv) >= 4):
    import re
    resolver = sys.argv[3]
    regex = re.compile('\d+\.\d+\.\d+\.\d+', flags=re.IGNORECASE)

    if regex.match(resolver):
        try:
            dns.nameservers = [resolver]
        except Exception as e:
            print("ZBXDNSERROR101: Can't set resolver: " + str(e.args), file=sys.stderr)
            exit(103)
    else:
        try:
            answer = dns.query(resolver, 'A')
            result = []
            for each in answer:
                result.append(each)

            strresult = []
            for string in result:
                strresult.append(str(string))
                
            dns.nameservers = strresult      
        except Exception as e:
            print("ZBXDNSERROR106 Can't resolve resolver name: " + str(e.args), file=sys.stderr)
            exit(106)

try:
    #print('Name: ' + name + ', type: ' + type + ', lifetime: ' + str(dns.lifetime) + ', resolver: ' + str(dns.nameservers))
    answer = dns.query(name, type)
except Exception as e:
    print('ZBXDNSERROR100: Error performing query: ' + str(e.args), file=sys.stderr)
    exit(100)

def generic_result_to_list_and_print(items):
    result = []
    for each in items:
        result.append(each)
    result.sort()
    for string in result:
        print(string)
    
def result_to_list_ns(items):
    result = []
    for rr in items:
        result.append(rr.target)
    result.sort()
    return result

if type == 'NS':
    result = result_to_list_ns(answer)
    for ss in result:
        print(ss)

elif type == 'MX':
    generic_result_to_list_and_print(answer)
        
elif type == 'A':
    generic_result_to_list_and_print(answer)
        
else:
    try:
        generic_result_to_list_and_print(answer)
    except Exception as e:
        print("ZBXDNSERROR104: Don't know how to handle this record type:" + str(e.args), file=sys.stderr)
        exit(104)

