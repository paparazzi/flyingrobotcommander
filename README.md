# Flying Robot Commander
![Alt Frankenstein Jr. and Buzz](doc/images/frc_banner.png?raw=true "Frankenstein Jr. and Buzz")

## Version:
This is beta version 0.3.4 of the Flying Robot Commander(FRC) and subject to major refactoring.

## Overview:
The Flying Robot Commander(FRC) is a web based, RESTful application for controlling multiple 
aircraft that use [Paparazzi UAV](https://github.com/paparazzi/paparazzi) and [PPRZLink](https://github.com/paparazzi/pprzlink).

    usage: frc.py [-h] [-i IP] [-p PORT] [-f FILE] [-g] [-c] [-s] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -i IP, --ip IP        ip address
      -p PORT, --port PORT  port number
      -f FILE, --file FILE  use the specified client configuration file
      -g, --generate        generate a client configuration stub
      -c, --curl            dump actions as curl commands
      -s, --subscribe       subscribe to the ivy bus
      -v, --verbose         verbose mode

The default values for `IP`, `PORT`, and `FILE`, if not specified, are `127.0.0.1`, `5000`, and `frc_conf.xml`, respectively.

### Getting Started

- Make sure [Python](https://www.python.org/), [Flask](http://flask.pocoo.org/), and [PPRZLink](https://github.com/paparazzi/pprzlink) are installed.
- Make sure the `PAPARAZZI_SRC` and `PAPARAZZI_HOME` enviroment variables are set. 

```
    $ env | grep paparazzi
    PAPARAZZI_SRC=/home/fred/paparazzi
    PAPARAZZI_HOME=/home/fred/paparazzi
```

- If they are not set add the following lines to your `~/.bashrc` file:

```
    export PAPARAZZI_HOME="your paparazzi software directory"
    export PAPARAZZI_SRC="your paparazzi software directory"
```

- Create a config file containing the aircrafts, flightblocks, waypoints, guided modes and status messages from paparazzi you would like to include. e.g. edit the example `frc_conf.xml` to match the names in the `conf/conf.xml` file found in your paparazzi installation.
- Run `$ python frc.py -f your_config_file.xml`. The server should now be running.
- Visit `http://localhost:5000/show/flightblock/` in your browser and you should see the flightblock interface.

### Running the Flying Robot Commander
Open a terminal window and type the following command:

    $ python frc.py

FRC is a python based `Flask` application. Please reference the [Flask documentation](http://flask.pocoo.org/docs/0.10/)
for the installation and usage of `Flask`. Here are some of the python packages(versions) needed by `Flask`:

- Flask (0.10.1)
- itsdangerous (0.24)
- Jinja2 (2.8)
- Werkzeug (0.11.3)

On startup, the FRC reads the main Paparazzi UAV configuration file `$PPRZ_HOME/conf/conf.xml`. 
Configuration data contained in the `conf.xml` and the associated airframe/flight plan files is 
used to initialize the FRC server. Note that the `--subscribe` option is also used to initialize 
runtime related aircraft data that includes `ivy bus messages`. It is recommended to start the FRC server
prior to starting the Paparazzi server to acquire a complete message dictionary. The `--file` option 
is used to configure client related data( see `frc_conf.xml` for an example of the default client configuration file).

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
        <status>
            name      = "<status name>"
            msg_name  = "<message name>"
            msg_key   = "<message key>"
            color     = "<color>"
            label     = "<label>"
            icon      = "<icon>"
            tooltip   = "<tooltip>"
       </status>
       <layout>
            name      = "<template name>"
            rows      = "<number of rows>"
            cols      = "<number of columns>"
       </layout>
    </client>

Flight block, waypoint, and guided blocks are ordered based on their order in the file(i.e. order is preserved). 
Either a valid block `id` or `name` attribute must be present in each block. If both are used, the `name` attribute 
overrideds the `id` attribute. The `color` attribute in a given block is used to specify the color to use when 
rendering the corrosponding button in the FRC. If the `color` attribute is not specified, the button defaults 
to `white`. The `label` attribute defines the text to display on a given button unless the `icon` attribute is 
specified. The `icon` attribute overrides the `label` attribute.

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
        <status  name="GPS_PA"       msg_name="GPS_INT"               msg_key="pacc"         color="magenta"     label="GA" icon="" tooltip="GPS Position Accuracy" />
        <status  name="GPS_SC"       msg_name="GPS_INT"               msg_key="numsv"        color="purple"      label="SN" icon="" tooltip="GPS Satellite Count" />
        <status  name="GPS_STAT"     msg_name="ROTORCRAFT_STATUS"     msg_key="gps_status"   color="deepskyblue" label="GS" icon="" tooltip="GPS Status" />
        <status  name="RC_STAT"      msg_name="ROTORCRAFT_STATUS"     msg_key="rc_status"    color="dodgerblue"  label="RS" icon="" tooltip="RC Status" />
        <status  name="VOLT_STAT"    msg_name="ROTORCRAFT_STATUS"     msg_key="vsupply"      color="lime"        label="VS" icon="" tooltip="Voltage Status" />
        <status  name="MOTOR_STAT"   msg_name="ROTORCRAFT_STATUS"     msg_key="ap_motors_on" color="green"       label="M"  icon="" tooltip="Motors On/Off" />
        <status  name="FLIGHT_STAT"  msg_name="ROTORCRAFT_STATUS"     msg_key="ap_in_flight" color="gold"        label="F"  icon="" tooltip="Aircraft On Ground/In Flight" />
        <status  name="AP_MODE"      msg_name="ROTORCRAFT_STATUS"     msg_key="ap_mode"      color="orange"      label="AP" icon="" tooltip="Autopilot Mode" />
        <status  name="NAV_STAT"     msg_name="ROTORCRAFT_NAV_STATUS" msg_key="cur_block"    color="orangered"   label="NS" icon="" tooltip="Navigation Block" />
        <layout name="flightblockredux"  rows="3" cols="7" />
    </client>

### Generating a Configuration Stub
The generate switch (`-g`, `--generate`) parses the Paparazzi `conf.xml` file and generates a FRC compliant xml
for use in a custom FRC configuration file.

    $ python frc.py -g
    $ python frc.py --generate

    <client>
        <aircraft name="Teensy_Fly_Quad_Elle0_v1_2_B" color="orange" label="6" icon="" tooltip="Teensy_Fly_Quad_Elle0_v1_2_B" />
        <aircraft name="Teensy_Fly_Quad_Elle0_v1_2_A" color="yellow" label="7" icon="" tooltip="Teensy_Fly_Quad_Elle0_v1_2_A" />
        ...
        <aircraft name="Racer_PEX_Octo" color="purple" label="13" icon="" tooltip="Racer_PEX_Octo" />
        <flightblock name="Wait GPS" color="lime" label="1" icon="" tooltip="Wait GPS" />
        <flightblock name="Geo init" color="green" label="2" icon="" tooltip="Geo init" />
        ...
        <flightblock name="land" color="darkred" label="22" icon="" tooltip="land" />
        <waypoint name="STDBY" color="green" label="4" icon="" tooltip="STDBY" />
        <waypoint name="p1" color="gold" label="5" icon="" tooltip="p1" />
        ...
        <waypoint name="CAM" color="dodgerblue" label="10" icon="" tooltip="CAM" />
        <layout name="flightblockredux"  rows="3" cols="7" />
    </client>

More likely than not, you will probably need to prune the output of this switch to only those aircraft, flight blocks and waypoints
that are applicable to your use case.


### Creating Customized Themes
FRC supports the creation of customized themes(i.e. colors, labels and icons). Here's an example of a custom `klingon` theme
that uses a `new_theme_name`_conf.xml file and a set of theme specific icon images. The new theme related icon 
images should reside in `./static/images/new_theme_name` folder. So, for our `klingon` example, there's a `klingon_conf.xml` file
along with a set of icon images located at `./static/images/kilingon`

Links to our custom theme configuration file and the associated icons:
- [klingon_conf.xml](https://github.com/paparazzi/flyingrobotcommander/blob/master/klingon_conf.xml)
- [klingon icons folder](https://github.com/paparazzi/flyingrobotcommander/tree/master/static/images/klingon)

**Invocation & Screenshot:**

    $ python frc.py -f klingon_conf.xml

![Alt Klingon Flight Block View](doc/images/klingon_screen.png?raw=true "Klingon Flight Block View")
    
### URL Parameters

#### Aircraft Coloring Scheme
Each row of aircraft buttons default to the colors specified for each block function, a column major view. 
This behavior can be overriden through the use of the `view_mode` URL parameter. If you would like to preserve/use
the colors assigned to each aircraft for each row's color, set the `view_mode` URL paramater to `row`.

    localhost:5000/show/flightblock/?view_mode=row

Each row of aircraft buttons will use the respective color assigned to each aircraft in the `frc_conf.xml` file, 
a row major view.

![Alt Flight Block view_mode=row View](doc/images/flightblock_viewmode_screen.png?raw=true "Flight Block view_mode=row View")

#### Resizing Buttons
The default button size is 64x64 pixels. Sometimes it is desireable to reduce or increase
button sizes based on display variants. The `button_size` URL parameter is used to specify a
desired button size. For example, to specify a button size of 50x50 pixels use the following:

    localhost:5000/show/flightblock/?button_size=50

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

    - Flight Block Route:       show/flightblock/
    - Flight Block Redux Route: show/flightblockredux/
    - Guided Route:             show/guided/
    - Waypoint Route:           show/waypoint/
    - Status Route:             show/status/

Assuming the server is running on the local host(ip=127.0.0.1), type one of the following URL's into
a browser(e.g. Chrome, Firefox, etc...) to execute the respective client view. 

    localhost:5000/show/flightblock/
    localhost:5000/show/flightblockredux/
    localhost:5000/show/guided/
    localhost:5000/show/waypoint/
    localhost:5000/show/status/   (NOTE: Inovke the FRC server with the -s/--subscribe option)

Remember to configure the aircraft, flight block, guided, waypoint and status client data prior to accessing 
the respective client view.

#### Flight Block View
![Alt Flight Block View](doc/images/flightblock_screen.png?raw=true "Flight Block View")

#### Flight Block Redux View
![Alt Flight Block Redux View](doc/images/flightblockredux_screen.png?raw=true "Flight Block Redux View")

#### Guided View
![Alt Guided View](doc/images/guided_screen.png?raw=true "Guided View")

#### Waypoint View
![Alt Waypoint View](doc/images/waypoint_screen.png?raw=true "Waypoint View")

#### Status View
The `Status` view relies on data supplied from the `ivy` message bus and the `-s/--subscribe` option must
be used to populate this view. It is recommended to start the FRC server prior to starting the Paparazzi 
server to acquire a complete message dictionary.

    python frc.py -i 192.168.1.147 -s
![Alt Status View](doc/images/status_screen.png?raw=true "Status View")

## Video Demos:
Here are a couple of informal demo videos of the Flying Robot Commander; captured from
Periscope broadcasts:

- [FRC: Flight Block Video](https://www.youtube.com/watch?v=NgT0K1RzfmE)
- [FRC: Guidance Video](https://www.youtube.com/watch?v=BdItVWyjLUc)

## TODO:
- [ ] Add/improve software installation section in the README
- [ ] Add more error handlers with appropriate feedback (this includes the `None` response for aircraft subset mismatches, etc....)
- [ ] Add support for `status` view generation via `-g` switch, note `-s` switch dependency
- [ ] Research ivy messaging inconsistencies when running live multi-MAV system tests
- [ ] Add client routes by name (i.e. waypoint/client/add/stay_p1)
- [ ] Revisit/refactor the button-to-command binding model
- [ ] Add wiki topic/page in paparazziuav.org wiki
- [ ] Document usage and testing strategies

## COMPLETED:
- [x] Added a `flightblockredux` view to facilitate an optimized UI with respect to large aircraft x flighblock datasets (i.e. >= 84 combinations/buttons). Bump version to v0.3.4.
- [x] Update `styles.css` and button sizes to improve support for iOS devices
- [x] Added support for resizing buttons(`?button_size=x`; where `x` is an even integer)
- [x] Added icons for the `Status` view and update documentation image
- [x] Added an `Update` button to the `Status` view that includes a timer interval refresh capability
- [x] Added initial support for a `Status` view
- [x] Added a feature that allows the aircraft colors specified in `conf.xml` to be used for each aircraft row(`?view_mode=row`)
- [x] Added `Cam Circle` flightblock to configuration files along with tooltip verbiage
- [x] Improved the output for the switch that generates a configuration file stub(`-g`)
- [x] Added `view_mode` URL parameters to enable/disable aircraft button color/tooltip attributes
- [x] Added documentation around adding a custom theme(i.e. klingon)
- [x] Updated PPRZLINK imports and bumped the version to 0.3.0
- [x] Started parsing XML with `lxml` library instead of `ElementTree` to hopefully improve parsing robustness
- [x] Added the option to generate a configuration file stub(`-g`)
- [x] Added support in `frc_conf.xml` for the following aircraft attributes: `color`, `label`, `icon` and `tooltip` 
- [x] Added support for the following view attributes: `color`, `label`, `icon` and `tooltip` 
- [x] Added refactoring of template views to handle dynamic button matrices
- [x] Completed refactoring of template views to handle dynamic button matrices
- [x] Added client configuration by name="string" in `frc_conf.xml` (i.e. name="stay_p1")
- [x] Added a client configuration file(`-f` switch to specify file name)
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
- [x] Added curl code generation and ivy message interface tracing support(`-c` and `-v`, respectively)
- [x] Refactor frc.py with direct calls to the IvyMessagesInterface
- [x] Removed external python scripts: flightblock.py, guidance.py, waypoint.py
- [x] Refactor code to use updated IvyMessagesInterface
- [x] Refactor python modules to use the pprzlink interface

