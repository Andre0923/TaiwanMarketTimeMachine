#!/usr/bin/env pwsh
# SpecKit + FlowKit 完整套件遷移腳本
# 用途：將舊專案升級到完整的 SpecKit + FlowKit 套件
# 使用方式：./migrate-to-full-kit.ps1 -TemplatePath "path/to/template" -TargetPath "path/to/old-project"
# 編碼：UTF-8 with BOM（支援繁體中文路徑）

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

# 設定輸出編碼為 UTF-8（支援繁體中文）
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

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

# 重試機制函式（處理 Dropbox 等雲端同步導致的檔案占用問題）
function Invoke-WithRetry {
    param(
        [Parameter(Mandatory=$true)]
        [scriptblock]$ScriptBlock,
        
        [int]$MaxRetries = 3,
        [int]$RetryDelaySeconds = 2,
        [string]$OperationName = "操作"
    )
    
    $attempt = 0
    $success = $false
    
    while (-not $success -and $attempt -lt $MaxRetries) {
        $attempt++
        try {
            & $ScriptBlock
            $success = $true
        }
        catch {
            if ($attempt -lt $MaxRetries) {
                Write-Status "  ⚠️ $OperationName 失敗（嘗試 $attempt/$MaxRetries）: $($_.Exception.Message)" "WARNING"
                Write-Status "  ⏳ 等待 $RetryDelaySeconds 秒後重試..." "INFO"
                Start-Sleep -Seconds $RetryDelaySeconds
            }
            else {
                Write-Status "  ❌ $OperationName 失敗，已達最大重試次數（$MaxRetries 次）" "ERROR"
                throw
            }
        }
    }
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

# Step 0: 同步遷移工具（先行執行）
# ⚠️ MUST 在所有其他步驟之前完成 — 確保目標專案日後升級可使用最新版本的遷移文件與腳本
Write-Status "`n=== Step 0: 同步遷移工具（先行執行）===" "INFO"

$step0Files = @(
    @{Source="docs/setup-guides/migration-guide.md";    Dest="docs/setup-guides/migration-guide.md";    Reason="完整遷移指南"},
    @{Source="docs/setup-guides/migration-quick-ref.md"; Dest="docs/setup-guides/migration-quick-ref.md"; Reason="遷移快速參考"},
    @{Source="docs/setup-guides/migrate-to-full-kit.ps1"; Dest="docs/setup-guides/migrate-to-full-kit.ps1"; Reason="遷移腳本"}
)

foreach ($item in $step0Files) {
    $sourcePath = Join-Path $TemplatePath $item.Source
    $destPath   = Join-Path $TargetPath   $item.Dest

    if (Test-Path $sourcePath) {
        $destDir = Split-Path $destPath -Parent
        if ($DryRun) {
            Write-Status "[DRY RUN] 將同步遷移工具: $($item.Source) - $($item.Reason)" "INFO"
        } else {
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            if ((Test-Path $destPath) -and -not $SkipBackup) {
                $backupDest = Join-Path $backupPath $item.Source
                $backupDir  = Split-Path $backupDest -Parent
                New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
                Copy-Item -Path $destPath -Destination $backupDest -Force
            }
            Copy-Item -Path $sourcePath -Destination $destPath -Force
            Write-Status "  ✅ 同步遷移工具: $($item.Dest) ($($item.Reason))" "SUCCESS"
        }
    } else {
        Write-Status "  [跳過] 範本中不存在: $($item.Source)" "WARNING"
    }
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
            Invoke-WithRetry -OperationName "移除舊檔案 $path" -ScriptBlock {
                if (Test-Path $destPath) {
                    Remove-Item -Path $destPath -Recurse -Force
                }
            }
            Invoke-WithRetry -OperationName "複製檔案 $path" -ScriptBlock {
                Copy-Item -Path $sourcePath -Destination $destPath -Recurse -Force
            }
        }
    } else {
        Write-Status "  [跳過] 範本中不存在: $path" "WARNING"
    }
}

# Tier 1.5: 範本檔案複製（需求文件範本 + 開發人員文件）
Write-Status "`n=== Tier 1.5: 範本檔案與開發人員文件 ===" "INFO"

# 需求文件範本
$templateFiles = @(
    @{Source="docs/requirements/Milestone/MNN-MilestoneName-template.md"; Dest="docs/requirements/Milestone/MNN-MilestoneName-template.md"; Reason="Milestone 範本"},
    @{Source="docs/requirements/user-stories/README-template.md"; Dest="docs/requirements/user-stories/README-template.md"; Reason="User Stories README 範本"},
    @{Source="docs/requirements/user-stories/US-X-GroupName-template.md"; Dest="docs/requirements/user-stories/US-X-GroupName-template.md"; Reason="User Stories 範本"}
)

