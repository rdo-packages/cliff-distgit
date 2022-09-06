
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global modname cliff

%global common_desc \
cliff is a framework for building command line programs. It uses setuptools \
entry points to provide subcommands, output formatters, and other \
extensions. \
\
Documentation for cliff is hosted on readthedocs.org at \
http://readthedocs.org/docs/cliff/en/latest/

%global common_desc_tests This package contains tests for the python cliff library.

Name:             python-%{modname}
Version:          XXX
Release:          XXX
Summary:          Command Line Interface Formulation Framework

Group:            Development/Libraries
License:          ASL 2.0
URL:              https://pypi.io/pypi/cliff
Source0:          https://pypi.io/packages/source/c/cliff/cliff-%{version}.tar.gz

BuildArch:        noarch

%package -n python3-%{modname}
Summary:          Command Line Interface Formulation Framework
%{?python_provide:%python_provide python3-%{modname}}

BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-prettytable
BuildRequires:    python3-stevedore
BuildRequires:    python3-cmd2 >= 0.8.0
BuildRequires:    python3-autopage
BuildRequires:    python3-importlib-metadata

Requires:         python3-prettytable
Requires:         python3-stevedore >= 2.0.1
Requires:         python3-cmd2 >= 1.0.0
Requires:         python3-yaml >= 3.12
Requires:         python3-autopage >= 0.4.0
Requires:         python3-importlib-metadata >= 4.4

%description -n python3-%{modname}
%{common_desc}

%package -n python3-%{modname}-tests
Summary:          Command Line Interface Formulation Framework
%{?python_provide:%python_provide python3-%{modname}-tests}

# Required for the test suite
BuildRequires:    python3-mock
BuildRequires:    bash
BuildRequires:    which
BuildRequires:    python3-subunit
BuildRequires:    python3-testtools
BuildRequires:    python3-testscenarios
BuildRequires:    python3-testrepository
BuildRequires:    python3-docutils
BuildRequires:    python3-PyYAML

Requires:         python3-%{modname} = %{version}-%{release}
Requires:         python3-mock
Requires:         bash
Requires:         which
Requires:         python3-subunit
Requires:         python3-testtools
Requires:         python3-testscenarios
Requires:         python3-testrepository
Requires:         python3-PyYAML

%description -n python3-%{modname}-tests
%{common_desc_tests}

%description
%{common_desc}

%prep
%setup -q -n %{modname}-%{upstream_version}
rm -rf {test-,}requirements.txt

# Remove bundled egg info
rm -rf *.egg-info

%build
%{py3_build}

%install
%{py3_install}

%check
PYTHON=python3 python3 setup.py test

%files -n python3-%{modname}
%license LICENSE
%doc doc/ README.rst ChangeLog AUTHORS CONTRIBUTING.rst
%{python3_sitelib}/%{modname}
%{python3_sitelib}/%{modname}-*.egg-info
%exclude %{python3_sitelib}/%{modname}/tests

%files -n python3-%{modname}-tests
%{python3_sitelib}/%{modname}/tests

%changelog
