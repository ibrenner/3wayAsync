# 3wayAsync
A solution written to enable 1 to many Async replication for InfiniBox

## Prerequisites
The script uses python3. <br>
The script uses Infinisdk module. <br>
Prior to running the script, please make sure to create an identical user within all relevant InfiniBox systems. 

## Authentication and configuration
Please make sure to create a config file for each pair of InfiniBox systems. <br>
Each file contents should be as follows:
```
src_ibox ibox1
src_user admin
dst_password MTIzNDU2
dst_ibox ibox2
dst_user admin
src_password MTIzNDU2
```
password value should be encrypted using base64.

## Usage
```
usage: 3WayAsync.py [-h] -v V1_NAME -b V2_NAME -c CONFIGFILE -r RPO -i
                    INTERVAL

Resize a replicated volume that is a member of a cg.

optional arguments:
  -h, --help            show this help message and exit
  -v V1_NAME, --volume V1_NAME
                        The local volume name
  -b V2_NAME, --remote_vol V2_NAME
                        The remote volume name
  -c CONFIGFILE, --configfile CONFIGFILE
                        Config file name
  -r RPO, --rpo RPO     RPO in minutes
  -i INTERVAL, --interval INTERVAL
                        Sync interval in minutes
```

## Example 

```
 ./3WayAsync.py -v vol3way  -b vol3way-target -c .testing2.sec -r 30 -i 1
  ```

### note
InfiniBox systems running version lower than 5.x won't be able to replicate filesystems using this tool.