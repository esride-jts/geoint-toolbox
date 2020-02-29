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

import datetime
from google.cloud import bigquery

class gdelt_event(object):
    """Represents a GDELT event record.
    """

    def __init__(self, record):
        self.__id = record.GLOBALEVENTID
        self.__location = (record.ActionGeo_Long, record.ActionGeo_Lat)
        self.__fullname = record.ActionGeo_FullName
        self.__values = [value for value in record]

        # DATEADDED creates a C-long overflow
        # must be treated as a string!
        self.__values[59] = str(self.__values[59])

    def __get_id(self):
        return self.__id

    def __set_id(self, id):
        self.__id = id

    def __get_location(self):
        return self.__location

    def __set_location(self, location):
        self.__location == location

    def __get_fullname(self):
        return self.__fullname

    def __set_fullname(self, fullname):
        self.__fullname = fullname

    def __get_values(self):
        return self.__values

    id = property(__get_id, __set_id)

    location = property(__get_location, __set_location)

    fullname = property(__get_fullname, __set_fullname)

    values = property(__get_values)



class gdelt_graph_record(object):
    """Represents a GDELT knowledge graph record.
    """

    def __init__(self, values):
        self.__id = values[0]
        self.__location = (float(values[7]), float(values[6]))
        self.__values = values

        # DATE creates a C-long overflow
        # must be treated as a string!
        self.__values[8] = str(self.__values[8])

    def __get_id(self):
        return self.__id

    def __get_location(self):
        return self.__location

    def __get_values(self):
        return self.__values

    id = property(__get_id)

    location = property(__get_location)
    
    values = property(__get_values)



class gdelt_graph_entry(object):
    """Represents an entry in the GDELT knowledge graph.
    """

    def __init__(self, record):
        self.__records = []
        locations = record[1].split(";")
        for location in locations:
            values = [record[0]]
            location_values = location.split("#")
            values += location_values[:7]
            values += [value for value in record[2:]]
            try:
                self.__records.append(gdelt_graph_record(values))
            except:
                # Swallow any exception like float parsing
                pass

    def __get_records(self):
        return self.__records

    records = property(__get_records)



class gdelt_client(object):
    """Client for accesing the GDELT events table.
    """
    
    def __init__(self):
        self._client = bigquery.Client()

    def __del__(self):
        # Close works with version 1.24.0
        # We had to downgrade to version 1.22.0
        # See https://github.com/esride-jts/geoint-toolbox/issues/2
        #self._client.close()
        del self._client

    def query(self, date, limit=1000):
        """Queries the GDELT events table partitioned using a days restricted on a specific date.
        """
        query = ("SELECT * "
                 "FROM `gdelt-bq.gdeltv2.events_partitioned` WHERE DATE(_PARTITIONTIME) = "
                 "'{0}' AND ActionGeo_Lat IS NOT NULL AND ActionGeo_Long IS NOT NULL LIMIT {1}".format(date, limit)
                 )
        query_job = self._client.query(query)
        return [gdelt_event(record) for record in query_job.result()]

    def query_bbox(self, date, bbox, limit=1000):
        """Queries the GDELT events table partitioned using a days restricted on a specific date and a bounding box.
        """
        query = ("SELECT * "
                 "FROM `gdelt-bq.gdeltv2.events_partitioned` WHERE DATE(_PARTITIONTIME) = "
                 "'{0}' AND ActionGeo_Lat IS NOT NULL AND ActionGeo_Long IS NOT NULL "
                 "AND ActionGeo_Long >= {1} AND ActionGeo_Long <= {2} AND ActionGeo_Lat >= {3} AND ActionGeo_Lat <= {4} LIMIT {5}".format(date, bbox["xmin"], bbox["xmax"], bbox["ymin"], bbox["ymax"], limit)
                 )
        query_job = self._client.query(query)
        return [gdelt_event(record) for record in query_job.result()]

    def query_today(self, limit=1000):
        """Queries the GDELT events table from today.
        """
        return self.query(datetime.date.today(), limit)

    def query_yesterday(self, limit=1000):
        """Queries the GDELT events table from yesterday.
        """
        return self.query((datetime.datetime.now()-datetime.timedelta(days=1)).date(), limit)

    def query_graph(self, date, theme, limit=1000):
        """Queries the global knowledge graph by using a specific date and a theme.
        """
        query = ("SELECT GKGRECORDID, V2Locations, DATE, SourceCommonName, DocumentIdentifier "
                 "FROM `gdelt-bq.gdeltv2.gkg_partitioned` WHERE DATE(_PARTITIONTIME) = "
                 "'{0}' AND V2Locations IS NOT NULL AND V2Themes LIKE '%{1}%' LIMIT {2}".format(date, theme, limit)
                 )
        query_job = self._client.query(query)
        return [record for graph_record in query_job.result() for record in gdelt_graph_entry(graph_record).records]