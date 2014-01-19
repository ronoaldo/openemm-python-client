#!/usr/bin/env python

# Copyright 2014 Ronoaldo JLP (http://www.ronoaldo.net)
# 
#   Licensed under the Apache License, Version 2.0 (the 'License');
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an 'AS IS' BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import unittest
import openemm

class TestSubscriberMethods(unittest.TestCase):
    """
    Integration tests on a local OpenEMM instance.
    """

    TEST_EMAIL = 'test@example.com'

    def test_SubscriptionManagement(self):
        client = openemm.Connect('test', 'test')

        parameters = {
            'email': self.TEST_EMAIL,
            'mailtype': '2',
            'gender': '0',
        }

        customerId = client.service.AddSubscriber(True, 'email', False,
                openemm.EncodeMap(client, parameters))
        self.assertTrue(customerId is not None)

        foundId = client.service.FindSubscriber('email', self.TEST_EMAIL)
        self.assertEquals(customerId, foundId)

        subscriber = client.service.GetSubscriber(customerId)
        has_gender = False
        for item in subscriber.parameters.item:
            if item.key == 'gender':
                self.assertEquals('0', item.value)
                has_gender = True
        self.assertTrue(has_gender)

if __name__ == '__main__':
    unittest.main()
