%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora}
%global with_python3 1
%endif

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

%package -n python2-%{modname}
Summary:          Command Line Interface Formulation Framework
%{?python_provide:%python_provide python2-%{modname}}

BuildRequires:    python2-devel
BuildRequires:    python2-setuptools
BuildRequires:    python2-pbr
BuildRequires:    python2-prettytable
BuildRequires:    python2-stevedore
BuildRequires:    python2-six
%if 0%{?fedora} > 0
BuildRequires:    python2-cmd2 >= 0.6.7
%else
BuildRequires:    python-cmd2 >= 0.6.7
%endif

Requires:         python2-prettytable
Requires:         python2-stevedore >= 1.20.0
Requires:         python2-six
Requires:         python2-unicodecsv
%if 0%{?fedora} > 0
Requires:         python2-cmd2 >= 0.6.7
Requires:         python2-pyyaml
Requires:         python2-pyparsing
%else
Requires:         python-cmd2 >= 0.6.7
Requires:         PyYAML
Requires:         pyparsing
%endif

%if %{?rhel}%{!?rhel:0} == 6
BuildRequires:    python-argparse
Requires:         python-argparse
%endif

%description -n python2-%{modname}
%{common_desc}

%package -n python-%{modname}-tests
Summary:          Command Line Interface Formulation Framework
# Required for the test suite
BuildRequires:    python2-mock
BuildRequires:    bash
BuildRequires:    python2-unicodecsv
BuildRequires:    which
BuildRequires:    python2-subunit
BuildRequires:    python2-testtools
%if 0%{?fedora} > 0
BuildRequires:    python2-docutils
BuildRequires:    python2-pyyaml
BuildRequires:    python2-testscenarios
BuildRequires:    python2-testrepository
%else
BuildRequires:    python-docutils
BuildRequires:    PyYAML
BuildRequires:    python-testscenarios
BuildRequires:    python-testrepository
%endif

Requires:         python2-%{modname} = %{version}-%{release}
Requires:         python2-mock
Requires:         bash
Requires:         python2-unicodecsv
Requires:         which
Requires:         python2-subunit
Requires:         python2-testtools
%if 0%{?fedora} > 0
Requires:         python2-pyyaml
Requires:         python2-testscenarios
Requires:         python2-testrepository
%else
Requires:         PyYAML
Requires:         python-testscenarios
Requires:         python-testrepository
%endif

%description -n python-%{modname}-tests
%{common_desc_tests}

%if 0%{?with_python3}
%package -n python3-cliff
Summary:        Command Line Interface Formulation Framework
Group:          Development/Libraries

BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr
BuildRequires:    python3-prettytable
BuildRequires:    python3-cmd2 >= 0.6.7
BuildRequires:    python3-stevedore
BuildRequires:    python3-six
BuildRequires:    python3-PyYAML
BuildRequires:    python3-testtools

Requires:         python3-prettytable
Requires:         python3-cmd2 >= 0.6.7
Requires:         python3-stevedore >= 1.20.0
Requires:         python3-six
Requires:         python3-pyparsing
Requires:         python3-PyYAML

%description -n python3-cliff
%{common_desc}

%package -n python3-%{modname}-tests
Summary:          Command Line Interface Formulation Framework
# Required for the test suite
BuildRequires:    bash
BuildRequires:    python3-unicodecsv
BuildRequires:    python3-PyYAML
BuildRequires:    which
BuildRequires:    python3-subunit
BuildRequires:    python3-testrepository
BuildRequires:    python3-testscenarios
BuildRequires:    python3-testtools

Requires:         python3-%{modname} = %{version}-%{release}
Requires:         bash
Requires:         python3-unicodecsv
Requires:         python3-PyYAML
Requires:         which
Requires:         python3-subunit
Requires:         python3-testrepository
Requires:         python3-testscenarios
Requires:         python3-testtools

%description -n python3-%{modname}-tests
%{common_desc_tests}
%endif

%description
%{common_desc}

%prep
%setup -q -n %{modname}-%{upstream_version}
rm -rf {test-,}requirements.txt

# Remove bundled egg info
rm -rf *.egg-info

%build
%{__python2} setup.py build

%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif

%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{modname}
%license LICENSE
%doc doc/ README.rst ChangeLog AUTHORS CONTRIBUTING.rst
%{python2_sitelib}/%{modname}
%{python2_sitelib}/%{modname}-*.egg-info
%exclude %{python2_sitelib}/%{modname}/tests

%files -n python-%{modname}-tests
%{python2_sitelib}/%{modname}/tests

%if 0%{?with_python3}
%files -n python3-%{modname}
%license LICENSE
%doc doc/ README.rst ChangeLog AUTHORS CONTRIBUTING.rst
%{python3_sitelib}/%{modname}
%{python3_sitelib}/%{modname}-*.egg-info
%exclude %{python3_sitelib}/%{modname}/tests

%files -n python3-%{modname}-tests
%{python3_sitelib}/%{modname}/tests
%endif

%changelog
