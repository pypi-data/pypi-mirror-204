;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; File:         dfiiBridgeUtils.il
;
; Description:  DfiiBridge utility functions
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridge__pyCaptureWarnings
;
; Capture the warnings
;
;   parameters:
;       body: The code that shall be executed
;
;   return: Captured warnings
;
; https://community.cadence.com/cadence_technology_forums/f/custom-ic-skill/38856/reading-warning-messages-from-ciw-using-skill
defmacro(DfiiBridge__pyCaptureWarnings (@rest body)
  `let(((tempPort outstring()))
    unwindProtect(
      ;------------------------------------------------------------------
      ; main clause - using dynamic scoping, redirect woport to tempPort
      ; and then invoke the forms passed in as the argument to the
      ; macro
      ;------------------------------------------------------------------
      {
        let(((woport tempPort))
          ,@body
          ; next two lines are to force final warning to be flushed
          warn("")
          getWarn()
        )
        ;----------------------------------------------------------------
        ; return value is the data written to the string port
        ;----------------------------------------------------------------
        getOutstring(tempPort)
      }
      ;------------------------------------------------------------------
      ; always execute the close even if there was an error in
      ; the code above
      ;------------------------------------------------------------------
      close(tempPort)
    )
  )
) ; defmacro

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridge__pyPropertyListToPython
;
; Translate a property list to a python object
;
;   parameters:
;       thing: The skill object that shall be translated into python code
;
;   return: Python code string
;
procedure(DfiiBridge__pyPropertyListToPython(propList)
    strcat("{"
        buildString(
            mapcar(
					lambda((key)
						DfiiBridge__pyPropertyListElementToPython(propList key)
					)
                propList->?
			)
        	",")
        "}"
    )
) ; procedure

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridge__pySaveToVariableAndReturn
;
; Translate a list to a python object
;
;   parameters:
;       thing: The skill object that shall be translated into python code
;
;   return: Python code string
;
procedure(DfiiBridge__pySaveToVariableAndReturn(thing)
    let((repr variableName split objectType address variableSymbol)
        repr = sprintf(nil "%L" thing)
        if(rexExecute(repr) then
            split = buildString(parseString(repr "_") "")
            split = parseString(split "@:")
            objectType = car(split)
            address = cadr(split)
            variableName = sprintf(nil "__py_%s_%s" objectType address)
            set(stringToSymbol(variableName) thing)
            lsprintf("Remote(%L)" variableName)
        else if(otherp(thing) then
            variableSymbol = gensym("__py_OTHER_")
            set(variableSymbol thing)
            lsprintf("Remote(%L)" symbolToString(variableSymbol))
        else if(portp(thing) then
            variableSymbol = gensym("__py_openfile_")
            set(variableSymbol thing)
            lsprintf("Remote(%L)" symbolToString(variableSymbol))
        else
            error("I could not parse %L\n" repr)
        )))
    )
) ; procedure

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridge__pyListToPython
;
; Translate a list to a python object
;
;   parameters:
;       thing: The skill object that shall be translated into python code
;
;   return: Python code string
;
procedure(DfiiBridge__pyListToPython(thing)
    strcat(
        "["
        buildString(mapcar('DfiiBridge__pySkillToPython thing) ",")
        "]"
    )
) ; procedure

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridge__pyPropertyListElementToPython
;
; Convert one dictionary entry (used in DfiiBridge__pyPropertyListToPython())
;
;   parameters:
;       propList: The entire property list
;       key: The key inside the property list that shall be converted
;
;   return: Python code string
;
procedure(DfiiBridge__pyPropertyListElementToPython(propList key)
	(prog ()

        (when or(symbolp(key) stringp(key)) ; This is the normal case
            return(sprintf(nil "'%s':%s" key DfiiBridge__pySkillToPython(get(propList key))))
        )

        ; In exceptional cases it can happen that a key is actually a list!
        (when listp(key)
            return(sprintf(nil "%s:%s"
                            DfiiBridge__pyListKeyToPython(key)
                            DfiiBridge__pySkillToPython(
                                nth(lindex(propList key) propList) ; This may not always work (e.g. if the key is a value before the key's position)
                            )
                        )
                )
        )

        ; Anything else cannot be handled
        error("Do not understand the key %L of type %L" key type(key))
	)
) ; procedure

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridge__pyListKeyToPython
;
; Used if lists are used as keys inside of skill -> translate to tuples
;
;   parameters:
;       thing: The key of type list that shall be translated into a tuple
;
;   return: Python code string
;
procedure(DfiiBridge__pyListKeyToPython(thing)
    strcat(
        "("
        buildString(mapcar('DfiiBridge__pySkillToPython thing) ",")
        ")"
    )
) ; procedure

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridge__pyVectorToPython
;
; Translate a vector to a python object
;
;   parameters:
;       thing: The skill object that shall be translated into python code
;
;   return: Python code string
;
procedure(DfiiBridge__pyVectorToPython(collection)
    let((symbol)
        symbol = gensym("__py_vector_")
        set(symbol collection)
        lsprintf("Vector(%L)" symbolToString(symbol))
    )
) ; procedure

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridge__pyTableToPython
;
; Translate a table to a python object
;
;   parameters:
;       thing: The skill object that shall be translated into python code
;
;   return: Python code string
;
procedure(DfiiBridge__pyTableToPython(collection)
    let((symbol)
        symbol = gensym("__py_table_")
        set(symbol collection)
        lsprintf("Table(%L)" symbolToString(symbol))
    )
) ; procedure

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridge__pySkillToPython
;
; Translate any skill object into python code
;
;   parameters:
;       thing: The skill object that shall be translated into python code
;
;   return: Python code string
;
procedure(DfiiBridge__pySkillToPython(thing)
    if(thing == t then
        "True"
    else if(!thing then
        "None"
    else if(or(numberp(thing) stringp(thing)) then
        sprintf(nil "%L" thing)
    else if(symbolp(thing) then
        sprintf(nil "Symbol('%s')" thing)
    else if(listp(thing) then
        if(and(!car(thing) symbolp(cadr(thing))) then
            DfiiBridge__pyPropertyListToPython(thing)
        else
            DfiiBridge__pyListToPython(thing)
        )
    else
        if(tablep(thing) then
                DfiiBridge__pyTableToPython(thing)
        else
            if(vectorp(thing) then
                DfiiBridge__pyVectorToPython(thing)
            else
                rexCompile("^[_a-zA-Z]+[:@][x0-9a-fA-F]+$")
                DfiiBridge__pySaveToVariableAndReturn(thing)
    )))))))
) ; procedure


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; DfiiBridge__pyReconstructSkillObjects
;
; Reconstruct skill object (special handling of lists)
; It is called from Python.
;
;   parameters:
;       data: Skill object to be reconstructed
;
;   return: Skill object
;
procedure(DfiiBridge__pyReconstructSkillObjects(data)
    ; Idea taken from: https://community.cadence.com/cadence_technology_forums/f/custom-ic-skill/38215/search-and-replace-in-a-sub-list
    foreach(map remainder data
        cond(
            (listp(car(remainder))
                DfiiBridge__pyReconstructSkillObjects(car(remainder))
            )
            (type(car(remainder))=='symbol
                when(substring(symbolToString(car(remainder)) 1 4)=="__py"
                    rplaca(remainder symeval(car(remainder)))
                )
            )
        )
    )
	data
) ; procedure