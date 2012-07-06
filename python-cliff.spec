%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 1
%endif

# Setting with_python3 manually to false until python3-prettytable becomes
# available.  https://bugzilla.redhat.com/show_bug.cgi?id=837087
%global with_python3 0


%global modname cliff

Name:             python-cliff
Version:          1.0
Release:          2%{?dist}
Summary:          Command Line Interface Formulation Framework

Group:            Development/Libraries
License:          ASL 2.0
URL:              http://pypi.python.org/pypi/cliff
Source0:          http://pypi.python.org/packages/source/c/cliff/cliff-%{version}.tar.gz

BuildArch:        noarch

BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-prettytable
BuildRequires:    python-cmd2
BuildRequires:    python-tablib
Requires:         python-setuptools
Requires:         python-prettytable
Requires:         python-cmd2
Requires:         python-tablib


%if 0%{?with_python3}
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-prettytable
BuildRequires:    python3-cmd2
BuildRequires:    python3-tablib
Requires:         python3-setuptools
Requires:         python3-prettytable
Requires:         python3-cmd2
Requires:         python3-tablib
%endif

%description
cliff is a framework for building command line programs. It uses setuptools
entry points to provide subcommands, output formatters, and other
extensions.

Documentation for cliff is hosted on readthedocs.org at
http://readthedocs.org/docs/cliff/en/latest/

%if 0%{?with_python3}
%package -n python3-cliff
Summary:        Command Line Interface Formulation Framework
Group:          Development/Libraries

%description -n python3-cliff
cliff is a framework for building command line programs. It uses setuptools
entry points to provide subcommands, output formatters, and other
extensions.

Documentation for cliff is hosted on readthedocs.org at
http://readthedocs.org/docs/cliff/en/latest/
%endif

%prep
%setup -q -n %{modname}-%{version}

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
%{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif


%files
%doc docs/
%{python_sitelib}/%{modname}
%{python_sitelib}/%{modname}-%{version}*

%if 0%{?with_python3}
%files -n python3-%{modname}
%doc docs/
%{python3_sitelib}/%{modname}
%{python3_sitelib}/%{modname}-%{version}-*

%endif


%changelog
* Thu Jul 05 2012 Ralph Bean <rbean@redhat.com> - 1.0-2
- Manually disable python3 support until python3-prettytable is available.

* Thu Jun 28 2012 Ralph Bean <rbean@redhat.com> - 1.0-1
- initial package for Fedora
