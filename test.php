<html>
<head>
<title>Run my Python files</title>
<?PHP
$command = escapeshellcmd('/home/billdanza/tool-two.py /home/billdanza/Downloads/wireshark-traces-8.1/ethernet-wireshark-trace1.pcapng');
$output = shell_exec($command);
echo $output;
shell_exec('sudo rm -r /var/www/html/files/my_plot.png; sudo cp my_plot.png /var/www/html/');
?>
</head>
<font size="8">Protocol Distribution:</font>
<img src="files/my_plot.png"/><br>
<font size="8">Packet Count between IPs:</font><br>
<img src="files/my_plot2.png"/>
</html>
