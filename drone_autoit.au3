#AutoIt3Wrapper_Au3Check_Parameters=-d -w 1 -w 2 -w 3 -w- 4 -w 5 -w 6 -w- 7
#include <AutoItConstants.au3>
#include <GUIConstantsEx.au3>
#include <File.au3>
#include <Array.au3>
#include <FileConstants.au3>
#include <MsgBoxConstants.au3>
#include <WinAPIFiles.au3>
Opt("WinTitleMatchMode", 2) ; makes it match substring of window. Useful for arduino

; TO DO: actually time things to see how long to wait. Remove the "click to proceed" boxes
; GUI drives everything, calls functions on start etc
MainGUI()

Func MainGUI()
  Local $StartFile, $StartFileValue, $Button1, $Button2, $msg
  Local $iHeight = 150, $iWidth = 550
  Local $continueFlights = 1
  GUICreate("Drone control Window", $iWidth, $iHeight)

  Opt("GUICoordMode", 2)
  $StartFile = GUICtrlCreateInput("C:\Users\naNU\Desktop\drone\testland4_921.waypoints", 30, 30, 500)
  $Button1 = GUICtrlCreateButton("Start", -500, 30, 100)
  GUISetState()

  ; Run the GUI until the window is closed
  While 1
    $msg = GUIGetMsg()
    Select
      Case $msg = $GUI_EVENT_CLOSE
        ExitLoop
      Case $msg = $Button1
	    ; Checks To See If The Internet Is Connected first
	    If(_IsInternetConnected() == "True") Then
	      $StartFileValue = GUICtrlRead($StartFile) ; Check to see the file exists
	      If(FileExists($StartFileValue)) Then
			_createContinueFile() ; this has a 1 in it and when that's changed to 0 it will stop the loop
			; Set up array of files to go through
		    Local $szDrive, $szDir, $szFName, $szExt ;get the directory path from filename
		    _PathSplit($StartFileValue, $szDrive, $szDir, $szFName, $szExt)
		    Local $aFileList = _FileListToArray($szDrive & $szDir, "*waypoints") ; find all waypoint files in directory  Display: ;_ArrayDisplay($aFileList, "$aFileList")
		    Local $indexResult = _ArrayFindAll($aFileList, $szFName & $szExt) ; find where this file is in the array so we can increment. Note result is also an array
		    MsgBox(0, 'Start', "Loop starting on: " & $aFileList[$indexResult[0]])
			_StartUpArduino() ;Leave these open throughout
		    For $i = $indexResult[0] To $aFileList[0] Step 1
		      If(_readContinueFile() == "1") Then ; Check if we should continue, otherwise end for loop
			    _RunMission($szDrive & $szDir & $aFileList[$i]) ; this flys the drone - assumes its ready to fly
				If(_readContinueFile() == "1") Then ; Again check if we should continue before actually doing so
					_CollectDroneSwap() ; this runs arduino program to collect drone, swap stuff and spit it out ready to fly
				Else
					MsgBox(0, 'Stopping', "Continue File doesn't show 1")
					ExitLoop
				Endif
			  Else
				MsgBox(0, 'Stopping', "Continue File doesn't show 1")
			    ExitLoop
			  EndIf
			Next
	      Else
		    MsgBox(0, 'No Start', "That file doesn't exist, can't start")
	      EndIf
	    Else
	      MsgBox(0, 'No Start', "Can't start because internet isn't connected")
	    EndIf
    EndSelect
  WEnd
  WinClose("donothing")
  WinClose("drone_battery_swap")
  _rmContinuefile()
EndFunc

Func _IsInternetConnected()
	Local $aReturn = DllCall('connect.dll', 'long', 'IsInternetConnected')
	If @error Then
	  Return SetError(1, 0, False)
	EndIf
	Return $aReturn[0] = 0
EndFunc ;==>_IsInternetConnected

