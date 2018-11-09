Name:           npmlib-packaging
Version:        1.0.4
Release:        1%{?dist}
Summary:        An improved framework for packaging npm modules

License:        GPLv2+
URL:            https://github.com/dashea/npmlib-packaging
Source0:        %{name}-%{version}.tgz

# piggyback on the old macros etc for now
Requires:       nodejs-packaging

# Pin to specific versions of the npm deps, since there's no way to
# bootstrap auto-generated requires
%global semver_version 5.6.0
Requires:       npmlib(semver) = %{semver_version}

BuildArch:      noarch
ExclusiveArch:  %{nodejs_arches} noarch

%description
This packaging contains RPM macros and other utilities for packaging
Node.js modules from npm. To generate packages using this framework,
use npm2spec.

%prep
%setup -q -n package

%build
# nothing to build

%install
mkdir -p %{buildroot}%{_prefix}/lib/npm-library/npmlib-packaging/%{version}/node_modules
cp -r rpm %{buildroot}%{_prefix}/lib/npm-library/npmlib-packaging/%{version}
# bootstrap the deps
ln -s %{_prefix}/lib/npm-library/semver/%{semver_version} %{buildroot}%{_prefix}/lib/npm-library/npmlib-packaging/%{version}/node_modules/semver

mkdir -p %{buildroot}%{_rpmconfigdir}
mkdir -p %{buildroot}%{_rpmmacrodir}
mkdir -p %{buildroot}%{_fileattrsdir}

ln -s %{_prefix}/lib/npm-library/npmlib-packaging/%{version}/rpm/macros.d/macros.npmlib %{buildroot}%{_rpmmacrodir}/macros.npmlib
ln -s %{_prefix}/lib/npm-library/npmlib-packaging/%{version}/rpm/fileattrs/npmlib.attr %{buildroot}%{_fileattrsdir}/npmlib.attr
ln -s %{_prefix}/lib/npm-library/npmlib-packaging/%{version}/rpm/npmlib.prov %{buildroot}%{_rpmconfigdir}/npmlib.prov
ln -s %{_prefix}/lib/npm-library/npmlib-packaging/%{version}/rpm/npmlib.req %{buildroot}%{_rpmconfigdir}/npmlib.req
ln -s %{_prefix}/lib/npm-library/npmlib-packaging/%{version}/rpm/npmlib-symlink-deps %{buildroot}%{_rpmconfigdir}/npmlib-symlink-deps

%files
%doc README.md
%license COPYING
%dir %{_prefix}/lib/npm-library/
%{_prefix}/lib/npm-library/npmlib-packaging/%{version}
%{_rpmmacrodir}/macros.npmlib
%{_fileattrsdir}/npmlib.attr
%{_rpmconfigdir}/npmlib.prov
%{_rpmconfigdir}/npmlib.req
%{_rpmconfigdir}/npmlib-symlink-deps

%changelog
* Fri Nov  9 2018 David Shea <dshea@redhat.com> - 1.0.4-1
- See git log for changes
