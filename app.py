import os
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime

# Create 'Results' folder
try:
    os.mkdir("Results")
except:
    ...

# Variables for the directories
current_directory = os.getcwd()
source_directory = os.path.join(current_directory, "XML\\")
results_directory = os.path.join(current_directory, "Results\\")

# Function to create the DB
def createDB(table_name):
    global con
    con = sqlite3.connect(results_directory + table_name + ".db")
    global cur
    cur = con.cursor()

    ### Table creation ###
    cur.execute("""CREATE TABLE IF NOT EXISTS
        Gadgets (
            IMEI string PRIMARY KEY,
            File string,
            Brand string,
            Model string,
            FactoryNumber string,
            BluetoothName string,
            BluetoothMAC string,
            MACAddress string
        );
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS 
        Contacts (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            IMEI string,
            File string,
            ContactName string,
            ContactPhone string,
            FOREIGN KEY (IMEI) REFERENCES Gadgets (IMEI)
        );
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS 
        Wifis (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            IMEI string,
            File string,
            SSID string,
            SecurityMode string,
            LastConnection string,
            Password string,
            FOREIGN KEY (IMEI) REFERENCES Gadgets (IMEI)
        );
    """)

# Class to handle the XMLs on the folder and extract information
class Read_xml():
    def __init__(self, directory) -> None:
        self.directory = directory

    def all_files(self):
        return [os.path.join(self.directory, arq) 
                for arq in os.listdir(self.directory) 
                if arq.lower().endswith('.xml')]

    def get_infos(self, xml):
        physical = ET.parse(xml).getroot()
        xmlns = {"ns": "http://pa.cellebrite.com/report/2.0"}
        global file_physical
        file_physical = xml.replace(self.directory, "").replace("\\", "")

        if (physical.find("ns:metadata/[@section='Device Info']/ns:item/[@name='IMEI1']", xmlns)) is None:
            imei_physical = physical.find("ns:metadata/[@section='Device Info']/ns:item/[@name='IMEI']", xmlns).text
        else:
            imei_physical = physical.find("ns:metadata/[@section='Device Info']/ns:item/[@name='IMEI1']", xmlns).text

        if (physical.find("ns:metadata/[@section='Extraction Data']/ns:item/[@name='DeviceInfoSelectedManufacturer']", xmlns)) is None:
            brand = "Vazio"
        else:
            brand = physical.find("ns:metadata/[@section='Extraction Data']/ns:item/[@name='DeviceInfoSelectedManufacturer']", xmlns).text

        if (physical.find("ns:metadata/[@section='Extraction Data']/ns:item/[@name='DeviceInfoSelectedDeviceName']", xmlns)) is None:
            model = "Vazio"
        else:
            model = physical.find("ns:metadata/[@section='Extraction Data']/ns:item/[@name='DeviceInfoSelectedDeviceName']", xmlns).text

        if (physical.find("ns:metadata/[@section='Device Info']/ns:item/[@name='Factory number']", xmlns)) is None:
            factory_number = "Vazio"
        else:
            factory_number = physical.find("ns:metadata/[@section='Device Info']/ns:item/[@name='Factory number']", xmlns).text

        if (physical.find("ns:metadata/[@section='Device Info']/ns:item/[@name='Bluetooth device name']", xmlns)) is None:
            bluetooth_nome = "Vazio"
        else:
            bluetooth_nome = physical.find("ns:metadata/[@section='Device Info']/ns:item/[@name='Bluetooth device name']", xmlns).text

        if (physical.find("ns:metadata/[@section='Device Info']/ns:item/[@name='Bluetooth MAC Address']", xmlns)) is None:
            bluetooth_mac = "Vazio"
        else:
            bluetooth_mac = physical.find("ns:metadata/[@section='Device Info']/ns:item/[@name='Bluetooth MAC Address']", xmlns).text

        if (physical.find("ns:metadata/[@section='Device Info']/ns:item/[@name='Mac Address']", xmlns)) is None:
            mac_address = "Vazio"
        else:
            mac_address = physical.find("ns:metadata/[@section='Device Info']/ns:item/[@name='Mac Address']", xmlns).text

        return {"File": file_physical, 
                "IMEI": imei_physical, 
                "Brand": brand,
                "Model": model,
                "FactoryNumber": factory_number,
                "BluetoothName": bluetooth_nome, 
                "BluetoothMAC": bluetooth_mac, 
                "MACAddress": mac_address}

    def get_contacts(self, xml):
        logical = ET.parse(xml).getroot()

        for x in logical.findall("./report/general_information"):
            global file, imei
            file = xml.replace(self.directory, "").replace("\\", "")

            if x.find('imei') is None:
                imei = "IMEI Não encontrado"
            else:
                imei = x.find('imei').text

        contacts = []
        for i in logical.findall("./report/contacts/contact"):
            if i.find('name') is None:
                contact_name = "Vazio"
            else: 
                contact_name = i.find('name').text

            if i.find('phone_number') is None:
                contact_phone = "Vazio"
            else:
                contact_phone = i.find('phone_number').find('value').text

            dict_contacts = {"File": file,
                             "IMEI": imei,
                             "ContactName": contact_name,
                             "ContactPhone": contact_phone}
            contacts.append(dict_contacts)
        return contacts

    def get_wifi(self, xml):
        physical = ET.parse(xml).getroot()
        xmlns = {"ns": "http://pa.cellebrite.com/report/2.0"}

        global file_physical
        file_physical = xml.replace(self.directory, "").replace("\\", "")
        global imei_physical

        list_wifis = physical.findall("ns:decodedData/ns:modelType/[@type='WirelessNetwork']/", xmlns)

        wifis = []
        for wifi in list_wifis:
            if (physical.find("ns:metadata/[@section='Device Info']/ns:item/[@name='IMEI1']", xmlns)) is None:
                imei_physical = physical.find("ns:metadata/[@section='Device Info']/ns:item/[@name='IMEI']", xmlns).text
            else:
                imei_physical = physical.find("ns:metadata/[@section='Device Info']/ns:item/[@name='IMEI1']", xmlns).text
                
            if wifi.find("ns:field/[@name='SSId']/ns:value", xmlns) is None:
                ssid = "Vazio"
            else:
                ssid = wifi.find("ns:field/[@name='SSId']/ns:value", xmlns).text

            if wifi.find("ns:field/[@name='SecurityMode']/ns:value", xmlns) is None:
                security_mode = "Vazio"
            else:
                security_mode = wifi.find("ns:field/[@name='SecurityMode']/ns:value", xmlns).text

            if wifi.find("ns:field/[@name='LastConnection']/ns:value", xmlns) is None:
                last_connection = "Vazio"
            else:
                last_connection = wifi.find("ns:field/[@name='LastConnection']/ns:value", xmlns).text

            if wifi.find("ns:field/[@name='Password']/ns:value", xmlns) is None:
                password = "Vazio"
            else:
                password = wifi.find("ns:field/[@name='Password']/ns:value", xmlns).text

            dict_wifis = {"IMEI": imei_physical,
                          "File": file_physical,
                          "SSID": ssid, 
                          "SecurityMode": security_mode, 
                          "LastConnection": last_connection, 
                          "Password": password}
            
            wifis.append(dict_wifis)
        
        return wifis


