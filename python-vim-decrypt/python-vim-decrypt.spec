%global srcname vim-decrypt

Name:           python-%{srcname}
Version:        2.0.0
Release:        0.4%{?dist}
Summary:        Command line tool for decrypting vim-blowfish-encrypted files
License:        GPL-3.0-or-later
URL:            https://github.com/gertjanvanzwieten/vimdecrypt
Source0:        https://files.pythonhosted.org/packages/04/2e/8a451aa1739b154e2182375a925410154ba4a69bb41b69b57c465fd6d037/%{srcname}-%{version}.tar.gz
# For compatibility with older Python releases
Source1:        setup.py
Source2:        vim-decrypt

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?fedora} || 0%{?amzn} || (0%{?rhel} && 0%{?rhel} >= 10)
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros
%endif
BuildRequires:  python3dist(pytest)
BuildRequires:  python3-blowfish

%global _description %{expand:
This project provides a very simple vimdecrypt Python module for decrypting
blowfish2-encoded file objects, as well as the vimdecrypt command line tool
for decrypting files to stdout.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
Requires:       python3-blowfish

%description -n python3-%{srcname} %_description

%prep
%autosetup -p1 -n %{srcname}-%{version}
# RHEL 8 doesn't support pyproject yet
# RHEL 9 supports pyproject but cannot properly build this release
%if 0%{?amzn} || (0%{?rhel} && 0%{?rhel} <= 9)
cp %{SOURCE1} setup.py
cp %{SOURCE2} vim-decrypt
%endif

%build
%if 0%{?fedora} || (0%{?rhel} && 0%{?rhel} >= 10)
%pyproject_wheel
%else
%py3_build
%endif

%install
%if 0%{?fedora} || (0%{?rhel} && 0%{?rhel} >= 10)
%pyproject_install
%else
%py3_install
%endif

# fix rpmlint: non-executable-script
sed --in-place '/#!\/usr\/bin\/env/d' %{buildroot}%{python3_sitelib}/vimdecrypt.py

%check
%pytest

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/*
%exclude %{python3_sitelib}/__pycache__/test_vimdecrypt.cpython-*.pyc
%exclude %{python3_sitelib}/test_vimdecrypt.py

%changelog
* Thu Feb 29 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch>
- Ensure Amazon Linux use custom build files

* Wed Feb 28 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.0.0-0.2
- Fix build for Amazon Linux

* Thu Feb 22 2024 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.0.0-0.1
- Initial package

