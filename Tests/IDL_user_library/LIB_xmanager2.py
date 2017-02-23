from numarray import *

# $Id: xmanager.pro,v 1.49 2003/02/03 18:13:32 scottm Exp $



#



# Copyright (c) 1991-2003, Research Systems, Inc.  All rights reserved.



#	Unauthorized reproduction prohibited.







#+



# NAME:



#	XMANAGER



#



# PURPOSE:



#	Provide management for widgets client applications created using IDL.



#



# CATEGORY:



#	Widgets.



#



# CALLING SEQUENCE:



#	XMANAGER [, Name, ID]



#



# OPTIONAL INPUTS:



#	NAME:	A string giving the name of the application that is being



#		registered.



#



#	ID:	The widget ID of the top level base of the new client.



#



# KEYWORD PARAMETERS:



#	BACKGROUND:



#		-------------------------------------------------------------



#		| PLEASE NOTE: This keyword is OBSOLETE. It's functionality |



#		| is provided by the TIMER keyword to the WIDGET_CONTROL    |



#		| procedure.                                                |



#		-------------------------------------------------------------



#



#	CATCH: If TRUE, tells XMANAGER to use CATCH when dispatching



#		widget events. If FALSE, CATCH is not used and execution



#		halts on error. The default is TRUE. If CATCH is specified,



#		the internal state of XMANAGER is updated and it returns



#		immediately without taking any further action. CATCH



#		is only effective if XMANAGER is blocking to dispatch



#		errors. If active command line event dispatching is in



#		use, it has no effect.



#



#	CLEANUP: This keyword contains a string that is the name of the



#		routine called when the widget dies.  If not specified,



#		no routine is called.  The cleanup routine must accept one



#		parameter which is the widget id of the dying widget. This



#		routine is set as the KILL_NOTIFY routine for the widget.



#



#	EVENT_HANDLER: The name of the event handling routine that is to be



#		called when a widget event occurs in the registered



#		application. If this keyword is not supplied, the Xmanager



#		will construct a default name by adding the "_EVENT" suffix



#		to the NAME argument. See below for a more detailed



#		explanation.



#



#	GROUP_LEADER: The widget id of the group leader for the application



#		being registered.  When the leader dies, all widgets that have



#		that leader will also die.



#



#		For example, a widget that views a help file for a demo



#		widget would have that demo widget as it's leader.  When



#		the help widget is registered, it sets the keyword



#		GROUP_LEADER to the widget id of the demo widget. If



#		the demo widget is destroyed, the help widget led by



#		the it would be killed by the XMANAGER.



#



#	JUST_REG:



#		This keyword tells the manager to just register the widget



#		but not to start doing the event processing.  This is useful



#		when you want to register a group of related top level widgets



#		but need to regain control immediately afterwards.



#



#		NOTE: JUST_REG does not do the same thing as NO_BLOCK. This is



#		explained in detail below under "SIDE EFFECTS".



#



#	 MODAL:



#		--------------------------------------------------------------



#		| PLEASE NOTE: This keyword is OBSOLETE. It's functionality  |



#		| is provided by the MODAL keyword to the WIDGET_BASE        |



#		| procedure.                                                 |



#		--------------------------------------------------------------



#



#		When this keyword is set, the widget that is being registered



#		traps all events and desensitizes all the other widgets.  It



#		is useful when input from the user is necessary before



#		continuing. Once the modal widget dies, the others are



#		resensitized and the normal event processing is restored.



#		XMANAGER is therefore using sensitivity to provide the



#		illusion of modality. The WIDGET_BASE keyword is a newer



#		IDL feature that provides the real thing.



#



#	NO_BLOCK: If set, tells XMANAGER that the registering client



#		does not require XMANAGER to block if active command line



#		event processing is available. If active command line



#		event processing is available AND* every current XMANAGER



#		client specifies NO_BLOCK, then XMANAGER will not block



#		and the user will have access to the command line while



#		widget applications are running.



#



#		NOTE: NO_BLOCK does not do the same thing as JUST_REG. This is



#		explained in detail below under "SIDE EFFECTS".



#



# OUTPUTS:



#	No outputs.



#



# COMMON BLOCKS:



#	MANAGED



#	XMANAGER_LOCAL:



#		Common blocks used for module state maintenance. These common



#		blocks are considered private to this module and should not



#		be referenced outside RSI supplied routines. They are



#		subject to change without notice.



#



#



