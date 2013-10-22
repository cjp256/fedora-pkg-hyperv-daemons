# HyperV KVP daemon binary name
%global hv_kvp_daemon hypervkvpd
# HyperV VSS daemon binary name
%global hv_vss_daemon hypervvssd
# snapshot version
%global snapver .20131022git
# use hardened build
%global _hardened_build 1

Name:     hyperv-daemons
Version:  0
Release:  0.3%{?snapver}%{?dist}
Summary:  HyperV daemons suite

Group:    System Environment/Daemons
License:  GPLv2
URL:      http://www.kernel.org

# Source files obtained from kernel upstream 2013-10-22.
# git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
# The daemon and scripts are located in "master branch - /tools/hv"
# COPYING -> https://git.kernel.org/cgit/linux/kernel/git/next/linux-next.git/plain/COPYING?id=refs/tags/next-20130822
Source0:  COPYING

# HYPERV KVP DAEMON
# hv_kvp_daemon.c -> https://git.kernel.org/cgit/linux/kernel/git/next/linux-next.git/plain/tools/hv/hv_kvp_daemon.c?id=refs/tags/next-20130927
Source1:  hv_kvp_daemon.c
# hv_get_dhcp_info.sh -> https://git.kernel.org/cgit/linux/kernel/git/next/linux-next.git/plain/tools/hv/hv_get_dhcp_info.sh?id=refs/tags/next-20130927
Source2:  hv_get_dhcp_info.sh
# hv_get_dns_info.sh -> https://git.kernel.org/cgit/linux/kernel/git/next/linux-next.git/plain/tools/hv/hv_get_dns_info.sh?id=refs/tags/next-20130927
Source3:  hv_get_dns_info.sh
# hv_set_ifconfig.sh -> https://git.kernel.org/cgit/linux/kernel/git/next/linux-next.git/plain/tools/hv/hv_set_ifconfig.sh?id=refs/tags/next-20130927
Source4:  hv_set_ifconfig.sh
Source5:  hypervkvpd.service

# HYPERV VSS DAEMON
# hv_vss_daemon.c -> https://git.kernel.org/cgit/linux/kernel/git/next/linux-next.git/plain/tools/hv/hv_vss_daemon.c?id=refs/tags/next-20130927
Source100:  hv_vss_daemon.c
Source101:  hypervvssd.service

# HYPERV KVP DAEMON
# Correct paths to external scripts ("/usr/libexec/hypervkvpd").
Patch0:   hypervkvpd-0-corrected_paths_to_external_scripts.patch
# use quoted include for linux/hyperv.h because we use gcc option
# -iquote for include PATH where it is located. This is because
# some headers in system include PATH are also in kernel-devel
# package.
Patch1:   hypervkvpd-0-include_fix.patch
# rhbz#872566
Patch2:   hypervkvpd-0-long_file_names_from_readdir.patch
# Remove daemon() call and let systemd handle it
Patch3:   hypervkvpd-0-dont_call_deamon.patch

# HYPERV VSS DAEMON
# use quoted include for linux/hyperv.h because we use gcc option
# -iquote for include PATH where it is located. This is because
# some headers in system include PATH are also in kernel-devel
# package.
Patch100:   hypervvssd-0-fix_includes.patch
# Remove daemon() call and let systemd handle it
Patch101:   hypervvssd-0-dont_call_daemon.patch

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# HyperV is available only on x86 architectures
ExclusiveArch:  i686 x86_64
Requires:       hypervkvpd = %{version}-%{release}
Requires:       hypervvssd = %{version}-%{release}

%description
Suite of daemons that are needed when Linux guest
is running on Windows Host with HyperV.


%package -n hypervkvpd
Summary: HyperV key value pair (KVP) daemon
Group:   System Environment/Daemons
Requires: %{name}-license = %{version}-%{release}
BuildRequires: systemd, kernel-devel
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description -n hypervkvpd
Hypervkvpd is an implementation of HyperV key value pair (KVP) 
functionality for Linux. The daemon first registers with the
kernel driver. After this is done it collects information 
requested by Windows Host about the Linux Guest. It also supports
IP injection functionality on the Guest.


%package -n hypervvssd
Summary: HyperV VSS daemon
Group:   System Environment/Daemons
Requires: %{name}-license = %{version}-%{release}
BuildRequires: systemd, kernel-devel
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description -n hypervvssd
Hypervvssd is an implementation of HyperV VSS functionality
for Linux. The daemon is used for host initiated guest snapshot
on HyperV hypervisor. The daemon first registers with the
kernel driver. After this is done it waits for instructions 
from Windows Host if to "freeze" or "thaw" the filesystem
on the Linux Guest.


