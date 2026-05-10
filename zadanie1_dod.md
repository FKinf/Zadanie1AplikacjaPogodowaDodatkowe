# Zadanie 1 NieObowiązkowe— Technologie Chmurowe

**Autor:** Filip Kwietniak 

**Repozytorium GitHub:** https://github.com/FKinf/Zadanie1AplikacjaPogodowaDodatkowe

**Obraz DockerHub:** https://hub.docker.com/repository/docker/fkinf/weather-app/general
---


Wybrany poziom trudności do 3

**Utworzenie nowego buildera na sterowniku docker-container:**

docker buildx create --name zadaniedodbuilder --driver docker-container --driver-opt network=host --bootstrap
wynik: 

[+] Building 2.6s (1/1) FINISHED
 => [internal] booting buildkit                                                                                  2.6s
 => => pulling image moby/buildkit:buildx-stable-1                                                               1.8s
 => => creating container buildx_buildkit_zadaniedodbuilder0                                                     0.8s
zadaniedodbuilder


**Sprawdzenie czy builder obsługuje obie wymagane platformy:**

docker buildx use zadaniedodbuilder
docker buildx inspect --bootstrap
wynik:
Name:          zadaniedodbuilder
Driver:        docker-container
Last Activity: 2026-05-10 19:05:43 +0000 UTC

Nodes:
Name:                  zadaniedodbuilder0
Endpoint:              unix:///var/run/docker.sock
Driver Options:        network="host"
Status:                running
BuildKit daemon flags: --allow-insecure-entitlement=network.host
BuildKit version:      v0.29.0
Platforms:             linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/arm64, linux/riscv64, linux/ppc64le, linux/s390x, linux/386, linux/mips64le, linux/mips64, linux/loong64, linux/arm/v7, linux/arm/v6


**Plik dockerfile.multiarch wykorzystujący frontend BuildKit umożliwiający klonowanie kodu został umieszony w repozytorium.**


**Przygotwanie klucza SSH**

Identity added: /home/filip/.ssh/gh_cli_tchlab6_ed25519 (email)
256 SHA256:xQvgyTtKOHokWle0xo************ <email> (ED25519)


**Budowanie obrazu z wykorzystaniem eksportera registry oraz backend-u registry w trybie max**

docker buildx build --builder zadaniedodbuilder --platform linux/amd64,linux/arm64 --ssh default --cache-to type=registry,ref=fkinf/weather-app:cache,mode=max --cache-from type=registry,ref=fkinf/weather-app:cache --tag fkinf/weather-app:latest --push -f Dockerfile.multiarch .
wynik:

