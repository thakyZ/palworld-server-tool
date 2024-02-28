FROM python:3.10.11-bullseye AS Builder

ARG branch

ENV py_site_packages=/usr/local/lib/python3.10/site-packages

RUN python -m pip install --upgrade pip setuptools
RUN pip install wheel cython pyinstaller>=5.7.0
RUN git clone --depth=1 -b ${branch} https://github.com/thakyz/palworld-server-tool --recurse-submodule /palworld-server-tool
WORKDIR /palworld-server-tool/module
RUN ls -ld
RUN ls -l
RUN pip install --no-cache -r ./requirements.txt
RUN mkdir ./dist
RUN pyinstaller --onefile ./sav_cli.py -n sav_cli_linux_aarch64

FROM scratch

COPY --from=Builder /palworld-server-tool/module/dist/sav_cli_linux_aarch64 /sav_cli_linux_aarch64
