
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; File:         dfiiBridgeClient.il
;
; Description:  DfiiBridge client functions (reverse communication)
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridgeClient__pyOnDataClient
;
; Callback for stdout messages
;
;   parameters:
;       id:   Process id
;       data: Exit code
;
;   return: nil
;
procedure(DfiiBridgeClient__pyOnDataClient(id data)
    or(id) ; silent the linter about unused arguments
    printf("[INFO] %s\n" data)
) ; procedure

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridgeClient__pyOnErrorClient
;
; Callback for return data
;
;   parameters:
;       id:   Process id
;       data: Exit code
;
;   return: nil
;
procedure(DfiiBridgeClient__pyOnErrorClient(id data)
    or(id) ; silent the linter about unused arguments
    DfiiBridge['client]['retval] = data
) ; procedure

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridgeClient__pyOnFinishClient
;
; Callback for finishing the virtuoso_client.py process
;
;   parameters:
;       id:   Process id
;       data: Exit code
;
;   return: nil
;
procedure(DfiiBridgeClient__pyOnFinishClient(id data)
    or(id) ; silent the linter about unused arguments
    (when data!=0
        printf("client was stopped with code %L\n" data)
    )
    DfiiBridge['client]['retcode] = data
    DfiiBridge['client]['ipc] = nil
) ; procedure

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridgeClient_executeCommand
;
; Execute a remote function on one or multiple clients.
; You can choose a client either by hostname and port, or connect to all
; clients that match the search_criteria.
;
;   parameters:
;       remoteFunction:   Name of the remote function
;       ?async:           Do not wait on the answers
;       ?sessionDir:      The session directory to use (default: nil -> ~/.dfiiBridge)
;       ?verbosity:       Verbosity of the skill side
;       ?search_criteria: Search criteria in the form "type=virtuoso,project=helloworld"
;       ?hostname:        Hostname to connect to (port must also be set)
;       ?port:            Port to connect to (hostname must also be set)
;       ?timeout_s:       Timeout in seconds that is waited
;       ?python_backend:  If true, convert arguments from skill to python representation and
;                         evaluate the output. If false, just use strings.
;       @rest args:       Arguments to pass to the remote function
;
;   return: if async: t if successfull or if not async a list of return values
;           (skill objects) of the clients
;
procedure(DfiiBridgeClient_executeCommand(remoteFunction @key (async nil)
                                                              (sessionDir nil)
                                                              (timeout_s 1000000)
                                                              (verbosity 30)
                                                              (search_criteria "")
                                                              (hostname "")
                                                              (port 0)
                                                              (python_backend t)
                                                              @rest args)

    let((executableWithArgs messageBuffer)
        ; reset return data structure
        DfiiBridge['client]['retcode] = -1
        DfiiBridge['client]['retval] = ""
        DfiiBridge['client]['verbosity] = verbosity

        (unless sessionDir sessionDir = DfiiBridge['server]['sessionDir])

        ; create execution command string
        executableWithArgs = sprintf(nil "%s -m dfiibridge_server.virtuoso_client" DfiiBridge['pyexe])
        executableWithArgs = sprintf(nil "%s --session_dir %L"                    executableWithArgs sessionDir)
        executableWithArgs = sprintf(nil "%s --origin_hostname %L"                executableWithArgs DfiiBridge['server]['hostname])
        executableWithArgs = sprintf(nil "%s --origin_port %L"                    executableWithArgs DfiiBridge['server]['port])
        executableWithArgs = sprintf(nil "%s --search_criteria '%s'"              executableWithArgs search_criteria)
        executableWithArgs = sprintf(nil "%s --hostname '%s'"                     executableWithArgs hostname)
        executableWithArgs = sprintf(nil "%s --port '%d'"                         executableWithArgs port)
        executableWithArgs = sprintf(nil "%s --function_name '%s'"                executableWithArgs remoteFunction)
        executableWithArgs = sprintf(nil "%s --verbosity '%d'"                    executableWithArgs verbosity)

        (when verbosity<=10 printf("Execute: %s\n" executableWithArgs))

        ; create command string for remote dfii server
        ;  $arg0\n
        ;  $arg1\n
        ;  <<<<END>>>>"
        messageBuffer = ""

        ; afterwards follow each argument pythonized per line
        foreach(arg args
            messageBuffer = strcat(messageBuffer sprintf(nil "%s\n" (if python_backend then DfiiBridge__pySkillToPython(arg) else arg)))
        )

        ; finally, termination marker
        messageBuffer = strcat(messageBuffer "<<<<END>>>>\n")

        (when verbosity<=10 printf("messageBuffer = \"\"\"\n%s\"\"\"\n" messageBuffer))

        ; create client process
        DfiiBridge['client]['ipc] = ipcBeginProcess(executableWithArgs
                                               ""
                                               'DfiiBridgeClient__pyOnDataClient
                                               'DfiiBridgeClient__pyOnErrorClient
                                               'DfiiBridgeClient__pyOnFinishClient)

        ; wait for the process to accept something on stdin
        ipcWaitForProcess(DfiiBridge['client]['ipc] 5) ; wait until ready

        ; write the message buffer to stdin
        ipcWriteProcess(DfiiBridge['client]['ipc] messageBuffer)

        ; stop here if async == true
        ; the user will call the wait function later if he wants the result
        if(!async then
            DfiiBridgeClient_waitForReturn(?timeout_s timeout_s ?eval python_backend)
        else
            t
        )
    )
) ; procedure

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridgeClient_waitForReturn
;
; Wait for the return value of all clients
;
;   parameters:
;       ?timeout_s: Timeout in seconds that is waited
;
;   return: t if successfull
;
procedure(DfiiBridgeClient_waitForReturn(@key (timeout_s 1000000) (eval t))
    let((result ret_list)
        ; wait for the process to finish (get the response from the remote side)
        (when DfiiBridge['client]['ipc] ipcWait(DfiiBridge['client]['ipc] 5 timeout_s)) ; wait for termination

        ; return the exit value of the client to the user
        ret_list = list()
        foreach(ret parseString(DfiiBridge['client]['retval] "\342\235\244") ; use heart unicode as seperator -> should never be used elsewhere

            (when DfiiBridge['client]['verbosity]<10 printf("Result from one client: %L\n" ret))

            if(eval then
                (when substring(ret 1 7)=="failure "
                    ret = sprintf(nil "error(%L)" substring(ret 8))
                )
                result = car(errsetstring(ret, t))

                if((errset.errset) then
                    (when DfiiBridge['client]['verbosity]<10
                        printf("Return value %L resulted in error %L\n" result errset.errset)
                    )
                    ret_list = append1(ret_list nil)
                else
                    ret_list = append1(ret_list result)
                )

            else
                result = ret
                ret_list = append1(ret_list result)
            )

        )
        ; return value
        ret_list
    )
) ; procedure


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridgeClient_init
;
; Initialize the fields in the client table
;
;   parameters: none
;
;   return: t if successfull
;
procedure(DfiiBridgeClient_init()
    ;
    ; Initialize global variables
    ;
    prog( ()
        (unless boundp('DfiiBridge)
            return(warn("Please first load the dfiiBridgeUtils.il, then the dfiiBridge.il and then the DfiiBridgeClient.il"))
        )

        (unless DfiiBridge['client]
            DfiiBridge['client] = makeTable("Client" nil)
        )

        DfiiBridge['client]['ipc] = nil
        DfiiBridge['client]['retcode] = -1
        DfiiBridge['client]['retval] = ""
        DfiiBridge['client]['verbosity] = 30

        return(t)
    )
) ; procedure

