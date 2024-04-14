$env:DEFAULT_PROJECT_ID=gcloud config get-value project
Write-Output DEFAULT_PROJECT_ID=$env:DEFAULT_PROJECT_ID

$env:DEFAULT_REGION=gcloud config get-value compute/region
$env:DEFAULT_REGION=$env:DEFAULT_REGION
Write-Output DEFAULT_REGION=$env:DEFAULT_REGION

$env:DEFAULT_LOCATION=gcloud config get-value compute/zone
$env:DEFAULT_ZONE=$env:DEFAULT_LOCATION
Write-Output DEFAULT_LOCATION=$env:DEFAULT_LOCATION
Write-Output DEFAULT_ZONE=$env:DEFAULT_ZONE