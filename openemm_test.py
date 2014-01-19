#!/usr/bin/env python

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
