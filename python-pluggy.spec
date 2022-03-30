#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-pluggy.spec)

%define 	module	pluggy
Summary:	Plugin and hook calling mechanisms for Python
Summary(pl.UTF-8):	Mechanizmy wtyczek dla Pythona
Name:		python-%{module}
# keep 0.13.x here for python2 support
Version:	0.13.1
Release:	3
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pluggy/
Source0:	https://files.pythonhosted.org/packages/source/p/pluggy/pluggy-%{version}.tar.gz
# Source0-md5:	7f610e28b8b34487336b585a3dfb803d
URL:		https://pypi.org/project/pluggy/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm
%if %{with tests}
BuildRequires:	python-importlib_metadata >= 0.12
BuildRequires:	python-pytest >= 3.7.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
%if %{with tests}
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-importlib_metadata >= 0.12
%endif
BuildRequires:	python3-pytest >= 3.7.0
%endif
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Plugin manager as used by pytest but stripped of pytest specific
details.

%description -l pl.UTF-8
Zarządca wtyczek tak jak używany przez pytest, ale pozbawiony detali
specyficznych dla pytest.

%package -n python3-%{module}
Summary:	Plugin and hook calling mechanisms for Python
Summary(pl.UTF-8):	Mechanizmy wtyczek dla Pythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-%{module}
Plugin manager as used by pytest but stripped of pytest specific
details.

%description -n python3-%{module} -l pl.UTF-8
Zarządca wtyczek tak jak używany przez pytest, ale pozbawiony detali
specyficznych dla pytest.

%package apidocs
Summary:	API documentation for Python pluggy module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pluggy
Group:		Documentation

%description apidocs
API documentation for Python pluggy module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pluggy.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest testing
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest testing
%endif
%endif

%if %{with doc}
PYTHONPATH="$PWD/src" \
sphinx-build -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py_sitescriptdir}/pluggy
%{py_sitescriptdir}/pluggy-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/pluggy
%{py3_sitescriptdir}/pluggy-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
