# 3 Console

## 3.1 Introduction

The Aegis Athena space mission is an illustrious epitome of such a pursuit. Primarily destined to accomplish a monumental milestone of delivering the first human astronaut to the lunar surface, this visionary mission is governed by a sophisticated piece of technology known as the S.P.A.C.E.C.R.A.F.T. console.

This highly innovative system adopts a dual-purpose role, integrating the essential features of both a command model and a service module. This strategically harmonious blend of utilitarian efficiency and comforting resources paves the way for an environment conducive for the astronaut-trio executing this expedition, turning it into a virtual sanctuary amidst the vast cosmos. The S.P.A.C.E.C.R.A.F.T. console operates with a plethora of commands, designed to modify the inherent system configurations and retrieve state-of-the-art status information. Such telemetry data is indubitably critical in assessing the spacecraft's performance and securing the triumphant fruition of the mission's objectives.

## 3.2 Command Overview

Each command embedded in this system meticulously rides on the principles of intuitive design and effective execution, quintessential to ensure the seamless operation of any space mission. This sophisticated league of commands ensures a detailed real-time assessment of the mission parameters, thus contributing to the overall success of the mission.

- `list`
- `details`
- `ask`
- `transmit`
- `set`

## 3.3 The `list` Command

The introductory rendition in this advanced series of commands is the `list` command.

### 3.3.1 Purpose

The `list` embodies an extensive command with a purpose to enumerate critical components or systems associated with the spacecraft.

### 3.3.2 Syntax

```
list parts | systems
```

The command elegantly simplifies the user interaction by applying the `list` invocation followed by an immediate specification of either `parts` or `systems`.

### 3.3.3 Listing Parts

Utilizing the `list parts` command generates a detailed, systematic listing of all the integral components of the S.P.A.C.E.C.R.A.F.T. console. Each part is represented by its unique ID, composed of 2 bytes encoded as 4 hexadecimal digits, complemented by the part's name and a real-time status display.

```
system:/ $ list parts

5534       ARS controller                           [[ NOMINAL ]]

3323       Aerojet AJ10                             [[ NOMINAL ]]

dc3c       Aerozine 50 tank                         [[ NOMINAL ]]

cd13       BRAINS Controller                        [[ NOMINAL ]]

...
```

### 3.3.4 Listing Systems

Comparatively, the `list systems` command initiates a comprehensive display of each independent spacecraft system along with a summarised report of its current operational status.

```
system:/ $ list systems

ARS                                                 [[ NOMINAL ]]

BRAINS                                              [[ NOMINAL ]]

COMS                                                [[ NOMINAL ]]

ECS                                                 [[ NOMINAL ]]

EPS                                                 [[ NOMINAL ]]

...
```

### 3.3.5 Status Types

The communicated status of each component or system can be categorised into one of three specifier types:

- `NOMINAL`: The component or system is optimally functioning and performing in accordance with the predetermined expectations.
- `MALFUNC`: There is a compromise or anomaly in the component's or system's performance due to a malfunction.
- `OFFLINE`: The component or system is at a non-operational stage being offline.

Hence, the `list` command provides an encompassing bird's-eye view of the operational health of vital elements making up the S.P.A.C.E.C.R.A.F.T. console. By ensuring real-time performance tracking and early detection of malfunctions, it contributes significantly to the mission's overall success and efficiency.

## 3.4 The `details` Command
3.4.1 Purpose
The `details` command infuses much needed specificity into the astronauts' mission information requests. This command impressively curates an extensive wealth of detailed information about particular parts involved in the spacecraft's operation. This level of granularity allows for specialized oversight and precisely targeted adjustments when necessary, further enhancing operational efficiency.

### 3.4.2 Syntax

The `details` command implementation requires the invocation of `details` followed by the specific Part ID.

```
details <PART-ID>
```

By referring to a distinct Part ID, this utilitarian command delivers comprehensive information about a specified part swiftly, enhancing the diagnostic efficiency for the astronaut team during the mission.

### 3.4.3 Command Output

The output displayed as a result of the `details` command always encompasses the part ID, its name, and the current operational status. Moreover, an intriguing feature of this command is the presentation of additional information tailored specifically to the type of part in question. This creates a streamlined overview of the component's unique properties, enhancing the understanding of its specific role and operational status within the overarching spacecraft system.

### 3.4.4 Examples

#### 3.4.4.1 COMS Controller Details

An example of this command in action is when it is used with the COMS controller:

```
system:/ $ details 1d40

id: 1d40

name: COMS controller

status: NOMINAL

antenna: b125
```

