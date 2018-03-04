#!/usr/bin/env python3
import subprocess
import json
import argparse
from influxdb import InfluxDBClient

argparser = argparse.ArgumentParser()
argparser.add_argument('--influx-host', default='localhost')
argparser.add_argument('--influx-port', default=8086, type=int)
argparser.add_argument('--influx-username', default='root')
argparser.add_argument('--influx-password', default='root')
argparser.add_argument('--influx-database', default='speedtest')
argparser.add_argument('--speedtest-bin', default='speedtest')
args = argparser.parse_args()

client = InfluxDBClient(args.influx_host, args.influx_port, args.influx_username, args.influx_password, args.influx_database)

output = subprocess.check_output('{} --json'.format(args.speedtest_bin), shell=True).decode('utf-8')
result = json.loads(output)

client.write_points([{
    'measurement': 'speedtest',
    'tags': {
        'host': result['server']['host'],
        'client_ip': result['client']['ip'],
        'client_isp': result['client']['isp'],
    },
    'fields': {
        'upload': result['upload'],
        'download': result['download'],
        'ping': result['ping'],
    },
}])

