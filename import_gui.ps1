# Local Windows Forms file picker; Python handles validation and import.
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[System.Windows.Forms.Application]::EnableVisualStyles()
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$OutputEncoding = [Console]::OutputEncoding
$taskToolRoot = $PSScriptRoot
$taskBridgeScript = Join-Path $taskToolRoot 'bridge.py'
# AIKG_PYTHON can select any local Python executable; otherwise use an optional
# Codex-bundled runtime or the standard Python Launcher/PATH discovery below.
$taskPython = $env:AIKG_PYTHON
if (-not $taskPython) {
    $taskPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
}
$taskPythonPrefix = @()
if (-not (Test-Path -LiteralPath $taskPython)) {
    $taskPythonCommand = Get-Command py -ErrorAction SilentlyContinue
    if ($taskPythonCommand) { $taskPython = $taskPythonCommand.Source; $taskPythonPrefix = @('-3') }
    else {
        $taskPythonCommand = Get-Command python -ErrorAction SilentlyContinue
        if ($taskPythonCommand) { $taskPython = $taskPythonCommand.Source }
        else { [System.Windows.Forms.MessageBox]::Show('未找到 Python 3.10+。请安装后重试。','无法启动'); exit 1 }
    }
}
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8 = '1'
$taskSettings = Join-Path $taskToolRoot 'settings.json'
$taskDefaultVault = Join-Path $taskToolRoot 'examples\demo-vault'
if (Test-Path -LiteralPath $taskSettings) {
    try { $taskDefaultVault = (Get-Content -LiteralPath $taskSettings -Raw -Encoding UTF8 | ConvertFrom-Json).vault } catch {}
}
$taskForm = New-Object System.Windows.Forms.Form
$taskForm.Text = 'AI Knowledge Bridge — 本地导入'
$taskForm.Size = New-Object System.Drawing.Size(880,650)
$taskForm.StartPosition = 'CenterScreen'
$taskForm.Font = New-Object System.Drawing.Font('Microsoft YaHei UI',10)
$taskHeader = New-Object System.Windows.Forms.Label
$taskHeader.Text = '选择 JSON → 选择仓库 → 检查并预览 → 导入'
$taskHeader.SetBounds(20,15,820,30)
$taskForm.Controls.Add($taskHeader)
$taskJsonLabel = New-Object System.Windows.Forms.Label
$taskJsonLabel.Text = 'JSON 文件'; $taskJsonLabel.SetBounds(20,60,145,25); $taskForm.Controls.Add($taskJsonLabel)
$taskJson = New-Object System.Windows.Forms.TextBox
$taskJson.SetBounds(170,55,570,30); $taskForm.Controls.Add($taskJson)
$taskPickJson = New-Object System.Windows.Forms.Button
$taskPickJson.Text = '选择…'; $taskPickJson.SetBounds(750,55,90,32); $taskForm.Controls.Add($taskPickJson)
$taskVaultLabel = New-Object System.Windows.Forms.Label
$taskVaultLabel.Text = 'Obsidian 仓库'; $taskVaultLabel.SetBounds(20,108,145,25); $taskForm.Controls.Add($taskVaultLabel)
$taskVault = New-Object System.Windows.Forms.TextBox
$taskVault.SetBounds(170,103,570,30); $taskVault.Text = $taskDefaultVault; $taskForm.Controls.Add($taskVault)
$taskPickVault = New-Object System.Windows.Forms.Button
$taskPickVault.Text = '选择…'; $taskPickVault.SetBounds(750,103,90,32); $taskForm.Controls.Add($taskPickVault)
$taskHint = New-Object System.Windows.Forms.Label
$taskHint.Text = '正文默认追加；保留手写区、已有节点位置；写入前备份。所有处理均在本地。'
$taskHint.SetBounds(20,150,820,35); $taskForm.Controls.Add($taskHint)
$taskOutput = New-Object System.Windows.Forms.TextBox
$taskOutput.Multiline = $true; $taskOutput.ReadOnly = $true; $taskOutput.ScrollBars = 'Vertical'
$taskOutput.SetBounds(20,190,820,340); $taskOutput.Anchor = 'Top,Bottom,Left,Right'; $taskForm.Controls.Add($taskOutput)
$taskPreview = New-Object System.Windows.Forms.Button
$taskPreview.Text = '检查并预览'; $taskPreview.SetBounds(20,550,150,38); $taskPreview.Anchor = 'Bottom,Left'; $taskForm.Controls.Add($taskPreview)
$taskApply = New-Object System.Windows.Forms.Button
$taskApply.Text = '导入到仓库'; $taskApply.SetBounds(190,550,150,38); $taskApply.Anchor = 'Bottom,Left'; $taskApply.Enabled = $false; $taskForm.Controls.Add($taskApply)
$taskQueryButton = New-Object System.Windows.Forms.Button
$taskQueryButton.Text = '生成节点追问…'; $taskQueryButton.SetBounds(630,550,210,38); $taskQueryButton.Anchor = 'Bottom,Right'; $taskForm.Controls.Add($taskQueryButton)
$taskReverse = New-Object System.Windows.Forms.CheckBox
$taskReverse.Text = '保留已审阅的反向候选'; $taskReverse.SetBounds(365,558,255,28); $taskReverse.Anchor = 'Bottom,Left'; $taskForm.Controls.Add($taskReverse)
$taskState = @{ hash = ''; preview = ''; vault = '' }
$taskJson.Add_TextChanged({ $taskApply.Enabled = $false })
$taskVault.Add_TextChanged({ $taskApply.Enabled = $false })
$taskReverse.Add_CheckedChanged({ $taskApply.Enabled = $false })
$taskPickJson.Add_Click({
    $taskDialog = New-Object System.Windows.Forms.OpenFileDialog
    $taskDialog.Filter = 'JSON 或文本 (*.json;*.txt)|*.json;*.txt|所有文件 (*.*)|*.*'
    if ($taskDialog.ShowDialog() -eq 'OK') { $taskJson.Text = $taskDialog.FileName }
    $taskDialog.Dispose()
})
$taskPickVault.Add_Click({
    $taskDialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $taskDialog.Description = '选择 Obsidian 仓库根目录（含 Concepts、Canvas）'
    if (Test-Path -LiteralPath $taskVault.Text) { $taskDialog.SelectedPath = $taskVault.Text }
    if ($taskDialog.ShowDialog() -eq 'OK') { $taskVault.Text = $taskDialog.SelectedPath }
    $taskDialog.Dispose()
})
function Invoke-TaskBridge([bool]$taskDoApply) {
    $taskArgs = @($taskPythonPrefix) + @($taskBridgeScript, $taskJson.Text, '--vault', $taskVault.Text)
    if ($taskDoApply) { $taskArgs += '--apply' }
    if ($taskReverse.Checked) { $taskArgs += '--allow-reverse' }
    $taskResult = & $taskPython @taskArgs 2>&1
    $taskCode = $LASTEXITCODE
    $taskText = ($taskResult | ForEach-Object { $_.ToString() }) -join [Environment]::NewLine
    return @{ code=$taskCode; text=$taskText }
}
$taskPreview.Add_Click({
    try {
        $taskForm.UseWaitCursor = $true; $taskApply.Enabled = $false
        $taskResult = Invoke-TaskBridge $false; $taskOutput.Text = $taskResult.text
        if ($taskResult.code -eq 0) {
            $taskState.hash = (Get-FileHash -LiteralPath $taskJson.Text -Algorithm SHA256).Hash
            $taskState.vault = $taskVault.Text; $taskState.preview = $taskResult.text
            $taskApply.Enabled = $taskResult.text -notmatch '这批 JSON 已导入'
        }
    } catch { $taskOutput.Text = $_.Exception.Message }
    finally { $taskForm.UseWaitCursor = $false }
})
$taskApply.Add_Click({
    try {
        $taskForm.UseWaitCursor = $true
        if ($taskState.hash -ne (Get-FileHash -LiteralPath $taskJson.Text -Algorithm SHA256).Hash -or $taskState.vault -ne $taskVault.Text) { throw '文件或仓库已改变，请重新预览。' }
        $taskFresh = Invoke-TaskBridge $false
        if ($taskFresh.code -ne 0 -or $taskFresh.text -ne $taskState.preview) { $taskOutput.Text = $taskFresh.text; throw '导入预览发生变化，请重新检查并预览。' }
        $taskResult = Invoke-TaskBridge $true; $taskOutput.Text = $taskResult.text
        if ($taskResult.code -eq 0) {
            try { @{vault=$taskVault.Text} | ConvertTo-Json | Set-Content -LiteralPath $taskSettings -Encoding UTF8 } catch {}
            [System.Windows.Forms.MessageBox]::Show('导入完成。重新打开 Canvas；若新节点显示未找到，请重启 Obsidian 刷新索引。','完成') | Out-Null
        }
    } catch { $taskOutput.AppendText([Environment]::NewLine + $_.Exception.Message) }
    finally { $taskApply.Enabled = $false; $taskForm.UseWaitCursor = $false }
})
$taskQueryButton.Add_Click({
    try {
        $taskGraphFile = Join-Path $taskVault.Text '_AIKG\graph.json'
        $taskLocalGraph = Get-Content -LiteralPath $taskGraphFile -Raw -Encoding UTF8 | ConvertFrom-Json
        $taskQueryForm = New-Object System.Windows.Forms.Form
        $taskQueryForm.Text = '节点与一跳上下文 → 追问文件'
        $taskQueryForm.Size = New-Object System.Drawing.Size(780,630)
        $taskQueryForm.StartPosition = 'CenterParent'; $taskQueryForm.Font = $taskForm.Font
        $taskChooseNode = New-Object System.Windows.Forms.ComboBox
        $taskChooseNode.DropDownStyle = 'DropDownList'; $taskChooseNode.SetBounds(20,20,720,35)
        foreach ($taskNode in $taskLocalGraph.nodes) { [void]$taskChooseNode.Items.Add($taskNode.id + ' | ' + $taskNode.name) }
        if ($taskChooseNode.Items.Count -gt 0) { $taskChooseNode.SelectedIndex = 0 }
        $taskQueryForm.Controls.Add($taskChooseNode)
        $taskQuestionLabel = New-Object System.Windows.Forms.Label
        $taskQuestionLabel.Text = '写出你不理解的地方，可以粘贴节点中的公式或段落：'; $taskQuestionLabel.SetBounds(20,65,720,30); $taskQueryForm.Controls.Add($taskQuestionLabel)
        $taskQuestionBox = New-Object System.Windows.Forms.TextBox
        $taskQuestionBox.Multiline = $true; $taskQuestionBox.ScrollBars = 'Vertical'; $taskQuestionBox.SetBounds(20,100,720,130); $taskQueryForm.Controls.Add($taskQuestionBox)
        $taskPromptBox = New-Object System.Windows.Forms.TextBox
        $taskPromptBox.Multiline = $true; $taskPromptBox.ReadOnly = $true; $taskPromptBox.ScrollBars = 'Vertical'; $taskPromptBox.SetBounds(20,290,720,230); $taskQueryForm.Controls.Add($taskPromptBox)
        $taskGenerate = New-Object System.Windows.Forms.Button
        $taskGenerate.Text = '生成追问文件'; $taskGenerate.SetBounds(20,245,170,35); $taskQueryForm.Controls.Add($taskGenerate)
        $taskCopy = New-Object System.Windows.Forms.Button
        $taskCopy.Text = '复制提示词'; $taskCopy.Enabled = $false; $taskCopy.SetBounds(20,540,170,35); $taskQueryForm.Controls.Add($taskCopy)
        $taskGenerate.Add_Click({
            try {
                if (-not $taskChooseNode.SelectedItem) { throw '仓库没有可选择的节点。' }
                $taskSelectedId = $taskChooseNode.SelectedItem.ToString().Split('|')[0].Trim()
                $taskQueryArgs = @($taskPythonPrefix) + @((Join-Path $taskToolRoot 'query_builder.py'), $taskSelectedId, '--vault', $taskVault.Text, '--question', $taskQuestionBox.Text, '--json')
                $taskQueryResult = & $taskPython @taskQueryArgs 2>&1
                if ($LASTEXITCODE -ne 0) { throw (($taskQueryResult | ForEach-Object { $_.ToString() }) -join [Environment]::NewLine) }
                $taskQueryFiles = ($taskQueryResult -join '') | ConvertFrom-Json
                $taskPromptBox.Text = Get-Content -LiteralPath $taskQueryFiles.prompt_file -Raw -Encoding UTF8
                $taskCopy.Enabled = $true
                $taskQueryForm.Text = '已生成：' + [System.IO.Path]::GetFileName($taskQueryFiles.prompt_file)
            } catch { $taskPromptBox.Text = $_.Exception.Message; $taskCopy.Enabled = $false }
        }.GetNewClosure())
        $taskCopy.Add_Click({ if ($taskPromptBox.Text) { [System.Windows.Forms.Clipboard]::SetText($taskPromptBox.Text) } }.GetNewClosure())
        [void]$taskQueryForm.ShowDialog($taskForm); $taskQueryForm.Dispose()
    } catch { [System.Windows.Forms.MessageBox]::Show($_.Exception.Message,'无法生成追问') | Out-Null }
})
[void]$taskForm.ShowDialog()
$taskForm.Dispose()
