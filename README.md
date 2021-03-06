# Speed testing

This is a collection of scripts I'm using to track my ISPs performance over a
period of time. It consists so far of three parts:

1. A script that uses sivel's
   [speedtest-cli](https://github.com/sivel/speedtest-cli) to generate a
   measurement. This uses the speedtest.net infrastructure to collect
   performance metrics.
2. An [InfluxDB](https://github.com/influxdata/influxdb) server that stores all
   the measurements
3. A [Chronograf](https://github.com/influxdata/chronograf) server that is used
   to visualize the collected measurements

In this repository you will also fijnd a `render.py` file which I previously
used for generating visualisations. Fortunately, I now have a more recent
RaspberryPI at my disposal and can therefore use Chronograf directly 🙂


## Installing on a RaspberryPI (auto-setup)

If you want to install speedtesting on a RaspberryPI with Raspbian, we have an
`install.sh` script which automates all the necessary steps for you.

Just open a terminal on your RaspberryPI and enter the following command:

```
curl https://raw.githubusercontent.com/zerok/speedtesting/master/install.sh | sudo /bin/bash
```

Under the hood, this uses the [Ansible](https://www.ansible.com/) roles defined
inside the `ansible` folder.


## Getting started (without auto-setup)

This collection has three dependencies:

* [Python](https://python.org) 3.x with [pip](https://pip.pypa.io/en/stable/)
* [Pipenv](https://docs.pipenv.org/)
* [InfluxDB](https://www.influxdata.com/time-series-platform/influxdb/)

Once you have all that installed, just run the following commands to create a
measurement and store it inside the `speedtest` database of your InfluxDB
server:

```
# Install all dependencies:
$ pipenv shell
$ pipenv sync

# Generate a measurement:
$ pipenv run python speedtest.py
```

If you have InfluxDB installed somewhere else, you can specify its connection
settings through various command-line flags on both scripts.

Now, you can inspect the details of the measurement either using the `influx`
command-line application or Chronograf.


## Chronograf

The `dashboards` folder includes dashboard configurations for Chronograf.


## Thanks

Big thanks to Josef Schneider and Eva Silberschneider for the inspiration with
their [speedtest_cron](https://gitgud.io/J0s3f/speedtest_cron/) package.
