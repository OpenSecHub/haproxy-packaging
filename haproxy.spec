##############################################################################
#                                                                            #
#                             HAproxy Packaging                              #
#                                                                            #
##############################################################################

Name:           haproxy
Version:        2.7.9
Release:        1%{?dist}
Summary:        The Reliable, High Performance TCP/HTTP Load Balancer
Group:          Proxy
License:        GPL-3.0+ and LGPL-2.1+
Url:            http://www.haproxy.org/
Vendor:         w@1wt.eu
BuildArch:      x86_64
ExclusiveArch:  x86_64
Packager:       https://github.com/OpenSecHub/haproxy-packaging

AutoReqProv:    yes
BuildRequires:  readline-devel
BuildRequires:  pcre-devel,pcre-static
BuildRequires:  openssl-devel
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(libsystemd)
 
Requires:       systemd
Requires:       openssl-libs
Requires:       pcre >= 8.32

%define LuaVersion 5.4.4

Source0:        http://www.haproxy.org/download/2.7/src/haproxy-2.7.9.tar.gz
Source1:        http://www.lua.org/ftp/lua-%{LuaVersion}.tar.gz
Source2:        haproxy.cfg
Source3:        haproxy.service




%description
HAProxy is a free, very fast and reliable reverse-proxy offering high availability,
load balancing, and proxying for TCP and HTTP-based applications.
It is particularly suited for very high traffic web sites and powers a significant 
portion of the world's most visited ones. Over the years it has become the de-facto 
standard opensource load balancer, is now shipped with most mainstream Linux distributions, 
and is often deployed by default in cloud platforms.



##############################################################################
#                                                                            #
#                             Expand Sources                                 #
#                                                                            #
##############################################################################
%prep
%setup -q -b 1

##############################################################################
#                                                                            #
#                                   Build                                    #
# https://github.com/haproxy/haproxy/blob/master/INSTALL                     #
##############################################################################

%build

### build lua
pushd .
cd ../lua-%{LuaVersion}
make linux
make install INSTALL_TOP=`pwd`/lua
popd

### build haproxy for linux
make -j $(nproc) TARGET=linux-glibc   \
                 USE_DL=1             \
                 USE_TFO=1            \
                 USE_NS=1             \
                 USE_GETADDRINFO=1    \
                 USE_PCRE=1           \
                 USE_PCRE_JIT=1       \
                 USE_STATIC_PCRE=1    \
                 USE_LIBCRYPT=1       \
                 USE_OPENSSL=1        \
                 USE_SYSTEMD=1        \
                 USE_SLZ=1            \
                 USE_LUA=1                              \
                 LUA_LIB_NAME=lua                       \
                 LUA_LIB=../lua-%{LuaVersion}/lua/lib   \
                 LUA_INC=../lua-%{LuaVersion}/lua/include


%install
%make_install PREFIX=/usr           \
              SBINDIR=/usr/sbin     \
              MANDIR=/usr/share/man \
              DOCDIR=/usr/share/doc/haproxy

install -d -m 0750 %{buildroot}/etc/haproxy/
install -d -m 0750 %{buildroot}/%{_unitdir}
install -d -m 0750 %{buildroot}/var/lib/haproxy
install -p -m 0644 %{SOURCE2} %{buildroot}/etc/haproxy/
install -p -m 0644 %{SOURCE3} %{buildroot}/%{_unitdir}


%pre
# Create the haproxy group if it doesn't exists
if ! id -g haproxy > /dev/null 2>&1; then
  groupadd -r haproxy
fi
# Create the haproxy user if it doesn't exists
if ! id -u haproxy > /dev/null 2>&1; then
  useradd -g haproxy -G haproxy -d /var/lib/haproxy -r -s /usr/sbin/nologin haproxy
fi
%systemd_post haproxy.service



%post
%systemd_post haproxy.service



%preun
%systemd_preun haproxy.service



%postun
# If the package is been uninstalled
if [ $1 = 0 ];then
  # Remove the haproxy user if it exists
  if id -u haproxy > /dev/null 2>&1; then
    userdel haproxy >/dev/null 2>&1
  fi
  # Remove the haproxy group if it exists
  if id -g haproxy > /dev/null 2>&1; then
    groupdel haproxy >/dev/null 2>&1
  fi
else
  %systemd_postun_with_restart haproxy.service
fi



%files
%defattr(-,root,root,-)
%license LICENSE
/usr/sbin/haproxy
/usr/share/man/man1/haproxy.1.gz
%doc /usr/share/doc/haproxy/*
%{_unitdir}/haproxy.service
%config(noreplace) /etc/haproxy/haproxy.cfg
%dir /var/lib/haproxy



%changelog
* Thu Jun 08 2023 lgbxyz@gmail.com
- Release version %{version}:
  * https://github.com/haproxy/haproxy/blob/master/CHANGELOG

