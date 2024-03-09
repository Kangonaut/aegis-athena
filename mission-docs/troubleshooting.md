# Troubleshooting

This section provides simple guides for common problems or errors that can occur on the SPACECRAFT module.

## Alarms

If the SPACECRAFT is in a non-nominal state, it will activate the alarm system, in order to signal the need of immediate action to the crew onboard. The alarm system does not indicate what has gone wrong, but merely that something has gone badly wrong. To ensure that the crew is unable to ignore the alarm, the system consists of an auditive component, i.e. loud annoying beeping and also a visual component, i.e. flashing red lights that will fill the whole cabin. In the unfortunate scenario, that the alarms are indeed activated, the crew is required to troubleshoot the origin of the problem on their own, using the onboard console. As a starting point, we recommend the `list system` and `list parts` commands, to get an overview of what systems and parts are affected. Once all systems return to state NOMINAL, the alarm system will shut off automatically. Although this was requested by the crew multiple times, leading up to the launch, the alarm system does not have a manual override, thus cannot be shut off manually. This is a design decision made to ensure that critical errors CANNOT and WILL NOT be ignored.

## System Status: `MALFUNC`

A system can be malfunctioning (console output: `MALFUNC`) for a wide variety of reasons. Usually, this means that one of its subcomponents is in a non-nominal state. A subcomponent can be both another system (e.g.: ARS is a subsystem of ECS), or a particular part that is of vital importance to the system (e.g.: the fuel cell is used to generate electric power, thus a subcomponent of the EPS). 

To diagnose the origin of malfunctioning system, we can start off by issuing the `list parts` command to look up the part ID of the controller corresponding to that system.