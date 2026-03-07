<#
.SYNOPSIS
    Applies common registry tweaks for performance and usability.
#>
param(
    [switch]$EnableVerboseOutput
)

if ($EnableVerboseOutput) {
    $VerbosePreference = "Continue"
}

Write-Verbose "Starting Registry Tweaks..."

function Set-RegistryKey {
    param (
        [string]$Path,
        [string]$Name,
        [string]$Value,
        [string]$PropertyType
    )

    try {
        if (-not (Test-Path $Path)) {
            New-Item -Path $Path -Force -ErrorAction SilentlyContinue | Out-Null
        }
        
        Set-ItemProperty -Path $Path -Name $Name -Value $Value -Type $PropertyType -ErrorAction Stop
        Write-Verbose "[OK] Registry Updated: $Name -> $Value"
    }
    catch {
        Write-Verbose "[ERROR] Failed to update registry key $Name at $Path."
    }
}

# 1. Disable Bing Web Search in the Start Menu
Set-RegistryKey -Path "HKCU:\Software\Policies\Microsoft\Windows\Explorer" -Name "DisableSearchBoxSuggestions" -Value 1 -PropertyType DWord

# 2. Show hidden files and folders by default
Set-RegistryKey -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "Hidden" -Value 1 -PropertyType DWord

# 3. Disable Lock Screen
Set-RegistryKey -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\Personalization" -Name "NoLockScreen" -Value 1 -PropertyType DWord

Write-Output "Registry tweaks successfully processed."
