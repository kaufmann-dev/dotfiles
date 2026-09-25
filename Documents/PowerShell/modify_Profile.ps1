[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$sourceLine = '. "$HOME/.config/powershell/agent-aliases.ps1"'
$content = [Console]::In.ReadToEnd()
[Console]::Out.Write($content)

if (($content -split '\r?\n') -notcontains $sourceLine) {
    if ($content.Length -gt 0 -and -not $content.EndsWith("`n")) {
        [Console]::Out.WriteLine()
    }
    [Console]::Out.WriteLine($sourceLine)
}
