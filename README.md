# Python Client for OpenEMM WS

Simple python client wrapper for the OpenEMM 2.0 WebService, using
the SUDS library.

## Instalation

To install this library run the following commands:

    git clone https://github.com/ronoaldo/openemm-python-client.git
    cd openemm-python-client
    pip install -r requirements.txt

## Basic usage

The API exposes a `Connect` method, that receives the username and
password configured on your OpenEMM instance. This method returns
a valid SUDS client object, exposing all methods on the `service`
attribute.

A basic workflow follows:

    import openemm
    client = openemm.Connect('username', 'password')
    subscriberId = client.service.FindSubscriber('email', 'bob@example.com')

Some methods on OpenEMM requires a special Map parameter. This
requires explicity setting the `xsi:type` value on `key` and `value`
attributes of `MapItem`. SUDS don't performs this by default, but
a SUDS plugin, properly configured on the `Connect` method takes
care of that.

Also, to avoid building the Map manually using the `factory` object,
the API exposes a convenience method that encodes a regular Python
`map`:

    enc_map = openemm.EncodeMap(client, { 'email' : 'bob@example.com' })

See the `openemm_test.py` for details.

## Local testing

You can take advantage of the project at https://github.com/ronoaldo/openemm/,
that contain some goodies for seting up a local development server.

To setup a local OpenEMM server for testing, you will need Maven and a MySQL
server installed.

To start the Web Services app:

    git clone https://github.com/ronoaldo/openemm openemm
    cd openemm
    mvn clean install
    mvn -pl openemm-ws clean tomcat6:run-war

This will checkout, build and start a local OpenEMM server. You have to
properly configure the server with a local MySQL database, using the
scripts under `openemm/src/main/scripts/sql`. Please take a look at the
OpenEMM documentation on how to setup the database, and on the project
bellow for more details on how to build with Maven.
