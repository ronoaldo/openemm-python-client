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
import datetime
import logging

logging.basicConfig(level=logging.INFO)

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

class TestCampaignMethods(unittest.TestCase):

    def test_SendCampaign(self):
        client = openemm.Connect('test', 'test')
        
        mailinglist_id = 1
        sender_name = 'Acme, Inc'
        sender_address = 'acme@example.com'
        reply_to_name = 'Customer Care'
        reply_to_address = 'customercare@example.com'
        subject = '[News] Great updates from our testing campaign'
        content = '<h1>Hello, world</h1>'
        
        # Create a new mailing
        mailing_id = client.service.AddMailing(
            'test-campaign-2014-01-01', # Campaign short name
            'Sample test campaign', # Campaign description
            mailinglist_id, # Target mailing list id
            [], # List of target group ids
            'all', # Match all target groups
            'regular', # Regular campaign
            subject, # Mailing subject
            sender_name,
            sender_address,
            reply_to_name,
            reply_to_address,
            'utf-8', # Content charset
            0, # Automatic linefeed column setup
            'online-html', # Display as online-html, no attachments
            'bottom' # Tracking pixel at bottom
        )
        logging.info("New mailing added: %s" % mailing_id)

        # Add mailing content
        content_id = client.service.AddContentBlock(
            mailing_id,
            'emailHtml',
            None,
            content,
            1,
        )
        logging.info("Added content-block %s" % content_id)

        # Schedule sending for now
        send_date = datetime.datetime.now() + datetime.timedelta(24)
        logging.info("Sending new mailing at %s" % send_date)
        client.service.SendMailing(
            mailing_id,
            'world',
            send_date.strftime('%Y-%m-%d %H:%M:%S GMT'),
            0, # Block size
            0  # Use default stepping
        )
        logging.info("New mailing schedule to be sent.")

if __name__ == '__main__':
    unittest.main()
