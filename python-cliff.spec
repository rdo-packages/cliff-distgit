%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora}
%global with_python3 1
%endif

%global modname cliff

Name:             python-cliff
Version:          XXX
Release:          XXX
Summary:          Command Line Interface Formulation Framework

Group:            Development/Libraries
License:          ASL 2.0
URL:              https://pypi.io/pypi/cliff
Source0:          https://pypi.io/packages/source/c/cliff/cliff-%{version}.tar.gz

BuildArch:        noarch

BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr
BuildRequires:    python-prettytable
BuildRequires:    python-cmd2 >= 0.6.7
BuildRequires:    python-stevedore
BuildRequires:    python-six

Requires:         python-setuptools
Requires:         python-prettytable
Requires:         python-cmd2 >= 0.6.7
Requires:         python-stevedore
Requires:         python-six
Requires:         python-unicodecsv
Requires:         PyYAML

%if %{?rhel}%{!?rhel:0} == 6
BuildRequires:    python-argparse
Requires:         python-argparse
%endif

%description
cliff is a framework for building command line programs. It uses setuptools
entry points to provide subcommands, output formatters, and other
extensions.

Documentation for cliff is hosted on readthedocs.org at
http://readthedocs.org/docs/cliff/en/latest/

%package -n python-%{modname}-tests
Summary:          Command Line Interface Formulation Framework
# Required for the test suite
BuildRequires:    python-mock
BuildRequires:    bash
BuildRequires:    bash-completion
BuildRequires:    python-unicodecsv
BuildRequires:    PyYAML
BuildRequires:    which
BuildRequires:    python-subunit
BuildRequires:    python-testrepository
BuildRequires:    python-testscenarios
BuildRequires:    python-testtools

%description -n python-%{modname}-tests
cliff is a framework for building command line programs. It uses setuptools
entry points to provide subcommands, output formatters, and other
extensions.

Documentation for cliff is hosted on readthedocs.org at
http://readthedocs.org/docs/cliff/en/latest/

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
BuildRequires:    python3-mock
BuildRequires:    python3-PyYAML
BuildRequires:    python3-testtools

Requires:         python3-setuptools
Requires:         python3-prettytable
Requires:         python3-cmd2 >= 0.6.7
Requires:         python3-stevedore
Requires:         python3-six

%description -n python3-cliff
cliff is a framework for building command line programs. It uses setuptools
entry points to provide subcommands, output formatters, and other
extensions.

Documentation for cliff is hosted on readthedocs.org at
http://readthedocs.org/docs/cliff/en/latest/

%package -n python3-%{modname}-tests
Summary:          Command Line Interface Formulation Framework
# Required for the test suite
BuildRequires:    python3-mock
BuildRequires:    bash
BuildRequires:    bash-completion
BuildRequires:    python3-unicodecsv
BuildRequires:    python3-PyYAML
BuildRequires:    which
BuildRequires:    python3-subunit
BuildRequires:    python3-testrepository
BuildRequires:    python3-testscenarios
BuildRequires:    python3-testtools

%description -n python3-%{modname}-tests
cliff is a framework for building command line programs. It uses setuptools
entry points to provide subcommands, output formatters, and other
extensions.

Documentation for cliff is hosted on readthedocs.org at
http://readthedocs.org/docs/cliff/en/latest/
%endif

%prep
%setup -q -n %{modname}-%{upstream_version}

# Remove setuptools dep.  We'll supply the rpm on epel.
sed -i '/argparse/d' requirements.txt

# Remove bundled egg info
rm -rf *.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif

%{__python} setup.py install -O1 --skip-build --root=%{buildroot}

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files
%license LICENSE
%doc doc/ README.rst ChangeLog AUTHORS CONTRIBUTING.rst
%{python_sitelib}/%{modname}
%{python_sitelib}/%{modname}-*.egg-info
%exclude %{python_sitelib}/%{modname}/tests

%files -n python-%{modname}-tests
%{python_sitelib}/%{modname}/tests

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
