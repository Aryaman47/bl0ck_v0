$base = "http://127.0.0.1:8000"  # change if needed
$apiPrefix = "api/v1"

function Resolve-ApiUrl {
    param(
        [Parameter(Mandatory = $false)]
        [string[]]$PathParts = @()
    )

    # Accept usage styles like:
    # cl /mining/backend
    # cl mining backend
    # cl /api/v1/mining/backend
    $joined = ($PathParts -join "/").Trim()

    if ([string]::IsNullOrWhiteSpace($joined)) {
        return "$base/$apiPrefix"
    }

    $normalized = $joined.TrimStart("/")
    if ($normalized -like "$apiPrefix/*" -or $normalized -eq $apiPrefix) {
        return "$base/$normalized"
    }

    return "$base/$apiPrefix/$normalized"
}

function cl {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        $Args
    )

    if ($Args.Count -eq 0) {
        Write-Host "Usage: cl </path parts> [curl options]" -ForegroundColor Yellow
        Write-Host "Example: cl /mining/backend" -ForegroundColor DarkGray
        return
    }

    # Separate path parts (non -options) from curl options (-X, -H, etc.)
    $pathParts = @()
    $curlOptions = @()

    foreach ($arg in $Args) {
        if ($arg -match '^-') {
            $curlOptions += $arg
        } else {
            $pathParts += $arg
        }
    }

    $url = Resolve-ApiUrl -PathParts $pathParts
    curl.exe @curlOptions $url
}

function clPost {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        $Args
    )

    if ($Args.Count -eq 0) {
        Write-Host "Usage: clPost </path parts> [curl options]" -ForegroundColor Yellow
        Write-Host "Example: clPost /mining/backend/cpu" -ForegroundColor DarkGray
        return
    }

    $pathParts = @()
    $curlOptions = @()

    foreach ($arg in $Args) {
        if ($arg -match '^-') {
            $curlOptions += $arg
        } else {
            $pathParts += $arg
        }
    }

    $url = Resolve-ApiUrl -PathParts $pathParts
    curl.exe -X POST @curlOptions $url
}

function clPut {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        $Args
    )

    if ($Args.Count -eq 0) {
        Write-Host "Usage: clPut </path parts> [curl options]" -ForegroundColor Yellow
        Write-Host "Example: clPut /difficulty/manual/5" -ForegroundColor DarkGray
        return
    }

    $pathParts = @()
    $curlOptions = @()

    foreach ($arg in $Args) {
        if ($arg -match '^-') {
            $curlOptions += $arg
        } else {
            $pathParts += $arg
        }
    }

    $url = Resolve-ApiUrl -PathParts $pathParts
    curl.exe -X PUT @curlOptions $url
}
