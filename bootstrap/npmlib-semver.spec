Name:           npmlib-semver
Version:        5.6.0
Release:        0.1%{?dist}
Summary:        The semantic version parser used by npm.

License:        ISC
URL:            https://github.com/npm/node-semver
Source0:        https://registry.npmjs.org/semver/-/semver-%{version}.tgz

BuildRequires:  nodejs-packaging

BuildArch:      noarch
ExclusiveArch:  %{nodejs_arches} noarch

Requires:       npmlib(semver) = %{version}

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
%setup -q -n package

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_prefix}/lib/npm-library/semver/%{version}
cp -pr bin package.json range.bnf semver.js %{buildroot}%{_prefix}/lib/npm-library/semver/%{version}/

mkdir -p %{buildroot}%{_bindir}
ln -s %{_prefix}/lib/npm-library/semver/%{version}/bin/semver %{buildroot}/%{_bindir}/semver

mkdir -p %{buildroot}%{nodejs_sitelib}
ln -s %{_prefix}/lib/npm-library/semver/%{version} %{buildroot}/%{nodejs_sitelib}/semver

%files
%doc README.md
%license LICENSE
%{nodejs_sitelib}/semver
%{_bindir}/semver

%files 5.6.0
%doc README.md
%license LICENSE
%{_prefix}/lib/npm-library/semver/%{version}

%changelog
* Thu Oct 25 2018 David Shea <dshea@redhat.com> - 5.6.0-0.1
- Initial bootstrap package