[+] Building 257.7s (35/35) FINISHED                                                                           docker-container:zadaniedodbuilder
 => [internal] load build definition from Dockerfile.multiarch                                                                               0.0s
 => => transferring dockerfile: 1.41kB                                                                                                       0.0s
 => resolve image config for docker-image://docker.io/docker/dockerfile:1.7                                                                  0.6s
 => CACHED docker-image://docker.io/docker/dockerfile:1.7@sha256:a57df69d0ea827fb7266491f2813635de6f17269be881f696fbfdf2d83dda33e            0.0s
 => => resolve docker.io/docker/dockerfile:1.7@sha256:a57df69d0ea827fb7266491f2813635de6f17269be881f696fbfdf2d83dda33e                       0.0s
 => [linux/amd64 internal] load metadata for docker.io/library/python:3.12-slim                                                              0.5s
 => [linux/arm64 internal] load metadata for docker.io/library/python:3.12-slim                                                              0.3s
 => [internal] load .dockerignore                                                                                                            0.0s
 => => transferring context: 2B                                                                                                              0.0s
 => ERROR importing cache manifest from fkinf/weather-app:cache                                                                              0.5s
 => [linux/amd64 final 1/7] FROM docker.io/library/python:3.12-slim@sha256:ec948fa5f90f4f8907e89f4800cfd2d2e91e391a4bce4a6afa77ba265bc3a2fe  0.0s
 => => resolve docker.io/library/python:3.12-slim@sha256:ec948fa5f90f4f8907e89f4800cfd2d2e91e391a4bce4a6afa77ba265bc3a2fe                    0.0s
 => [linux/arm64 final 1/7] FROM docker.io/library/python:3.12-slim@sha256:ec948fa5f90f4f8907e89f4800cfd2d2e91e391a4bce4a6afa77ba265bc3a2fe  0.0s
 => => resolve docker.io/library/python:3.12-slim@sha256:ec948fa5f90f4f8907e89f4800cfd2d2e91e391a4bce4a6afa77ba265bc3a2fe                    0.0s
 => CACHED [linux/arm64 final 2/7] RUN adduser --disabled-password --gecos "" appuser                                                        0.0s
 => CACHED [linux/arm64 final 3/7] WORKDIR /app                                                                                              0.0s
 => CACHED [linux/amd64 final 2/7] RUN adduser --disabled-password --gecos "" appuser                                                        0.0s
 => CACHED [linux/amd64 final 3/7] WORKDIR /app                                                                                              0.0s
 => CACHED [linux/amd64 builder 2/6] WORKDIR /app                                                                                            0.0s
 => CACHED [linux/amd64 builder 3/6] RUN apt-get update && apt-get install -y --no-install-recommends git openssh-client     && rm -rf /var  0.0s
 => CACHED [linux/amd64 builder 4/6] RUN mkdir -p /root/.ssh &&     ssh-keyscan github.com >> /root/.ssh/known_hosts                         0.0s
 => CACHED [linux/amd64 builder 5/6] RUN --mount=type=ssh     git clone git@github.com:FKinf/Zadanie1AplikacjaPogodowaDodatkowe.git .        0.0s
 => CACHED [linux/amd64 builder 6/6] RUN --mount=type=cache,target=/root/.cache/pip     pip install --no-cache-dir --prefix=/install -r app  0.0s
 => CACHED [linux/amd64 final 4/7] COPY --from=builder /install /usr/local                                                                   0.0s
 => CACHED [linux/amd64 final 5/7] COPY --from=builder /app/app/ .                                                                           0.0s
 => CACHED [linux/amd64 final 6/7] COPY --from=builder /app/app/templates/ ./templates/                                                      0.0s
 => CACHED [linux/amd64 final 7/7] RUN chown -R appuser:appuser /app                                                                         0.0s
 => CACHED [linux/arm64 builder 2/6] WORKDIR /app                                                                                            0.0s
 => [linux/arm64 builder 3/6] RUN apt-get update && apt-get install -y --no-install-recommends git openssh-client     && rm -rf /var/lib/  125.5s
 => [linux/arm64 builder 4/6] RUN mkdir -p /root/.ssh &&     ssh-keyscan github.com >> /root/.ssh/known_hosts                                5.0s 
 => [linux/arm64 builder 5/6] RUN --mount=type=ssh     git clone git@github.com:FKinf/Zadanie1AplikacjaPogodowaDodatkowe.git .               3.7s 
 => [linux/arm64 builder 6/6] RUN --mount=type=cache,target=/root/.cache/pip     pip install --no-cache-dir --prefix=/install -r app/requi  74.0s 
 => [linux/arm64 final 4/7] COPY --from=builder /install /usr/local                                                                          0.1s 
 => [linux/arm64 final 5/7] COPY --from=builder /app/app/ .                                                                                  0.1s 
 => [linux/arm64 final 6/7] COPY --from=builder /app/app/templates/ ./templates/                                                             0.1s 
 => [linux/arm64 final 7/7] RUN chown -R appuser:appuser /app                                                                                0.3s 
 => exporting to image                                                                                                                      21.4s 
 => => exporting layers                                                                                                                      0.9s 
 => => exporting manifest sha256:f1a08ed0f8f1f31df3c99f0f66a00b386e14c92e8584d4e0e17d38931ae6f710                                            0.0s
 => => exporting config sha256:d56c690bf9b5016a5a1babc2ae4f158f6c4529ef8d35e59ac0e0198de0552d3f                                              0.0s
 => => exporting attestation manifest sha256:d4d1d55ffac64ce800f4171882176a9fe37b1def0fecd358308ec5ecb297b446                                0.0s
 => => exporting manifest sha256:ec8a0da4091565d0c4eec0d2275fefbb5604a35091338a485700e49871df9a6f                                            0.0s
 => => exporting config sha256:4e901517dedf4165bb709b5c68a43f3d048c63d19973fa2d690406f8eb50cf5b                                              0.0s
 => => exporting attestation manifest sha256:ab00c010c923cbb9e33f13aaebfacc5b86ab232e96180520cdb91d03ead8b64b                                0.0s
 => => exporting manifest list sha256:d05440af38281bf3246cf4a4a0ff486fb49b9f90fc61dd6281ade06353f835df                                       0.0s
 => => pushing layers                                                                                                                       15.4s
 => => pushing manifest for docker.io/fkinf/weather-app:latest@sha256:d05440af38281bf3246cf4a4a0ff486fb49b9f90fc61dd6281ade06353f835df       4.9s
 => exporting cache to registry                                                                                                             45.5s
 => => preparing build cache for export                                                                                                     15.2s
 => => sending cache export                                                                                                                 30.3s
 => => writing layer sha256:03ce5a201283786d8fee8cbef4941f2ae6176ae6d684a1226a6fcff64dd0032b                                                 2.0s
 => => writing layer sha256:06185850ed3336fcd84aed8aa5a082a4262604bea3335c8805d7977f1e12eddc                                                 0.8s
 => => writing layer sha256:00347e1fa32fa7430f0c0c53f6b09daaad5ac682793a230264849651c876f316                                                 0.8s
 => => writing layer sha256:31b91bd35ca917f78335164ebff64a2e9181d9f54856dc31a43e8f8b2b8c8375                                                 1.2s
 => => writing layer sha256:368609fd37ed147b0593ecda9d652c261e0c9d54c4dca995da147bb4e82327f9                                                 1.2s
 => => writing layer sha256:39c6ed9287cd3e2bae77dfeb04d264e4dcf70ed517b260a6405708228f728a83                                                 0.3s
 => => writing layer sha256:3f1525dcf3b52674d5aa17504c7786270033ca28151022b56b0ebd3a5d53fc5c                                                11.6s
 => => writing layer sha256:4d279c951f9d428876fb79d5372ca40f0c68c152590625e627f4b0e55456080f                                                 0.1s
 => => writing layer sha256:4ea9d2fbf76ded2045014f04dd924a047822b13c05d999eb8bab1c6d3bfe857d                                                 5.8s
 => => writing layer sha256:4f4fb700ef54461cfa02571ae0db9a0dc1e0cdb5577484a6d75e68dc38e8acc1                                                 0.0s
 => => writing layer sha256:57fb71246055257a374deb7564ceca10f43c2352572b501efc08add5d24ebb61                                                 0.1s
 => => writing layer sha256:5a4bba030a4e7d84809d6a15917a33fa4a6ae9c355e82a39cede70abe2836c82                                                 0.1s
 => => writing layer sha256:759e0c85a86e6d82ceccf351143d3f4a17e4ba196c9684240898abe3b8ec13a9                                                 0.1s
 => => writing layer sha256:6e78bf62b21cf7444f4f5eb820f4ec4bbc28f9a03b36f5cac42cf70c009bc42f                                                 1.1s
 => => writing layer sha256:78dd7fa10051811fb732fd71f698f0369dfda32c475f00b631ad6f042bd2b367                                                 0.1s
 => => writing layer sha256:797809503061a7d1332e7b5c3df030896846f0a6a179f90060e85564dca1cf65                                                 0.1s
 => => writing layer sha256:8ba4a7ba167169f2aebc1c43730d586ce45a4a207e0540db8dd7f1330f9806b7                                                 0.1s
 => => writing layer sha256:9211ef59ca24d77cea1778cfe7a10491887e969ee4b7b0fbc24329d6511b1400                                                 0.1s
 => => writing layer sha256:9659c6f28df5f8c1e1220cbc2a4cca4563c57e1522a422a8e577730a362bbaba                                                24.0s
 => => writing layer sha256:97e3d73b2d9f0d0a6c119c6e22eb7368104e0866e103a4c1c3189bd7e8ff235e                                                 0.2s
 => => writing layer sha256:9ebf9a1d0c9ca1bcb377e9dba38a3fdd3e89cf37164f4245286c24f8cd50a39e                                                 0.3s
 => => writing layer sha256:a0835c23b443d9f549c48872c17873cd7967508c3a1a1439b201e3ea48db430b                                                 0.2s
 => => writing layer sha256:a14292ff3e4fdb0e28a13aba631a3171ca69cf3beebab3abbbe9915035dbffda                                                 1.7s
 => => writing layer sha256:b33ff618953dcb6177e78bc33883a49817e571a1d9f0a3aa039e3228e0f21684                                                 0.3s
 => => writing layer sha256:ba7bdcf9fc798bad17be17fe7db5f33acdf53a681bf60d9e1bdf8906203d7e44                                                 3.0s
 => => writing layer sha256:be513e2c6b2cc8e5703fb841f9a8d034ec4bba39cc3b2c86ae285f8075b8481d                                                 0.2s
 => => writing layer sha256:cadafacd1d6b5e7151a17d73518501ddd084056246079581b4a02795b87fffd5                                                 0.1s
 => => writing layer sha256:cb3c183a046355b37541422a2b19f16b59a8d75fea9ca6beb4853b119d1fce56                                                 0.1s
 => => writing config sha256:5ea35fff35c5916fc06410652138b1ff370652f35fbb57b1bf6d374833fa5d48                                                1.3s
 => => writing cache image manifest sha256:30ea70ef66b36d7631ebe7e17493879782a475652bc915bc2a049eca4300567d                                  2.0s
 => [auth] fkinf/weather-app:pull,push token for registry-1.docker.io                                                                        0.0s
 => [auth] fkinf/weather-app:pull,push token for registry-1.docker.io                                                                        0.0s
