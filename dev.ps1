param([string]$Action = "up")

$compose_file = "compose/docker-compose.development.yml"

switch ($Action.ToLower()) {
    "up" { docker compose -f $compose_file up --build }
    "down" { docker compose -f $compose_file down }
    default { Write-Host "Invalid command. Usage: .\dev.ps1 [up|down]" }
}
