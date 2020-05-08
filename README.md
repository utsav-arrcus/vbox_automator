usage: vbox_automation_functions.py [-h] -n Matrix_filename [-c] [-p] [-m]
                                    [-l] [-d] [-r 'comands'] [-f] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -n Matrix_filename, --network Matrix_filename
                        Input network file
  -c, --create          create network
  -p, --password        change pasword
  -m, --ssh_config      configure ssh access
  -l, --login           Login using default passwd
  -d, --dhclient        run dhclient on ma1
  -r 'comands', --commands 'comands'
                        run command on linux
  -f, --flush           flush all interfaces
  -s, --show            show ip address of ma1
  
  
  you can create a martix file, example is provided in topolgy_files/ 
  the top row and first coloumn are VM names, and the matrix is number of connections you want 
  between the two VMs of a row and coloumn.
  
  directions:
  create and clone VMs
  name them
  dont start them and run, python vbox_automation_functions.py -n <filename> -c, to create the connections
  run -p options to change the password
  run -m to configure ssh on the devices 
  run -s to display ip addresses