------
 > importing cache manifest from fkinf/weather-app:cache:
------



**Weryfikacja działania cache**

docker buildx build --builder zadaniedodbuilder --platform linux/amd64,linux/arm64 --ssh default --cache-to type=registry,ref=fkinf/weather-app:cache,mode=max --cache-from type=registry,ref=fkinf/weather-app:cache --tag fkinf/weather-app:latest --push -f Dockerfile.multiarch .
wynik:

+] Building 10.2s (37/37) FINISHED                                                                            docker-container:zadaniedodbuilder
 => [internal] load build definition from Dockerfile.multiarch                                                                               0.0s
 => => transferring dockerfile: 1.41kB                                                                                                       0.0s
 => resolve image config for docker-image://docker.io/docker/dockerfile:1.7                                                                  1.0s
 => [auth] docker/dockerfile:pull token for registry-1.docker.io                                                                             0.0s
 => CACHED docker-image://docker.io/docker/dockerfile:1.7@sha256:a57df69d0ea827fb7266491f2813635de6f17269be881f696fbfdf2d83dda33e            0.0s
 => => resolve docker.io/docker/dockerfile:1.7@sha256:a57df69d0ea827fb7266491f2813635de6f17269be881f696fbfdf2d83dda33e                       0.0s
 => [linux/amd64 internal] load metadata for docker.io/library/python:3.12-slim                                                              0.5s
 => [linux/arm64 internal] load metadata for docker.io/library/python:3.12-slim                                                              0.4s
 => [auth] library/python:pull token for registry-1.docker.io                                                                                0.0s
 => [internal] load .dockerignore                                                                                                            0.0s
 => => transferring context: 2B                                                                                                              0.0s
 => importing cache manifest from fkinf/weather-app:cache                                                                                    1.5s
 => => inferred cache manifest type: application/vnd.oci.image.manifest.v1+json                                                              0.0s
 => [linux/arm64 final 1/7] FROM docker.io/library/python:3.12-slim@sha256:ec948fa5f90f4f8907e89f4800cfd2d2e91e391a4bce4a6afa77ba265bc3a2fe  0.0s
 => => resolve docker.io/library/python:3.12-slim@sha256:ec948fa5f90f4f8907e89f4800cfd2d2e91e391a4bce4a6afa77ba265bc3a2fe                    0.0s
 => [linux/amd64 builder 1/6] FROM docker.io/library/python:3.12-slim@sha256:ec948fa5f90f4f8907e89f4800cfd2d2e91e391a4bce4a6afa77ba265bc3a2  0.0s
 => => resolve docker.io/library/python:3.12-slim@sha256:ec948fa5f90f4f8907e89f4800cfd2d2e91e391a4bce4a6afa77ba265bc3a2fe                    0.0s
 => [auth] fkinf/weather-app:pull token for registry-1.docker.io                                                                             0.0s
 => CACHED [linux/arm64 final 2/7] RUN adduser --disabled-password --gecos "" appuser                                                        0.0s
 => CACHED [linux/arm64 final 3/7] WORKDIR /app                                                                                              0.0s
 => CACHED [linux/arm64 builder 2/6] WORKDIR /app                                                                                            0.0s
 => CACHED [linux/arm64 builder 3/6] RUN apt-get update && apt-get install -y --no-install-recommends git openssh-client     && rm -rf /var  0.0s
 => CACHED [linux/arm64 builder 4/6] RUN mkdir -p /root/.ssh &&     ssh-keyscan github.com >> /root/.ssh/known_hosts                         0.0s
 => CACHED [linux/arm64 builder 5/6] RUN --mount=type=ssh     git clone git@github.com:FKinf/Zadanie1AplikacjaPogodowaDodatkowe.git .        0.0s
 => CACHED [linux/arm64 builder 6/6] RUN --mount=type=cache,target=/root/.cache/pip     pip install --no-cache-dir --prefix=/install -r app  0.0s
 => CACHED [linux/arm64 final 4/7] COPY --from=builder /install /usr/local                                                                   0.0s
 => CACHED [linux/arm64 final 5/7] COPY --from=builder /app/app/ .                                                                           0.0s
 => CACHED [linux/arm64 final 6/7] COPY --from=builder /app/app/templates/ ./templates/                                                      0.0s
 => CACHED [linux/arm64 final 7/7] RUN chown -R appuser:appuser /app                                                                         0.4s
 => CACHED [linux/amd64 final 2/7] RUN adduser --disabled-password --gecos "" appuser                                                        0.0s
 => CACHED [linux/amd64 final 3/7] WORKDIR /app                                                                                              0.0s
 => CACHED [linux/amd64 builder 2/6] WORKDIR /app                                                                                            0.0s
 => CACHED [linux/amd64 builder 3/6] RUN apt-get update && apt-get install -y --no-install-recommends git openssh-client     && rm -rf /var  0.0s
 => CACHED [linux/amd64 builder 4/6] RUN mkdir -p /root/.ssh &&     ssh-keyscan github.com >> /root/.ssh/known_hosts                         0.0s
 => CACHED [linux/amd64 builder 5/6] RUN --mount=type=ssh     git clone git@github.com:FKinf/Zadanie1AplikacjaPogodowaDodatkowe.git .        0.0s
 => CACHED [linux/amd64 builder 6/6] RUN --mount=type=cache,target=/root/.cache/pip     pip install --no-cache-dir --prefix=/install -r app  0.0s
 => CACHED [linux/amd64 final 4/7] COPY --from=builder /install /usr/local                                                                   0.0s
 => CACHED [linux/amd64 final 5/7] COPY --from=builder /app/app/ .                                                                           0.0s
 => CACHED [linux/amd64 final 6/7] COPY --from=builder /app/app/templates/ ./templates/                                                      0.0s
 => CACHED [linux/amd64 final 7/7] RUN chown -R appuser:appuser /app                                                                         0.4s
 => exporting to image                                                                                                                       6.3s


