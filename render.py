import argparse
from influxdb import InfluxDBClient
from jinja2 import Template, Environment
import pendulum
import humanfriendly

def format_bytes(val):
    return humanfriendly.format_size(val, binary=True).replace('B', 'b')

def format_datetime(val):
    return pendulum.parse(val).to_datetime_string() + ' UTC'

def format_date(val):
    return pendulum.parse(val).to_date_string()

def format_number(val):
    return humanfriendly.format_number(val)

env = Environment()
env.filters['humanize_size'] = format_bytes
env.filters['datetime'] = format_datetime
env.filters['date'] = format_date
env.filters['number'] = format_number

tmpl = env.from_string('''<!doctype html>
<html lang="en">
    <head>
        <title>Speed testing</title>
        <meta charset="utf-8">
        <style>
        body {
            font-family: Arial, sans serif;
        }
        .row {
            display: flex;
            orientation: row;
            justify-content: center;
        }
        section {
            margin: 0 10px;
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
        <div class="row">
        <section>
            <h2>Last 24h</h2>
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
                        <td>{{ point.time|datetime }}</td>
                        <td>{{ point.host }}</td>
                        <td>{{ point.ping|number }}ms</td>
                        <td>{{ point.download|humanize_size }}/s</td>
                        <td>{{ point.upload|humanize_size }}/s</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </section>
        {% if avg_pings %}
        <section>
            <h2>Avg. ping</h2>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Avg ping</th>
                    </tr>
                </thead>
                <tbody>
                    {% for ping in avg_pings %}
                    <tr>
                        <td>{{ ping.time|date }}</td>
                        <td>{{ ping.mean|number }}ms</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </section>
        {% endif %}
    </div>
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
avg_pings = []
measurements = [m['name'] for m in client.get_list_measurements()]

for point in client.query('select * from speedtest where time > now() - 24h order by time desc').get_points():
    points.append(point)
if 'avg_ping' in measurements:
    for point in client.query('select * from avg_ping order by time desc limit 5').get_points():
        avg_pings.append(point)

print(tmpl.render(points=points, avg_pings=avg_pings))
