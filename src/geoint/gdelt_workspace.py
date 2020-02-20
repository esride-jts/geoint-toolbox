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
        Swallows any exception during insert row!
        """
        (feature_class, fields) = self._create_gdelt_feature_class(table_name)
        field_names = ["SHAPE@"] + [field[0] for field in fields]
        with arcpy.da.InsertCursor(feature_class, field_names) as insert_cursor:
            for gdelt_feature in gdelt_features:
                try:
                    insert_cursor.insertRow(gdelt_feature)
                except BaseException as ex:
                    print(ex)

    def _create_gdelt_feature_class(self, table_name):
        feature_class_result = arcpy.management.CreateFeatureclass(self._path, table_name, geometry_type="POINT", spatial_reference=4326)
        feature_class = feature_class_result[0]
        fields = self._create_fields()
        arcpy.management.AddFields(feature_class, fields)
        return (feature_class, fields)

    def _create_fields(self):
        return [
            ["GlobalEventId", "LONG"],
            ["Day", "LONG"],
            ["MonthYear", "LONG"],
            ["Year", "LONG"],
            ["FractionDate", "DOUBLE"],
            ["Actor1Code", "TEXT", "Actor1Code", 255],
            ["Actor1Name", "TEXT", "Actor1Name", 255],
            ["Actor1CountryCode", "TEXT", "Actor1CountryCode", 255],
            ["Actor1KnownGroupCode", "TEXT", "Actor1KnownGroupCode", 255],
            ["Actor1EthnicCode", "TEXT", "Actor1EthnicCode", 255],
            ["Actor1Religion1Code", "TEXT", "Actor1Religion1Code", 255],
            ["Actor1Religion2Code", "TEXT", "Actor1Religion2Code", 255],
            ["Actor1Type1Code", "TEXT", "Actor1Type1Code", 255],
            ["Actor1Type2Code", "TEXT", "Actor1Type2Code", 255],
            ["Actor1Type3Code", "TEXT", "Actor1Type3Code", 255],
            ["Actor2Code", "TEXT", "Actor2Code", 255],
            ["Actor2Name", "TEXT", "Actor2Name", 255],
            ["Actor2CountryCode", "TEXT", "Actor2CountryCode", 255],
            ["Actor2KnownGroupCode", "TEXT", "Actor2KnownGroupCode", 255],
            ["Actor2EthnicCode", "TEXT", "Actor2EthnicCode", 255],
            ["Actor2Religion1Code", "TEXT", "Actor2Religion1Code", 255],
            ["Actor2Religion2Code", "TEXT", "Actor2Religion2Code", 255],
            ["Actor2Type1Code", "TEXT", "Actor2Type1Code", 255],
            ["Actor2Type2Code", "TEXT", "Actor2Type2Code", 255],
            ["Actor2Type3Code", "TEXT", "Actor2Type3Code", 255],
            ["IsRootEvent", "LONG"],
            ["EventCode", "TEXT", "EventCode", 255],
            ["EventBaseCode", "TEXT", "EventBaseCode", 255],
            ["EventRootCode", "TEXT", "EventRootCode", 255],
            ["QuadClass", "LONG"],
            ["GoldsteinScale", "DOUBLE"],
            ["NumMentions", "LONG"],
            ["NumSources", "LONG"],
            ["NumArticles", "LONG"],
            ["AvgTone", "DOUBLE"],
            ["Actor1Geo_Type", "LONG"],
            ["Actor1Geo_Fullname", "TEXT", "Actor1Geo_Fullname", 1000],
            ["Actor1Geo_CountryCode", "TEXT", "Actor1Geo_CountryCode", 255],
            ["Actor1Geo_ADM1Code", "TEXT", "Actor1Geo_ADM1Code", 255],
            ["Actor1Geo_ADM2Code", "TEXT", "Actor1Geo_ADM2Code", 255],
            ["Actor1Geo_Lat", "DOUBLE"],
            ["Actor1Geo_Long", "DOUBLE"],
            ["Actor1Geo_FeatureID", "TEXT", "Actor1Geo_FeatureID", 255],
            ["Actor2Geo_Type", "LONG"],
            ["Actor2Geo_FullName", "TEXT", "Actor2Geo_FullName", 1000],
            ["Actor2Geo_CountryCode", "TEXT", "Actor2Geo_CountryCode", 255],
            ["Actor2Geo_ADM1Code", "TEXT", "Actor2Geo_ADM1Code", 255],
            ["Actor2Geo_ADM2Code", "TEXT", "Actor2Geo_ADM2Code", 255],
            ["Actor2Geo_Lat", "DOUBLE"],
            ["Actor2Geo_Long", "DOUBLE"],
            ["Actor2Geo_FeatureID", "TEXT", "Actor2Geo_FeatureID", 255],
            ["ActionGeo_Type", "LONG"],
            ["ActionGeo_FullName", "TEXT", "ActionGeo_FullName", 1000],
            ["ActionGeo_CountryCode", "TEXT", "ActionGeo_CountryCode", 255],
            ["ActionGeo_ADM1Code", "TEXT", "ActionGeo_ADM1Code", 255],
            ["ActionGeo_ADM2Code", "TEXT", "ActionGeo_ADM2Code", 255],
            ["ActionGeo_Lat", "DOUBLE"],
            ["ActionGeo_Long", "DOUBLE"],
            ["ActionGeo_FeatureID", "TEXT", "ActionGeo_FeatureID", 255],
            ["DATEADDED", "TEXT", "DATEADDED", 255],
            ["SOURCEURL", "TEXT", "SOURCEURL", 1000]
        ]