**Weryfikacja manifestu**

docker buildx imagetools inspect fkinf/weather-app:latest
wynik:

Name:      docker.io/fkinf/weather-app:latest
MediaType: application/vnd.oci.image.index.v1+json
Digest:    sha256:d05440af38281bf3246cf4a4a0ff486fb49b9f90fc61dd6281ade06353f835df
           
Manifests: 
  Name:        docker.io/fkinf/weather-app:latest@sha256:f1a08ed0f8f1f31df3c99f0f66a00b386e14c92e8584d4e0e17d38931ae6f710
  MediaType:   application/vnd.oci.image.manifest.v1+json
  Platform:    linux/amd64
               
  Name:        docker.io/fkinf/weather-app:latest@sha256:ec8a0da4091565d0c4eec0d2275fefbb5604a35091338a485700e49871df9a6f
  MediaType:   application/vnd.oci.image.manifest.v1+json
  Platform:    linux/arm64
               


**Weryfikacja obrazu cache na registry**

docker buildx imagetools inspect fkinf/weather-app:cache
wynik:

Name:      docker.io/fkinf/weather-app:cache
MediaType: application/vnd.oci.image.manifest.v1+json
Digest:    sha256:30ea70ef66b36d7631eb****************************

**Skanowanie podatności CVE(trivy)**

