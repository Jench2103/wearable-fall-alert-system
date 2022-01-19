# Wearable Fall Alert System
This is the final project of Group 7 on SINGLE CHIP SYSTEM DESIGN & APPLICATION (Fall 2021) in NCKUEE. The project combined Arduino, sensor modules, android app, Line bot, and website to realize a system which could detects fall accidents, sends messages to call for help automatically, and provides an information & status center for users' families, EMS, and hospitals.


## Group Members
|                  Name                   |          Email           |
|:---------------------------------------:|:------------------------:|
| [張仁謙](https://github.com/Jench2103)  | E24084208@gs.ncku.edu.tw |
|  [王宣雅](https://github.com/hsuanya)   | E24086640@gs.ncku.edu.tw |
| [廖祐誼](https://github.com/RuoliiLiao) | E24084711@gs.ncku.edu.tw |
| [郭佩穎](https://github.com/KuoRegina)  | E24086153@gs.ncku.edu.tw |


## Table of Contents
- [Structure of the Project](#structure-of-the-project)
- [Environment Setup](#environment-setup)
- [Working on this Project](#working-on-this-project)
    - [Web Service Deploying](#web-service-deploying)
    - [Docker Workspace for Server](#docker-workspace-for-server)
- [Dependencies](#dependencies)
    - [Arduino](#arduino)
    - [Server](#server)
- [Attribution](#attribution)


## Structure of the Project
```bash
Wearable Fall Alert System
    ├── android-application/    # android application developed with App Inventor
    ├── arduino/                # source code for Arduino
    ├── server/                 # source code for Linebot and database server
    └── workspace/              # docker workspace for server development
        └── run                 # workspace controlling script
```


## Environment Setup
- [Arduino IDE](https://www.arduino.cc/en/software)
- [Git](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/get-docker/)
    - [Install Docker on Windows 10](https://hackmd.io/@Jench2103/ByBj5vMbY)
- [Python](https://www.python.org/downloads/)


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


## Dependencies
### Arduino
- [I2Cdevlib-Core](https://github.com/jrowberg/i2cdevlib.git)
- [I2Cdevlib-MPU6050](https://github.com/jrowberg/i2cdevlib.git)
- [PulseSensor Playground](https://github.com/WorldFamousElectronics/PulseSensorPlayground.git)
- [TinyGPSPlus](https://github.com/mikalhart/TinyGPSPlus.git)

### Server
- [Flask](https://pypi.org/project/Flask/)
- [Flask-SQLAlchemy](https://pypi.org/project/Flask-SQLAlchemy/)
- [Flask-Markdown](https://pypi.org/project/Flask-Markdown/)
- [line-bot-sdk](https://pypi.org/project/line-bot-sdk/)


## Attribution
- [Mirko Broadband Services Website Bootstrap HTML Template - Inovatik](https://inovatik.com/mirko-broadband-services-website-bootstrap-html-template.html)
