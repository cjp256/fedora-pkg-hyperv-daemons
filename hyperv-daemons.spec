# HyperV KVP daemon binary name
%global hv_kvp_daemon hypervkvpd
# HyperV VSS daemon binary name
%global hv_vss_daemon hypervvssd
# HyperV FCOPY daemon binary name
%global hv_fcopy_daemon hypervfcopyd
# snapshot version
%global snapver .20150702git
# use hardened build
%global _hardened_build 1

Name:     hyperv-daemons
Version:  0
Release:  0.12%{?snapver}%{?dist}
Summary:  HyperV daemons suite

Group:    System Environment/Daemons
License:  GPLv2
URL:      http://www.kernel.org

# Source files obtained from kernel upstream 4.2-rc0 (4da3064d1775810f10f7ddc1c34c3f1ff502a654)
# git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
# The daemon and scripts are located in "master branch - /tools/hv"
# COPYING -> https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/tree/COPYING?id=b1940cd21c0f4abdce101253e860feff547291b
Source0:  COPYING

# HYPERV KVP DAEMON
# hv_kvp_daemon.c -> https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/plain/tools/hv/hv_kvp_daemon.c?id=4da3064d1775810f10f7ddc1c34c3f1ff502a654
Source1:  hv_kvp_daemon.c
# hv_get_dhcp_info.sh -> https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/plain/tools/hv/hv_get_dhcp_info.sh?id=4da3064d1775810f10f7ddc1c34c3f1ff502a654
Source2:  hv_get_dhcp_info.sh
# hv_get_dns_info.sh -> https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/plain/tools/hv/hv_get_dns_info.sh?id=4da3064d1775810f10f7ddc1c34c3f1ff502a654
Source3:  hv_get_dns_info.sh
# hv_set_ifconfig.sh -> https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/plain/tools/hv/hv_set_ifconfig.sh?id=4da3064d1775810f10f7ddc1c34c3f1ff502a654
Source4:  hv_set_ifconfig.sh
Source5:  hypervkvpd.service

# HYPERV VSS DAEMON
# hv_vss_daemon.c -> https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/plain/tools/hv/hv_vss_daemon.c?id=4da3064d1775810f10f7ddc1c34c3f1ff502a654
Source100:  hv_vss_daemon.c
Source101:  hypervvssd.service

# HYPERV FCOPY DAEMON
# hv_fcopy_daemon.c -> https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/plain/tools/hv/hv_fcopy_daemon.c?id=4da3064d1775810f10f7ddc1c34c3f1ff502a654
Source200:  hv_fcopy_daemon.c
Source201:  hypervfcopyd.service


# HYPERV KVP DAEMON
# Correct paths to external scripts ("/usr/libexec/hypervkvpd").
Patch0:   hypervkvpd-0-corrected_paths_to_external_scripts.patch
# rhbz#872566
Patch1:   hypervkvpd-0-long_file_names_from_readdir.patch


# HyperV is available only on x86 architectures
# The base empty (a.k.a. virtual) package can not be noarch
# due to http://www.rpm.org/ticket/78
ExclusiveArch:  i686 x86_64

Requires:       hypervkvpd = %{version}-%{release}
Requires:       hypervvssd = %{version}-%{release}
Requires:       hypervfcopyd = %{version}-%{release}

%description
Suite of daemons that are needed when Linux guest
is running on Windows Host with HyperV.


%package -n hypervkvpd
Summary: HyperV key value pair (KVP) daemon
Group:   System Environment/Daemons
Requires: %{name}-license = %{version}-%{release}
BuildRequires: systemd, kernel-headers
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
BuildRequires: systemd, kernel-headers
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


%package -n hypervfcopyd
Summary: HyperV FCOPY daemon
Group:   System Environment/Daemons
Requires: %{name}-license = %{version}-%{release}
BuildRequires: systemd, kernel-headers
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description -n hypervfcopyd
Hypervfcopyd is an implementation of file copy service functionality
for Linux Guest running on HyperV. The daemon enables host to copy
a file (over VMBUS) into the Linux Guest. The daemon first registers
with the kernel driver. After this is done it waits for instructions 
from Windows Host.


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

cp -pvL %{SOURCE200} hv_fcopy_daemon.c
cp -pvL %{SOURCE201} hypervfcopyd.service

