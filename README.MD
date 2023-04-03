<h1>XML Analyzer </h1>

<h3>This script was created to read multiple XML files and extract data. It works with XML files from **Cellebrite
    extractions**. Feel free to clone the repository and adapt it to your needs.</h3>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
<br>

<h3>This code reads all XML files that are located in a folder called "XML", at the same level of the "app.py" and saves
    data to a SQLITE DB as shown below:</h3>

#### get_infos() returns a {DICT}
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

#### get_contacts() returns a [LIST] with multiple {DICT}
[{
File: value,
IMEI: value,
ContactName: value,
ContactPhone: value
}]

#### get_wifi() returns [LIST] with multiple {DICT}
[{
IMEI: value,
File: value,
SSID: value,
SecurityMode: value,
LastConnection: value,
Password: value
}]

<br>

<h3>Usage:</h3>
<ol>
    <li>Clone the repository to your machine;</li>
    <li>Create a folder called "XML" in the same directory where app.py is located;</li>
    <li>Place your XML files in the recently created "XML" folder;</li>
    <li>Open the terminal and run "_python app.py_".</li>
</ol>