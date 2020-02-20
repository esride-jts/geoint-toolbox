# GEOINT Toolbox is a python toolbox for geospatial intelligence workflows.
# Copyright (C) 2020 Esri Deutschland GmbH
# Jan Tschada (j.tschada@esri.de)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Additional permission under GNU LGPL version 3 section 4 and 5
# If you modify this Program, or any covered work, by linking or combining
# it with ArcGIS (or a modified version of these libraries),
# containing parts covered by the terms of ArcGIS libraries,
# the licensors of this Program grant you additional permission to convey the resulting work.
# See <https://developers.arcgis.com/> for further information.
#

import arcpy
import datetime
import os
from geoint.gdelt_client import gdelt_client
from geoint.gdelt_feature_factory import gdelt_feature_factory
from geoint.gdelt_workspace import gdelt_workspace

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
        self.label = "Make layer from GDELT events"
        self.description = "Queries the GDELT events table and saves the result as a layer."
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        # See https://pro.arcgis.com/de/pro-app/arcpy/geoprocessing_and_python/defining-parameters-in-a-python-toolbox.htm
        
        eventDate = arcpy.Parameter(
            displayName="Event date",
            name="event_date",
            datatype="GPDate",
            parameterType="Required",
            direction="Input"
        )
        eventDate.value = str(datetime.date.today())

        limit = arcpy.Parameter(
            displayName="Max number of records",
            name="limit",
            datatype="GPLong",
            parameterType="Required",
            direction="Input"
        )
        limit.value = 1000

        outFeatures = arcpy.Parameter(
            displayName="Output features",
            name="out_features",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output"
        )

        params = [eventDate, limit, outFeatures]
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
        """Creates a new GDELT client and queries the GDELT events table."""

        eventDate = parameters[0].value
        limit = parameters[1].value
        outFeatures = parameters[2].valueAsText
        workspacePath = os.path.dirname(outFeatures)
        tableName = os.path.basename(outFeatures).rstrip(os.path.splitext(outFeatures)[1])

        client = gdelt_client()
        try:
            gdelt_events = client.query_today(limit)
            workspace = gdelt_workspace(workspacePath)
            feature_factory = gdelt_feature_factory()
            gdelt_features = [feature_factory.create_feature(gdelt_event) for gdelt_event in gdelt_events]
            workspace.insert_features(tableName, gdelt_features)
            arcpy.AddMessage("GDELT records were inserted into the feature class.")
        except BaseException as ex:
            arcpy.AddError(ex)
        finally:
            del client
        return