Func _RunMission($droneFile)
	;Now bring up mission planner. Connect to drone. Connect to base station. Load Plan. Start Mission
	Run("C:\Program Files (x86)\Mission Planner\MissionPlanner.exe")
	Sleep(30000)
	If WinExists("Update Now") Then
	  WinActivate("Update Now") ;Update Now window - exit out
	  Sleep(1000)
	  MouseClick($MOUSE_CLICK_PRIMARY, 886, 485, 1) 
	  Sleep(1000)
	EndIf
	Sleep(1000)
	MouseClick($MOUSE_CLICK_PRIMARY, 1580, 43, 1) ; 1580, 43 is position of connect button (connect to drone). single click
	Sleep(20000); allow connection to proceed
	MouseClick($MOUSE_CLICK_PRIMARY, 123, 53, 1) ; 123, 53 is position of setup bar
	Sleep(1000)
	MouseClick($MOUSE_CLICK_PRIMARY, 89, 142, 1) ; optional hardware
	Sleep(1000)
	MouseClick($MOUSE_CLICK_PRIMARY, 80, 180, 1) ; rtk/gps inject
	Sleep(1000)
	MouseClick($MOUSE_CLICK_PRIMARY, 341, 87, 1) ; connect
	Sleep(1000)
	MouseClick($MOUSE_CLICK_PRIMARY, 862, 482, 1) ; exit out error if it's there
	Sleep(1000)
	MouseClick($MOUSE_CLICK_PRIMARY, 862, 482, 1) ; OK on connect. wait longer to connect
	Sleep(60000) ; wait for connection to complete, let rtk settle in
	If WinExists("New Firmware") Then
		WinActivate("New Firmware")
		Sleep(1000)
		MouseClick($MOUSE_CLICK_PRIMARY, 883, 479, 1) 
		Sleep(1000)
	EndIf
	MouseClick($MOUSE_CLICK_PRIMARY, 73, 53, 1) ; 73, 53 is position of plan
	Sleep(1000)
	MouseClick($MOUSE_CLICK_PRIMARY, 1518, 223, 1) ; 1518, 223 is position of load plan
	Sleep(1000)
	Send($droneFile)
	Send("{ENTER}")
	Sleep(1000)
	if WinExists("Reset") Then
	  WinActivate("Reset")
	  MouseClick($MOUSE_CLICK_PRIMARY, 798, 472, 1) ; position of yes reset home to loaded coords
	  Sleep(1000)
	EndIf
	MouseClick($MOUSE_CLICK_PRIMARY, 1535, 327, 1) ; position of write to drone
	Sleep(15000); wait longer to write all the points to drone
	MouseClick($MOUSE_CLICK_PRIMARY, 15, 42, 1) ; position of data tab
	Sleep(1000)
	MouseClick($MOUSE_CLICK_PRIMARY, 68, 540, 1) ; position of actions subtab
	Sleep(1000)
	MouseClick($MOUSE_CLICK_PRIMARY, 300, 583, 1) ; position of auto - drone setting
	Sleep(1000)
	MouseClick($MOUSE_CLICK_PRIMARY, 418, 693, 1) ; position of arm/disarm
	Sleep(20000) 
	;Sleep(600000) ; wait 10 minutes for drone flight to complete
	MsgBox(0, 'Proceed', 'Click to proceed')
	MouseClick($MOUSE_CLICK_PRIMARY, 1580, 43, 1) ; disconnect
	Sleep(5000)
	WinClose("Mission Planner")
	 ; IMPROVE: figure out how to detect the drone has landed rather than long wait
 EndFunc
Func _CollectDroneSwap()
	Sleep(2000)
	WinActivate("drone_battery_swap")
	Sleep(1000)
	Send("^u") ;uploads drone connect and swap to arduino
	Sleep(25000)
	;Sleep(4800000); wait for gathering of drone and prep to launch. wait 1 20 hr.
	MsgBox(0, 'Proceed', 'Click to proceed')
	WinActivate("donothing")
	Sleep(1000)
	Send("^u") ;uploads drone connect and swap to arduino
	;Then start loop over on mission planner with new file
EndFunc
Func _StartUpArduino()
	; Open arduino connection. Load "do nothing" script so we don't run the lander accidentally. keep do nothing and lander arduino windows ready
	;$iPID = Run('C:\Users\naNU\Desktop\ardu\arduino-1.8.19-windows\arduino.exe', @SW_MAXIMIZE)
	$cmds = "C:\Users\naNU\Desktop\ardu\arduino-1.8.19-windows\arduino.exe"
	$iPID = Run(@ComSpec & " /c " & $cmds)    ; don't forget " " before "/c".  startup of arduino only runs reliably from cmd line for some reason
	;Allow window to initialize...
	Sleep (15000)
	;Send("#d") ;minimize all windows
	;WinActivate("Arduino")
	Send("^o")
	Sleep(1000)
	Send("C:\Users\naNU\Desktop\ardu\donothing\donothing.ino")
	Send("{ENTER}")
	Sleep(1000)
	WinActivate("donothing")
	Sleep(1000)
	Send("^u") ;uploads donothing to arduino
	Sleep(20000); wait for upload
	Send("^o")
	Sleep(1000)
	Send("C:\Users\naNU\Desktop\ardu\drone_battery_swap_full\drone_battery_swap_full.ino")
	Send("{ENTER}")
	Sleep(1000)
	; Both arduino programs are now open.  Use WinActivate("donothing") or WinActivate("drone_battery_swap") to bring them up and upload to arduino
EndFunc
Func _createContinueFile()
  ; Create file in same folder as script
  $sFileName = @ScriptDir &"\continue.txt"
  ; Open file - deleting any existing content
  $hFilehandle = FileOpen($sFileName, $FO_OVERWRITE)
  ; Write a line
  FileWrite($hFilehandle, "1")
  ; Close the handle so it can be modified  by hand as needed
  FileClose($hFilehandle)
EndFunc 

Func _readContinueFile()
  ; Create file in same folder as script
  $sFileName = @ScriptDir &"\continue.txt"
  ; Open file - deleting any existing content
  $hFilehandle = FileOpen($sFileName, $FO_READ)
  ; Read it
  local $fileContent = FileRead($sFileName)
  ; Close the handle so it can be modified  by hand as needed
  FileClose($hFilehandle)
  Return $fileContent
EndFunc 

Func _rmContinueFile()
  ; Create file in same folder as script
  $sFileName = @ScriptDir &"\continue.txt"
  ; Delete the temporary file.
  FileDelete($sFileName)
EndFunc