%package license
Summary:    License of the HyperV daemons suite
Group:      Applications/System
BuildArch:  noarch

%description license
Contains license of the HyperV daemons suite.


%prep
%setup -Tc
cp -pvL %{SOURCE0} COPYING

cp -pvL %{SOURCE1} hv_kvp_daemon.c
cp -pvL %{SOURCE2} hv_get_dhcp_info.sh
cp -pvL %{SOURCE3} hv_get_dns_info.sh
cp -pvL %{SOURCE4} hv_set_ifconfig.sh
cp -pvL %{SOURCE5} hypervkvpd.service

cp -pvL %{SOURCE100} hv_vss_daemon.c
cp -pvL %{SOURCE101} hypervvssd.service

%patch0 -p1 -b .external_scripts
%patch1 -p1 -b .include
%patch2 -p1 -b .long_names
%patch3 -p1 -b .daemon

%patch100 -p1 -b .include
%patch101 -p1 -b .daemon


%build
# kernel-devel version
%{!?kversion: %global kversion `ls %{_usrsrc}/kernels | sort -dr | head -n 1`}

# HYPERV KVP DAEMON
gcc \
    $RPM_OPT_FLAGS \
    -iquote %{_usrsrc}/kernels/%{kversion}/include \
    -c hv_kvp_daemon.c
    
gcc \
    $RPM_LD_FLAGS \
    hv_kvp_daemon.o \
    -o %{hv_kvp_daemon}

# HYPERV VSS DAEMON
gcc \
    $RPM_OPT_FLAGS \
    -iquote %{_usrsrc}/kernels/%{kversion}/include \
    -c hv_vss_daemon.c
    
gcc \
    $RPM_LD_FLAGS \
    hv_vss_daemon.o \
    -o %{hv_vss_daemon}


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sbindir}
install -p -m 0755 %{hv_kvp_daemon} %{buildroot}%{_sbindir}
install -p -m 0755 %{hv_vss_daemon} %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_unitdir}
# Systemd unit file
install -p -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE101} %{buildroot}%{_unitdir}
# Shell scripts for the KVP daemon
mkdir -p %{buildroot}%{_libexecdir}/%{hv_kvp_daemon}
install -p -m 0755 hv_get_dhcp_info.sh %{buildroot}%{_libexecdir}/%{hv_kvp_daemon}/hv_get_dhcp_info
install -p -m 0755 hv_get_dns_info.sh %{buildroot}%{_libexecdir}/%{hv_kvp_daemon}/hv_get_dns_info
install -p -m 0755 hv_set_ifconfig.sh %{buildroot}%{_libexecdir}/%{hv_kvp_daemon}/hv_set_ifconfig
# Directory for pool files
mkdir -p %{buildroot}%{_sharedstatedir}/hyperv


%post -n hypervkvpd
%systemd_post hypervkvpd.service

%preun -n hypervkvpd
%systemd_preun hypervkvpd.service

%postun -n hypervkvpd
# hypervkvpd daemon does NOT support restarting (driver, neither)
%systemd_postun hypervkvpd.service
# If removing the package, delete %%{_sharedstatedir}/hyperv directory
if [ "$1" -eq "0" ] ; then
    rm -rf %{_sharedstatedir}/hyperv || :
fi


%post -n hypervvssd
%systemd_post hypervvssd.service

%postun -n hypervvssd
%systemd_postun hypervvssd.service

%preun -n hypervvssd
%systemd_preun hypervvssd.service


%files -n hypervkvpd
%{_sbindir}/%{hv_kvp_daemon}
%{_unitdir}/hypervkvpd.service
%dir %{_libexecdir}/%{hv_kvp_daemon}
%{_libexecdir}/%{hv_kvp_daemon}/*
%dir %{_sharedstatedir}/hyperv

%files -n hypervvssd
%{_sbindir}/%{hv_vss_daemon}
%{_unitdir}/hypervvssd.service

%files license
%doc COPYING

%changelog
* Tue Oct 22 2013 Tomas Hozza <thozza@redhat.com> - 0-0.3.20131022git
- rebase to the latest git snapshot next-20130927 (obtained 2013-10-22)
  - KVP, VSS: daemon use single buffer for send/recv
  - KVP: FQDN is obtained on start and cached

* Fri Sep 20 2013 Tomas Hozza <thozza@redhat.com> - 0-0.2.20130826git
- Use 'hypervkvpd' directory in libexec for KVP daemon scripts (#1010268)
- daemons are now WantedBy multi-user.target instead of basic.target (#1010260)

* Mon Aug 26 2013 Tomas Hozza <thozza@redhat.com> - 0-0.1.20130826git
- Initial package
