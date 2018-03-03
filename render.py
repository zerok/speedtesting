import argparse
from influxdb import InfluxDBClient
from jinja2 import Template

tmpl = Template('''<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
    </head>
    <body>
        <table>
            <thead>
                <tr>
                    <th>Time</th>
                    <th>Ping</th>
                    <th>Download</th>
                    <th>Upload</th>
                </tr>
            </thead>
            <tbody>
                {% for point in points %}
                <tr>
                    <td>{{ point.time }}</td>
                    <td>{{ point.ping }}</td>
                    <td>{{ point.download }}</td>
                    <td>{{ point.upload }}</td>
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
for point in client.query('select * from speedtest where time > now() - 6h order by time desc').get_points():
    points.append(point)
print(tmpl.render(points=points))
