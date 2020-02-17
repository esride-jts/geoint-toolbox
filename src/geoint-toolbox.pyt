import arcpy
class Toolbox(object):
    def __init__(self):
        """GEOINT Toolbox"""
        self.label = "GEOINT Toolbox"
        self.alias = "GEOINT Toolbox"
        # List of tool classes associated with this toolbox
        self.tools = [MakeLayerFromGdeltTool]

class MakeLayerFromGdeltTool(object):
    def __init__(self):
        """Make a layer from GDELT"""
        self.label = "Make layer from GDELT Tool"
        self.description = "Queries Big Tables and save the result as a layer."
        self.canRunInBackground = True
    def getParameterInfo(self):
        """Define parameter definitions"""
        params = None
        return params
    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True
    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return
    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    def execute(self, parameters, messages):
        """The source code of the tool."""
        return