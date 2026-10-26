$ curl -i http://127.0.0.1:2375/version
HTTP/1.1 200 OK
api-version: 1.56
content-type: application/json
date: Mon, 26 Oct 2026 09:03:09 GMT
docker-experimental: false
ostype: linux
server: Docker/29.9.2 (linux)
transfer-encoding: chunked


$ curl -i -s "http://127.0.0.1:2375/containers/json?all=true"
HTTP/1.1 200 OK
api-version: 1.56
content-type: application/json
date: Mon, 26 Oct 2026 10:05:47 GMT
docker-experimental: false
ostype: linux
server: Docker/29.9.2 (linux)
transfer-encoding: chunked


$ curl -i -s --get http://127.0.0.1:2375/containers/json      --data-urlencode 'all=true'      --data-urlencode 'filters={"label":["adminapi.managed=true"]}'
HTTP/1.1 200 OK
api-version: 1.56
content-type: application/json
date: Mon, 26 Oct 2026 10:06:56 GMT
docker-experimental: false
ostype: linux
server: Docker/29.9.2 (linux)
transfer-encoding: chunked


$ curl -i -s http://127.0.0.1:2375/containers/web1/json
HTTP/1.1 200 OK
api-version: 1.56
content-type: application/json
date: Mon, 26 Oct 2026 10:07:39 GMT
docker-experimental: false
ostype: linux
server: Docker/29.9.2 (linux)
transfer-encoding: chunked



$ curl -s -o /dev/null -w "%{http_code}\n" -X POST http://127.0.0.1:2375/containers/web1/stop
204


$ curl -s -o /dev/null -w "%{http_code}\n" -X POST http://127.0.0.1:2375/containers/web1/stop
304


$ curl -s -o /dev/null -w "%{http_code}\n" -X POST http://127.0.0.1:2375/containers/existepas/stop
404

$ curl -i -s -X POST http://127.0.0.1:8080/api/users/tokens/provision/      -H "Content-Type: application/json" -H "Accept: application/json"      -d '{"username": "admin", "password": "admin"}'
HTTP/1.1 201 Created
content-type: application/json
vary: HX-Request, Accept-Language, Cookie, origin
allow: POST, OPTIONS
x-request-id: ea072440-1673-47f7-8a84-80a072d1f363
api-version: 4.7
x-content-type-options: nosniff
referrer-policy: same-origin
cross-origin-opener-policy: same-origin
x-frame-options: SAMEORIGIN
content-length: 465
content-language: en
server: granian
date: Mon, 26 Oct 2026 10:28:57 GMT


$ curl -i -s -X POST http://127.0.0.1:8080/api/virtualization/cluster-types/ \
     -H "Authorization: Bearer nbt_9CV43twQVEFV.48l0fMxMNUU8bFF4ufOQ6fhVzsyivHDub6jVqhmL" \
     -H "Content-Type: application/json" -H "Accept: application/json" \
     -d '{"name": "Docker", "slug": "docker"}'
HTTP/1.1 201 Created
content-type: application/json
location: http://127.0.0.1:8080/api/virtualization/cluster-types/2/
etag: W/"2026-10-26T10:36:03.294221+00:00"
vary: HX-Request, Accept-Language, Cookie, origin
allow: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
x-request-id: 8db9d026-fda7-4f98-a9c5-3916e4fe8701
api-version: 4.7
x-content-type-options: nosniff
referrer-policy: same-origin
cross-origin-opener-policy: same-origin
x-frame-options: SAMEORIGIN
content-length: 371
content-language: en
server: granian
date: Mon, 26 Oct 2026 10:36:03 GMT



$ curl -i -s -X POST http://127.0.0.1:8080/api/virtualization/clusters/      -H "Authorization: Bearer nbt_9CV43twQVEFV.48l0fMxMNUU8bFF4ufOQ6fhVzsyivHDub6jVqhmL"      -H "Content-Type: application/json" -H "Accept: application/json"      -d '{"name": "docker-local", "type": 2}'
HTTP/1.1 201 Created
content-type: application/json
location: http://127.0.0.1:8080/api/virtualization/clusters/3/
etag: W/"2026-10-26T10:39:06.028593+00:00"
vary: HX-Request, Accept-Language, Cookie, origin
allow: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
x-request-id: 735fee12-1733-4bf1-a2f0-d85e3cbe6767
api-version: 4.7
x-content-type-options: nosniff
referrer-policy: same-origin
cross-origin-opener-policy: same-origin
x-frame-options: SAMEORIGIN
content-length: 719
content-language: en
server: granian
date: Mon, 26 Oct 2026 10:39:06 GMT
