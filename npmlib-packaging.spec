Name:           npmlib-packaging
Version:        1.0.0
Release:        1%{?dist}
Summary:        An improved framework for packaging npm modules

License:        GPLv2+
URL:            https://github.com/dashea/npmlib-packaging
Source0:        %{name}-%{version}.tgz

# piggyback on the old macros etc for now
Requires:       nodejs-packaging

# Pin to specific versions of the npm deps, since there's no way to
# bootstrap auto-generated requires
%global fs_extra_version 7.0.0
%global semver_version 5.6.0
Requires:       npmlib(fs-extra) = %{fs_extra_version}
Requires:       npmlib(semver) = %{semver_version}

%description
This packaging contains RPM macros and other utilities for packaging
Node.js modules from npm. To generate packages using this framework,
use npm2spec.

%prep
%setup -q

%build
# nothing to build

%install
mkdir -p %{buildroot}%{_prefix}/lib/npm-library/npmlib-packaging/node_modules
cp -r rpm %{buildroot}%{_prefix}/lib/npm-library/npmlib-packaging/
# bootstrap the deps
ln -s %{_prefix}/lib/npm-library/fs-extra/%{fs_extra_version} %{buildroot}%{_prefix}/lib/npm-library/npmlib-packaging/node_modules/fs-extra
ln -s %{_prefix}/lib/npm-library/semver/%{semver_version} %{buildroot}%{_prefix}/lib/npm-library/npmlib-packaging/node_modules/semver

mkdir -p %{buildroot}%{_rpmconfigdir}
mkdir -p %{buildroot}%{_rpmmacrodir}
mkdir -p %{buildroot}%{_fileattrsdir}

ln -s %{nodejs_sitelib}/rpm/macros.d/macros.npmlib %{buildroot}%{_rpmmacrodir}/macros.npmlib
ln -s %{nodejs_sitelib}/rpm/fileattrs/npmlib.attr %{buildroot}%{_fileattrsdir}/npmlib.attr
ln -s %{nodejs_sitelib}/rpm/npmlib.prov %{buildroot}%{_rpmconfigdir}/npmlib.prov
ln -s %{nodejs_sitelib}/rpm/npmlib.req %{buildroot}%{_rpmconfigdir}/npmlib.req
ln -s %{nodejs_sitelib}/rpm/npmlib-symlink-deps %{buildroot}%{_rpmconfigdir}/npmlib-symlink-deps

%files
%doc README.md
%license COPYING
%{_prefix}/lib/npm-library/npmlib-packaging/
%{_rpmmacrodir}/macros.npmlib
%{_fileattrsdir}/npmlib.attr
%{_rpmconfigdir}/npmlib.prov
%{_rpmconfigdir}/npmlib.req
%{_rpmconfigdir}/npmlib-symlink-deps

%changelog
* Wed Oct 24 2018 David Shea <dshea@redhat.com> - 1.0.0-1
- Initial package
