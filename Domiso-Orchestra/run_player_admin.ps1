param(
    [string]$Server = "ws://127.0.0.1:8765/ws/player",
    [string]$ClientId = "PC-A",
    [string]$Backend = "ahk-tap",
    [string]$WindowExe = "Sky.exe",
    [string]$Layout = "sky15",
    [int]$DelayOffsetMs = 0,
    [switch]$ManualReady
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
        "-Server", $Server,
        "-ClientId", $ClientId,
        "-Backend", $Backend,
        "-WindowExe", $WindowExe,
        "-Layout", $Layout,
        "-DelayOffsetMs", "$DelayOffsetMs"
    )
    if ($ManualReady) {
        $arguments += "-ManualReady"
    }
    Start-Process -FilePath $powershell -ArgumentList $arguments -Verb RunAs -WorkingDirectory $PSScriptRoot
    exit
}

Set-Location $PSScriptRoot

$clientArgs = @(
    "-m", "domiso_orchestra.player_client",
    "--server", $Server,
    "--client-id", $ClientId,
    "--backend", $Backend,
    "--window-exe", $WindowExe,
    "--layout", $Layout,
    "--delay-offset-ms", "$DelayOffsetMs"
)
if ($ManualReady) {
    $clientArgs += "--manual-ready"
}

python @clientArgs
