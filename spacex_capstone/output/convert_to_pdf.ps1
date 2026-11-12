
    $ppt = New-Object -ComObject PowerPoint.Application
    $pres = $ppt.Presentations.Open('C:\Users\Freiweiss\.gemini\antigravity\scratch\spacex_capstone\output\Data Science Capstone Project Report.pptx', [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    $pres.SaveAs('C:\Users\Freiweiss\.gemini\antigravity\scratch\spacex_capstone\output\Data Science Capstone Project Report.pdf', 32) # 32 is ppSaveAsPDF
    $pres.Close()
    $ppt.Quit()
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
    