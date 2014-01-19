#!/usr/bin/env python

import uuid
import datetime
import time

from suds.plugin import MessagePlugin
from suds.client import Client
from suds.wsse import Security, UsernameToken
from hashlib import md5, sha1
from base64 import b64encode
from suds.wsse import UsernameToken, Token
from time import gmtime


WSDL = 'http://localhost:9090/openemm-ws2/emmservices.wsdl'
LOCATION = 'http://localhost:9090/openemm-ws2/'

class MapItemPlugin(MessagePlugin):
    """
    SUDS plugin to properly handle the ns0:Map and ns0:MapItem
    encoding for the OpenEMM API.
    """
    
    def marshalled(self, context):
        """
        Walks over the request Body and properly encodes the
        key and value attributes of MapItem.
        """
        
        body = context.envelope.getChild('Body')
        def v(node):
            if node.name in ['key','value']:
                node.addPrefix('xsd', 'http://www.w3.org/2001/XMLSchema')
                node.addPrefix('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
                node.set('xsi:type', 'xsd:string')
        body.walk(v)

def Connect(username, password):
    """
    Connects to the OpenEMM server at L{LOCATION}, parsing the 
    L{WSDL} using SUDS.

    @ivar username: the openemm webserivce username
    @type username: str
    @ivar password: the openemm webservice password
    @type password: str

    @return a valid L{suds.client.Client} object
    """
    client = Client(WSDL, location=LOCATION, plugins=[MapItemPlugin()])
    # WSSE header authentication handler
    token = UsernameDigestToken(username, password)
    security = Security()
    security.tokens.append(token)
    client.set_options(wsse=security)
    return client

class UsernameDigestToken(UsernameToken):
    """
    Represents a basic I{UsernameToken} WS-Security token with password digest
    @ivar username: A username.
    @type username: str
    @ivar password: A password.
    @type password: str
    @ivar nonce: A set of bytes to prevent reply attacks.
    @type nonce: str
    @ivar created: The token created.
    @type created: L{datetime}

    @doc: http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0.pdf
    """

    def __init__(self, username=None, password=None):
        UsernameToken.__init__(self, username, password)
        self.setcreated()
        self.setnonce()

    def setcreated(self, created=None):
        if created is None:
            # Local offset required to properly validate on server.
            # See discussion here:
            #    http://forum.openemm.org/using-openemm-f3/topic2607.html
            local_offset = time.timezone / 60
            local_offset_delta = datetime.timedelta(minutes=local_offset)
            created = datetime.datetime.utcnow() + local_offset_delta
            created_str = created.strftime('%Y-%m-%dT%H:%M:%SZ')
            self.created = created_str
        else:
            self.created = created

    def setnonce(self, text=None):
        """
        Set I{nonce} which is arbitraty set of bytes to prevent
        reply attacks.
        @param text: The nonce text value.
            Generated when I{None}.
        @type text: str

        @override: Nonce save binary string to build digest password
        """
        if text is None:
            s = []
            s.append(self.username)
            s.append(self.password)
            s.append(Token.sysdate())
            m = md5()
            m.update(':'.join(s))
            self.raw_nonce = m.digest()
            self.nonce = b64encode(self.raw_nonce)
        else:
            self.nonce = text

    def xml(self):
        self.setnonce()
        self.setcreated()
        usernametoken = UsernameToken.xml(self)
        password = usernametoken.getChild('Password')
        nonce = usernametoken.getChild('Nonce')
        created = usernametoken.getChild('Created')
        password.set('Type', 'http://docs.oasis-open.org/wss/2004/01/'
                             'oasis-200401-wss-username-token-profile-1.0'
                             '#PasswordDigest')
        s = sha1()
        s.update(self.raw_nonce)
        s.update(created.getText())
        s.update(password.getText())
        password.setText(b64encode(s.digest()))
        nonce.set('EncodingType', 'http://docs.oasis-open.org/wss/2004'
            '/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary')
        return usernametoken

def EncodeMap(client, parameters):
    """
    Utility function to encode a python map into a Map/MapItem object
    set required on some OpenEMM method calls. 
    
    @ivar client: the SUDS client connected with OpenEMM.
    @type client: suds.client.Client
    @ivar parameters: the python parameter map
    @type parameters: map
    
    @return an object properly encoded as a Map/MapItem structure.
    """
    result = client.factory.create('ns0:Map')
    for k, v in parameters.iteritems():
        entry = client.factory.create('ns0:MapItem')
        entry.key = k
        entry.value = v
        result.item.append(entry)
    return result

if __name__ == '__main__':
    client = Connect('test', 'test')
    print client
