%global modulename semver

%global npmlib_dir %{_prefix}/lib/npm-library
%global nodejs_dir %{nodejs_sitelib}

%define __requires_exclude_from ^%{npmlib_dir}/%{modulename}/%{version}/tests?/.*

Name:           npmlib-semver
Version:        5.6.0
Release:        0.3%{?dist}
Summary:        The semantic version parser used by npm.

License:        ISC
URL:            https://github.com/npm/node-semver#readme
Source0:        https://registry.npmjs.org/semver/-/semver-5.6.0.tgz


BuildRequires:  nodejs-packaging

BuildArch:      noarch
ExclusiveArch:  %{nodejs_arches} noarch


Requires:       npmlib(%{modulename}) = %{version}

%description
The semantic version parser used by npm.

This package is a hand-written spec used to bootstrap npmlib-packaging.

%package 5.6.0
Summary:        The semantic version parser used by npm.
Provides:       npmlib(semver) = %{version}

%description 5.6.0
The semantic version parser used by npm.

This package is a hand-written spec used to bootstrap npmlib-packaging.

%prep
%autosetup -p0 -n package

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{npmlib_dir}/%{modulename}/%{version}
cp -pr bin %{buildroot}%{npmlib_dir}/%{modulename}/%{version}
cp -pr package.json %{buildroot}%{npmlib_dir}/%{modulename}/%{version}
cp -pr range.bnf %{buildroot}%{npmlib_dir}/%{modulename}/%{version}
cp -pr semver.js %{buildroot}%{npmlib_dir}/%{modulename}/%{version}

mkdir -p %{buildroot}%{_bindir}
ln -s %{npmlib_dir}/%{modulename}/%{version}/bin/semver %{buildroot}/%{_bindir}/semver


mkdir -p %{buildroot}%{nodejs_dir}
ln -s %{npmlib_dir}/%{modulename}/%{version} %{buildroot}/%{nodejs_dir}/%{modulename}

%files
%doc README.md
%license LICENSE
%{_bindir}/semver
%{nodejs_dir}/%{modulename}

%files 5.6.0
%doc README.md
%license LICENSE
%{npmlib_dir}/%{modulename}/%{version}
%dir %{npmlib_dir}/%{modulename}/

%changelog
* Fri Nov 16 2018 David Shea <dshea@redhat.com> - 5.6.0-0.3
- bootstrap package
