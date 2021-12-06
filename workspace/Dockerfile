FROM ubuntu:20.04

ENV TZ=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ARG UID=1000
ARG GID=1000
ARG NAME=user
ENV DEFAULT_PWD=abcd

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install apt-utils software-properties-common
RUN add-apt-repository ppa:git-core/ppa

RUN apt-get update && apt-get upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install sudo vim git nano wget openssh-server
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python3.8 python3-pip

ADD server_requirements.txt /tmp
RUN pip3 install -r /tmp/server_requirements.txt

RUN groupadd -g $GID -o $NAME
RUN useradd -u ${UID} -m -s /bin/bash -g ${NAME} -G plugdev ${NAME} && \
	echo "${NAME} ALL = NOPASSWD: ALL" > /etc/sudoers.d/${NAME} && \
    chmod 0440 /etc/sudoers.d/${NAME}
RUN chown -R ${NAME}:${NAME} /home/${NAME}
RUN echo "${NAME}:${DEFAULT_PWD}" | chpasswd

RUN ln -s /workspace /home/${NAME}/workspace

RUN echo "Port 22" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin no" >> /etc/ssh/sshd_config
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN /etc/init.d/ssh restart
EXPOSE 22

CMD [ "/usr/sbin/sshd" , "-D" ]
