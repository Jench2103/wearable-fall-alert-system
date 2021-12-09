FROM ubuntu:20.04

ARG UID=1000
ARG GID=1000
ARG NAME=user
ARG DEFAULT_PWD=abcd
ARG TZ=Asia/Taipei
ARG VSCODE_SERVER_VERSION=ccbaa2d27e38e5afa3e5c21c1c7bef4657064247

# change timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install apt-utils software-properties-common
RUN add-apt-repository ppa:git-core/ppa

RUN apt-get update && apt-get upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install sudo vim git nano wget locales openssh-server
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python3.8 python3-pip

# add support of locale zh_TW
RUN sed -i 's/# en_US.UTF-8/en_US.UTF-8/g' /etc/locale.gen \
    && sed -i 's/# zh_TW.UTF-8/zh_TW.UTF-8/g' /etc/locale.gen \
    && sed -i 's/# zh_TW BIG5/zh_TW BIG5/g' /etc/locale.gen
RUN locale-gen && dpkg-reconfigure --frontend=noninteractive locales
RUN update-locale LANG=en_US.UTF-8 && update-locale LC_ALL=en_US.UTF-8

# install python modules
ADD server_requirements.txt /tmp
RUN pip3 install -r /tmp/server_requirements.txt

# add non-root user account
RUN groupadd -g $GID -o $NAME
RUN useradd -u ${UID} -m -s /bin/bash -g ${NAME} -G plugdev ${NAME} && \
	echo "${NAME} ALL = NOPASSWD: ALL" > /etc/sudoers.d/${NAME} && \
    chmod 0440 /etc/sudoers.d/${NAME}

# setup vscode server for SSH development
RUN wget -O /tmp/vscode-server-linux-x64.tar.gz https://update.code.visualstudio.com/commit:${VSCODE_SERVER_VERSION}/server-linux-x64/stable
RUN mkdir -p /home/${NAME}/.vscode-server/bin/${VSCODE_SERVER_VERSION}
RUN tar -xf /tmp/vscode-server-linux-x64.tar.gz -C /home/${NAME}/.vscode-server/bin
RUN mv -T /home/${NAME}/.vscode-server/bin/vscode-server-linux-x64 /home/${NAME}/.vscode-server/bin/${VSCODE_SERVER_VERSION}

# user account configuration
RUN ln -s /workspace /home/${NAME}/workspace
ADD ./scripts/.bash_profile /home/${NAME}/
RUN chown -R ${NAME}:${NAME} /home/${NAME}
RUN echo "${NAME}:${DEFAULT_PWD}" | chpasswd

# setup ngrok
ADD ./bin/ngrok /bin/ngrok
RUN chmod 755 /bin/ngrok

# SSH configuration
RUN echo "Port 22" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin no" >> /etc/ssh/sshd_config
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN /etc/init.d/ssh restart
EXPOSE 22

VOLUME /workspace

CMD [ "/usr/sbin/sshd" , "-D" ]
