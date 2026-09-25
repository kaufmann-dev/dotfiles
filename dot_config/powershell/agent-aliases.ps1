function muse {
    $program = Get-Command muse -CommandType Application, ExternalScript -ErrorAction Stop | Select-Object -First 1
    & $program.Source --yolo @args
}

function agy {
    $program = Get-Command agy -CommandType Application, ExternalScript -ErrorAction Stop | Select-Object -First 1
    & $program.Source --dangerously-skip-permissions @args
}

function claude {
    $program = Get-Command claude -CommandType Application, ExternalScript -ErrorAction Stop | Select-Object -First 1
    & $program.Source --dangerously-skip-permissions @args
}