foreach ($item in $templateFiles) {
    $sourcePath = Join-Path $TemplatePath $item.Source
    $destPath = Join-Path $TargetPath $item.Dest
    
    if (Test-Path $sourcePath) {
        $destDir = Split-Path $destPath -Parent
        if (-not (Test-Path $destDir)) {
            if ($DryRun) {
                Write-Status "[DRY RUN] 將建立目錄: $destDir" "INFO"
            } else {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
        }
        
        if ($DryRun) {
            Write-Status "[DRY RUN] 將複製範本: $($item.Source) - $($item.Reason)" "INFO"
        } else {
            Copy-Item -Path $sourcePath -Destination $destPath -Force
            Write-Status "  複製範本: $($item.Dest) - $($item.Reason)" "SUCCESS"
        }
    } else {
        Write-Status "  [跳過] 範本中不存在: $($item.Source)" "WARNING"
    }
}

# 開發人員文件（整個目錄複製）
$devDocSource = Join-Path $TemplatePath "docs/01.開發人員doc"
$devDocDest = Join-Path $TargetPath "docs/01.開發人員doc"

if (Test-Path $devDocSource) {
    if ($DryRun) {
        Write-Status "[DRY RUN] 將複製開發人員文件: docs/01.開發人員doc" "INFO"
    } else {
        if (-not (Test-Path $devDocDest)) {
            New-Item -ItemType Directory -Path $devDocDest -Force | Out-Null
        }
        Get-ChildItem -Path $devDocSource -File | ForEach-Object {
            Copy-Item -Path $_.FullName -Destination $devDocDest -Force
            Write-Status "  複製: docs/01.開發人員doc/$($_.Name)" "SUCCESS"
        }
    }
} else {
    Write-Status "  [跳過] 範本中不存在: docs/01.開發人員doc" "WARNING"
}

# Migration 相關文件已在 Step 0（先行執行）同步，此處跳過
Write-Status "  [跳過] 遷移工具文件已於 Step 0 同步完成" "INFO"

# .flowkit/version-manifest.md（檔式：不存在時建立，已存在時提示比對）
Write-Status "`n=== Tier 1.5: .flowkit/version-manifest.md ===" "INFO"

$versionManifestSource = Join-Path $TemplatePath ".flowkit/version-manifest.md"
$versionManifestDest   = Join-Path $TargetPath   ".flowkit/version-manifest.md"

if (Test-Path $versionManifestSource) {
    if (Test-Path $versionManifestDest) {
        if ($DryRun) {
            Write-Status "  [DRY RUN] .flowkit/version-manifest.md 已存在，將提示比對" "INFO"
        } else {
            Write-Status "  ⛏️ .flowkit/version-manifest.md 已存在" "WARNING"
            Write-Status "  建議比對版號同步狀態：code --diff `"$versionManifestSource`" `"$versionManifestDest`"" "INFO"
        }
    } else {
        if ($DryRun) {
            Write-Status "  [DRY RUN] 將建立: .flowkit/version-manifest.md" "INFO"
        } else {
            $destDir = Split-Path $versionManifestDest -Parent
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            Copy-Item -Path $versionManifestSource -Destination $versionManifestDest -Force
            Write-Status "  ✅ 建立: .flowkit/version-manifest.md（指令版號追蹤清單）" "SUCCESS"
        }
    }
}

# Tier 2: 選擇性覆蓋（需檢查）
$tier2Files = @(
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
            Invoke-WithRetry -OperationName "移除舊檔案 $($item.Path)" -ScriptBlock {
                if (Test-Path $destPath) {
                    Remove-Item -Path $destPath -Recurse -Force
                }
            }
            Invoke-WithRetry -OperationName "複製檔案 $($item.Path)" -ScriptBlock {
                Copy-Item -Path $sourcePath -Destination $destPath -Recurse -Force
            }
        }
    }
}

# Tier 2.5: 智慧比對檔案（需手動判斷）
Write-Status "`n=== Tier 2.5: 智慧比對檔案 ===" "INFO"

# tests/conftest.py（測試基礎設施：marker 註冊、慢測試自動偵測）
# 注意：tests/ 通常🚫絕不覆蓋，但 conftest.py 是範本基礎設施，非專案測試
$conftestSource = Join-Path $TemplatePath "tests/conftest.py"
$conftestDest = Join-Path $TargetPath "tests/conftest.py"

