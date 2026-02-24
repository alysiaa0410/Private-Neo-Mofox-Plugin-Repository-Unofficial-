Param(
  [string]$RepoRoot = (Get-Location).Path
)

Set-Location $RepoRoot

Write-Host "Running validate_repo.py ..."
python tools\validate_repo.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

if (Test-Path "requirements-dev.txt") {
  Write-Host "Installing dev tools (optional) ..."
  python -m pip install -r requirements-dev.txt
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host "Running ruff check ..."
  ruff check .
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host "Running ruff format --check ..."
  ruff format --check .
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

Write-Host "OK"