# SIDE EFFECTS:



#



#    JUST_REG vs NO_BLOCK



#    --------------------



#       Although their names imply a similar function, the JUST_REG and



#	NO_BLOCK keywords perform very different services. It is important



#	to understand what they do and how they differ.



#



#       JUST_REG tells XMANAGER that it should simply register a client



#	and then return immediately. The result is that the client becomes



#	known to XMANAGER, and that future calls to XMANAGER will take this



#	client into account. Therefore, JUST_REG only controls how the



#	registering call to XMANAGER should behave. The registered client



#	can still be registered as requiring XMANAGER to block by not setting



#	NO_BLOCK. In this case, future calls to XMANAGER will block.



#



#	NO_BLOCK tells XMANAGER that the registered client does not



#	require XMANAGER to block if the command processing front end



#	is able to support active command line event processing (described



#	below). XMANAGER remembers this attribute of the client until



#	the client exits, even after the call to XMANAGER that registered the



#	client returns. NO_BLOCK is just a "vote" on how XMANAGER should



#	behave. The final decision is made by XMANAGER by considering the



#	NO_BLOCK attributes of all of its current clients as well as the



#	ability of the command front end in use to support the active command



#	line.



#



#    Blocking vs Non-blocking



#    ------------------------



#	The issue of blocking in XMANAGER requires some explanation.



#	IDL places incoming widget events into a queue of pending events.



#	The only way to get these events processed and dispatched is to



#	call the WIDGET_EVENT function. Arranging for WIDGET_EVENT to be



#	called properly is the primary job of XMANAGER. XMANAGER offers



#	two different modes of operation:



#



#	    - The first (outermost) XMANAGER processes events by calling



#	      WIDGET_EVENT as necessary until no managed clients remain on



#	      the screen. This is referred to as "blocking", because XMANAGER



#	      does not return to the caller until it is done, and the IDL



#	      command line is not available.



#



#	    - XMANAGER does not block, and instead, the part of IDL



#	      that reads command input also watches for widget events



#	      and calls WIDGET_EVENT as necessary while also reading



#	      command input. This is referred to as "non-blocking" or



#	      "active command line" mode.



#



#	The default is to block. However, if every currently active



#	application specified the NO_BLOCK keyword to XMANAGER, non-blocking



#	mode is used, if possible.



#



#	There are currently 5 separate IDL command input front end



#	implementations:



#



#		- Apple Macintosh IDE



#		- Microsoft Windows IDE



#		- Motif IDE (Unix and VMS)



#		- Unix plain tty



#		- VMS plain tty



#



#	Except for the VMS plain tty, all of these front ends are able to



#	support the non-blocking active command line. VMS users can have



#	an active command line by using the IDLde interface. The decision



#	on whether XMANAGER blocks to process widget events is determined



#	by the following rules, in order of precedence:



#



#	    - Use of the MODAL keyword will cause XMANAGER to block.



#	    - Setting JUST_REG to 1 ensures that XMANAGER will not block.



#	    - If using the VMS plain tty interface, XMANAGER will block.



#	    - If none of the previous rules apply, XMANAGER will block



#	      if any of its currently active clients were registered without



#	      specifying NO_BLOCK. If NO_BLOCK is specified for every client,



#	      XMANAGER will not block and will instead return and allow



#	      active command line processing to take place.



#



#	When possible, applications should set the NO_BLOCK keyword.



#	This allows the IDL command line to be active while events are



#	being processed, which is highly desirable.



#



#



# RESTRICTIONS:



#	The implementation of XMANAGER may change in the future. Details



#	of its internal implementation must not be relied upon --- only



#	its external definition can be considered stable.



#



#	XMANAGER uses several undocumented features provided by the



#	internal WIDGET routines. These features are private to RSI, and



#	are not guaranteed to remain in IDL or to remain unchanged. They



#	exist only to support XMANAGER and should not be used elsewhere:



#



#		WIDGET_CONTROL, /XMANAGER_ACTIVE_COMMAND



#		WIDGET_CONTROL, /MODAL



#		WIDGET_EVENT,   /BREAK_ON_EXPOSE



#		WIDGET_EVENT,   /EVENT_BREAK



#		WIDGET_EVENT,   /XMANAGER_BLOCK



#		WIDGET_INFO,    /XMANAGER_BLOCK



#



#	These features are undocumented because they are not considered



#	permanent. Research Systems reserves the right to remove or alter



