import paramiko, time, csv

#this Python script connects to a list of network devices which IPs are listed in the file enbList.csv
#on each device the script runs the commands listed in commandList.csv
#the files enbList.csv and commandList.csv should be stored in the same folder than this script.
print("batch SSH")
with open('enbList.csv') as IPs:  #read the csv file with the list of IPs
    reader=csv.reader(IPs)
    eNodeBs=list(reader)
    lenght=eNodeBs.__len__()
    print(lenght)
with open('commandList.csv') as Commands:
	reader=csv.reader(Commands)
	Comm=list(Commands)
	Commandlenght=Comm.__len__()
i=0
j=0
while i<lenght:
    string=str(eNodeBs[i])
    string=string.replace("[","")
    string=string.replace("]","")
    string=string.replace("'","")
    i=i+1
    print(string)
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(string,username='op',password="PZ8Hfy3=Ve7fQkt*",auth_timeout=15,banner_timeout=15)
    except:
        print ("connection error")    
    else:
        time.sleep(2)
        channel=client.invoke_shell()
        out = channel.recv(9999)
        time.sleep(1)
        while not channel.recv_ready():
            time.sleep(1)
            channel.recv(1024)
        channel.send("show date\n")
        time.sleep(1)
        channel.send("airspansu\n")
        time.sleep(1)
        output=channel.recv(9999).decode('ascii')
        print (output)
        channel.send("S-N<&t8{<wu98wCD\n")
        time.sleep(1)
        output=channel.recv(9999).decode('ascii')
        print (output)
        while j<Commandlenght:
            channel.send(Comm[j]+"\n")
            time.sleep(1)
            output=channel.recv(9999).decode('ascii')
            print (output)
            j=j+1
    finally:
        j=0
        client.close()
