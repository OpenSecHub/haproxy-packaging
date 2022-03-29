FROM centos:7

# install buildtools and deps
RUN yum -y install epel-release
RUN yum -y install make gcc
RUN yum -y install readline-devel pcre-devel pcre-static openssl-devel systemd-devel
RUN yum -y install rpm-build redhat-rpm-config rpmdevtools systemd-rpm-macros

WORKDIR /

ADD haproxy.spec     /
ADD haproxy.cfg      /
ADD haproxy.service  /

ADD entrypoint.sh    /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