#	these features at any time.



#



# EXAMPLE USE:



#	To create a widget named Example that is just a base widget with a done



#	button using the XMANAGER you would do the following:



#



#



#	;------ first - the event handler routine ------;



#



#     PRO example_event, ev			;this is the routine that



#						;deals with the events in the



#						;example widget.



#



#	WIDGET_CONTROL, ev.id, GET_UVALUE = uv	;the uservalue is retrieved



#						;from the widget where the



#						;event occurred



#



#	if(uv eq 'DONE') then $			;if the event occurred in the



#	  WIDGET_CONTROL, ev.top, /DESTROY	;done button then kill the



#     END					;widget example



#



#



#	;------ second - the main routine ------;



#



#     PRO example				;this is the main routine



#						;that builds the widget and



#						;registers it with the Xmanager



#



#	base = WIDGET_BASE(TITLE = 'Example')	;first the base is created



#



#	done = WIDGET_BUTTON(base, $		;next the done button is



#			     TITLE = 'DONE', $	;created and it's user value



#			     UVALUE = 'DONE')	;set to "DONE"



#



#	WIDGET_CONTROL, base, /REALIZE		;the widget is realized



#



#	XManager, 'example', base		;finally the example widget



#						;is registered with the



#						;Xmanager



#     END



#



#	notes:	First the event handler routine is listed.  The handler



#		routine has the same name as the main routine with the



#		characters "_event" added.  If you would like to use another



#		event handler name, you would need to pass it's name in as



#		a string to the EVENT_HANDLER keyword.  Also notice that the



#		event routine is listed before the main routine.  This is



#		because the compiler will not compile the event routine if



#		it was below the main routine.  This is only needed if both



#		routines reside in the same file and the file name is the same



#		as the main routine name with the ".pro" extension added.



#



#



# PROCEDURE:



#	When the first widget is registered, initialize the lists and then



#	start processing events.  Continue registering widgets and dispatching



#	events until all the widgets have been destroyed.  When a widget is



#	killed, destroy all widgets that list the destroyed widget as their



#	leader, if any.



#



# RELATED FUNCTIONS AND PROCEDURES:



#	XREGISTERED, XMTOOL



#



# MODIFICATION HISTORY: Written by Steve Richards, November, 1990



#	SMR, Mar,  1991	Added a cleanup routine keyword to allow dying



#	    widgets to clean themselves up when dying.



#	SMR, May,  1991 Fixed a bug found by Diane Parchomchuk where an error



#	    occurred when registering a widget  ight after destroying another.



#	SMR & ACY, July, 1991



#	    Fixed a bug found by Debra Wolkovitch where lone widgets being



#	    destroyed and new ones created caused problems.



#	SMR, Sept, 1991	Changed cleanup to use the new WIDGET_INFO routine.



#	SMR & ACY, Oct,  1991



#	    Fixed a bug where a background event that unregistered itself



#	    after a time would result in an XMANAGER error.



# 	SMR, Mar.  1992	Changed XMANAGER to use enhanced widget functions for



#	    event processing.



#	SMR, Nov.  1992 Changed modal widget handling allowing nesting of



#	    modal widgets.  The first modal desensitizes all current widgets



#	    and subsequent modals only desensitize the modal that called them.



#	JIY, Apr.  1993 Changed modal widget handling process to not run the



#	    event loop for nested modal widgets. Allowed for multiple modal



#	    widgets.



#	AB & SMR, 17 November 1993



#	    Added ID validity checking to desensitizing of modal widgets to



#	    fix a bug where already dead widgets were being accessed.



#	DJE, Feb, 1995



#	    Made it so that non-modal widgets created from a modal widget have



#	    events processed in the modal widget's event loop. This fixes a



#	    bug where xmanager wouldn't return immediately if there was a



#	    modal widget somewhere in the nesting, even though a non-modal



#	    widget was being added. The nesting level could get _very_ deep.



#	DJE, Apr 1995



#	    Pass a local variable to WIDGET_EVENT in the MODAL case, instead



#	    of passing the common block variable modalList. This avoids a bug



#	    where modalList gets changed behind WIDGET_EVENT's back.



#	DJE, Apr 1996



#	    Changes for handling asynchronous widget event dispatching.



#	    Complete rewrite. Background tasks are no longer supported. The



#	    MODAL keyword is now obsolete. Added CATCH and BLOCK keywords.



#	AB, May 1996



