# Wearable Fall Alert System


## Table of Contents
- [Structure of the Project](#structure-of-the-project)
- [Environment Setup](#environment-setup)
- [Working on this Project](#working-on-this-project)
    - [Web Service Deploying](#web-service-deploying)
    - [Docker Workspace for Server](#docker-workspace-for-server)
- [Configuration Example for VSCode Development](#configuration-example-for-vscode-development)
- [Attribution](#attribution)
- [Reference](#reference)


## Structure of the Project
```bash
Wearable Fall Alert System
    ├── Arduino/        # source code for Arduino
    ├── Server/         # source code for Linebot and database server
    └── workspace/      # docker workspace for server development
        └── run         # workspace controlling script
```


## Environment Setup
- [Arduino IDE](https://www.arduino.cc/en/software)
- [Git](https://git-scm.com/downloads)
- [Install Docker on Windows 10](https://hackmd.io/@Jench2103/ByBj5vMbY)
- [Visual Studio Code](https://code.visualstudio.com/)


## Working on this Project
- Clone this repository before start working
    ```bash
    $ git clone https://github.com/Jench2103/wearable-fall-alert-system.git
    ```

### Web Service Deploying
- The service will run in a docker container and could be access via `Port 5000`
    ```bash
    $ cd /path/to/wearable-fall-alert-system
    $ cd Server
    $ docker-compose up --build
    ```
- Stop the container by pressing `CTRL + C`
- Remove the container
    ```bash
    $ cd /path/to/wearable-fall-alert-system
    $ cd Server
    $ docker-compose down
    ```

### Docker Workspace for Server
- Show all available commands provided py `workspace/run`
    ```bash
    $ cd /path/to/wearable-fall-alert-system
    $ ./workspace/run
    ```
- Start and enter the environment
    ```bash
    $ cd /path/to/wearable-fall-alert-system
    $ ./workspace/run --start
    ```
- Leave and shutdown the environment
    ```bash
    $ cd /path/to/wearable-fall-alert-system
    $ ./workspace/run --stop
    ```
- Rebuild and enter the environment
    ```bash
    $ cd /path/to/wearable-fall-alert-system
    $ ./workspace/run --prune
    $ ./workspace/run --start
    ```


## Configuration Example for VSCode Development
- `.vscode/c_cpp_properties.json`
    ```json
    {
        "configurations": [
            {
                "name": "Arduino Uno",
                "includePath": [
                    "${workspaceFolder}/**",
                    "C:/Program Files (x86)/Arduino/hardware/arduino/avr/cores/arduino",
                    "C:/Program Files (x86)/Arduino/tools/**",
                    "C:/Program Files (x86)/Arduino/hardware/arduino/avr/**",
                    "C:/Program Files (x86)/Arduino/hardware/tools/**",
                    "C:/Program Files (x86)/Arduino/libraries/**",
                    "C:/Users/${env:Username}/Documents/Arduino/libraries/**"
                ],
                "forcedInclude": [
                    "C:/Program Files (x86)/Arduino/hardware/arduino/avr/cores/arduino/Arduino.h"
                ],
                "defines": [
                    "USBCON",
                    "ARDUINO=10809"
                ],
                "intelliSenseMode": "clang-x64",
                "compilerPath": "C:/Program Files (x86)/Arduino/hardware/tools/avr/bin/avr-gcc.exe",
                "cStandard": "c11",
                "cppStandard": "c++17"
            }
        ],
        "version": 4
    }
    ```


## Attribution
- [Mirko Broadband Services Website Bootstrap HTML Template - Inovatik](https://inovatik.com/mirko-broadband-services-website-bootstrap-html-template.html)


## Reference
- [ArduinoSTL - Arduino Reference](https://www.arduino.cc/reference/en/libraries/arduinostl/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [EditorConfig](https://editorconfig.org/)
- [Docker Overview](https://docs.docker.com/get-started/overview/)
