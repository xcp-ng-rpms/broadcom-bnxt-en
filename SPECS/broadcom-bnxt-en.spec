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
Version: 1.10.0_216.0.119.1
Release: 1%{?dist}
License: GPL

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-broadcom-bnxt-en/archive?at=1.10.0_216.0.119.1&format=tgz&prefix=driver-broadcom-bnxt-en-1.10.0_216.0.119.1#/broadcom-bnxt-en-1.10.0_216.0.119.1.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-broadcom-bnxt-en/archive?at=1.10.0_216.0.119.1&format=tgz&prefix=driver-broadcom-bnxt-en-1.10.0_216.0.119.1#/broadcom-bnxt-en-1.10.0_216.0.119.1.tar.gz) = 6062a8fb465543a6dda689f50ed0b04363b5c064


BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n driver-%{name}-%{version}

%build
%{?cov_wrap} %{__make} KVER=%{kernel_version}

%install
%{?cov_wrap} %{__make} PREFIX=%{buildroot} KVER=%{kernel_version} BCMMODDIR=/lib/modules/%{kernel_version}/%{module_dir} DEPMOD=/bin/true install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+wx

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

%changelog
* Wed May 20 2020 Tim Smith <tim.smith@citrix.com> - 1.10.0_216.0.119.1-1
- CP-32954 Update broadcom-bnxt-en driver to 1.10.0_216.0.119.1-1

* Tue Jan 22 2019 Deli Zhang <deli.zhang@citrix.com> - 1.10.0-1
- CP-30070: Upgrade broadcom-bnxt-en driver to version 1.10.0