#	    Made changes so that XMANAGER always blocks under VMS with the



#	    non-GUI interface. This is due to the fact that the SMG$ system



#	    routines used by IDL in the plain tty case cannot support



#	    interleaving of X events with tty input.



#	AB, 9 January 1997



#	    Changed the meaning of the CATCH keyword so that catching is the



#	    default. Removed BLOCK and replaced with NO_BLOCK. Switched



#	    default action back to blocking from unblocking based on feedback



#	    from the IDL 5 beta. Added the ability to block only as long as a



#	    client without NO_BLOCK is running, and then revert to the active



#	    command line.



#	AB, 10 February 1997



#	    Cleaned up code to make it easier to understand and maintain.



#	    Also cleaned up the distinction between real modality (MODAL



#	    keyword to WIDGET_BASE) and XMANAGER's older fake modality



#	    (MODAL keyword to XMANAGER), and fixed bugs in the current



#	    implementation of fake modality.



#-















def xmanagerprinterror():



# Called when a client error is caught to print the error out for



# the user. Unfortunately no stack trace is available, but that's



# why XMANAGER,CATCH=0 exists.







   n_params = 0
   def _ret():  return None
   
   # COMPILE_OPT HIDDEN
   
   
   
   
   
   
   
   err = _sys_error_state.msg
   
   
   
   syserr = _sys_error_state.sys_msg
   
   
   
   printf(-2, _sys_error_state.msg_prefix, 'XMANAGER: Caught unexpected error from client application. Message follows...', format='(A, A)')
   
   
   
   help(last_message=True)
   
   
   
   
   return _ret()
















def validatemanagedwidgets():



# Makes sure all the widgets in the list of managed widgets are still



# valid, and removes those that aren't.







   n_params = 0
   def _ret():  return None
   
   # COMPILE_OPT HIDDEN
   
   
   
   global ids, names, modallist	# list of active modal widgets
   
   
   
   
   
   
   
   # initialize the lists
   
   
   
   if (bitwise_not((ids is not None))):   
      
      
      
      ids = 0
      
      
      
      names = 0
      
      
      
   
   
   
   
   
   
   
   # if the list is empty, it's valid
   
   
   
   if (ids[0] == 0):   
      return _ret()
   
   
   
   
   
   
   
   # which ones are valid?
   
   
   
   valid = where(ravel(widget_info(ids, managed=True)))[0]
   
   
   
   
   
   
   
   # build new lists from those that were valid in the old lists
   
   
   
   if (valid[0] == -1):   
      
      
      
      ids = 0
      
      
      
      names = 0
      
      
      
   else:   
      
      
      
      ids = ids[valid]
      
      
      
      names = names[valid]
      
      
      
   
   
   
   
   
   
   
   
   return _ret()
















def addmanagedwidget(name, id):



# Adds the given widget with its name to the list of managed widgets



#



# The list of managed widgets is kept as a convenience for applications



# that want to register their functionality by name. For instance, an app



# may not want to bring up a particular dialog if there is already one up.



# They can find out if the dialog is running by calling the XREGISTERED



# routine







   n_params = 2
   def _ret():  return (name, id)
   
   # COMPILE_OPT HIDDEN
   
   
   
   global 
   
   
   
   
   
   
   
   validatemanagedwidgets()
   
   
   
   
   
   
   
   if (ids[0] == 0):   
      
      
      
      # create new lists
      
      
      
      ids = concatenate([id])
      
      
      
      names = concatenate([name])
      
      
      
   else:   
      
      
      
      # insert at the beginning of the lists
      
      
      
      ids = concatenate([id, ids])
      
      
      
      names = concatenate([name, names])
      
      
      
   
   
   
   
   
   
   
   
   return _ret()
















def lookupmanagedwidget(name):



# Returns the widget id of the named widget, or 0L if not found







   n_params = 1
   
   # COMPILE_OPT HIDDEN
   
   
   
   global 
   
   
   
   
   
   
   
   validatemanagedwidgets()
   
   
   
   
   
   
   
   if (ids[0] != 0):   
      
      
      
      found = where(ravel(names == name))[0]
      
      
      
      if (found[0] != -1):   
         
         
         
         return ids[found[0]]
         
         
         
      
      
      
   
   
   
   
   
   
   
   return 0
   
   
   
















def xunregister(corpse):



# ------------------------------------------------------------------



# | PLEASE NOTE: This routine is OBSOLETE. It's functionality is   |