if (Test-Path $conftestSource) {
    if (Test-Path $conftestDest) {
        if ($Force) {
            if ($DryRun) {
                Write-Status "[DRY RUN] 將強制覆蓋: tests/conftest.py" "WARNING"
            } else {
                if (-not $SkipBackup) {
                    $backupDest = Join-Path $backupPath "tests/conftest.py"
                    $backupDir = Split-Path $backupDest -Parent
                    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
                    Copy-Item -Path $conftestDest -Destination $backupDest -Force
                }
                Copy-Item -Path $conftestSource -Destination $conftestDest -Force
                Write-Status "  強制覆蓋: tests/conftest.py" "SUCCESS"
            }
        } else {
            Write-Status "  ⚗️ tests/conftest.py 已存在（測試基礎設施，包含 marker 註冊與慢測試自動偵測）" "WARNING"
            Write-Status "  建議手動比對：code --diff `"$conftestSource`" `"$conftestDest`"" "INFO"
        }
    } else {
        if ($DryRun) {
            Write-Status "[DRY RUN] 將建立: tests/conftest.py（含 slow/serial marker 註冊）" "INFO"
        } else {
            $destDir = Split-Path $conftestDest -Parent
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            Copy-Item -Path $conftestSource -Destination $conftestDest -Force
            Write-Status "  建立: tests/conftest.py（測試基礎設施）" "SUCCESS"
        }
    }
}

# 測試依賴檢查：確認 pytest-xdist 已安裝
$targetPyproject = Join-Path $TargetPath "pyproject.toml"
if (Test-Path $targetPyproject) {
    $pyprojectContent = Get-Content $targetPyproject -Raw -Encoding UTF8
    if ($pyprojectContent -notmatch "pytest-xdist") {
        Write-Status "  ⚠️ pyproject.toml 缺少 pytest-xdist 依賴（並行測試必備）" "WARNING"
        Write-Status "  建議執行：cd `"$TargetPath`" && uv add pytest-xdist" "INFO"
    } else {
        Write-Status "  ✅ pytest-xdist 依賴已存在" "SUCCESS"
    }
}

# docs/00.目錄結構.md（每個專案結構不同，需手動比對）
$dirStructureSource = Join-Path $TemplatePath "docs/00.目錄結構.md"
$dirStructureDest = Join-Path $TargetPath "docs/00.目錄結構.md"

if (Test-Path $dirStructureSource) {
    if (Test-Path $dirStructureDest) {
        if ($Force) {
            if ($DryRun) {
                Write-Status "[DRY RUN] 將強制覆蓋: docs/00.目錄結構.md" "WARNING"
            } else {
                if (-not $SkipBackup) {
                    $backupDest = Join-Path $backupPath "docs/00.目錄結構.md"
                    $backupDir = Split-Path $backupDest -Parent
                    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
                    Copy-Item -Path $dirStructureDest -Destination $backupDest -Force
                }
                Copy-Item -Path $dirStructureSource -Destination $dirStructureDest -Force
                Write-Status "  強制覆蓋: docs/00.目錄結構.md" "SUCCESS"
            }
        } else {
            Write-Status "  ⚗️ docs/00.目錄結構.md 已存在，每個專案結構不同" "WARNING"
            Write-Status "  建議手動比對：code --diff `"$dirStructureSource`" `"$dirStructureDest`"" "INFO"
        }
    } else {
        if ($DryRun) {
            Write-Status "[DRY RUN] 將建立: docs/00.目錄結構.md" "INFO"
        } else {
            $destDir = Split-Path $dirStructureDest -Parent
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            Copy-Item -Path $dirStructureSource -Destination $dirStructureDest -Force
            Write-Status "  建立: docs/00.目錄結構.md" "SUCCESS"
        }
    }
}

# docs/technical-debt.md（智慧判斷：不存在→建立，已存在→提示比對）
$tdSource = Join-Path $TemplatePath "docs/technical-debt.md"
$tdDest = Join-Path $TargetPath "docs/technical-debt.md"

