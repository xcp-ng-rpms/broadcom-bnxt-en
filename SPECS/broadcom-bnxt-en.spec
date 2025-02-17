%global package_speccommit 6d87d73326a77175defc8bf1deeb5cf036bbd493
%global usver 1.10.2_223.0.183.0
%global xsver 2
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit 1.10.2_223.0.183.0
%define vendor_name Broadcom
%define vendor_label broadcom
%define driver_name bnxt-en

%if %undefined module_dir
%define module_dir updates
%endif

## kernel_version will be set during build because then kernel-devel
## package installs an RPM macro which sets it. This check keeps
## rpmlint happy.
%if %undefined kernel_version
%define kernel_version dummy
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 1.10.2_223.0.183.0
Release: %{?xsrel}%{?dist}
License: GPL
Source0: broadcom-bnxt-en-1.10.2_223.0.183.0.tar.gz
Patch0: Fix-GSO-type-for-HW-GRO-packets-on-5750X-chips.patch

BuildRequires: gcc
BuildRequires: kernel-devel
%{?_cov_buildrequires}
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{name}-%{version}
%{?_cov_prepare}

%build
%{?_cov_wrap} %{__make} KVER=%{kernel_version}

%install
%{?_cov_wrap} %{__make} PREFIX=%{buildroot} KVER=%{kernel_version} BCMMODDIR=/lib/modules/%{kernel_version}/%{module_dir} DEPMOD=/bin/true install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+wx

%{?_cov_install}

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%{?_cov_results_package}

%changelog
* Fri Dec 06 2024 Alex Brett <alex.brett@cloud.com> - 1.10.2_223.0.183.0-2
- CA-401596: Backport patch to fix GSO type for HW GRO packets on 5750X chips

* Thu Jun 29 2023 Stephen Cheng <stephen.cheng@citrix.com> - 1.10.2_223.0.183.0-1
- CP-43650: Update broadcom-bnxt-en driver to version 1.10.2_223.0.183.0

* Wed Aug 24 2022 Zhuangxuan Fei <zhuangxuan.fei@citrix.com> - 1.10.1_216.1.123.0-1
- CP-40163: Update broadcom-bnxt-en driver to version 1.10.1_216.1.123.0-1

* Mon Feb 14 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.10.0_216.0.119.1-3
- CP-38416: Enable static analysis

* Wed Dec 02 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.10.0_216.0.119.1-2
- CP-35517: Fix build for koji

* Wed May 20 2020 Tim Smith <tim.smith@citrix.com> - 1.10.0_216.0.119.1-1
- CP-32954 Update broadcom-bnxt-en driver to 1.10.0_216.0.119.1-1

* Tue Jan 22 2019 Deli Zhang <deli.zhang@citrix.com> - 1.10.0-1
- CP-30070: Upgrade broadcom-bnxt-en driver to version 1.10.0
