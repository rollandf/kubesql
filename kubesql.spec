%global provider        github
%global provider_tld    com
%global project         yaacov
%global repo            kubesql
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}

%undefine _missing_build_ids_terminate_build
%define debug_package %{nil}

Name:           %{repo}
Version:        0.1.17
Release:        1%{?dist}
Summary:        kubesql uses sql like language to query the Kubernetes cluster manager
License:        Apache
URL:            https://%{import_path}
Source0:        https://github.com/yaacov/kubesql/archive/%{version}.tar.gz

BuildRequires:  git
BuildRequires:  golang >= 1.2.8

%description
kubesql let you select Kubernetes resources based on the value of one or more resource fields, using human readable easy to use SQL like query langauge.

%prep
%setup -q -n kubesql-%{version}

%build
# set up temporary build gopath, and put our directory there
mkdir -p ./_build/src/github.com/yaacov
ln -s $(pwd) ./_build/src/github.com/yaacov/kubesql

make

%install
install -d %{buildroot}%{_bindir}
install -p -m 0755 ./kubesql %{buildroot}%{_bindir}/kubesql

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_bindir}/kubesql

%changelog

* Thu Feb 22 2020 Yaacov Zamir <kobi.zamir@gmail.com> 0.1.17-1
- Add config option

* Thu Feb 22 2020 Yaacov Zamir <kobi.zamir@gmail.com> 0.1.16-1
- Fix parsing of anotations

* Thu Feb 22 2020 Yaacov Zamir <kobi.zamir@gmail.com> 0.1.15-1
- Fix parsing of labels and anotations

* Thu Feb 22 2020 Yaacov Zamir <kobi.zamir@gmail.com> 0.1.14-1
- Fix parsing of numbers

* Thu Feb 22 2020 Yaacov Zamir <kobi.zamir@gmail.com> 0.1.13-1
- Parse dates and booleans

* Thu Feb 20 2020 Yaacov Zamir <kobi.zamir@gmail.com> 0.1.12-1
- No debug rpm

* Thu Feb 20 2020 Yaacov Zamir <kobi.zamir@gmail.com> 0.1.11-1
- Initial RPM release
