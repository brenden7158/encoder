# encoder
**This project is open-sourced under the MIT license and is provided as-is.**

This software handles data collection and processing for The Weather Channel's IntelliStar 2 software using a mix of TWC's v1, v2, and v3 APIs. 

To use this encoder you will need to have an Intellistar 2 unit ``jr,xd,hd``, **note that the HD uses Windows XP so the setup may be a bit diffrent**

# Requirements
* Firewall on the stock I2 image fixed to allow incoming connections from ``224.1.1.77`` on ports ``7787`` and ``7788``
* [Python 3.8.0](https://www.python.org/downloads/release/python-380/)

# Usage instructions
[Download a release](https://github.com/the5dcrew/i2MessageEncoder-Rewrite/releases) for the most stable version, or clone the repository.

``git clone https://github.com/the5dcrew/i2MessageEncoder-Rewrite``

Install the requirements ``py -3 -m pip install -r requirements.txt``

Drop your ``MachineProductCfg.xml`` file into the root of the directory of the encoder

Open Powershell and run mkdir ``.temp`` and move the ``msgId.txt`` from the root of the encoder to ``.temp``

Inside of the ``.temp`` folder, make a folder named ``tiles``

Run ``main.py`` and profit.

# This project is made possible by [mewtek](https://github.com/mewtek), [Floppaa](https://github.com/Floppa-2), [Goldblaze](https://github.com/buffbears), [The 5D Crew](https://github.com/the5dcrew), and [OpenTelecom 2D](https://github.com/OpenTelecom2D). If you enjoy this project, say thank you to them!