# | is no longer necessary.                                        |



# ------------------------------------------------------------------



#



#	This procedure used to remove a dead widget from the Xmanagers common



#	block, but that information is now maintained internally by IDL.







   n_params = 1
   def _ret():  return corpse
   
   # COMPILE_OPT HIDDEN
   
   
   
   global obsolete
   
   
   
   
   
   
   
   if (bitwise_not((obsolete is not None))):   
      
      
      
      obsolete = 1
      
      
      
      message('this routine is obsolete', info=True)
      
      
      
   
   
   
   
   
   
   
   # Might as well validate the list now (even though it would happen later)
   
   
   
   validatemanagedwidgets()
   
   
   
   
   
   
   
   
   return _ret()
























def xmanager_evloop_standard():



# This is the standard XMANAGER event loop. It works by dispatching



# events for all managed widgets until there are none left that require



# blocking. In the best case, the command line is able to dispatch events



# and there are no clients that require blocking (specified via the



# NO_BLOCK keyword to XMANAGER) and we are able to return immediately.







   n_params = 0
   def _ret():  return None
   
   # COMPILE_OPT HIDDEN
   
   
   
   global fake_modal_obsolete, xmanager_catch
   
   
   
   
   
   
   
   
   
   
   
   # WARNING: Undocumented feature. See RESTRICTIONS above for details.
   
   
   
   active = widget_info(xmanager_block=True)
   
   
   
   while (active != 0):
   
   
   
      err = 0
      
      
      
      if (xmanager_catch):   
         catch(err)
      
      
      
      if (err == 0):   
         
         
         
         # WARNING: Undocumented feature. See RESTRICTIONS above for details.
         
         
         
         tmp = widget_event(xmanager_block=True)
         
         
         
      else:   
         xmanagerprinterror()
      
      
      
      if (xmanager_catch):   
         catch(cancel=True)
      
      
      
      # WARNING: Undocumented feature. See RESTRICTIONS above for details.
      
      
      
      active = widget_info(xmanager_block=True)
      
      
      
   
   
   
   
   
   
   
   
   return _ret()
















def xmanager_evloop_real_modal(modal_id):



# This version of the XMANAGER event loop is used when a client with



# the MODAL keyword set on its TLB has been passed in. It dispatches



# events for that client until it is done. Events for other clients



# are also flushed at critical points so that expose events are not



# delayed unnecessarily.







   n_params = 1
   def _ret():  return modal_id
   
   # COMPILE_OPT HIDDEN
   
   
   
   global 
   
   
   
   
   
   
   
   
   
   
   
   active = 1
   
   
   
   while (active != 0):
   
   
   
      err = 0
      
      
      
      if (xmanager_catch):   
         catch(err)
      
      
      
      if (err == 0):   
         
         
         
         # WARNING: Undocumented feature. See RESTRICTIONS above for details.
         
         
         
         tmp = widget_event(modal_id, bad_id=bad, break_on_expose=True)
         
         
         
      else:   
         xmanagerprinterror()
      
      
      
      if (xmanager_catch):   
         catch(cancel=True)
      
      
      
      active = widget_info(modal_id, managed=True)
      
      
      
      
      
      
      
      # Modal event handling returned. Flush events for other widgets
      
      
      
      # so we do not keep expose events (among others) blocked.
      
      
      
      if (active):   
         
         
         
         err = 0
         
         
         
         if (xmanager_catch):   
            catch(err)
         
         
         
         if (err == 0):   
            
            
            
            tmp = widget_event(nowait=True)
            
            
            
         else:   
            xmanagerprinterror()
         
         
         
         if (xmanager_catch):   
            catch(cancel=True)
         
         
         
      
      
      
   
   
   
   
   return _ret()
















def xmanager_evloop_fake_modal(id):



# This version of the XMANAGER event loop is used when a client is



# registered with the MODAL keyword to XMANAGER. It fakes the appearance



# of real modality by making the other existing clients insensitive while



