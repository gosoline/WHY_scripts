oh-my-posh.exe init pwsh --config $env:POSH_THEMES_PATH\why_ys.omp.json | Invoke-Expression
Set-PSReadLineKeyHandler -Chord "Ctrl+RightArrow" -Function ForwardWord