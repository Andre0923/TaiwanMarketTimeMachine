<#
.SYNOPSIS
    建立新的 Feature 分支與目錄結構
.DESCRIPTION
    自動建立 Feature 分支並初始化必要的 spec.md, plan.md, tasks.md 檔案
.PARAMETER FeatureName
    Feature 名稱（必填）
.PARAMETER FeatureNumber
    Feature 編號（選用，預設自動遞增）
.EXAMPLE
    .\create-new-feature.ps1 -FeatureName "user-authentication"
    .\create-new-feature.ps1 -FeatureName "payment-integration" -FeatureNumber 5
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$FeatureName,
    
    [int]$FeatureNumber = 0
)

# 取得專案根目錄
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Get-Item $ScriptDir).Parent.Parent.Parent.FullName

# 切換到專案根目錄
Push-Location $ProjectRoot

try {
    # 檢查 Git 狀態
    $gitStatus = git status --porcelain 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Not a git repository or git is not available"
        exit 1
    }
    
    if ($gitStatus) {
        Write-Warning "Working directory has uncommitted changes. Please commit or stash them first."
        $continue = Read-Host "Continue anyway? (y/N)"
        if ($continue -ne "y" -and $continue -ne "Y") {
            exit 0
        }
    }
    
    # 決定 Feature 編號
    if ($FeatureNumber -eq 0) {
        $featuresDir = Join-Path $ProjectRoot "specs/features"
        if (Test-Path $featuresDir) {
            $existingFeatures = Get-ChildItem -Path $featuresDir -Directory | 
                Where-Object { $_.Name -match "^\d+-" } |
                ForEach-Object { [int]($_.Name -split "-")[0] } |
                Sort-Object -Descending
            
            if ($existingFeatures.Count -gt 0) {
                $FeatureNumber = $existingFeatures[0] + 1
            } else {
                $FeatureNumber = 1
            }
        } else {
            $FeatureNumber = 1
        }
    }
    
    # 建立目錄名稱
    $featureDirName = "$FeatureNumber-$FeatureName"
    $featurePath = Join-Path $ProjectRoot "specs/features/$featureDirName"
    $branchName = "$FeatureNumber-$FeatureName"
    
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Creating New Feature" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Feature Name:   $FeatureName" -ForegroundColor White
    Write-Host "Feature Number: $FeatureNumber" -ForegroundColor White
    Write-Host "Directory:      specs/features/$featureDirName" -ForegroundColor White
    Write-Host "Branch:         $branchName" -ForegroundColor White
    Write-Host ""
    
    # 確認
    $confirm = Read-Host "Proceed? (Y/n)"
    if ($confirm -eq "n" -or $confirm -eq "N") {
        Write-Host "Cancelled." -ForegroundColor Yellow
        exit 0
    }
    
    # 建立 Git 分支
    Write-Host "Creating git branch..." -ForegroundColor Yellow
    git checkout -b $branchName
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create git branch"
        exit 1
    }
    
    # 建立目錄
    Write-Host "Creating feature directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $featurePath -Force | Out-Null
    New-Item -ItemType Directory -Path "$featurePath/checklists" -Force | Out-Null
    
    # 取得模板
    $specTemplatePath = Join-Path $ProjectRoot ".specify/templates/spec-template.md"
    $planTemplatePath = Join-Path $ProjectRoot ".specify/templates/plan-template.md"
    $tasksTemplatePath = Join-Path $ProjectRoot ".specify/templates/tasks-template.md"
    
    # 建立 spec.md
    if (Test-Path $specTemplatePath) {
        $specContent = Get-Content $specTemplatePath -Raw
        $specContent = $specContent -replace '\{FEATURE_ID\}', $featureDirName
        $specContent = $specContent -replace '\{FEATURE_NAME\}', $FeatureName
        $specContent = $specContent -replace '\{DATE\}', (Get-Date -Format "yyyy-MM-dd")
    } else {
        $specContent = @"
# Feature Specification: $FeatureName

> **Feature ID**: $featureDirName  
> **Status**: Draft  
> **Created**: $(Get-Date -Format "yyyy-MM-dd")  
> **Last Updated**: $(Get-Date -Format "yyyy-MM-dd")

---

## 1. Feature Overview

### 1.1 Problem Statement

<!-- 描述要解決的問題 -->

### 1.2 Goal

<!-- 本 Feature 的目標 -->

### 1.3 Success Criteria

| 指標 | 目標值 | 驗證方式 |
|------|--------|----------|
| - | - | - |

---

## 2. User Stories

### US1: [Story Name]

**As a** [角色]  
**I want** [目標]  
**So that** [價值]

#### Acceptance Criteria

- **AC1 — [標題]**
    - Given [前置條件]
    - When [觸發動作]
    - Then [預期結果]

---

## 3. Assumptions

1. <!-- 假設條件 -->

---

## 4. Dependencies

- <!-- 依賴項目 -->

---

## 5. Out of Scope

1. <!-- 不在範圍內的項目 -->
"@
    }
    Set-Content -Path "$featurePath/spec.md" -Value $specContent -Encoding UTF8
    
    # 建立 plan.md
    if (Test-Path $planTemplatePath) {
        $planContent = Get-Content $planTemplatePath -Raw
        $planContent = $planContent -replace '\{FEATURE_ID\}', $featureDirName
        $planContent = $planContent -replace '\{FEATURE_NAME\}', $FeatureName
        $planContent = $planContent -replace '\{DATE\}', (Get-Date -Format "yyyy-MM-dd")
    } else {
        $planContent = @"
# Implementation Plan: $FeatureName

> **Feature ID**: $featureDirName  
> **Plan Version**: 1.0  
> **Created**: $(Get-Date -Format "yyyy-MM-dd")  
> **Spec Reference**: [spec.md](./spec.md)

---

## 1. Technical Context

<!-- 技術背景與分析 -->

---

## 2. Detailed Design

<!-- 詳細設計 -->

---

## 3. Risk Assessment

| 風險 | 可能性 | 影響 | 緩解措施 |
|------|--------|------|----------|
| - | - | - | - |

---

## 4. Test Strategy

<!-- 測試策略 -->
"@
    }
    Set-Content -Path "$featurePath/plan.md" -Value $planContent -Encoding UTF8
    
    # 建立 tasks.md
    if (Test-Path $tasksTemplatePath) {
        $tasksContent = Get-Content $tasksTemplatePath -Raw
        $tasksContent = $tasksContent -replace '\{FEATURE_ID\}', $featureDirName
        $tasksContent = $tasksContent -replace '\{FEATURE_NAME\}', $FeatureName
        $tasksContent = $tasksContent -replace '\{DATE\}', (Get-Date -Format "yyyy-MM-dd")
    } else {
        $tasksContent = @"
# Tasks: $FeatureName

> **Feature ID**: $featureDirName  
> **Created**: $(Get-Date -Format "yyyy-MM-dd")  
> **Spec Reference**: [spec.md](./spec.md)  
> **Plan Reference**: [plan.md](./plan.md)

---

## Phase 1: Setup

- [ ] T001 [任務描述]

---

## Phase 2: Implementation

- [ ] T002 [US1] [任務描述]

---

## Phase 3: Verification

- [ ] T003 執行測試驗證
"@
    }
    Set-Content -Path "$featurePath/tasks.md" -Value $tasksContent -Encoding UTF8
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Feature Created Successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Created files:" -ForegroundColor Yellow
    Write-Host "  📄 specs/features/$featureDirName/spec.md"
    Write-Host "  📄 specs/features/$featureDirName/plan.md"
    Write-Host "  📄 specs/features/$featureDirName/tasks.md"
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Edit spec.md to define the feature specification"
    Write-Host "  2. Run /speckit.plan to create implementation plan"
    Write-Host "  3. Run /speckit.tasks to generate task list"
    Write-Host ""
    
} finally {
    Pop-Location
}
