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

"""
Please set GOOGLE_APPLICATION_CREDENTIALS or explicitly create credentials and re-run the application.
For more information, please see https://cloud.google.com/docs/authentication/getting-started.
"""

import unittest
from geoint.gdelt_client import gdelt_client

class TestGdeltQueries(unittest.TestCase):

    def setUp(self):
        # Recreate the client before any test
        self._client = gdelt_client()

    def test_gdelt_query_today(self):
        gdelt_events = self._client.query_today()
        self.assertIsNotNone(gdelt_events, "The events must not be none!")
        for gdelt_event in gdelt_events:
            self.assertIsNotNone(gdelt_event.id, "The event ID must not be none!")
            self.assertIsNotNone(gdelt_event.location, "The location must not be none!")

    def test_gdelt_query_yesterday(self):
        gdelt_events = self._client.query_yesterday()
        self.assertIsNotNone(gdelt_events, "The events must not be none!")
        for gdelt_event in gdelt_events:
            self.assertIsNotNone(gdelt_event.id, "The event ID must not be none!")
            self.assertIsNotNone(gdelt_event.location, "The location must not be none!")



if "__main__" == __name__:
    unittest.main()