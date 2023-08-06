
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; File:         dfiiBridgeServer.il
;
; Description:  DfiiBridge server functions
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridge__safeExit
;
; If >DfiiBridge__safeExit( ) is captured in the DfiiBridge__pyOnErrorServer()
; then we softly kill the dfiibridge server here, write a comment in the log
; and exit Virtuoso with the exit code 0.
;
;   parameters: none
;
;   return: nil
;
procedure(DfiiBridge__safeExit()
  println("[INFO] Virtuoso is going to be remotely terminated")
  DfiiBridge_killServer()
  ; Make a note in the CDS log so that crash loggers can detect that
  ; the session has been terminated remotely
  hiPrintToLogFile("DfiiBridge__exit()")
  hiFlushLogFile()
  exit(0)
) ; procedure

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridge__pyOnDataServer
;
; Callback if server process has written something to stdout.
; Here, we just redirect this directly to the CIW.
;
;   parameters:
;       id:       Process id
;       data:     Received string
;
;   return: nil
;
procedure(DfiiBridge__pyOnDataServer(id data)
    or(id) ; silent the linter about unused arguments
    printf("%s\n" data)
) ; procedure

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridge__pyOnErrorServer
;
; Callback if server process has written something to stderr.
; We use this to capture the skill code from the python process, because
; stdout is usually much less controlled. Other python packages may print
; things (strings starting with >) that will be then falsely interpreted.
;
;   parameters:
;       id:       Process id
;       data:     Received string
;
;   return: nil
;
procedure(DfiiBridge__pyOnErrorServer(id data)
    (prog ()

        (if substring(data 1 1)==">" then
            data = substring(data 2)
            foreach(chunk parseString(data "\n")

                let((result capturedWarning pythonCode)


                    foreach(line parseString(chunk "\342\235\244")

                        ; Save exiting virtuoso
                        when( line == "DfiiBridge__safeExit( )"
                            ipcWriteProcess(id lsprintf("True\n"))
                            hiRegTimer( "DfiiBridge__safeExit()" 10 )
                            return()
                        )

                        capturedWarning = DfiiBridge__pyCaptureWarnings(result=car(errsetstring(line)))

                        if((DfiiBridge['server]['verbosity] <= 10) then
                            printf("Command: '%L' -> Result: '%L'\n" line result)
                        )
                        if((errset.errset) then
                            printf("command %L resulted in error %L\n" line errset.errset)
                            ipcWriteProcess(id lsprintf("failure %L\n" errset.errset))
                            return(nil)
                        )
                    )

                    pythonCode = car(errset(DfiiBridge__pySkillToPython(result)))
                    if((errset.errset) then
                        printf("Translation from Skill to Python of %L resulted in error %L\n" result errset.errset)
                        ipcWriteProcess(id lsprintf("failure %L\n" errset.errset))
                        return(nil)
                    else
                        if((capturedWarning != "" && capturedWarning != "*WARNING* ") then
                            pythonCode = lsprintf("warning(%L, %s)" capturedWarning pythonCode)
                        )
                        if((DfiiBridge['server]['verbosity] <= 10) then
                            printf("Sending back: '%L'\n" pythonCode)
                        )
                        ipcWriteProcess(id strcat(pythonCode "\n"))
                        return(t)
                    )

                )
            )
        else
            fprintf(stderr "ERROR %s\n" data)
        )
    ) ; prog
) ; procedure

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridge__pyOnFinishServer
;
; Callback if server process has been terminated
;
;   parameters:
;       id:       Process id
;       exitCode: exit code
;
;   return: nil
;
procedure(DfiiBridge__pyOnFinishServer(id exitCode)
    or(id) ; silent the linter about unused arguments
    printf("server was stopped with code %L\n" exitCode)
    DfiiBridge['server]['ipc] = nil
) ; procedure

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridge_killServer
;
; Kill the DfiiBridge server
;
;   parameters: none
;
;   return: t if successfull
;
procedure(DfiiBridge_killServer()
    if(DfiiBridge['server]['ipc] == nil then
        t
    else
        ; send interrupt signal to process, not kill (otherwise it cannot shut itself down)
        ipcSignalProcess( DfiiBridge['server]['ipc] 'INT )
        ; wait for process to exit, maximum 60sec, print interval 5sec
        ipcWait( DfiiBridge['server]['ipc] 5 60 )
        t
    )
) ; procedure

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridge_startServer
;
; Start the dfiibridge server
;
;   parameters:
;       ?pyexe:      The path to the python executable
;       ?verbosity:  Set the verbosity level of the server
;       ?sessionDir: Directory of the session files (default: nil -> ~/.dfiiBridge)
;       ?userData:   Json formatted string that contains additional userdata that shall be
;                    stored in the session file
;
;   return: t if successfull
;
procedure(DfiiBridge_startServer(@key (pyexe "python3") (verbosity 30) (sessionDir nil) (userData "{}"))

    prog( ()
        ; Stop server from before
        (when boundp('DfiiBridge)
            (when tablep(DfiiBridge)
                (when DfiiBridge['server]['ipc]
                    DfiiBridge_killServer()
                )
            )
        )

        ; Create new global variable (there can always be just one server!)
        DfiiBridge = makeTable("DfiiBridge" nil)
        DfiiBridge['pyexe] = pyexe
        DfiiBridge['server] = makeTable("Server" nil)
        DfiiBridge['server]['ipc] = nil
        DfiiBridge['server]['sessionDir] = sessionDir
        DfiiBridge['server]['userData] = userData
        DfiiBridge['server]['verbosity] = verbosity

        (unless DfiiBridge['pyexe]
            return(warn("DfiiBridge['pyexe] is set to nil! Please set it to a valid path to an executable python binary."))
        )

        ; Make sure that the executable can be found
        unless(system(strcat("which " DfiiBridge['pyexe]))==0
            return(warn("The python executable of the DfiiBridge (%s) cannot be found! Please set DfiiBridge['pyexe] to a valid value." DfiiBridge['pyexe]))
        )

        ; The following fields are set in the virtuoso_server.py from python
        DfiiBridge['server]['hostname] = nil
        DfiiBridge['server]['port] = nil
        DfiiBridge['server]['log] = nil
        DfiiBridge['server]['session_file] = nil

        regExitBefore('DfiiBridge_killServer)

        let(((executableWithArgs "-m dfiibridge_server.virtuoso_server"))

            executableWithArgs = sprintf(nil "%s --cdslog %L" executableWithArgs hiGetLogFileName())

            when(DfiiBridge['server]['sessionDir]
                executableWithArgs = sprintf(nil "%s --session_dir %L" executableWithArgs DfiiBridge['server]['sessionDir])
            )
            when(DfiiBridge['server]['userData]
                executableWithArgs = sprintf(nil "%s --user_data %s" executableWithArgs DfiiBridge['server]['userData])
            )
            when(DfiiBridge['server]['verbosity]
                executableWithArgs = sprintf(nil "%s --verbose %L" executableWithArgs DfiiBridge['server]['verbosity])
            )
            executableWithArgs = sprintf(nil "%s %s" DfiiBridge['pyexe] executableWithArgs)
            (when DfiiBridge['server]['verbosity]<=10 printf("[INFO] DfiiBridgeServer Execute: %s\n" executableWithArgs))
            DfiiBridge['server]['ipc] = ipcBeginProcess(executableWithArgs
                                                        ""
                                                        'DfiiBridge__pyOnDataServer
                                                        'DfiiBridge__pyOnErrorServer
                                                        'DfiiBridge__pyOnFinishServer)
            return(t)
        ) ; let
    ) ; prog
) ; procedure
