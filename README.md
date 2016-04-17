# Flying Robot Commander
![Alt Frankenstein Jr. and Buzz](doc/images/frc_banner.png?raw=true "Frankenstein Jr. and Buzz")

## Version:
This is beta version 0.2.4 of the Flying Robot Commander(FRC) and subject to major refactoring.

## Overview:
The Flying Robot Commander(FRC) is a web based, RESTful application for controlling multiple 
aircraft that use [Paparazzi UAV](https://github.com/paparazzi/paparazzi) and [PPRZLink](https://github.com/paparazzi/pprzlink).

    usage: frc.py [-h] [-i IP] [-p PORT] [-f FILE] [-c] [-s] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -i IP, --ip IP        ip address
      -p PORT, --port PORT  port number
      -f FILE, --file FILE  client configuration file
      -c, --curl            dump actions as curl commands
      -s, --subscribe       subscribe to the ivy bus
      -v, --verbose         verbose mode

The default values for `IP`, `PORT`, and `FILE`, if not specified, are `127.0.0.1`, `5000`, and `frc_conf.xml`, respectively.

### Running the Flying Robot Commander
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
runtime related aircraft data that includes `ivy bus messages`. The `--file` is used to configure
client related data( see `frc_conf.xml` for an example of the default client configuration file).

### Configuration File: frc_conf.xml
The `frc_conf.xml` is an XML file used to configure the FRC views.

    Format/Syntax:

    <client>
        <aircraft>
            ac_id   = "<aircraft id>"
            name    = "<aircraft name>"
            color   = "<color>"
            label   = "<label>"
            icon    = "<icon>"
            tooltip = "<tooltip>"
        </aircraft>
        <flightblock>
            fb_id   = "<flight block id>"
            name    = "<flight block name>"
            color   = "<color>"
            label   = "<label>"
            icon    = "<icon>"
            tooltip = "<tooltip>"
        </flightblock>
        <waypoint>
            wp_id   = "<waypoint id>"
            name    = "<waypoint name>"
            color   = "<color>"
            label   = "<label>"
            icon    = "<icon>"
            tooltip = "<tooltip>"
        </waypoint>
        <guided>
            gd_id   = "<guided id>"
            name    = "<guided name>"
            color   = "<color>"
            label   = "<label>"
            icon    = "<icon>"
            tooltip = "<tooltip>"
       </guided>
    </client>

Flight block, waypoint, and guided blocks are ordered based on their order in the file(i.e. order is preserved). 
Either a valid block `id` or `name` attribute must be present in each block. If both are used, the `name` attribute overrideds the `id` attribute. The `color` attribute in a given block is used to specify the color to use when rendering the corrosponding button in the FRC. If the `color` attribute is not specified, the button defaults to `white`. The `label` attribute defines the text to display on a given button unless the `icon` attribute is specified. The `icon` attribute overrides the `label` attribute.

Example `frc_conf.xml` file:

    <client>
        <aircraft     name="Teensy_Fly_Quad_Elle0_v1_2_B" color="red"         label="1" icon="" tooltip="" />
        <aircraft     name="Teensy_Fly_Quad_Elle0_v1_2_A" color="orange"      label="2" icon="" tooltip="" />
        <aircraft     name="Teensy_Fly_Quad_Elle0"        color="green"       label="3" icon="" tooltip="" />
        <aircraft     name="Teensy_Fly_Quad"              color="deepskyblue" label="4" icon="" tooltip="" />
        <aircraft     name="Teensy_Fly_Hexa"              color="dodgerblue"  label="5" icon="" tooltip="" />
        <aircraft     name="Racer_PEX_Quad"               color="purple"      label="6" icon="" tooltip="" />
        <flightblock  name="Start Motors"  color="lime"        label=""  icon="propeller.png" tooltip="Props On" />
        <flightblock  name="Takeoff"       color="green"       label=""  icon="aircraft-take-off.png" tooltip="Takeoff" />
        <flightblock  name="Standby"       color="deepskyblue" label="S" icon="" tooltip="Stdby" />
        <flightblock  name="stay_p1"       color="dodgerblue"  label="1" icon="" tooltip="" />
        <flightblock  name="stay_p2"       color="yellow"      label="2" icon="" tooltip="" />
        <flightblock  name="stay_p3"       color="gold"        label="3" icon="" tooltip="" />
        <flightblock  name="stay_p4"       color="orange"      label="4" icon="" tooltip="" />
        <flightblock  name="stay_HOV"      color="darkorange"  label="H" icon="" tooltip="" />
        <flightblock  name="land here"     color="orangered"   label=""  icon="aircraft-landing.png" tooltip="Land Here" />
        <flightblock  name="land"          color="red"         label=""  icon="aircraft-landing.png" tooltip="Land" />
        <flightblock  name="Holding point" color="darkred"     label=""  icon="propeller.png" tooltip="Props Off" />
        <waypoint  name="STDBY" color="deepskyblue" label="" icon="" tooltip="" />
        <waypoint  name="p1"    color="dodgerblue"  label="" icon="" tooltip="" />
        <waypoint  name="p2"    color="lime"        label="" icon="" tooltip="" />
        <waypoint  name="p3"    color="green"       label="" icon="" tooltip="" />
        <waypoint  name="p4"    color="gold"        label="" icon="" tooltip="" />
        <waypoint  name="HOV"   color="orange"      label="" icon="" tooltip="" />
        <waypoint  name="CAM"   color="orangered"   label="" icon="" tooltip="" />
        <waypoint  name="S1"    color="red"         label="" icon="" tooltip="" />
        <guided  name="Forward"          color="magenta"     label=""  icon="arrow-with-circle-up.png" tooltip="Forward" />
        <guided  name="Back"             color="purple"      label=""  icon="arrow-with-circle-down.png" tooltip="Back" />
        <guided  name="Left"             color="deepskyblue" label=""  icon="arrow-with-circle-left.png" tooltip="Left" />
        <guided  name="Right"            color="dodgerblue"  label=""  icon="arrow-with-circle-right.png" tooltip="Right" />
        <guided  name="Up"               color="lime"        label=""  icon="aircraft-take-off.png" tooltip="Up" />
        <guided  name="Down"             color="green"       label=""  icon="aircraft-landing.png" tooltip="Down" />
        <guided  name="Counterclockwise" color="gold"        label=""  icon="arrows-rotate-counterclockwise.png" tooltip="Counterclockwise" />
        <guided  name="Clockwise"        color="orange"      label=""  icon="arrows-rotate-clockwise.png" tooltip="Clockwise" />
        <guided  name="Guided"           color="orangered"   label="G" icon="" tooltip="Guided" />
        <guided  name="Nav"              color="red"         label="N" icon="" tooltip="Nav" />
    </client>
    
### Adding Client Data via Routes
If the `--file` option is not used when starting the FRC server, the client related configuration must
be completed using the `object`/client/add/`id` routes; where `object` is one of aircraft, flightblock,
or waypoint and `id` is a valid object id. The aircraft, flight block, and waypoint related `client` data 
need to be configured(see syntax below) prior to using one of the client views( `show/flightblock`, 
`show/guided`, `show/waypoint`).

    Syntax:

    - Aircraft Route: aircraft/client/add/<ac_id>
    - Flight Block Route: flightblock/client/add/<fb_id>
    - Waypoint Route: waypoint/client/add/<wp_id>

Example `bash` script that uses `curl` to configure client data for five aircraft with 10 shared flight blocks and
8 shared waypoints:

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
    curl http://$host:$port/waypoint/client/add/3
    curl http://$host:$port/waypoint/client/add/5
    curl http://$host:$port/waypoint/client/add/6
    curl http://$host:$port/waypoint/client/add/7
    curl http://$host:$port/waypoint/client/add/8
    curl http://$host:$port/waypoint/client/add/9
    curl http://$host:$port/waypoint/client/add/10


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
- [ ] Add a feature that allows the aircraft colors specified in `conf.xml` to be used for each aircraft row
- [ ] Research ivy messaging inconsistencies when running live multi-MAV system tests
- [ ] Add client routes by name (i.e. waypoint/client/add/stay_p1)
- [ ] Revisit/refactor the button-to-command binding model
- [ ] Add wiki topic/page in paparazziuav.org wiki
- [ ] Document usage and testing strategies

## COMPLETED:
- [x] Added support in `frc_conf.xml` for the following aircraft attributes: `color`, `label`, `icon` and `tooltip` 
- [x] Added support for the following view attributes: `color`, `label`, `icon` and `tooltip` 
- [x] Added refactoring of template views to handle dynamic button matrices
- [x] Completed refactoring of template views to handle dynamic button matrices
- [x] Added client configuration by name="string" in `frc_conf.xml` (i.e. name="stay_p1")
- [x] Added a client configuration file(-f switch to specify file name)
- [x] Fixed blocking/hanging http requests when using development server by setting threaded=True in app.run() method
- [x] Refactoring of template views to better deal with dynamic button matrices
- [x] Update route testing script
- [x] Remove static html files and associated `img` folder
- [x] Reduce http requests for group aircraft commands from N to 1
- [x] Consolidate/share CSS related UI controls across views
- [x] Integrate the use aircraft/flight plan configurations
- [x] Consolidate network related configurations with respect to IP addresses and port assignments
- [x] Completed first pass at Flask/Jinja2 template support for flightblock, guided and waypoint views
- [x] Added Flask/Jinja2 template support and refactor flightblock view using template approach
- [x] Parse configuration files and populate aircraft data objects on startup
- [x] Integrate real-time aircraft message handling features(-s switch to subscribe to ivy message bus)
- [x] Added curl code generation and ivy message interface tracing support(-c and -v, respectively)
- [x] Refactor frc.py with direct calls to the IvyMessagesInterface
- [x] Removed external python scripts: flightblock.py, guidance.py, waypoint.py
- [x] Refactor code to use updated IvyMessagesInterface
- [x] Refactor python modules to use the pprzlink interface

