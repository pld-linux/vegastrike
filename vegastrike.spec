Summary:	Vegastrike - a free 3D space fight simulator
Summary(pl):	Vegastrike - trójwymiarowy symulator lotu
Name:		vegastrike
Version:	0.1.0
Release:	2
License:	GPL
Group:		X11/Applications/Games
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	6397c57ca9a70508e820dae3a3309975
Source1:	http://dl.sourceforge.net/%{name}/%{name}-%{version}_data.tar.gz
# Source1-md5:	50a7ff3bdf41c0fee66c66d9ee4d15b2
Patch0:		%{name}-opt.patch
Patch1:		%{name}-c++.patch
Patch2:		%{name}-gl.patch
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	glut-devel
Requires:	OpenGL
Requires:	%{name}-data = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1

%description
Vega Strike is an Interactive Flight Simulator/Real Time Strategy
being developed for Linux and Windows in 3D OpenGL... With stunning
Graphics reminiscent of Wing Commander, Vega Strike will be a hit for
all gamers!!!

%description -l pl
Vega Strike to interaktyny symulator lotu / strategia czasu
rzeczywistego korzystaj±ca z OpenGL, rozwijana pod Linuksa i Windows.

%package data
Summary:	Vegastrike data files
Summary(pl):	Dane dla Vegastrike
Group:		X11/Applications/Games
Requires:	%{name} = %{version}

%description data
This provides data files for Vega Strike game and simple configuration
script.

%description data -l pl
Ten pakiet zawiera pliki danych dla gry Vega Strike i prosty skrypt
konfiguracyjny.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-sdltest \
	--with-data-dir=%{_datadir}/%{name} \
	--with-gl-inc=/usr/X11R6/include \
	--with-glut-inc=/usr/X11R6/include

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	bindir=%{_bindir} \
	pkgdatadir=%{_datadir}/%{name}/objconv \
	DESTDIR=$RPM_BUILD_ROOT

# Makefiles not created - data must be installed manually
find %{name}-%{version}_data -type d -name CVS \
	-o -type d -name .xvpics \
	-o -type f -name 'Makefile*' | xargs rm -rf

cp -rf %{name}-%{version}_data/* $RPM_BUILD_ROOT%{_datadir}/%{name}

# Instalacja skryptu konfiguracyjnego
# ???

%clean
rm -rf $RPM_BUILD_ROOT

# no such file
#%post data
#echo "Remember to run /usr/X11R6/bin/vegastrike-config"
#echo "After configuration run Vega Strike with: /usr/X11R6/bin/vegastrike"

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*

%files data
%defattr(644,root,root,755)
%{_datadir}/%{name}
