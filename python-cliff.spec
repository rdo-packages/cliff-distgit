# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

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
Version:          2.16.0
Release:          2%{?dist}
Summary:          Command Line Interface Formulation Framework

Group:            Development/Libraries
License:          ASL 2.0
URL:              https://pypi.io/pypi/cliff
Source0:          https://pypi.io/packages/source/c/cliff/cliff-%{version}.tar.gz

BuildArch:        noarch

%package -n python%{pyver}-%{modname}
Summary:          Command Line Interface Formulation Framework
%{?python_provide:%python_provide python%{pyver}-%{modname}}

BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-pbr
BuildRequires:    python%{pyver}-prettytable
BuildRequires:    python%{pyver}-stevedore
BuildRequires:    python%{pyver}-six
BuildRequires:    python%{pyver}-pyparsing
# FIXME (jcapitao): As soon as CentOS8 is out, bump version of python-cmd2 to 0.8.3
BuildRequires:    python%{pyver}-cmd2 >= 0.6.7

Requires:         python%{pyver}-prettytable
Requires:         python%{pyver}-stevedore >= 1.20.0
Requires:         python%{pyver}-six
Requires:         python%{pyver}-cmd2 >= 0.6.7
Requires:         python%{pyver}-pyparsing
# Handle python2 exception
%if %{pyver} == 2
Requires:         PyYAML
Requires:         python%{pyver}-unicodecsv
%else
Requires:         python%{pyver}-PyYAML
%endif

%description -n python%{pyver}-%{modname}
%{common_desc}

%package -n python%{pyver}-%{modname}-tests
Summary:          Command Line Interface Formulation Framework
%{?python_provide:%python_provide python%{pyver}-%{modname}-tests}

# Required for the test suite
BuildRequires:    python%{pyver}-mock
BuildRequires:    bash
BuildRequires:    which
BuildRequires:    python%{pyver}-subunit
BuildRequires:    python%{pyver}-testtools
BuildRequires:    python%{pyver}-testscenarios
BuildRequires:    python%{pyver}-testrepository
# Handle python2 exception
%if %{pyver} == 2
BuildRequires:    python-docutils
BuildRequires:    PyYAML
BuildRequires:    python%{pyver}-unicodecsv
%else
BuildRequires:    python%{pyver}-docutils
BuildRequires:    python%{pyver}-PyYAML
%endif

Requires:         python%{pyver}-%{modname} = %{version}-%{release}
Requires:         python%{pyver}-mock
Requires:         bash
Requires:         which
Requires:         python%{pyver}-subunit
Requires:         python%{pyver}-testtools
Requires:         python%{pyver}-testscenarios
Requires:         python%{pyver}-testrepository
# Handle python2 exception
%if %{pyver} == 2
Requires:         PyYAML
Requires:         python%{pyver}-unicodecsv
%else
Requires:         python%{pyver}-PyYAML
%endif

%description -n python%{pyver}-%{modname}-tests
%{common_desc_tests}

%description
%{common_desc}

%prep
%setup -q -n %{modname}-%{upstream_version}
rm -rf {test-,}requirements.txt

# Remove bundled egg info
rm -rf *.egg-info

%build
%{pyver_build}

%install
%{pyver_install}

%check
PYTHON=python%{pyver} %{pyver_bin} setup.py test

%files -n python%{pyver}-%{modname}
%license LICENSE
%doc doc/ README.rst ChangeLog AUTHORS CONTRIBUTING.rst
%{pyver_sitelib}/%{modname}
%{pyver_sitelib}/%{modname}-*.egg-info
%exclude %{pyver_sitelib}/%{modname}/tests

%files -n python%{pyver}-%{modname}-tests
%{pyver_sitelib}/%{modname}/tests

%changelog
* Thu Oct 03 2019 Joel Capitao <jcapitao@redhat.com> 2.16.0-2
- Removed python2 subpackages in no el7 distros

* Thu Sep 19 2019 RDO <dev@lists.rdoproject.org> 2.16.0-1
- Update to 2.16.0

