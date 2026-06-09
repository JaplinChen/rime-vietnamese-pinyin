$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir

Set-Location $repoRoot
$env:PYTHONIOENCODING = "utf-8"
python .\make_dict\verify.py
