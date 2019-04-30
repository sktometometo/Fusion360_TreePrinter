#Author-sktometometo
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        #
        folderDiag = ui.createFolderDialog()
        diagResult = folderDiag.showDialog()

        if diagResult == 0:        
            destDir = folderDiag.folder
        else:
            print("error\n")
            return

        # Get root rootComponent
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent

        # progress dialog
        progressDialog = ui.createProgressDialog()
        progressDialog.cancelButtonText = "Cancel"
        progressDialog.isBackgroundTranslucent = False
        progressDialog.isCancelButtonShown = True
        progressDialog.isValid = True

        #
        occurrences = rootComp.occurrences
        progressDialog.show("counting objects...", \
                            "Counting target objects : %p %", 0, occurrences.count, 1)
        numtotaloccs = 0
        for occ in occurrences:
            progressDialog.message = "Counting objects in " + occ.name + " : %p \%"
            numtotaloccs += countTargetLink( occ )
            progressDialog.progressValue += 1
            if progressDialog.wasCancelled:
                # TODO
                break
        progressDialog.hide()
        progressDialog.reset()

        #
        ret = True
        progressDialog.show("printing tree structure...", \
                            "printing tree structure : %p %", 0, numtotaloccs, 1)

        printcontent = ""
        for occ in occurrences:
            ret = printLinkStructure( occ, progressDialog, None )
            if ret == "DialogCancel":
                progressDialog.reset()
                progressDialog.hide()
            else:
                printcontent += ret
        progressDialog.hide()
        progressDialog.reset()

        with open( dest_dir+"\\output.csv", mode="w" ) as f:
            f.write(printcontent)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def countTargetLink( occurrence ):
    """
    """
    ret = 1
    childOccs = occurrence.childOccurrences
    for childOcc in childOccs:
        ret += countTargetLink( childOcc )
    return ret

def printLinkStructure( occurrence, progressDialog, preprint ):
    """
    """
    ret = True

    progressDialog.message = "printing tree structure of " + occurrence.name + "...." + "\n" + "progress : %p"
    progressDialog.progressValue += 1

   # if occurrence.isReferencedComponent:
   #    ret = occurrence.breakLink()

    printcontent = ""
    printcontentraw = ""
    if preprint == None:
        printcontentraw = ""
    else:
        printcontentraw = preprint + occurrence.name + ","

    printcontent += printcontentraw + "\n"

    progressDialog.message = "printing tree structure of " + occurrence.name + "." + "\n" + "progress : %p"

    if progressDialog.wasCancelled:
        return "DialogCancel"

    childOccs = occurrence.childOccurrences
    for childOcc in childOccs:
        tempret = printLinkStructure( childOcc, progressDialog, printcontentraw )
        if tempret == "DialogCancel":
            return "DialogCancel"
        else:
            printcontent += tempret + "\n"

    return printcontent
