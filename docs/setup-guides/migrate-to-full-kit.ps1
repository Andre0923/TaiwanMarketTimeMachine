#!/usr/bin/env pwsh
# SpecKit + FlowKit 完整套件遷移腳本
# 用途：將舊專案升級到完整的 SpecKit + FlowKit 套件
# 使用方式：./migrate-to-full-kit.ps1 -TemplatePath "path/to/template" -TargetPath "path/to/old-project"

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$TemplatePath,
    
    [Parameter(Mandatory=$true)]
    [string]$TargetPath,
    
    [switch]$DryRun,
    [switch]$Force,
    [switch]$SkipBackup
)

$ErrorActionPreference = 'Stop'

# 顏色輸出函式
function Write-Status {
    param([string]$Message, [string]$Level = "INFO")
    $color = switch($Level) {
        "SUCCESS" { "Green" }
        "WARNING" { "Yellow" }
        "ERROR" { "Red" }
        "INFO" { "Cyan" }
        default { "White" }
    }
    Write-Host "[$Level] $Message" -ForegroundColor $color
}

# 檢查路徑
if (-not (Test-Path $TemplatePath)) {
    Write-Status "範本路徑不存在: $TemplatePath" "ERROR"
    exit 1
}

if (-not (Test-Path $TargetPath)) {
    Write-Status "目標專案路徑不存在: $TargetPath" "ERROR"
    exit 1
}

$TemplatePath = (Resolve-Path $TemplatePath).Path
$TargetPath = (Resolve-Path $TargetPath).Path

Write-Status "範本路徑: $TemplatePath" "INFO"
Write-Status "目標路徑: $TargetPath" "INFO"
Write-Status "Dry Run: $DryRun" "INFO"

# 備份
if (-not $SkipBackup -and -not $DryRun) {
    $backupPath = Join-Path $TargetPath ".migration-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Write-Status "建立備份: $backupPath" "INFO"
    New-Item -ItemType Directory -Path $backupPath -Force | Out-Null
}

# Tier 1: 直接覆蓋（無風險）
$tier1Paths = @(
    ".specify/scripts",
    ".specify/templates",
    ".flowkit/templates",
    ".cursor/commands",
    ".github/agents",
    ".github/prompts"
)

Write-Status "`n=== Tier 1: 直接覆蓋 ===" "INFO"
foreach ($path in $tier1Paths) {
    $sourcePath = Join-Path $TemplatePath $path
    $destPath = Join-Path $TargetPath $path
    
    if (Test-Path $sourcePath) {
        if ($DryRun) {
            Write-Status "[DRY RUN] 將覆蓋: $path" "INFO"
        } else {
            # 備份舊版（如果存在）
            if ((Test-Path $destPath) -and -not $SkipBackup) {
                $backupDest = Join-Path $backupPath $path
                Write-Status "  備份: $path" "WARNING"
                Copy-Item -Path $destPath -Destination $backupDest -Recurse -Force
            }
            
            # 覆蓋
            Write-Status "  覆蓋: $path" "SUCCESS"
            if (Test-Path $destPath) {
                Remove-Item -Path $destPath -Recurse -Force
            }
            Copy-Item -Path $sourcePath -Destination $destPath -Recurse -Force
        }
    } else {
        Write-Status "  [跳過] 範本中不存在: $path" "WARNING"
    }
}

# Tier 2: 選擇性覆蓋（需檢查）
$tier2Files = @(
    @{Path="docs/00.目錄結構.md"; Action="覆蓋"; Reason="標準化"},
    @{Path="docs/77.flowkit相關文件"; Action="覆蓋"; Reason="FlowKit 文件"},
    @{Path="docs/76.改版歷史"; Action="覆蓋"; Reason="套件改版歷史"}
)

Write-Status "`n=== Tier 2: 選擇性覆蓋 ===" "INFO"
foreach ($item in $tier2Files) {
    $sourcePath = Join-Path $TemplatePath $item.Path
    $destPath = Join-Path $TargetPath $item.Path
    
    if (Test-Path $sourcePath) {
        if ($DryRun) {
            Write-Status "[DRY RUN] 將$($item.Action): $($item.Path) - $($item.Reason)" "INFO"
        } else {
            if ((Test-Path $destPath) -and -not $SkipBackup) {
                $backupDest = Join-Path $backupPath $item.Path
                Write-Status "  備份: $($item.Path)" "WARNING"
                Copy-Item -Path $destPath -Destination $backupDest -Recurse -Force
            }
            
            Write-Status "  $($item.Action): $($item.Path) - $($item.Reason)" "SUCCESS"
            if (Test-Path $destPath) {
                Remove-Item -Path $destPath -Recurse -Force
            }
            Copy-Item -Path $sourcePath -Destination $destPath -Recurse -Force
        }
    }
}

