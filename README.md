# flyingrobotcommander

This is an alpha version 0.0.3 used as a proof-of-concept and is subject to major refactoring.

## Video Demos

Here are a couple of informal demo videos of the Flying Robot Commander; captured from Periscope broadcasts:

* [FRC: Flight Block Video](https://www.youtube.com/watch?v=NgT0K1RzfmE)
* [FRC: Guidance Video](https://www.youtube.com/watch?v=BdItVWyjLUc)

## TODO:
- [ ] Integration of code generation tools that use aircraft/flight plan configurations
- [ ] Consolidation of network related configurations with respect to IP addresses and port assignments
- [ ] Consolidate CSS related UI controls
- [ ] Revisit/refactor the button-to-command binding model
- [ ] Add wiki topic/page in paparazziuav.org wiki
- [ ] Document usage and testing strategies

## COMPLETED:
- [x] Integrate real-time aircraft message handling features(-s switch to subscribe to ivy message bus)
- [x] Add curl code generation and ivy message interface tracing support(-c and -v, respectively)
- [x] Refactor frc.py with direct calls to the IvyMessagesInterface
- [x] Remove external python scripts: flightblock.py, guidance.py, waypoint.py
- [x] Refactor code to use updated IvyMessagesInterface
- [x] Refactor python modules to use the pprzlink interface

