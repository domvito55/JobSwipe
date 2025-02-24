$startPath = Get-Location
$excludeFolder = "__pycache__"

function Get-DirectoryTree {
    param (
        [string]$path,
        [string]$prefix = ""
    )
    $items = Get-ChildItem -Path $path
    foreach ($item in $items) {
        if ($item.Name -eq $excludeFolder) {
            continue
        }
        Write-Output "$prefix`-- $($item.Name)"
        if ($item.PSIsContainer) {
            Get-DirectoryTree -path $item.FullName -prefix "$prefix`   "
        }
    }
}

Get-DirectoryTree -path $startPath
