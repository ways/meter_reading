# Aidon/Hafslund AMS data parser

Modified to read HAN data from mqtt (i.e. from a Tibber Pulse sending to a local server instead of to Tibber), but the aidon_obis.py doesn't quite match upstream. Did I get it from another project?


### Example output

    Subscribing to topic tibber
    {'p_act_in': 3456}
    {'version_id': b'AIDON_V0001', 'meter_id': b'735********', 'meter_type': b'6525', 'p_act_in': 3459, 'p_act_out': 0, 'p_react_in': 0, 'p_react_out': 311, 'il1': 5.3, 'il2': 9.6, 'ul1': 238.0, 'ul2': 238.8, 'ul3': 236.9}
    {'p_act_in': 3458}
    {'p_act_in': 3461}
    {'p_act_in': 3469}


### How to get Tibber Pulse to send data to a local broker

https://github.com/iotux/ElWiz#oppsett-av-pulse


# Original readme continues

Use with an M-Bus dongle such as [this one](https://www.aliexpress.com/item/USB-to-MBUS-slave-module-MBUS-master-slave-communication-debugging-bus-monitor-TSS721-No-spontaneity-Self/32894249052.html).

### aidon_obis.py
A class for decoding HDLC and extracting OBIS fields. Requires python module crcmod (sudo pip install crcmod).
*NB: This is not a full COSEM parser, as the number of OBIS fields and their sequence is assumed to be as on a Hafslund meter.*

### aidon_test.py
Test output. <br/>
```
./aidon_test.py <port>
./aidon_test.py /dev/ttyUSB0
```

### aidon_forward.py
Forward to influxdb and Home Assistant.
Forwarding to only one of them is possible. Just omit the influx* or hass* arguments.
<br/>
Will generate sensors in Home assistant named `sensor.aidon_*`. Not done with a component, so these sensors will disappear on Home Assistant restart, and can't be renamed.
<br/>
For InfluxDB, readings are placed in the provided database under `voltage`, `current`, `power` and `energy`, and key `dev` holds device name (which begins with aidon).

```
python aidon_forward.py \
/dev/ttyUSB0 \
--influx_host http://localhost:8086 \
--influx_db metering \
--hass_host https://myhass.com:8123 \
--hass_token abcdefgh0123456789
```

### aidon_read.py
Parses preliminary/old protocol used by Hafslund. <br/>
`./aidon_read.py /dev/ttyUSB0` <br/>