In this scenario, alongside the common information (id, name, and status), the generated output also includes a distinct attribute specific to the COMS controller, in this case, the antenna's ID. This tailoring of information richly contributes to a comprehensive understanding of the part's individual functions and connections within the system.

#### 3.4.4.2 BRAINS Controller Details

The command's utility and flexibility are further illustrated when considering its application for the BRAINS controller:

```
system:/ $ details cd13

id: cd13

name: BRAINS Controller

status: NOMINAL

gpus: a9c3 b561 41d1 15f9 837c 9ba6 f68a 07ca b583 ea2a

storage: 2220
```

In this case, the additional information output includes the IDs of the Graphic Processing Units (GPUs) associated with the BRAINS controller, and its storage capacity. This level of detailed information allows for deep insights into the operational parameters of this critically important part of the spacecraft.

## 3.5 The `transmit` Command

### 3.5.1 Purpose

The `transmit` command represents a quintessential component of the command suite by facilitating communication between the spacecraft and the mission control on Earth as well as the A.P.O.L.L.O. module. Specifically, this command is designed to send data using the spacecraft's Communication (COMS) controller along with the configured equipment, i.e., the antenna. By enabling the conveyance of vital information and updates, the `transmit` command plays an instrumental role in guaranteeing seamless connectivity during the entire span of the mission.

### 3.5.2 Syntax

In the context of syntax, the `transmit` command stipulates the invocation of `transmit`, immediately proceeded by the COMS ID and the message intended for transmission.

```
transmit <COMS-ID> <MESSAGE>
```

By indicating the COMS ID, the command precisely identifies the communication module responsible for transmitting the message, thus ensuring the efficient delivery of mission-critical messages.

### 3.5.3 Command Execution

#### 3.5.3.1 Transmitting a "Hello World!" Message

To illustrate its functionality, consider the scenario of transmitting a "Hello World!" message:

```
system:/ $ transmit 1d40 Hello World!

INFO: transmitting message

DEBUG: 

INFO: transmission complete

INFO: awaiting response

DEBUG: ..

INFO: receiving response

Hello World!

INFO: received EOT
```

This instance represents a successful execution of the `transmit` command. It initiates data transmission using the COMS controller designated by the ID `1d40`. Upon command initiation, it conveys real-time process updates including the start of transmission, completion of transmission, the waiting period for the response, receipt of response, and the End Of Transmission (EOT), thereby providing comprehensive visibility of the transmission process at each stage.

In summary, the `transmit` command embodies an invaluable facilitator of communication, effectively bridging the spatial distance between the mission control on Earth and the astronaut team mid-mission. By ensuring mission-critical data transference in real-time, this command significantly bolsters both mission safety and success.

## 3.6 The `ask` Command

### 3.6.1 Purpose

The `ask` command acts as a conduit to the spacecraft's advanced onboard Artificial Intelligence (AI) assistant known as M.A.R.S. This command's primary function is to prompt M.A.R.S with queries or command messages by leveraging the capabilities of the Binary Regulated Artificial Intelligence Network System (BRAINS), thus creating an efficient, reliable interface between the crew and the operational features of the S.P.A.C.E.C.R.A.F.T.

M.A.R.S., run on BRAINS, represents a marvel of computational craft and machine intelligence. Serving as the cerebral backbone of the S.P.A.C.E.C.R.A.F.T., BRAINS is the comprehensive hardware setup that brings M.A.R.S to operational life. It nests all the components foundational to execute the complex tasks assigned to M.A.R.S., enhancing the overall operational efficiency and decision-making process of the mission.

### 3.6.2 Syntax

To interact with M.A.R.S., the `ask` command is followed by the BRAINS controller ID and the message intended for M.A.R.S. The syntax thus takes the following form:

```
ask <BRAINS-ID> <MESSAGE>
```

By specifying the BRAINS controller ID, the command precisely identifies the part responsible for controlling M.A.R.S., facilitating accurate and direct communication with the AI assistant.

### 3.6.3 Command Execution

#### 3.6.3.1 Example Usage: "Hello World!"

Consider a scenario in which an astronaut wants to greet M.A.R.S. by sending a "Hello World!" message.

```
system:/ $ ask cd13 Hello World!

Hello! How can I assist you today?
```

In this example, M.A.R.S. responds to a `ask` command directed to the BRAINS system with the ID `cd13`, exemplifying its readiness to assist the astronaut. This exchange highlights how the `ask` command facilitates instantaneous communication between the onboard crew and the AI assistant M.A.R.S - making complex operations manageable by human astronauts.

In summary, the `ask` command provides astronauts with an invaluable tool to seamlessly engage with and command the onboard AI assistant M.A.R.S., thus amplifying the capacity for real-time problem-solving, communicative flexibility, and ensuring the overall success of the mission.