trivy image fkinf/weather-app:latest

wynik:

fkinf/weather-app:latest (debian 13.4)

Total: 112 (UNKNOWN: 0, LOW: 63, MEDIUM: 42, HIGH: 7, CRITICAL: 0)

Brak podaności „Critical”

Uzasadnie podatności critical:
Wszystkie 7 podatności HIGH pochodzą wyłącznie z obrazu bazowego python:3.12-slim (Debian 13.4), a nie z kodu aplikacji ani zainstalowanych pakietów Pythona.

CVE-2026-4878 - Wymaga lokalnego dostępu do systemu plików z uprawnieniami do zmiany atrybutów plików. Aplikacja działa jako niepriwilegowany użytkownik „appuser” bez uprawnień do cap_set_file().
CVE-2025-69720 - biblioteka ncurses nie jest używana przez aplikację Flask/gunicorn. Podatność wymaga interaktywnego terminala, lecz kontener nie udostępnia terminala.

CVE-2026-29111 - systemd nie działa w kontenerze Docker — brak procesu init. Podatność dotyczy komunikacji IPC przez D-Bus, który jest niedostępny w środowisku kontenerowym. 

Przy wszystkich „podatnościach” kolumna „fixed version” jest pusta co oznacza że Debian 13 nie ma jeszcze poprawek

























