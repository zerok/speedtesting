import argparse
from influxdb import InfluxDBClient
from jinja2 import Template, Environment
import pendulum
import humanfriendly

def format_bytes(val):
    return humanfriendly.format_size(val, binary=True).replace('B', 'b')

def format_date(val):
    return pendulum.parse(val).to_datetime_string() + ' UTC'

env = Environment()
env.filters['humanize_size'] = format_bytes
env.filters['date'] = format_date

tmpl = env.from_string('''<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <style>
        body {
            font-family: Arial, sans serif;
        }
        table {
            border: 1px solid #DDD;
            border-spacing: 0;
            border-bottom: 0;
        }
        td, th {
            padding: 5px;
        }
        th {
            background: #DDD;
        }
        tbody tr:nth-child(even) td {
            background: #EFEFEF; 
        }
        tbody td {
            border-bottom: 1px solid #DDD;
        }
        </style>
    </head>
    <body>
        <table>
            <thead>
                <tr>
                    <th>Time</th>
                    <th>Host</th>
                    <th>Ping</th>
                    <th>Download</th>
                    <th>Upload</th>
                </tr>
            </thead>
            <tbody>
                {% for point in points %}
                <tr>
                    <td>{{ point.time|date }}</td>
                    <td>{{ point.host }}</td>
                    <td>{{ point.ping }}ms</td>
                    <td>{{ point.download|humanize_size }}/s</td>
                    <td>{{ point.upload|humanize_size }}/s</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
</html>''')

parser = argparse.ArgumentParser()
parser.add_argument('--influx-host', default='localhost')
parser.add_argument('--influx-port', default=8086, type=int)
parser.add_argument('--influx-username', default='root')
parser.add_argument('--influx-password', default='root')
parser.add_argument('--influx-database', default='speedtest')
args = parser.parse_args()

client = InfluxDBClient(args.influx_host, args.influx_port, args.influx_username, args.influx_password, args.influx_database)
points = []
for point in client.query('select * from speedtest where time > now() - 24h order by time desc').get_points():
    points.append(point)
print(tmpl.render(points=points))
