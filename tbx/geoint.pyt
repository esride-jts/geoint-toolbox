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
        self.tools = [MakeLayerFromGdeltTool, MakeLayerFromGraphGdeltTool]

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
        outFeatures.value = "Events_{0}".format(str(datetime.date.today()).replace("-", ""))

        inFeatures = arcpy.Parameter(
            displayName="Input features",
            name="in_features",
            datatype="GPFeatureRecordSetLayer",
            parameterType="Optional",
            direction="Input"
        )

        params = [eventDate, limit, outFeatures, inFeatures]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if (parameters[0].altered):
            parameters[2].value = "Events_{0}".format(str(parameters[0].value.date()).replace("-", ""))
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

        inFeatures = parameters[3].value
        areas_of_interests = None
            
        client = gdelt_client()
        try:
            if (inFeatures):
                gdelt_events = []
                inCatalogPath = arcpy.Describe(inFeatures).catalogPath
                wgs84 = arcpy.SpatialReference(4326)
                areas_of_interests = []
                with arcpy.da.SearchCursor(inCatalogPath, ["SHAPE@"], spatial_reference=wgs84) as cursor:
                    for inFeature in cursor:
                        geometry = inFeature[0]
                        areas_of_interests.append(geometry)
                        extent = geometry.extent
                        bbox = { "xmin": extent.XMin, "xmax": extent.XMax, "ymin": extent.YMin, "ymax": extent.YMax }
                        gdelt_events += client.query_bbox(eventDate.date(), bbox, limit)
            else:
                gdelt_events = client.query(eventDate.date(), limit)
            workspace = gdelt_workspace(workspacePath)
            feature_factory = gdelt_feature_factory()
            gdelt_features = [feature_factory.create_feature(gdelt_event) for gdelt_event in gdelt_events]
            if (areas_of_interests):
                workspace.insert_features(tableName, gdelt_features, areas_of_interests)
            else:
                workspace.insert_features(tableName, gdelt_features)
            arcpy.AddMessage("GDELT records were inserted into the feature class.")
        except BaseException as ex:
            arcpy.AddError(ex)
        finally:
            del client
        return



class MakeLayerFromGraphGdeltTool(object):
    def __init__(self):
        """Make a layer from GDELT"""
        self.label = "Make layer from GDELT knowledge graph entries"
        self.description = "Queries the GDELT knowledge graph and saves the result as a layer."
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

        theme = arcpy.Parameter(
            displayName="Theme",
            name="theme",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        theme.filter.list = [
            "ARMEDCONFLICT", "ARREST", "ASSASSINATION", 
            "BLACK_MARKET", 
            "CEASEFIRE", "CORRUPTION", "CYBER_ATTACK",
            "DELAY", "DEMOCRACY",
            "ECON_COST_OF_LIVING", "ECON_IDENTITYTHEFT", "ECON_STOCKMARKET",
            "ENV_CLIMATECHANGE",
            "EVACUATION",
            "EXTREMISM",
            "GENERAL_HEALTH",
            "IMMIGRATION",
            "INTERNET_BLACKOUT",
            "JIHAD",
            "KILL",
            "MEDICAL",
            "MILITARY",
            "NATURAL_DISASTER",
            "REFUGEES",
            "STRIKE",
            "TAX_DISEASE",
            "TERROR",
            "VANDALIZE",
            "WOUND"]

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
        outFeatures.value = "Events_{0}".format(str(datetime.date.today()).replace("-", ""))

        inFeatures = arcpy.Parameter(
            displayName="Input features",
            name="in_features",
            datatype="GPFeatureRecordSetLayer",
            parameterType="Optional",
            direction="Input"
        )

        params = [eventDate, theme, limit, outFeatures, inFeatures]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if (parameters[0].altered):
            parameters[3].value = "Themes_{0}".format(str(parameters[0].value.date()).replace("-", ""))
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """Creates a new GDELT client and queries the GDELT knowledge graph."""

        eventDate = parameters[0].value
        theme = parameters[1].valueAsText
        limit = parameters[2].value
        outFeatures = parameters[3].valueAsText
        workspacePath = os.path.dirname(outFeatures)
        tableName = os.path.basename(outFeatures).rstrip(os.path.splitext(outFeatures)[1])

        inFeatures = parameters[4].value
        areas_of_interests = None
            
        client = gdelt_client()
        try:
            if (inFeatures):
                gdelt_graph_records = []
                inCatalogPath = arcpy.Describe(inFeatures).catalogPath
                wgs84 = arcpy.SpatialReference(4326)
                areas_of_interests = []
                with arcpy.da.SearchCursor(inCatalogPath, ["SHAPE@"], spatial_reference=wgs84) as cursor:
                    for inFeature in cursor:
                        geometry = inFeature[0]
                        areas_of_interests.append(geometry)
                        gdelt_graph_records += client.query_graph(eventDate.date(), theme, limit)
            else:
                gdelt_graph_records = client.query_graph(eventDate.date(), theme, limit)
            workspace = gdelt_workspace(workspacePath)
            feature_factory = gdelt_feature_factory()
            gdelt_features = [feature_factory.create_feature(gdelt_graph_record) for gdelt_graph_record in gdelt_graph_records]
            if (areas_of_interests):
                workspace.insert_graph_features(tableName, gdelt_features, areas_of_interests)
            else:
                workspace.insert_graph_features(tableName, gdelt_features)
            arcpy.AddMessage("GDELT graph records were inserted into the feature class.")
        except BaseException as ex:
            arcpy.AddError(ex)
        finally:
            del client
        return