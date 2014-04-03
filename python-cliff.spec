%if 0%{?fedora}
%global with_python3 1
%endif

%global modname cliff

Name:             python-cliff
Version:          1.6.0
Release:          1%{?dist}
Summary:          Command Line Interface Formulation Framework

Group:            Development/Libraries
License:          ASL 2.0
URL:              http://pypi.python.org/pypi/cliff
Source0:          http://pypi.python.org/packages/source/c/cliff/cliff-%{version}.tar.gz

BuildArch:        noarch

BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr
BuildRequires:    python-prettytable
BuildRequires:    python-cmd2 >= 0.6.7
BuildRequires:    python-stevedore
BuildRequires:    python-six

# Required for the test suite
BuildRequires:    python-nose
BuildRequires:    python-mock
BuildRequires:    bash
BuildRequires:    bash-completion

Requires:         python-setuptools
Requires:         python-prettytable
Requires:         python-cmd2 >= 0.6.7
Requires:         python-stevedore
Requires:         python-six

%if %{?rhel}%{!?rhel:0} == 6
BuildRequires:    python-argparse
Requires:         python-argparse
%endif


%if 0%{?with_python3}
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr
BuildRequires:    python3-prettytable
BuildRequires:    python3-cmd2 >= 0.6.7
BuildRequires:    python3-stevedore
BuildRequires:    python3-six
BuildRequires:    python3-nose
BuildRequires:    python3-mock
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
%endif

%prep
%setup -q -n %{modname}-%{version}

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
PYTHONPATH=. nosetests

%if 0%{?with_python3}
pushd %{py3dir}
PYTHONPATH=. nosetests-%{python3_version}
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
* Tue Jan 28 2014 Ralph Bean <rbean@redhat.com> - 1.6.0-1
- Latest upstream.
- Add dep on python-pbr (python build reasonableness)
- Add dep on python-stevedore
- Add build requirements on python-nose, python-mock, and bash
- Change check to use 'nosetests' directly.
- Remove bundled egg-info

* Thu Nov 14 2013 Ralph Bean <rbean@redhat.com> - 1.4.5-1
- Latest upstream.
- Remove patch now that the latest cmd2 and pyparsing are required.

* Thu Nov 14 2013 Ralph Bean <rbean@redhat.com> - 1.4.4-2
- Enable python3 subpackage now that python3-pyparsing is available.
- Adjust patch to simplify pyparsing setuptools constraints further.

* Fri Sep 13 2013 Pádraig Brady <pbrady@redhat.com> - 1.4.4-1
- Latest upstream.

* Tue Aug 06 2013 Ralph Bean <rbean@redhat.com> - 1.4-1
- Latest upstream.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 10 2013 Ralph Bean <rbean@redhat.com> - 1.3.2-1
- Latest upstream.
- Patched pyparsing version constraint for py2.
- Modernized python3 conditional.
- Temporarily disabled python3 subpackage for python3-pyparsing dep.
- Added temporary explicit dependency on python3-pyparsing>=2.0.0.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Ralph Bean <rbean@redhat.com> - 1.3-1
- Latest upstream.
- Enabled python3 subpackage.
- Remove requirement on python-tablib

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 06 2012 Ralph Bean <rbean@redhat.com> - 1.0-3
- Require python-argparse on epel.

* Thu Jul 05 2012 Ralph Bean <rbean@redhat.com> - 1.0-2
- Manually disable python3 support until python3-prettytable is available.

* Thu Jun 28 2012 Ralph Bean <rbean@redhat.com> - 1.0-1
- initial package for Fedora
