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

class gdelt_workspace(object):
    """Represents a simple feature workspace hosting feature classes.
    """

    def __init__(self, path):
        self._path = path

    def insert_features(self, table_name, gdelt_features):
        """Inserts a bunch of GDELT features into a feature class of this workspace.
        """
        (feature_class, fields) = self._create_gdelt_feature_class(table_name)
        field_names = ["SHAPE@"] + [field[0] for field in fields]
        with arcpy.da.InsertCursor(feature_class, field_names) as insert_cursor:
            for gdelt_feature in gdelt_features:
                insert_cursor.insertRow(gdelt_feature)

    def _create_gdelt_feature_class(self, table_name):
        feature_class_result = arcpy.management.CreateFeatureclass(self._path, table_name, geometry_type="POINT", spatial_reference=4326)
        feature_class = feature_class_result[0]
        fields = self._create_fields()
        arcpy.management.AddFields(feature_class, fields)
        return (feature_class, fields)

    def _create_fields(self):
        return [
            ["ID", "LONG", "Unique ID"],
            ["Fullname", "TEXT", "Action location", 255]
        ]
