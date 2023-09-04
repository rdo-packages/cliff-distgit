
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order sphinx coverage stestr

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
Version:          4.3.0
Release:          1%{?dist}
Summary:          Command Line Interface Formulation Framework

Group:            Development/Libraries
License:          Apache-2.0
URL:              https://pypi.io/pypi/cliff
Source0:          https://pypi.io/packages/source/c/cliff/cliff-%{version}.tar.gz

BuildArch:        noarch

%package -n python3-%{modname}
Summary:          Command Line Interface Formulation Framework

BuildRequires:    python3-devel
BuildRequires:    pyproject-rpm-macros
%description -n python3-%{modname}
%{common_desc}

%package -n python3-%{modname}-tests
Summary:          Command Line Interface Formulation Framework

BuildRequires:    bash
BuildRequires:    which
# cliff imports docutils in code which is not in requirements.txt and it is
# needed to run tests.
BuildRequires:    python3-docutils
Requires:         python3-%{modname} = %{version}-%{release}
Requires:         bash
Requires:         which
# Keep manual runtime reqs in -tests subpackages for now
Requires:         python3-subunit
Requires:         python3-testtools
Requires:         python3-testscenarios
Requires:         python3-PyYAML

%description -n python3-%{modname}-tests
%{common_desc_tests}

%description
%{common_desc}

%prep
%setup -q -n %{modname}-%{upstream_version}

# Remove bundled egg info
rm -rf *.egg-info

sed -i /.*-c{env:TOX_CONSTRAINTS_FILE.*/d tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Avoid sphinx as BR as we are not building doc
rm cliff/tests/test_sphinxext.py

%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv}

%build
%pyproject_wheel

%install
%pyproject_install

%check
# stestr depends on cliff which introduces cyclic dep so i'm avoiding stestr.
PYTHON=python3 python3 setup.py test


%files -n python3-%{modname}
%license LICENSE
%doc doc/ README.rst ChangeLog AUTHORS CONTRIBUTING.rst
%{python3_sitelib}/%{modname}
%{python3_sitelib}/%{modname}-*.dist-info
%exclude %{python3_sitelib}/%{modname}/tests

%files -n python3-%{modname}-tests
%{python3_sitelib}/%{modname}/tests

%changelog
* Mon Sep 04 2023 RDO <dev@lists.rdoproject.org> 4.3.0-1
- Update to 4.3.0

