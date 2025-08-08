$base = "http://127.0.0.1:8000"  # change if needed

function cl {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        $Args
    )

    if ($Args.Count -eq 0) {
        Write-Host "Usage: cl <path parts> [curl options]" -ForegroundColor Yellow
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

    $url = "$base/" + ($pathParts -join "/")
    curl.exe @curlOptions $url
}

function clPost {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        $Args
    )

    if ($Args.Count -eq 0) {
        Write-Host "Usage: clP <path parts> [curl options]" -ForegroundColor Yellow
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

    $url = "$base/" + ($pathParts -join "/")
    curl.exe -X POST @curlOptions $url
}
