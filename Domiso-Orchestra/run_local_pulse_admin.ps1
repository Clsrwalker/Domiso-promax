param(
    [string]$Backend = "ahk-tap",
    [string]$WindowExe = "Sky.exe",
    [string]$Key = "y"
)

function Test-IsAdmin {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-IsAdmin)) {
    $powershell = (Get-Process -Id $PID).Path
    $arguments = @(
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-File", $PSCommandPath,
        "-Backend", $Backend,
        "-WindowExe", $WindowExe,
        "-Key", $Key
    )
    Start-Process -FilePath $powershell -ArgumentList $arguments -Verb RunAs -WorkingDirectory $PSScriptRoot
    exit
}

Set-Location $PSScriptRoot

python -m domiso_orchestra.player_client --local-pulse --backend $Backend --window-exe $WindowExe --local-pulse-key $Key
