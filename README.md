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

You must setup the `openemm.WSDL` and `openmm.LOCATION` variables,
used to perform some operations on client setup. A basic workflow
would be:

	import openemm
	openemm.WSDL = 'http://....'
	openemm.LOCATIN = 'http://...'
	client = openemm.Connect('username', 'password')
	subscriberId = client.service.FindSubscriber(
		'email', 'bob@example.com')

Please referr to the [openemm webservices documentation][WSDoc]
for a full reference on the API methods. Optionally, you can quick
dump the method signatures by 'printing' the client:

	print client

## Handling Map and MapItem

Some methods on OpenEMM requires a special `Map` parameter. This
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

You can take advantage of [my openemm fork][OpenemmFork] that contains
some goodies for seting up a local development server.

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
[OpenEMM documentation][AdminGuide] on how to setup the database.

[OpenemmFork]: https://github.com/ronoaldo/openemm/
[AdminGuide]: http://sourceforge.net/projects/openemm/files/OpenEMM%20documentation/Documentation%20%28latest%20versions%29/OpenEMM-2013_InstallAdminGuide_1.1.pdf/download
[WSDoc]: http://sourceforge.net/projects/openemm/files/OpenEMM%20documentation/Documentation%20%28latest%20versions%29/Webservice-API_2.0_EN_1.1.2.pdf/download