if (Test-Path $tdSource) {
    if (Test-Path $tdDest) {
        Write-Status "  ⚗️ docs/technical-debt.md 已存在，建議手動比對範本是否有新欄位或規則" "WARNING"
        Write-Status "  建議比對：code --diff `"$tdSource`" `"$tdDest`"" "INFO"
    } else {
        if ($DryRun) {
            Write-Status "[DRY RUN] 將建立: docs/technical-debt.md" "INFO"
        } else {
            Copy-Item -Path $tdSource -Destination $tdDest -Force
            Write-Status "  建立: docs/technical-debt.md（TD Registry 範本）" "SUCCESS"
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
Write-Status "`n=== Tier 3: Constitution 檔案（🔴 重要）===" "WARNING"
$constitutionSource = Join-Path $TemplatePath ".specify/memory/constitution.md"
$constitutionDest = Join-Path $TargetPath ".specify/memory/constitution.md"

Write-Status "  ⚠️ 範本中的 constitution.md 是「刻意製造的精簡優化版」" "WARNING"
Write-Status "  ⚠️ 舊版本較長不代表較完整，AI 常因此誤判而拒絕更新" "WARNING"

if (Test-Path $constitutionDest) {
    Write-Status "  發現現有 constitution.md" "WARNING"
    if ($Force) {
        if ($DryRun) {
            Write-Status "[DRY RUN] 將強制覆蓋: constitution.md（使用範本精簡版）" "WARNING"
        } else {
            if (-not $SkipBackup) {
                $backupDest = Join-Path $backupPath ".specify/memory/constitution.md"
                $backupDir = Split-Path $backupDest -Parent
                New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
                Copy-Item -Path $constitutionDest -Destination $backupDest -Force
                Write-Status "  已備份舊版 constitution.md" "INFO"
            }
            $destDir = Split-Path $constitutionDest -Parent
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            Copy-Item -Path $constitutionSource -Destination $constitutionDest -Force
            Write-Status "  ✅ 已強制覆蓋為範本版本（精簡優化版）" "SUCCESS"
            Write-Status "  💡 請手動補回客製化規則（若有）" "INFO"
        }
    } else {
        Write-Status "  🔴 建議：使用 -Force 強制覆蓋為範本版本" "WARNING"
        Write-Status "  💡 範本版本是精簡優化版，舊版較長不代表較完整" "INFO"
        Write-Status "    範本: $constitutionSource" "INFO"
        Write-Status "    專案: $constitutionDest" "INFO"
    }
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
    Write-Status "0. ✅ Step 0 已完成：遷移工具（migration-guide.md / migration-quick-ref.md / migrate-to-full-kit.ps1）已同步至目標專案" "SUCCESS"
    Write-Status "1. 檢查 .github/copilot-instructions.md 是否需要手動合併" "INFO"
    Write-Status "2. 🔴 確認 constitution.md 已使用範本版本（精簡優化版）" "WARNING"
    Write-Status "   → 舊版較長不代表較完整，請勿保留舊版" "WARNING"
    Write-Status "   → 手動補回客製化規則（若有）" "INFO"
    Write-Status "3. ⚗️ 比對 docs/00.目錄結構.md（每個專案結構不同，需手動合併）" "WARNING"
    Write-Status "4. ⚗️ 比對 docs/technical-debt.md（確認範本規則已涵蓋）" "WARNING"
    Write-Status "5. ⚗️ 比對 tests/conftest.py（測試基礎設施：marker 註冊與慢測試自動偵測）" "WARNING"
    Write-Status "6. 🟡 確認 pytest-xdist 依賴已安裝（並行測試必備）" "WARNING"
    Write-Status "   → 若缺少：uv add pytest-xdist" "INFO"
    Write-Status "7. .flowkit/version-manifest.md 與 .flowkit/memory/ 已處理（見上方 Tier 1.5 / Tier 3 輸出）" "SUCCESS"
    Write-Status "   → 若 .flowkit/memory/ 已複製初始記憶，仍建議執行 /flowkit.system-context 重新產生符合本專案的內容" "INFO"
    Write-Status "8. 🟡 驗證 FlowKit 指令化已更新（不要只更新 SpecKit）" "WARNING"
    Write-Status "   → 檢查 .cursor/commands/flowkit.* 和 .github/agents/flowkit.*" "INFO"
    Write-Status "9. 執行 git diff 檢查所有變更" "INFO"
    Write-Status "10. 提交變更: git add . && git commit -m 'chore: 升級至完整 SpecKit + FlowKit 套件'" "INFO"
    Write-Status "`n📁 目錄結構調整建議（參考 docs/00.目錄結構.md）：" "INFO"
    Write-Status "   → 確保 tests/ 目錄存在且對應 src/ 結構" "INFO"
    Write-Status "   → 確保 logs/ 目錄存在，日誌不應散落在專案根目錄" "INFO"
    Write-Status "   → 建立 .artifacts/ 存放 coverage、build 等可再生產物" "INFO"
    Write-Status "   → 將 .artifacts/ 加入 .gitignore" "INFO"
} else {
    Write-Status "`n移除 -DryRun 參數以實際執行遷移" "WARNING"
}

Write-Status "`n✅ 遷移腳本執行完成" "SUCCESS"
