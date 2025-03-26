#!/usr/bin/env pwsh
# Documentation Structure Validator
# This script checks for common documentation structure issues

# Define absolute paths - simpler and more reliable
$projectRoot = "D:\PROJECTS\hephaestus"
$docsDir = Join-Path $projectRoot "docs"
$configFile = Join-Path $docsDir "mkdocs.yml"

Write-Host "Validating documentation structure in $docsDir" -ForegroundColor Cyan
Write-Host "Looking for config file at $configFile" -ForegroundColor Cyan

# Check if mkdocs.yml exists
if (-not (Test-Path $configFile)) {
    Write-Host "ERROR: mkdocs.yml not found at $configFile" -ForegroundColor Red
    exit 1
}

# Collect information
$allFiles = Get-ChildItem -Path $docsDir -Filter "*.md" -Recurse
$allDirectories = Get-ChildItem -Path $docsDir -Directory
$issues = @()

# Read mkdocs.yml content
try {
    $yamlContent = Get-Content $configFile -Raw
    Write-Host "Successfully read mkdocs.yml file" -ForegroundColor Green
} 
catch {
    Write-Host "ERROR: Unable to read mkdocs.yml: $_" -ForegroundColor Red
    exit 1
}

# 1. Check if each directory has an index.md file
Write-Host "Checking for missing index.md files..." -ForegroundColor Yellow
foreach ($dir in $allDirectories) {
    $indexFile = Join-Path $dir.FullName "index.md"
    if (-not (Test-Path $indexFile)) {
        $issues += "Directory $($dir.Name) is missing an index.md file"
    }
}

# 2. Check for broken internal links
Write-Host "Checking for broken internal links..." -ForegroundColor Yellow
$internalLinkPattern = '\]\((?!http)([^)]+\.md(?:#[^)]*)?)\)'
$brokenLinks = @()

foreach ($file in $allFiles) {
    $content = Get-Content $file.FullName -Raw
    $matches = [regex]::Matches($content, $internalLinkPattern)
    
    foreach ($match in $matches) {
        $link = $match.Groups[1].Value
        
        # Remove anchor if present
        if ($link -match '#') {
            $link = $link.Substring(0, $link.IndexOf('#'))
        }
        
        # Convert relative path to absolute path
        $targetPath = $null
        if ($link.StartsWith('/')) {
            # Absolute from docs root
            $targetPath = Join-Path $docsDir $link.TrimStart('/')
        } else {
            # Relative to current file
            $targetPath = Join-Path $file.DirectoryName $link
        }
        
        # Check if target file exists
        if (-not (Test-Path $targetPath)) {
            $brokenLinks += "Broken link in $($file.FullName): $link"
        }
    }
}

$issues += $brokenLinks

# 3. Check for files referenced in mkdocs.yml that don't exist
Write-Host "Checking for files referenced in mkdocs.yml that don't exist..." -ForegroundColor Yellow

$yamlFilePattern = ':\s+([^:]+\.md)'
$yamlMatches = [regex]::Matches($yamlContent, $yamlFilePattern)
$missingFiles = @()

foreach ($match in $yamlMatches) {
    $filePath = $match.Groups[1].Value.Trim()
    $targetPath = Join-Path $docsDir $filePath
    
    if (-not (Test-Path $targetPath)) {
        $missingFiles += "File referenced in mkdocs.yml not found: $filePath"
    }
}

$issues += $missingFiles

# 4. Check for empty directories
Write-Host "Checking for empty directories..." -ForegroundColor Yellow
foreach ($dir in $allDirectories) {
    $files = Get-ChildItem -Path $dir.FullName -File
    if ($files.Count -eq 0) {
        $issues += "Empty directory found: $($dir.FullName)"
    }
}

# 5. Check for files not referenced in mkdocs.yml
Write-Host "Checking for Markdown files not referenced in mkdocs.yml..." -ForegroundColor Yellow

$unreferencedFiles = @()
foreach ($file in $allFiles) {
    # Get relative path from docs dir
    $relativePath = $file.FullName.Substring($docsDir.Length + 1).Replace("\", "/")
    
    # Skip index.md files - these might be auto-included
    if ($file.Name -eq "index.md") {
        continue
    }
    
    # Skip files in specific directories that might not be directly referenced
    if ($relativePath -match "^(status/|scripts/|assets/|templates/|research/|progress/)") {
        continue
    }
    
    # Skip other non-documentation files
    if ($file.Name -match "^(README|roadmap|phase|status)") {
        continue 
    }
    
    if (-not $yamlContent -match [regex]::Escape($relativePath)) {
        $unreferencedFiles += "File not referenced in mkdocs.yml: $relativePath"
    }
}

$issues += $unreferencedFiles

# Print results
if ($issues.Count -eq 0) {
    Write-Host "Documentation structure validation completed successfully! No issues found." -ForegroundColor Green
} else {
    Write-Host "Documentation structure validation completed with $($issues.Count) issues:" -ForegroundColor Red
    foreach ($issue in $issues) {
        Write-Host "- $issue" -ForegroundColor Yellow
    }
    
    Write-Host "`nRecommendations:" -ForegroundColor Cyan
    Write-Host "1. Fix any missing index.md files in directories" -ForegroundColor White
    Write-Host "2. Correct broken internal links between documentation files" -ForegroundColor White
    Write-Host "3. Update mkdocs.yml to remove references to non-existent files" -ForegroundColor White
    Write-Host "4. Create missing files referenced in mkdocs.yml" -ForegroundColor White
    Write-Host "5. Consider removing empty directories or adding content to them" -ForegroundColor White
    Write-Host "6. Add unreferenced files to mkdocs.yml if they should be included in the documentation" -ForegroundColor White
} 