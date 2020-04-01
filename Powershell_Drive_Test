#Powershell script to do drive test.
#the script reads via bluetooth the GPS coordinates and reads at the same time the throughput on the Laptop ethernet interface.
#the results are recorded on a CSV file.

$oldLat=0
$oldLong=0
$stop=Test-Path -Path stop.txt #to stop the script please create a file stop.txt on the SW path
if ($stop -ne 'True')
{
$autopause=Read-Host -Prompt "Do you want to activate autopause? [Y]Yes [N]No"	   
$COM = Read-Host -Prompt "Enter the GPS COM port (upper case)"

Get-Counter -Counter "\Network Interface(*)\Bytes Sent/sec" | Format-List -Property CounterSamples

$network= Read-host -Prompt "Enter network interface name (copy and paste the selected from above)"

$outpath= Read-host -Prompt "Enter path and CSV file"

$myArray=('counter','date','UL Kbps','DL Kbps','latitude','longitude')
$myArray | Format-Wide {$_} -Column 6 -Force
$myArray | Format-Wide {$_} -Column 6 -Force | Out-File $outpath -Append
$line = ""
$counter=0
$splitline = $line.split(",")
$port = new-Object System.IO.Ports.SerialPort $COM,9600,None,8,one
#$port.close()
#Start-Sleep -Milliseconds 10000
#if ($port.IsOpen -eq 'False')
#{
$port.open()
#}
	function Nmea2dec {
    Param ([double]$degrees, $o)
    $deg = [math]::floor($degrees/100.0)
    $frac = (($degrees/100.0) - $deg)/0.6
    $ret = $deg + $frac
    if ($o -eq "S" -or $o -eq "W") {$ret = $ret * (-1)}
    return $ret
}
$latitude = Nmea2dec $splitline[3] $splitline[4]
$longtitude = Nmea2dec $splitline[5] $splitline[6]
	

$cond=1
$inp=1
#while(($inp = Read-Host -Prompt "Select a command") -ne "Q")
while($cond -eq 1)
    {
	$counter=$counter+1
	$myArray[0]=$counter
	#$myArray[0]
	$myArray[1]=Get-Date -Format s  #get the date
	#$myArray[1]
	$myArray[2]=$($(Get-Counter -Counter "\Network Interface($network)\Bytes Sent/sec").countersamples).cookedvalue*0.008 #read network interface UL
	$myArray[2]=[string]$myArray[2]+" Kbps UL"
	#$myArray[2]
	$myArray[3]=$($(Get-Counter -Counter "\Network Interface($network)\Bytes Received/sec").countersamples).cookedvalue*0.008 #read network interface DL
	$myArray[3]=[string]$myArray[3]+" Kbps DL"
	#$myArray[3]
	$line = ""
	#GPS read
	$port.DiscardInBuffer()
	while (-not ($line -match ".GPRMC.*")) 
	{
	$line = $port.readline()
	}
	$splitline = $line.split(",")
	$myArray[4] = Nmea2dec $splitline[3] $splitline[4]
	$newLat=$myArray[4]
	$myArray[4] = [string]$myArray[4] + " latitude"
	#$myArray[4]
	$myArray[5] = Nmea2dec $splitline[5] $splitline[6]
	$newLong=$myArray[5]
	$myArray[5] = [string]$myArray[5] + " longitude"
	#$myArray[5]
	$myArray | Format-Wide {$_} -Column 6 -Force
	
	if($oldLat -eq $newLat -And $oldLong -eq $newLong -And $autopause -eq 'Y') #autopause
	{
	"autopause"} else {
	$myArray | Format-Wide {$_} -Column 6 -Force | Out-File $outpath -Append }
	Start-Sleep -Milliseconds 1000
	$oldLat=$newLat
	$oldLong=$newLong
	$stop=Test-Path -Path stop.txt #to stop the script please create a file stop.txt on the SW path
	if ($stop -eq 'True')
	{$port.close()
	"you stoped the program"
	Break}
	if ($counter -eq 10000)  #when 10000 measurements are reached the program will stop
	{
	$port.close()
	"Counter reached 10000 measurements"
	Break}
	}
}else
{"please delete the stop.txt file before start"}