# the modal widget exists.







   n_params = 1
   def _ret():  return id
   
   # COMPILE_OPT HIDDEN
   
   
   
   global 
   
   
   
   global 
   
   
   
   
   
   
   
   
   
   
   
   # Remember the current modal list so it can be restored afterwards
   
   
   
   oldmodallist = modallist
   
   
   
   modallist = concatenate([id])
   
   
   
   # WARNING: Undocumented feature. See RESTRICTIONS above for details.
   
   
   
   widget_control(id, modal=True)
   
   
   
   
   
   
   
   # Get list of clients that should be desensitized to mimic modality.
   
   
   
   # If this is the outermost modal, then the list of all currently
   
   
   
   # managed widgets is used. If this is a nested inner modal, then
   
   
   
   # use the oldModalList.
   
   
   
   if ((oldmodallist is not None)):   
      
      
      
      senslist = oldmodallist
      
      
      
   else:   
      
      
      
      widget_control(id, managed=0)    # So won't show up in following statement
      
      
      
      senslist = widget_info(managed=True)
      
      
      
      widget_control(id, managed=True)     # Put it back
      
      
      
   
   
   
   for i in arange(0, (array(senslist, copy=0).nelements() - 1)+(1)):
      widget_control(senslist[i], bad_id=ignore_bad, sensitive=0)
   
   
   
   
   
   
   
   
   
   
   
   # Process events only for clients in the modal list. This list may gain
   
   
   
   # members if event processing leads to other applications being registered
   
   
   
   # via a recursive call to XMANAGER.
   
   
   
   tmp = where(ravel(widget_info(modallist, managed=True)))[0]
   
   
   
   while (active != 0):
   
   
   
      err = 0
      
      
      
      if (xmanager_catch):   
         catch(err)
      
      
      
      tmp = modallist
      
      
      
      if (err == 0):   
         
         
         
         # WARNING: Undocumented feature. See RESTRICTIONS above for details.
         
         
         
         tmp = widget_event(tmp, bad_id=bad, break_on_expose=True)
         
         
         
      else:   
         xmanagerprinterror()
      
      
      
      if (xmanager_catch):   
         catch(cancel=True)
      
      
      
      tmp = where(ravel(widget_info(modallist, managed=True)))[0]
      
      
      
      if (active != 0):   
         modallist = modallist[tmp]
      
      
      
      #
      
      
      
      # Modal event handling returned, flush events for other widgets
      
      
      
      # if any so we do not keep expose events etc. blocked
      
      
      
      #
      
      
      
      if (active):   
         
         
         
         err = 0
         
         
         
         if (xmanager_catch):   
            catch(err)
         
         
         
         if (err == 0):   
            
            
            
            tmp = widget_event(nowait=True)
            
            
            
         else:   
            xmanagerprinterror()
         
         
         
         if (xmanager_catch):   
            catch(cancel=True)
         
         
         
      
      
      
   
   
   
   
   
   
   
   for i in arange(0, (array(senslist, copy=0).nelements() - 1)+(1)):
      widget_control(senslist[i], bad_id=ignore_bad, sensitive=True)
   
   
   
   
   
   
   
   # restore the outer XMANAGER's list of modal widgets
   
   
   
   modallist = oldmodallist
   
   
   
   
   
   
   
   
   return _ret()
























