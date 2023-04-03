# XML Analyzer

### This script was created to read multiple XML files and extract data. It works with XML files from **Cellebrite
extractions**. Feel free to clone the repository and adapt it to your needs.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


#### This code reads all XML files that are located in a folder called "XML", at the same level of the "app.py" and
saves data to a SQLITE DB as shown below:
#

#### **get_infos() _returns a {DICT}_**
{
File: value,
IMEI: value,
Brand: value,
Model: value,
FactoryNumber: value,
BluetoothName: value,
BluetoothMAC: value,
MACAddress: value
}

#### **get_contacts() _returns a [LIST] with multiple {DICT}_**
[{
File: value,
IMEI: value,
ContactName: value,
ContactPhone: value
}]

#### **get_wifi() _returns [LIST] with multiple {DICT}_**
[{
IMEI: value,
File: value,
SSID: value,
SecurityMode: value,
LastConnection: value,
Password: value
}]

### Usage:
- Clone the repository to your machine;
- Create a folder called "XML" in the same directory where app.py is located;
- Place your XML files in the recently created "XML" folder;
- Open the terminal and run "**python app.py**".