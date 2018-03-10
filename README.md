# Speed testing

This is a collection of scripts I'm using to track my ISPs performance over a
period of time. It consists so far of three parts:

1. A script that uses sivel's speedtest-cli to generate a measurement
2. An InfluxDB server that stores all the measurements
3. A rendering script that takes the data stored inside Influx to generate a
   report

I originally didn't want to write a custom rendering script but things like
Grafana and Chronograf are simply to heavy weight for the resources I have at
my disposal right now.

## Getting started

This collection has three dependencies:

* [Python](https://python.org) 3.x with [pip](https://pip.pypa.io/en/stable/)
* [Pipenv](https://docs.pipenv.org/)
* [InfluxDB](https://www.influxdata.com/time-series-platform/influxdb/)

Once you have all that installed, just run the following commands to create a
measurement and store it inside the `speedtest` database of your Influx server:

```
# Install all dependencies:
$ pipenv shell
$ pipenv sync

# Generate a measurement:
$ python speedtest.py

# Generate a report:
$ python render.py > output.html
```

If you have InfluxDB installed somewhere else, you can specify its connection
settings through various command-line flags on both scripts.

## Continuous queries

If you also want to have aggregates showing up on the rendered page, you can
create the a handful of continuous queries inside InfluxDB that will be checked
by the rendering script. You can find the statements for creating the queries
inside the `continuous_queries.tick` file.

## Thanks

Big thanks to Josef Schneider and Eva Silberschneider for the inspiration with
their [speedtest_cron](https://gitgud.io/J0s3f/speedtest_cron/) package.
