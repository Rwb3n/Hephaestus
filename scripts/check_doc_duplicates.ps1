# check_doc_duplicates.ps1
# 
# This script checks for potential duplicate documentation files by comparing
# files in the docs root directory with files in subdirectories.
#
# Usage: ./scripts/check_doc_duplicates.ps1

# Get current directory and docs path
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$docsPath = Join-Path (Split-Path -Parent $scriptPath) "docs"

Write-Host "Checking for duplicate documentation files..." -ForegroundColor Cyan

# Get all markdown files in the docs root
$rootMarkdownFiles = Get-ChildItem -Path $docsPath -Filter "*.md" | Where-Object { $_.DirectoryName -eq $docsPath }

# Get all subdirectories
$subdirectories = Get-ChildItem -Path $docsPath -Directory

# Initialize arrays to store results
$potentialDuplicates = @()

# Check each file in the root against files in subdirectories
foreach ($rootFile in $rootMarkdownFiles) {
    $rootFilename = $rootFile.Name
    
    foreach ($subdir in $subdirectories) {
        $subdirFiles = Get-ChildItem -Path $subdir.FullName -Filter "*.md" -Recurse
        
        foreach ($subdirFile in $subdirFiles) {
            if ($subdirFile.Name -eq $rootFilename) {
                $potentialDuplicates += [PSCustomObject]@{
                    RootFile = $rootFile.FullName
                    SubdirFile = $subdirFile.FullName
                }
            }
        }
    }
}

# Check for files with similar content (even if filenames differ)
$allMarkdownFiles = Get-ChildItem -Path $docsPath -Filter "*.md" -Recurse
$contentSimilarities = @()

for ($i = 0; $i -lt $allMarkdownFiles.Count; $i++) {
    $file1 = $allMarkdownFiles[$i]
    
    # Skip files in the root docs directory that are likely to be specialized
    if ($file1.DirectoryName -eq $docsPath -and 
        ($file1.Name -eq "index.md" -or 
         $file1.Name -like "*status*.md" -or 
         $file1.Name -like "*README.md" -or
         $file1.Name -like "*roadmap.md")) {
        continue
    }
    
    for ($j = $i + 1; $j -lt $allMarkdownFiles.Count; $j++) {
        $file2 = $allMarkdownFiles[$j]
        
        # Skip comparisons between files in the same directory
        if ($file1.DirectoryName -eq $file2.DirectoryName) {
            continue
        }
        
        # Skip files in the root docs directory that are likely to be specialized
        if ($file2.DirectoryName -eq $docsPath -and 
            ($file2.Name -eq "index.md" -or 
             $file2.Name -like "*status*.md" -or 
             $file2.Name -like "*README.md" -or
             $file2.Name -like "*roadmap.md")) {
            continue
        }
        
        # Read first 10 lines of each file to compare titles and frontmatter
        $content1 = Get-Content -Path $file1.FullName -TotalCount 10
        $content2 = Get-Content -Path $file2.FullName -TotalCount 10
        
        # Check if the title lines are similar
        $titleMatch = $false
        foreach ($line1 in $content1) {
            if ($line1 -match "^# (.+)$") {
                $title1 = $matches[1].Trim()
                
                foreach ($line2 in $content2) {
                    if ($line2 -match "^# (.+)$") {
                        $title2 = $matches[1].Trim()
                        
                        if ($title1 -eq $title2) {
                            $titleMatch = $true
                            break
                        }
                    }
                }
                
                break
            }
        }
        
        if ($titleMatch) {
            $contentSimilarities += [PSCustomObject]@{
                File1 = $file1.FullName
                File2 = $file2.FullName
                Title = $title1
            }
        }
    }
}

# Display results
if ($potentialDuplicates.Count -gt 0) {
    Write-Host "`nPotential duplicate files (same filename):" -ForegroundColor Yellow
    $potentialDuplicates | ForEach-Object {
        Write-Host "Root file: $($_.RootFile)" -ForegroundColor Red
        Write-Host "Subdir file: $($_.SubdirFile)`n" -ForegroundColor Red
    }
} else {
    Write-Host "`nNo duplicate filenames found." -ForegroundColor Green
}

if ($contentSimilarities.Count -gt 0) {
    Write-Host "`nPotential content duplicates (same title):" -ForegroundColor Yellow
    $contentSimilarities | ForEach-Object {
        Write-Host "Title: $($_.Title)" -ForegroundColor Red
        Write-Host "File 1: $($_.File1)" -ForegroundColor Red
        Write-Host "File 2: $($_.File2)`n" -ForegroundColor Red
    }
} else {
    Write-Host "`nNo content duplicates found." -ForegroundColor Green
}

# Provide recommendations if duplicates found
if ($potentialDuplicates.Count -gt 0 -or $contentSimilarities.Count -gt 0) {
    Write-Host "Recommendations:" -ForegroundColor Cyan
    Write-Host "1. Review the identified duplicates and determine which should be kept"
    Write-Host "2. For files that should be moved rather than deleted, update any references in other documents"
    Write-Host "3. Update the mkdocs.yml navigation to reflect any changes"
    Write-Host "4. Run this script again after making changes to verify duplicates are resolved"
    exit 1
} else {
    Write-Host "`nDocumentation structure looks good!" -ForegroundColor Green
    exit 0
} 