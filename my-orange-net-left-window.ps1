$pinfo = New-Object System.Diagnostics.ProcessStartInfo
$pinfo.FileName = "my-orange-net-left.bat"
$pinfo.RedirectStandardError = $true
$pinfo.RedirectStandardOutput = $true
$pinfo.UseShellExecute = $false
$pinfo.Arguments = "localhost"
$p = New-Object System.Diagnostics.Process
$p.StartInfo = $pinfo
$p.Start() | Out-Null
$p.WaitForExit()
$stdout = $p.StandardOutput.ReadToEnd()
$stderr = $p.StandardError.ReadToEnd()

# $stdout = $stdout.replace('.',',')
# $stdout = $stdout -replace "`n","" -replace "`r",""

$wshell = New-Object -ComObject Wscript.Shell
$wshell.Popup("$stdout",0, "pozosta³o internetu", 0)