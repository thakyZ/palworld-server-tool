[CmdLetBinding()]
Param()

Begin {
  If ($IsWindows) {
    $ProgramExtension = ".exe"
    $ScriptExtension = ".ps1"
  } Else {
    $ProgramExtension = ""
    $ScriptExtension = ".sh"
  }

  $SystemPython = (Get-Command -Name "python$($ProgramExtension)" -ErrorAction SilentlyContinue);
  If ($Null -eq $SystemPython) {
    Throw "Program python$($ProgramExtension) not found on system path."
  }
  $OhMyPosh = (Get-Command -Name "oh-my-posh" -ErrorAction SilentlyContinue);
  If ($Null -eq $SystemPython) {
    Write-Warning -Message "Program oh-my-posh not found on system path, skipping..."
  }

  Push-Location -Location (Get-Item -Path $PSScriptRoot).FullName
}
Process {
  & "$($SystemPython)" "-m venv" "--prompt `"sav_cli`"" "--upgrade-deps" "env";
  $LocalActivateVenv = (Get-Item -LiteralPath (Join-Path -Path $PWD -ChildPath "env" -AdditionalChildPath @("Scripts", "activate$($ScriptExtension)")) -ErrorAction SilentlyContinue);
  If ($Null -eq $LocalPython) {
    Throw "PowerShell script ``activate$($ScriptExtension)`` not found on local environment path."
  }
  & "$($LocalActivateVenv)"
  & "$($OhMyPosh)" "init" "pwsh" | Invoke-Expression
  $LocalPython = (Get-Item -LiteralPath (Join-Path -Path $PWD -ChildPath "env" -AdditionalChildPath @("Scripts", "python$($ProgramExtension)")) -ErrorAction SilentlyContinue);
  If ($Null -eq $LocalPython) {
    Throw "Program python$($ProgramExtension) not found on local environment path."
  }
  & "$($LocalPython)" "-m pip" "install" "-r" "requirements.txt"
  & "$($LocalPython)" "-m poetry" "install" "--sync"
}
End {
  Pop-Location
}