# Tier 2.5: copilot-instructions.md（特殊處理）
Write-Status "`n=== Tier 2.5: copilot-instructions.md ===" "INFO"
$copilotSource = Join-Path $TemplatePath ".github/copilot-instructions.md"
$copilotDest = Join-Path $TargetPath ".github/copilot-instructions.md"

if (Test-Path $copilotSource) {
    if (Test-Path $copilotDest) {
        if ($Force) {
            if ($DryRun) {
                Write-Status "[DRY RUN] 將強制覆蓋: .github/copilot-instructions.md" "WARNING"
            } else {
                if (-not $SkipBackup) {
                    $backupDest = Join-Path $backupPath ".github/copilot-instructions.md"
                    Copy-Item -Path $copilotDest -Destination $backupDest -Force
                }
                Copy-Item -Path $copilotSource -Destination $copilotDest -Force
                Write-Status "  強制覆蓋: .github/copilot-instructions.md" "SUCCESS"
            }
        } else {
            Write-Status "  [跳過] 已存在，使用 -Force 強制覆蓋" "WARNING"
            Write-Status "  建議手動比對：" "INFO"
            Write-Status "    範本: $copilotSource" "INFO"
            Write-Status "    專案: $copilotDest" "INFO"
        }
    } else {
        if ($DryRun) {
            Write-Status "[DRY RUN] 將建立: .github/copilot-instructions.md" "INFO"
        } else {
            Copy-Item -Path $copilotSource -Destination $copilotDest -Force
            Write-Status "  建立: .github/copilot-instructions.md" "SUCCESS"
        }
    }
}

# Tier 3: 需要重建的檔案
Write-Status "`n=== Tier 3: 需要重建的 AI 記憶檔案 ===" "WARNING"
$memoryFiles = @(
    ".flowkit/memory/system-context.md",
    ".flowkit/memory/system-context-index.md"
)

foreach ($file in $memoryFiles) {
    $destPath = Join-Path $TargetPath $file
    if (Test-Path $destPath) {
        Write-Status "  發現現有檔案: $file" "WARNING"
        if ($Force) {
            if ($DryRun) {
                Write-Status "  [DRY RUN] 將刪除（需重建）: $file" "WARNING"
            } else {
                if (-not $SkipBackup) {
                    $backupDest = Join-Path $backupPath $file
                    Copy-Item -Path $destPath -Destination $backupDest -Force
                }
                Remove-Item -Path $destPath -Force
                Write-Status "  已刪除（需重建）: $file" "SUCCESS"
            }
        } else {
            Write-Status "  [保留] 使用 -Force 刪除並重建" "INFO"
        }
    } else {
        Write-Status "  不存在，執行 /flowkit.system-context 建立" "INFO"
    }
}

# 憲法檔案特殊處理
Write-Status "`n=== Tier 3: Constitution 檔案 ===" "WARNING"
$constitutionSource = Join-Path $TemplatePath ".specify/memory/constitution.md"
$constitutionDest = Join-Path $TargetPath ".specify/memory/constitution.md"

if (Test-Path $constitutionDest) {
    Write-Status "  發現現有 constitution.md" "WARNING"
    Write-Status "  建議手動比對並合併客製化規則" "INFO"
    Write-Status "    範本: $constitutionSource" "INFO"
    Write-Status "    專案: $constitutionDest" "INFO"
} else {
    if ($DryRun) {
        Write-Status "[DRY RUN] 將複製範本 constitution.md" "INFO"
    } else {
        $destDir = Split-Path $constitutionDest -Parent
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        Copy-Item -Path $constitutionSource -Destination $constitutionDest -Force
        Write-Status "  已建立: constitution.md" "SUCCESS"
    }
}

# 摘要報告
Write-Status "`n=== 遷移摘要 ===" "SUCCESS"
Write-Status "範本路徑: $TemplatePath" "INFO"
Write-Status "目標路徑: $TargetPath" "INFO"
Write-Status "Dry Run: $DryRun" "INFO"

if (-not $DryRun) {
    if (-not $SkipBackup) {
        Write-Status "備份位置: $backupPath" "INFO"
    }
    
    Write-Status "`n下一步操作：" "INFO"
    Write-Status "1. 檢查 .github/copilot-instructions.md 是否需要手動合併" "INFO"
    Write-Status "2. 檢查 .specify/memory/constitution.md 客製化規則" "INFO"
    Write-Status "3. 刪除 .flowkit/memory/*.md 後執行 /flowkit.system-context 重建" "INFO"
    Write-Status "4. 執行 git diff 檢查所有變更" "INFO"
    Write-Status "5. 提交變更: git add . && git commit -m 'chore: 升級至完整 SpecKit + FlowKit 套件'" "INFO"
} else {
    Write-Status "`n移除 -DryRun 參數以實際執行遷移" "WARNING"
}

Write-Status "`n✅ 遷移腳本執行完成" "SUCCESS"
