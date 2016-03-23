# Flying Robot Commander

## Version:

This is beta version 0.1.0 of the Flying Robot Commander(FRC) and subject to major refactoring.

## Overview:

The Flying Robot Commander(FRC) is a web based, RESTful application for controlling multiple 
aircraft that use Paparazzi UAV and PPRZLink.

    usage: frc.py [-h] [-i IP] [-p PORT] [-c] [-s] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -i IP, --ip IP        ip address
      -p PORT, --port PORT  port number
      -c, --curl            dump actions as curl commands
      -s, --subscribe       subscribe to the ivy bus
      -v, --verbose         verbose mode

The default values for `IP` and `PORT`, if not specified, are `127.0.0.1` and `5000`, respectively.

### Running the Flying Robot Command

Open a terminal window and type the following command:

    python frc.py

FRC is a python based `Flask` application. Please reference the [Flask documentation](http://flask.pocoo.org/docs/0.10/)
for the installation and usage of `Flask`. Here are some of the python packages(versions) needed by `Flask`:

- Flask (0.10.1)
- itsdangerous (0.24)
- Jinja2 (2.8)
- Werkzeug (0.11.3)

On startup, the FRC reads the main Paparazzi UAV configuration file `$PPRZ_HOME/conf/conf.xml`. 
Configuration data contained in the `conf.xml` and the associated airframe/flight plan files is 
used to initialize the FRC server. Note that the `--subscribe` option is also used to initialize 
runtime related aircraft data that includes `ivy bus messages`.

### Adding Client Data

Once the FRC server is running, the aircraft and flight block related `client` data need to be
configured prior to using one of the client views( `show/flightblock`, `show/guided`, `show/waypoint`).

    Syntax:

    - Aircraft Route: aircraft/client/add/<ac_id>
    - Flight Block Route: flightblock/client/add/<fb_id>

Example `bash` script that uses `curl` to configure client data for five aircraft with 10 shared flight blocks:

    #!/bin/bash
    host=127.0.0.1
    port=5000
    curl http://$host:$port/aircraft/client/add/215
    curl http://$host:$port/aircraft/client/add/216
    curl http://$host:$port/aircraft/client/add/217
    curl http://$host:$port/aircraft/client/add/218
    curl http://$host:$port/aircraft/client/add/219
    curl http://$host:$port/flightblock/client/add/3
    curl http://$host:$port/flightblock/client/add/4
    curl http://$host:$port/flightblock/client/add/6
    curl http://$host:$port/flightblock/client/add/7
    curl http://$host:$port/flightblock/client/add/8
    curl http://$host:$port/flightblock/client/add/9
    curl http://$host:$port/flightblock/client/add/12
    curl http://$host:$port/flightblock/client/add/32
    curl http://$host:$port/flightblock/client/add/33
    curl http://$host:$port/flightblock/client/add/2

### Showing Client Views

Once the client related data is configured, the various client views of the FRC are available for use.

    Syntax:

    - Flight Block Route: show/flightblock/
    - Guided Route: show/guided/
    - Waypoint Route: show/waypoint/

Assuming the server is running on the local host(ip=127.0.0.1), type one of the following URL's into
a browser(e.g. Chrome, Firefox, etc...) to execute the respective client view. 

    localhost:5000/show/flightblock/
    localhost:5000/show/guided/
    localhost:5000/show/waypoint/

Remember to configure the aircraft and flight block client data prior to accessing a client view.

#### Flight Block View

![Alt Flight Block View](doc/images/flightblock_screen.png?raw=true "Flight Block View")

#### Guided View

![Alt Guided View](doc/images/guided_screen.png?raw=true "Guided View")

#### Waypoint View

![Alt Waypoint View](doc/images/waypoint_screen.png?raw=true "Waypoint View")

## Video Demos:

Here are a couple of informal demo videos of the Flying Robot Commander; captured from
Periscope broadcasts:

- [FRC: Flight Block Video](https://www.youtube.com/watch?v=NgT0K1RzfmE)
- [FRC: Guidance Video](https://www.youtube.com/watch?v=BdItVWyjLUc)

## TODO:
- [ ] Add a mechanism for persisting client configuration information
- [ ] Investigate issue related to unexpected blocking/hanging http requests when using localhost
- [ ] Revisit/refactor the button-to-command binding model
- [ ] Add wiki topic/page in paparazziuav.org wiki
- [ ] Document usage and testing strategies

## COMPLETED:
- [x] Update route testing script
- [x] Remove static html files and associated `img` folder
- [x] Reduce http requests for group aircraft commands from N to 1
- [x] Consolidate/share CSS related UI controls across views
- [x] Integrate the use aircraft/flight plan configurations
- [x] Consolidate network related configurations with respect to IP addresses and port assignments
- [x] Completed first pass at Flask/Jinja2 template support for flightblock, guided and waypoint views
- [x] Add Flask/Jinja2 template support and refactor flightblock view using template approach
- [x] Parse configuration files and populate aircraft data objects on startup
- [x] Integrate real-time aircraft message handling features(-s switch to subscribe to ivy message bus)
- [x] Add curl code generation and ivy message interface tracing support(-c and -v, respectively)
- [x] Refactor frc.py with direct calls to the IvyMessagesInterface
- [x] Remove external python scripts: flightblock.py, guidance.py, waypoint.py
- [x] Refactor code to use updated IvyMessagesInterface
- [x] Refactor python modules to use the pprzlink interface

