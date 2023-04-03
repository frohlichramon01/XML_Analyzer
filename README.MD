# This code reads all XML files that are located in a folder called "XML", at the same level of the "app.py":


#### get_infos(): returns a {DICT}
    {
        File: "string",
        IMEI: "string",
        Brand: "string",
        Model: "string",
        FactoryNumber: "string",
        BluetoothName: "string",
        BluetoothMAC: "string",
        MACAddress: "string"
    }

#### get_contacts() => returns a [LIST] with multiple {DICT}
    [{
        File: "string", 
        IMEI: "string", 
        ContactName: "string", 
        ContactPhone: "string"
    }]

#### get_wifi(): returns [LIST] with multiple {DICT}
    [{
        IMEI: "string",
        File: "string",
        SSID: "string", 
        SecurityMode: "string", 
        LastConnection: "string", 
        Password: "string"
    }]