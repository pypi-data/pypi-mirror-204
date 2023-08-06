## MongoDB Python CRUD Operations

This project offers an easy-to-use Python interface that enables you to perform CRUD (Create, Read, Update, Delete) operations on a MongoDB database. It uses the PyMongo library and is designed to work seamlessly with a prebuilt MongoDB instance installed on your system or hosted elsewhere.
To use this code, you'll need a prebuilt MongoDB instance that's up and running. In my case, I created a MongoDB instance through https://cloud.mongodb.com/. However, you can also run your database locally or use a different provider if you prefer. Just make sure that your MongoDB instance is configured correctly before you start working with the code.
To ensure that the code can connect to your MongoDB instance, it's important to whitelist the appropriate IP addresses. This can be done using a mask or by specifying specific IP addresses. Before you start working with the code, make sure that your MongoDB instance is reachable via whitelisting. This will ensure that your code can access the database without any issues.
 

 
![image](https://user-images.githubusercontent.com/36086368/231573735-4af57894-d0a2-415c-ab29-8a26e4d67e06.png)



### Clone Repo

```sh
git clone https://github.com/melihteke/mongo-db-operation
```

```sh
pip install -r requirements.txt
```

### Package Installation

```sh
pip install mongo-db-operation
```

### Pypi URL

https://pypi.org/project/mongo-db-operation/


#### Create .env file in to relative root directory and fill in below variables
```sh
DB_URI=mongodb+srv://<DB_USERNAME>:<DB_PASSWORD>@cluster0.ybl2347fog.mongodb.net/test?retryWrites=true&w=majority
DB_NAME=<DB_NAME>
DB_COLLECTION_NAME=<DB_COLLECTION_NAME>
```



#### Usage
```sh
mongo_db_operation.mongo_client import MongoDBOperation
mongo_db_operation import environment

operation = MongoDBOperation()

In [8]: operation.view_all_records()
                   add_record()           db                     update_record()       
                   client                 environment            view_all_records()    
                   collection             remove_record()        view_specific_record()


```




##### Viewing all the records
```sh
In [8]: operation.view_all_records()
Out[8]: 
[{'_id': ObjectId('64370dbf0971a02bdf950163'),
  'hostname': 'DEV2010R01',
  'device_type': 'router',
  'site_number': '2010',
  'site': 'Craydon',
  'status': 'Operational',
  'local_subnets': ['10.10.1.0/24', '10.10.2.0/24', '10.10.3.0/24'],
  'wan_a_provider': 'BT',
  'wan_a_ip_setting': 'dhcp',
  'wan_b_provider': 'BT',
  'wan_b_ip_setting': '32.45.31.141/30',
  'hardware': 'C1111-4PLTEEA',
  'serial': 'FOCXXSDF5K9',
  'vlans': ['8', '110'],
  'l3_ints': ['GigabitEthernet0/0/0', 'GigabitEthernet0/0/1'],
  'l2_ints': ['GigabitEthernet0/1/0',
   'GigabitEthernet0/1/1',
   'GigabitEthernet0/1/2',
   'GigabitEthernet0/1/3']}]
}
  ```
  
  
  
 ##### Adding Records:
 ```sh
 In [9]: data = {  "hostname": "DEV2012R01",
   ...:   "device_type":"router",
   ...:   "site_number":"2012",
   ...:   "site": "Dublin",
   ...:   "status":"Operational",
   ...:   "local_subnets":["10.12.1.0/24", "10.12.2.0/24", "10.12.3.0/24"],
   ...:   "wan_a_provider":"GTT",
   ...:   "wan_a_ip_setting":"dhcp",
   ...:   "wan_b_provider":"BT",
   ...:   "wan_b_ip_setting":"213.45.23.143/30",
   ...:   "hardware": "C1111-4PLTEEA",
   ...:   "serial":"FOC2XXX7L599",
   ...:   "vlans":["8", "110"],
   ...:   "l3_ints":["GigabitEthernet0/0/0", "GigabitEthernet0/0/1"],
   ...:   "l2_ints":["GigabitEthernet0/1/0","GigabitEthernet0/1/1", "GigabitEthernet0/1/2", "GigabitEthernet0/1/3"]
   ...: }

In [10]: operation.add_record(data)

In [11]: operation.view_all_records()
Out[11]: 
[{'_id': ObjectId('64370dbf0971a02bdf950163'),
  'hostname': 'DEV2010R01',
  'device_type': 'router',
  'site_number': '2010',
  'site': 'Craydon',
  'status': 'Operational',
  'local_subnets': ['10.10.1.0/24', '10.10.2.0/24', '10.10.3.0/24'],
  'wan_a_provider': 'BT',
  'wan_a_ip_setting': 'dhcp',
  'wan_b_provider': 'BT',
  'wan_b_ip_setting': '32.45.31.141/30',
  'hardware': 'C1111-4PLTEEA',
  'serial': 'FOCXXSDF5K9',
  'vlans': ['8', '110'],
  'l3_ints': ['GigabitEthernet0/0/0', 'GigabitEthernet0/0/1'],
  'l2_ints': ['GigabitEthernet0/1/0',
   'GigabitEthernet0/1/1',
   'GigabitEthernet0/1/2',
   'GigabitEthernet0/1/3']},
 {'_id': ObjectId('64370e340971a02bdf950164'),
  'hostname': 'DEV2012R01',
  'device_type': 'router',
  'site_number': '2012',
  'site': 'Dublin',
  'status': 'Operational',
  'local_subnets': ['10.12.1.0/24', '10.12.2.0/24', '10.12.3.0/24'],
  'wan_a_provider': 'GTT',
  'wan_a_ip_setting': 'dhcp',
  'wan_b_provider': 'BT',
  'wan_b_ip_setting': '213.45.23.143/30',
  'hardware': 'C1111-4PLTEEA',
  'serial': 'FOC2XXX7L599',
  'vlans': ['8', '110'],
  'l3_ints': ['GigabitEthernet0/0/0', 'GigabitEthernet0/0/1'],
  'l2_ints': ['GigabitEthernet0/1/0',
   'GigabitEthernet0/1/1',
   'GigabitEthernet0/1/2',
   'GigabitEthernet0/1/3']}]

In [12]: 
```




##### Updating a record

```sh
In [12]: data_to_be_updated = {  "hostname": "DEV2012R01",
    ...:   "device_type":"router",
    ...:   "site_number":"2012",
    ...:   "site": "Dublin_XXXXXXXXXXXXXXXX",
    ...:   "status":"Operational",
    ...:   "local_subnets":["10.12.1.0/24", "10.12.2.0/24", "10.12.3.0/24"],
    ...:   "wan_a_provider":"GTT",
    ...:   "wan_a_ip_setting":"dhcp",
    ...:   "wan_b_provider":"BT",
    ...:   "wan_b_ip_setting":"213.45.23.143/30",
    ...:   "hardware": "C1111-4PLTEEA",
    ...:   "serial":"FOC2XXX7L599",
    ...:   "vlans":["8", "110"],
    ...:   "l3_ints":["GigabitEthernet0/0/0", "GigabitEthernet0/0/1"],
    ...:   "l2_ints":["GigabitEthernet0/1/0","GigabitEthernet0/1/1", "GigabitEthernet0/1/2", "GigabitEthernet0/1/3"]
    ...: }

In [13]: operation.update_record('64370e340971a02bdf950164',data_to_be_updated)

In [15]: operation.view_all_records()
Out[15]: 
[{'_id': ObjectId('64370dbf0971a02bdf950163'),
  'hostname': 'DEV2010R01',
  'device_type': 'router',
  'site_number': '2010',
  'site': 'Craydon',
  'status': 'Operational',
  'local_subnets': ['10.10.1.0/24', '10.10.2.0/24', '10.10.3.0/24'],
  'wan_a_provider': 'BT',
  'wan_a_ip_setting': 'dhcp',
  'wan_b_provider': 'BT',
  'wan_b_ip_setting': '32.45.31.141/30',
  'hardware': 'C1111-4PLTEEA',
  'serial': 'FOCXXSDF5K9',
  'vlans': ['8', '110'],
  'l3_ints': ['GigabitEthernet0/0/0', 'GigabitEthernet0/0/1'],
  'l2_ints': ['GigabitEthernet0/1/0',
   'GigabitEthernet0/1/1',
   'GigabitEthernet0/1/2',
   'GigabitEthernet0/1/3']},
 {'_id': ObjectId('64370e340971a02bdf950164'),
  'hostname': 'DEV2012R01',
  'device_type': 'router',
  'site_number': '2012',
  'site': 'Dublin_XXXXXXXXXXXXXXXX',
  'status': 'Operational',
  'local_subnets': ['10.12.1.0/24', '10.12.2.0/24', '10.12.3.0/24'],
  'wan_a_provider': 'GTT',
  'wan_a_ip_setting': 'dhcp',
  'wan_b_provider': 'BT',
  'wan_b_ip_setting': '213.45.23.143/30',
  'hardware': 'C1111-4PLTEEA',
  'serial': 'FOC2XXX7L599',
  'vlans': ['8', '110'],
  'l3_ints': ['GigabitEthernet0/0/0', 'GigabitEthernet0/0/1'],
  'l2_ints': ['GigabitEthernet0/1/0',
   'GigabitEthernet0/1/1',
   'GigabitEthernet0/1/2',
   'GigabitEthernet0/1/3']}]

In [16]: 
```




##### Removing a record

```sh

In [16]: operation.view_all_records()
Out[16]: 
[{'_id': ObjectId('64370dbf0971a02bdf950163'),
  'hostname': 'DEV2010R01',
  'device_type': 'router',
  'site_number': '2010',
  'site': 'Craydon',
  'status': 'Operational',
  'local_subnets': ['10.10.1.0/24', '10.10.2.0/24', '10.10.3.0/24'],
  'wan_a_provider': 'BT',
  'wan_a_ip_setting': 'dhcp',
  'wan_b_provider': 'BT',
  'wan_b_ip_setting': '32.45.31.141/30',
  'hardware': 'C1111-4PLTEEA',
  'serial': 'FOCXXSDF5K9',
  'vlans': ['8', '110'],
  'l3_ints': ['GigabitEthernet0/0/0', 'GigabitEthernet0/0/1'],
  'l2_ints': ['GigabitEthernet0/1/0',
   'GigabitEthernet0/1/1',
   'GigabitEthernet0/1/2',
   'GigabitEthernet0/1/3']},
 {'_id': ObjectId('64370e340971a02bdf950164'),
  'hostname': 'DEV2012R01',
  'device_type': 'router',
  'site_number': '2012',
  'site': 'Dublin_XXXXXXXXXXXXXXXX',
  'status': 'Operational',
  'local_subnets': ['10.12.1.0/24', '10.12.2.0/24', '10.12.3.0/24'],
  'wan_a_provider': 'GTT',
  'wan_a_ip_setting': 'dhcp',
  'wan_b_provider': 'BT',
  'wan_b_ip_setting': '213.45.23.143/30',
  'hardware': 'C1111-4PLTEEA',
  'serial': 'FOC2XXX7L599',
  'vlans': ['8', '110'],
  'l3_ints': ['GigabitEthernet0/0/0', 'GigabitEthernet0/0/1'],
  'l2_ints': ['GigabitEthernet0/1/0',
   'GigabitEthernet0/1/1',
   'GigabitEthernet0/1/2',
   'GigabitEthernet0/1/3']}]

In [17]: operation.remove_record('64370e340971a02bdf950164')

In [18]: operation.view_all_records()
Out[18]: 
[{'_id': ObjectId('64370dbf0971a02bdf950163'),
  'hostname': 'DEV2010R01',
  'device_type': 'router',
  'site_number': '2010',
  'site': 'Craydon',
  'status': 'Operational',
  'local_subnets': ['10.10.1.0/24', '10.10.2.0/24', '10.10.3.0/24'],
  'wan_a_provider': 'BT',
  'wan_a_ip_setting': 'dhcp',
  'wan_b_provider': 'BT',
  'wan_b_ip_setting': '32.45.31.141/30',
  'hardware': 'C1111-4PLTEEA',
  'serial': 'FOCXXSDF5K9',
  'vlans': ['8', '110'],
  'l3_ints': ['GigabitEthernet0/0/0', 'GigabitEthernet0/0/1'],
  'l2_ints': ['GigabitEthernet0/1/0',
   'GigabitEthernet0/1/1',
   'GigabitEthernet0/1/2',
   'GigabitEthernet0/1/3']}]

In [19]: 
```




  
  