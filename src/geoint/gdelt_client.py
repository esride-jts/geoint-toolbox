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
