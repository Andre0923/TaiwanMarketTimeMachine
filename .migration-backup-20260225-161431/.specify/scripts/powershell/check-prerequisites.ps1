<#
.SYNOPSIS
    檢查 Speckit 開發環境的前置條件
.DESCRIPTION
    驗證專案目錄結構、必要檔案是否存在，並輸出環境資訊供 AI Agent 使用。
.PARAMETER Json
    以 JSON 格式輸出結果
.PARAMETER FeatureDir
    指定 Feature 目錄路徑（選用）
.EXAMPLE
    .\check-prerequisites.ps1
    .\check-prerequisites.ps1 -Json
    .\check-prerequisites.ps1 -FeatureDir "specs/features/001-my-feature"
#>

param(
    [switch]$Json,
    [string]$FeatureDir = ""
)

# 取得專案根目錄（從 .specify/scripts/powershell/ 往上三層）
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Get-Item $ScriptDir).Parent.Parent.Parent.FullName

# 檢查結果物件
$Result = @{
    PROJECT_ROOT = $ProjectRoot
    FEATURE_DIR = ""
    AVAILABLE_DOCS = @()
    CHECKS = @{
        DirectoryStructure = @{}
        SystemFiles = @{}
        SpecifyStructure = @{}
    }
    STATUS = "OK"
    ERRORS = @()
}

# 檢查目錄結構
$RequiredDirs = @(
    "specs/system",
    "specs/system/contracts",
    "specs/features",
    "specs/history",
    "specs/history/specs",
    "specs/history/plans",
    "specs/history/tasks",
    "src",
    "tests",
    "logs",
    "docs"
)

foreach ($dir in $RequiredDirs) {
    $fullPath = Join-Path $ProjectRoot $dir
    $exists = Test-Path $fullPath -PathType Container
    $Result.CHECKS.DirectoryStructure[$dir] = $exists
    if (-not $exists) {
        $Result.ERRORS += "Missing directory: $dir"
        $Result.STATUS = "ERROR"
    }
}

# 檢查 System 層檔案
$SystemFiles = @(
    "specs/system/spec.md",
    "specs/system/data-model.md",
    "specs/system/flows.md",
    "specs/system/unify-flow.md"
)

foreach ($file in $SystemFiles) {
    $fullPath = Join-Path $ProjectRoot $file
    $exists = Test-Path $fullPath -PathType Leaf
    $Result.CHECKS.SystemFiles[$file] = $exists
}

# 檢查 .specify 結構
$SpecifyFiles = @(
    ".specify/memory/constitution.md",
    ".specify/scripts/powershell/check-prerequisites.ps1",
    ".specify/templates/spec-template.md"
)

foreach ($file in $SpecifyFiles) {
    $fullPath = Join-Path $ProjectRoot $file
    $exists = Test-Path $fullPath -PathType Leaf
    $Result.CHECKS.SpecifyStructure[$file] = $exists
}

# 處理 Feature 目錄
if ($FeatureDir) {
    $featurePath = if ([System.IO.Path]::IsPathRooted($FeatureDir)) {
        $FeatureDir
    } else {
        Join-Path $ProjectRoot $FeatureDir
    }
    
    if (Test-Path $featurePath -PathType Container) {
        $Result.FEATURE_DIR = $featurePath
        
        # 收集 Feature 目錄中的文件
        $featureFiles = @("spec.md", "plan.md", "tasks.md", "research.md", "quickstart.md", "data-model.md")
        foreach ($file in $featureFiles) {
            $filePath = Join-Path $featurePath $file
            if (Test-Path $filePath -PathType Leaf) {
                $Result.AVAILABLE_DOCS += $file
            }
        }
        
        # 檢查 contracts 子目錄
        $contractsDir = Join-Path $featurePath "contracts"
        if (Test-Path $contractsDir -PathType Container) {
            $contractFiles = Get-ChildItem -Path $contractsDir -Filter "*.md" -File
            foreach ($cf in $contractFiles) {
                $Result.AVAILABLE_DOCS += "contracts/$($cf.Name)"
            }
        }
    } else {
        $Result.ERRORS += "Feature directory not found: $FeatureDir"
        $Result.STATUS = "WARNING"
    }
} else {
    # 嘗試自動偵測 Feature 目錄（從 Git 分支名稱）
    try {
        $branch = git -C $ProjectRoot rev-parse --abbrev-ref HEAD 2>$null
        if ($branch -and $branch -ne "main" -and $branch -ne "master") {
            # 嘗試匹配 feature 目錄
            $featuresDir = Join-Path $ProjectRoot "specs/features"
            if (Test-Path $featuresDir) {
                $matchingDirs = Get-ChildItem -Path $featuresDir -Directory | Where-Object {
                    $branch -like "*$($_.Name)*" -or $_.Name -like "*$branch*"
                }
                if ($matchingDirs.Count -eq 1) {
                    $Result.FEATURE_DIR = $matchingDirs[0].FullName
                }
            }
        }
    } catch {
        # 忽略 Git 錯誤
    }
}

# 輸出結果
if ($Json) {
    $Result | ConvertTo-Json -Depth 4
} else {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Speckit Prerequisites Check" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Project Root: $($Result.PROJECT_ROOT)" -ForegroundColor White
    Write-Host "Feature Dir:  $($Result.FEATURE_DIR)" -ForegroundColor White
    Write-Host "Status:       $($Result.STATUS)" -ForegroundColor $(if ($Result.STATUS -eq "OK") { "Green" } else { "Red" })
    Write-Host ""
    
    Write-Host "Directory Structure:" -ForegroundColor Yellow
    foreach ($key in $Result.CHECKS.DirectoryStructure.Keys | Sort-Object) {
        $status = if ($Result.CHECKS.DirectoryStructure[$key]) { "✅" } else { "❌" }
        Write-Host "  $status $key"
    }
    Write-Host ""
    
    Write-Host "System Files:" -ForegroundColor Yellow
    foreach ($key in $Result.CHECKS.SystemFiles.Keys | Sort-Object) {
        $status = if ($Result.CHECKS.SystemFiles[$key]) { "✅" } else { "⚠️" }
        Write-Host "  $status $key"
    }
    Write-Host ""
    
    if ($Result.AVAILABLE_DOCS.Count -gt 0) {
        Write-Host "Available Docs:" -ForegroundColor Yellow
        foreach ($doc in $Result.AVAILABLE_DOCS) {
            Write-Host "  📄 $doc"
        }
        Write-Host ""
    }
    
    if ($Result.ERRORS.Count -gt 0) {
        Write-Host "Errors:" -ForegroundColor Red
        foreach ($err in $Result.ERRORS) {
            Write-Host "  ❌ $err"
        }
    }
    
    Write-Host "========================================" -ForegroundColor Cyan
}