def xmanager(name, id, background=None, catch=None, cleanup=None, event_handler=None, group_leader=None, just_reg=None, modal=None, no_block=None):







   n_params = 2
   _opt = (background, catch, cleanup, event_handler, group_leader, just_reg, modal, no_block)
   def _ret():
      _optrv = zip(_opt, [background, catch, cleanup, event_handler, group_leader, just_reg, modal, no_block])
      _rv = [name, id]
      _rv += [_o[1] for _o in _optrv if _o[0] is not None]
      return tuple(_rv)
   
   global 
   
   
   
   global 
   
   
   
   
   
   
   
   
   
   
   
   isfakemodal = (modal is not None)
   
   
   
   
   
   
   
   # print out obsolete keyword messages
   
   
   
   if ((background is not None)):   
      
      
      
      message("The BACKGROUND keyword to the XMANAGER procedure is " + "obsolete. It is superseded by the TIMER keyword to " + "the WIDGET_CONTROL procedure.", info=True)
      
      
      
   
   
   
   if (bitwise_and(isfakemodal, (bitwise_not((fake_modal_obsolete is not None))))):   
      
      
      
      fake_modal_obsolete = 1
      
      
      
      message("The MODAL keyword to the XMANAGER procedure is " + "obsolete. It is superseded by the MODAL keyword to " + "the WIDGET_BASE function.", info=True)
      
      
      
   
   
   
   
   
   
   
   
   
   
   
   # Initialization
   
   
   
   if (array(catch, copy=0).nelements() != 0):   
      
      
      
      xmanager_catch = catch != 0
      
      
      
      message('Error handling is now ' + (concatenate(['off', 'on']))[xmanager_catch], info=True)
      
      
      
      return _ret()
      
      
      
   else:   
      if (array(xmanager_catch, copy=0).nelements() == 0):   
         xmanager_catch = 1#
   
   
   
   isrealmodal = 0
   
   
   
   if (array(just_reg, copy=0).nelements() == 0):   
      just_reg = 0
   
   
   
   if (isfakemodal):   
      just_reg = 0#
   
   
   
   if (bitwise_not((modallist is not None))):   
      modallist = 0
   
   
   
   validatemanagedwidgets()
   
   
   
   
   
   
   
   
   
   
   
   # Argument setup
   
   
   
   if (n_params == 0):   
      
      
      
      if (ids[0] == 0):   
         
         
         
         message('No widgets are currently being managed.', info=True)
         
         
         
         return _ret()
         
         
         
      
      
      
   else:   
      if (n_params != 2):   
         
         
         
         message('Wrong number of arguments, usage: XMANAGER [, name, id]')
         
         
         
      else:   	#2 argument case
         
         
         
         
         
         
         
         # Check the arguments
         
         
         
         if (bitwise_not(widget_info(id, valid=True))):   
            message('Invalid widget ID.')
         
         
         
         nameinfo = size(name)
         
         
         
         if (bitwise_or((nameinfo[0] != 0), (nameinfo[1] != 7))):   
            message('Invalid widget name.')
         
         
         
         
         
         
         
         
         
         
         
         # If TLB is modal, block in XMANAGER till you are done
         
         
         
         if (widget_info(id, modal=True)):   
            isrealmodal = 1
         
         
         
         
         
         
         
         if ((cleanup is not None)):   
            widget_control(id, kill_notify=cleanup)
         
         
         
         if (bitwise_not((event_handler is not None))):   
            event_handler = name + '_event'
         
         
         
         
         
         
         
         # Register new widget
         
         
         
         name, id = addmanagedwidget(name, id)
         
         
         
         
         
         
         
         # Mark the widget for event processing
         
         
         
         widget_control(id, managed=True, event_pro=event_handler)
         
         
         
         
         
         
         
         # Unless the caller set NO_BLOCK to indicate otherwise, mark
         
         
         
         # this client as requiring XMANAGER to block. This decision is driven
         
         
         
         # by backward compatibility concerns. During the IDL 5.0 beta we discovered
         
         
         
         # that many customers have code that depends on the blocking behavior.
         
         
         
         #
         
         
         
         # WARNING: Undocumented feature. See RESTRICTIONS above for details.
         
         
         
         if (no_block is not None):   
            widget_control(id, xmanager_active_command=True)
         
         
         
         
         
         
         
         # pass the group_leader keyword through
         
         
         
         if ((group_leader is not None)):   
            widget_control(id, group_leader=group_leader)
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         # Modal Widget Registration
         
         
         
         if (bitwise_and((modallist is not None), (bitwise_not(isfakemodal)))):   
            
            
            
            
            
            
            
            # This client is a non-modal widget, being started while a
            
            
            
            # fake modal is already up. Just add the new widget to the modal
            
            
            
            # list and return immediately. The fake modal event loop will
            
            
            
            # dispatch its events as well as the modal clients.
            
            
            
            modallist = concatenate([modallist, id])
            
            
            
            just_reg = 1	# Don't process events. Instead, return immediately
            
            
            
            
            
            
            
            # need to break out of the outer widget_event call so that the
            
            
            
            # outer xmanager can see that outmodal has changed
            
            
            
            # WARNING: Undocumented feature. See RESTRICTIONS above for details.
            
            
            
            widget_control(event_break=True)
            
            
            
            
            
            
             		# modal
         
         
         
         
         
         		# 2 argument case
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   # Event Processing.
   
   
   
   if (bitwise_not(just_reg)):   
      
      
      
      if (isrealmodal):   
         
         
         
         id = xmanager_evloop_real_modal(id)
         
         
         
      else:   
         if isfakemodal:   
            
            
            
            id = xmanager_evloop_fake_modal(id)
            
            
            
         else:   
            
            
            
            xmanager_evloop_standard()
            
            
      
      
      
      
      
      
      
      # keep our list clean and up to date
      
      
      
      validatemanagedwidgets()
      
      
      
      
      
      
      
   
   
   
   
   
   
   
   
   return _ret()