%patch0 -p1 -b .external_scripts
%patch1 -p1 -b .long_names

%build
# HYPERV KVP DAEMON
gcc $RPM_OPT_FLAGS -c hv_kvp_daemon.c
gcc $RPM_LD_FLAGS  hv_kvp_daemon.o -o %{hv_kvp_daemon}

# HYPERV VSS DAEMON
gcc $RPM_OPT_FLAGS -c hv_vss_daemon.c
gcc $RPM_LD_FLAGS hv_vss_daemon.o -o %{hv_vss_daemon}

# HYPERV FCOPY DAEMON
gcc $RPM_OPT_FLAGS -c hv_fcopy_daemon.c
gcc $RPM_LD_FLAGS hv_fcopy_daemon.o -o %{hv_fcopy_daemon}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sbindir}
install -p -m 0755 %{hv_kvp_daemon} %{buildroot}%{_sbindir}
install -p -m 0755 %{hv_vss_daemon} %{buildroot}%{_sbindir}
install -p -m 0755 %{hv_fcopy_daemon} %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_unitdir}
# Systemd unit file
install -p -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE101} %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE201} %{buildroot}%{_unitdir}
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


%post -n hypervfcopyd
%systemd_post hypervfcopyd.service

%postun -n hypervfcopyd
%systemd_postun hypervfcopyd.service

%preun -n hypervfcopyd
%systemd_preun hypervfcopyd.service


%files
# the base package does not contain any files.

%files -n hypervkvpd
%{_sbindir}/%{hv_kvp_daemon}
%{_unitdir}/hypervkvpd.service
%dir %{_libexecdir}/%{hv_kvp_daemon}
%{_libexecdir}/%{hv_kvp_daemon}/*
%dir %{_sharedstatedir}/hyperv

%files -n hypervvssd
%{_sbindir}/%{hv_vss_daemon}
%{_unitdir}/hypervvssd.service

%files -n hypervfcopyd
%{_sbindir}/%{hv_fcopy_daemon}
%{_unitdir}/hypervfcopyd.service

%files license
%doc COPYING

%changelog
* Thu Jul 02 2015 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.12.20150702git
- Rebase to 4.2-rc0 (20150702 git snapshot)
- Switch to new chardev-based communication layer (#1195029)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.11.20150108git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 08 2015 Vitaly Kuznetsov <vkuznets@redhat.com> - 0-0.10.20150108git
- Rebase to 3.19-rc3 (20150108 git snapshot)
- Drop 'nodaemon' patches, use newly introduced '-n' option

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.9.20140714git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 14 2014 Tomas Hozza <thozza@redhat.com> - 0-0.8.20140714git
- Update the File copy daemon to the latest git snapshot
- Fix hyperfcopyd.service to check for /dev/vmbus/hv_fcopy

* Wed Jun 11 2014 Tomas Hozza <thozza@redhat.com> - 0-0.7.20140611git
- Fix FTBFS (#1106781)
- Use kernel-headers instead of kernel-devel for building
- package new Hyper-V fcopy daemon as hypervfcopyd sub-package

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.6.20140219git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 19 2014 Tomas Hozza <thozza@redhat.com> - 0-0.5.20140219git
- rebase to the latest git snapshot next-20140219
  - KVP, VSS: removed inclusion of linux/types.h
  - VSS: Ignore VFAT mounts during freeze operation

* Fri Jan 10 2014 Tomas Hozza <thozza@redhat.com> - 0-0.4.20131022git
- provide 'hyperv-daemons' package for convenient installation of all daemons

* Tue Oct 22 2013 Tomas Hozza <thozza@redhat.com> - 0-0.3.20131022git
- rebase to the latest git snapshot next-20130927 (obtained 2013-10-22)
  - KVP, VSS: daemon use single buffer for send/recv
  - KVP: FQDN is obtained on start and cached

* Fri Sep 20 2013 Tomas Hozza <thozza@redhat.com> - 0-0.2.20130826git
- Use 'hypervkvpd' directory in libexec for KVP daemon scripts (#1010268)
- daemons are now WantedBy multi-user.target instead of basic.target (#1010260)

* Mon Aug 26 2013 Tomas Hozza <thozza@redhat.com> - 0-0.1.20130826git
- Initial package
