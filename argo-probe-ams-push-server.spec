%define dir /usr/libexec/argo/probes/ams-push-server

Name: argo-probe-ams-push-server
Summary: Probes for ARGO AMS Push Server.
Version: 0.1.0
Release: 1%{?dist}
License: ASL 2.0
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Group: Network/Monitoring
BuildArch: noarch
BuildRequires:  python3-devel
Requires:       python3-requests

%description
This package includes probes for ARGO AMS Push Server component.

%prep
%setup -q

%build
%{py3_build}

%install
install --directory --mode 755 $RPM_BUILD_ROOT/%{_localstatedir}/spool/argo/argo-probe-ams-push-server
%{py3_install "--record=INSTALLED_FILES" }

%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root,-)
%{python3_sitelib}/argo_probe_ams_push_server
%{dir}
%{_localstatedir}/spool/argo/argo-probe-ams-push-server


%changelog
* Mon Jan 27 2025 Angelos Tsalapatis <agelostsal@admin.grnet.gr> - 0.1.0-1%{dist}
- Introduction of the ams push server probe package