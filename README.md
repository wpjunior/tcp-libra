TCP/Libra
-----

Simple TCP/IP Load balancer written in python (tornado)

Instalation
-----------

pip install tcp-libra


Running
-------

tcp-libra


API
---

GET localhost:4001/api/reals
----------------------------

List all reals

output:

[{"available": true, "connections": 0, "host": "localhost", "id": 1, "port": 8080}, {"available": true, "connections": 0, "host": "localhost", "id": 2, "port": 8080}]


POST localhost:4001/api/reals
-----------------------------

Create a real

Curl example:
curl -H "Content-Type: application/json" -XPOST http://localhost:4001/api/reals -d'{"host": "localhost", "port": 8080}'

output:
{"available": true, "connections": 0, "host": "localhost", "id": 2, "port": 8080}


DELETE localhost:4001/api/reals/:id
-----------------------------------

Delete a real

Curl example:
curl-json -XDELETE http://localhost:4001/api/reals/1
