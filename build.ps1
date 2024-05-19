[CmdletBinding()]
Param(
  # Specifies a task to conduct.
  [Parameter(Mandatory = $False,
             Position = 0,
             HelpMessage = "A task to conduct.")]
  [ValidateSet("Build", "Clean")]
  [System.String[]]
  $Task = "Build"
)

# cSpell:ignore GOARCH

Begin {
  $script:GIT_TAG = (& "bash" -c "git tag | sort --version-sort | tail -n1")
  $script:PREFIX = "pst_$($script:GIT_TAG)"

  Function Invoke-Build {
    [CmdletBinding()]
    Param()
    New-Item -Path dist -ItemType Directory | Out-Null;
    Push-Location -LiteralPath "web"
    & "pnpm" install
    & "pnpm" build
    Pop-Location
    Write-Host -Object "Building for $($script:GIT_TAG)"
    & "go" mod download
    New-Item -Path dist/windows_x86_64 -ItemType Directory | Out-Null;
    New-Item -Path dist/linux_x86_64 -ItemType Directory | Out-Null;
    New-Item -Path dist/linux_aarch64 -ItemType Directory | Out-Null;
    New-Item -Path dist/darwin_arm64 -ItemType Directory | Out-Null;
    Write-Host -Object "Building windows-386"
    $env:GOOS = "windows"
    $env:GOARCH = "386"
    & "go" build -ldflags="-s -w -X 'main.version=$($GIT_TAG)'" -o "./dist/windows_x86_64/pst.exe" "main.go"
    Write-Host -Object "Building linux-amd"
    $env:GOOS = "linux"
    $env:GOARCH = "amd64"
    & "go" build -ldflags="-s -w -X 'main.version=$($GIT_TAG)'" -o "./dist/linux_x86_64/pst.exe" "main.go"
    Write-Host -Object "Building linux-arm"
    $env:GOOS = "linux"
    $env:GOARCH = "arm64"
    & "go" build -ldflags="-s -w -X 'main.version=$($GIT_TAG)'" -o "./dist/linux_aarch64/pst.exe" "main.go"
    Write-Host -Object "Building darwin-arm"
    $env:GOOS = "darwin"
    $env:GOARCH = "arm64"
    & "go" build -ldflags="-s -w -X 'main.version=$($GIT_TAG)'" -o "./dist/darwin_arm64/pst.exe" "main.go"
    Write-Host -Object "Building windows-386"
    $env:GOOS = "windows"
    $env:GOARCH = "386"
    & "go" build -ldflags="-s -w" -o "./dist/pst-agent_$($GIT_TAG)_windows_x86_64.exe" "./cmd/pst-agent/main.go"
    Write-Host -Object "Building linux-amd"
    $env:GOOS = "linux"
    $env:GOARCH = "amd64"
    & "go" build -ldflags="-s -w" -o "./dist/pst-agent_$($GIT_TAG)_linux_x86_64" "./cmd/pst-agent/main.go"
    Write-Host -Object "Building linux-arm"
    $env:GOOS = "linux"
    $env:GOARCH = "arm64"
    & "go" build -ldflags="-s -w" -o "./dist/pst-agent_$($GIT_TAG)_linux_aarch64" "./cmd/pst-agent/main.go"
    Write-Host -Object "Building darwin-arm"
    $env:GOOS = "darwin"
    $env:GOARCH = "arm64"
    & "go" build -ldflags="-s -w" -o "./dist/pst-agent_$($GIT_TAG)_darwin_arm64" "./cmd/pst-agent/main.go"

    Copy-Item -Path "test/config.yaml" -Destination "dist/windows_x86_64/config.yaml"
    Copy-Item -Path "test/config.yaml" -Destination "dist/linux_x86_64/config.yaml"
    Copy-Item -Path "test/config.yaml" -Destination "dist/linux_aarch64/config.yaml"
    Copy-Item -Path "test/config.yaml" -Destination "dist/darwin_arm64/config.yaml"

    Copy-Item -Path "script/start.bat" -Destination "dist/windows_x86_64/start.bat"

    & "bash" -c "chmod -R 755 dist/*"
  }

  Function Invoke-Clean {
    [CmdletBinding()]
    Param()
  }
}
Process {
}
End {

}