if __name__ == "__main__":
    print("########## Welcome to the XML Analyzer ##########", end="\n\n")

    db_name = input("What's the name of the Database you want to create/update? ")
    if db_name is None:
        db_name = input("Please, type the name of the Database you want to create/update? ")
    else:
        createDB(db_name)

    print("\nProcess started: " + str(datetime.now()))

    process = Read_xml(source_directory)
    all_files = process.all_files()

    for _ in all_files:
        if "physical" in _: 
            try:
                cur.execute("""INSERT INTO Gadgets(File, IMEI, Brand, Model, FactoryNumber, BluetoothName, BluetoothMAC, MACAddress) 
                            VALUES(:File, :IMEI, :Brand, :Model, :FactoryNumber, :BluetoothName, :BluetoothMAC, :MACAddress)""", process.get_infos(_))
                con.commit()
            except:
                print(str(_) + "  =>  This file is already registered (Infos Data)")

            for w in process.get_wifi(_): # Iteration over the list of dicts coming from .get_wifi
                try:
                    cur.execute("""INSERT INTO Wifis(IMEI, File, SSID, SecurityMode, LastConnection, Password)
                                VALUES(:IMEI, :File, :SSID, :SecurityMode, :LastConnection, :Password)""", w)
                    con.commit()
                except:
                    print(str(_) + "  =>  This file is already registered (WIFI Data)")

        if "logical" in _:
            for c in process.get_contacts(_): # Iteration over the list of dicts coming from .get_contacts
                try:
                    cur.execute("""INSERT INTO Contacts(IMEI, File, ContactName, ContactPhone)
                                VALUES(:IMEI, :File, :ContactName, :ContactPhone)""", c)
                    con.commit()
                except:
                    print(str(_) + "  =>  This file is already registered (Contacts Data)")
    con.close()

    print("Process finished: " + str(datetime.now()))
