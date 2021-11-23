# Wearable Fall Alert System


## Structure of the Project
```bash
Wearable Fall Alert System
    ├── Arduino/        # source code for Arduino
    │   ├── .gitkeep    # placeholder for empty directory
    └── Server/         # source code for Linebot and database server
        └── .gitkeep    # placeholder for empty directory
```


## Development Environment
- [Arduino IDE](https://www.arduino.cc/en/software)
- [Visual Studio Code](https://code.visualstudio.com/)
- [EditorConfig for VS Code](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig)
- [Install Docker on Windows 10](https://hackmd.io/@Jench2103/ByBj5vMbY)

### Configuration Example for VS Code : `./vscode/c_cpp_properties.json`
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


## Reference
- [ArduinoSTL - Arduino Reference](https://www.arduino.cc/reference/en/libraries/arduinostl/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [EditorConfig](https://editorconfig.org/)
- [Docker Overview](https://docs.docker.com/get-started/overview/)
