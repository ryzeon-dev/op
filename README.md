# op - Open Ports
FOSS utility to detect open listening ports in linux systems 

## Installation
Run the installation script as root
 
``` 
sudo ./install.sh 
```

## Usage
Run with no arguments to display both TCP and UDP open ports 
```
$ op
```


Pass `tcp` to only show TCP open ports
```
$ op tcp
``` 


Pass `udp` to only show UDP open ports 
```
$ op udp
``` 


If ran as `root`, pid and process name (which opened the port) will be displaye will be displayed


Pass `help` to get help
```
$ op help
```
