Summary:	Vegastrike - a free 3D space fight simulator
Summary(pl):	Vegastrike - trójwymiarowy symulator lotu
Name:		vegastrike
Version:	0.1.0
Release:	1
License:	GPL
Group:		X11/Applications/Games
Group(de):	X11/Applikationen/Spiele
Group(pl):	X11/Aplikacje/Gry
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}_data.tar.gz
BuildRequires:	SDL-devel, XFree86-OpenGL-devel, glut-devel, expat
BuildRequires:	OpenGL-devel
BuildRequires:	glut-devel
BuildRequires:	SDL-devel
Requires:	OpenGL
Requires:	%{name}-data = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
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
Group(de):	X11/Applikationen/Spiele
Group(pl):	X11/Aplikacje/Gry
Requires:	%{name} = %{version}

%description data
This provides data files for Vega Strike game and simple configuration
script.

%description data -l pl
Ten pakiet zawiera pliki danych dla gry Vega Strike i prosty skrypt
konfiguracyjny.

%prep
%setup -q -a 1

%build
CC=%{__cc}
CFLAGS="%{rpmcflags} -I/usr/include -I%{_includedir}"
LDFLAGS="-L%{_libdir} -L/usr/lib"
export CC CFLAGS LDFLAGS

./configure --prefix=%{_prefix} --disable-sdltest --with-data-dir=%{_datadir}/%{name} \
	    --with-gl-inc=%{_includedir} --with-glut-inc=%{_includedir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} DESTDIR=$RPM_BUILD_ROOT install

# Zmieñ nazwê /usr/X11R6/games na /usr/X11R6/share 
# -- mo¿na ³atkê daæ zamiast tego
mv -f $RPM_BUILD_ROOT%{_prefix}/games $RPM_BUILD_ROOT/%{_datadir}

# Skopiuj pliki danych 
# Mo¿na spróbowaæ make install w tym katalogu >> TODO
cp -rf $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version}_data/* $RPM_BUILD_ROOT%{_datadir}/%{name}

# Przenie¶ binarkê do /usr/X11R6/bin
install -d $RPM_BUILD_ROOT%{_bindir}
mv -f $RPM_BUILD_ROOT%{_datadir}/%{name}/bin/* $RPM_BUILD_ROOT%{_bindir}/%{name}-%{version}

# Spakuj dokumentacjê
gzip -9nf README

# Instalacja skryptu konfiguracyjnego

%clean
rm -rf $RPM_BUILD_ROOT

%post data
echo "Remember to run /usr/X11R6/bin/vegastrike-config"
echo "After configuration run Vega Strike with: /usr/X11R6/bin/vegastrike"

%files
%defattr(644,root,root,755)
%doc README.gz
%attr(755,root,root) %{_bindir}/*

%files data
%defattr(644,root,root,755)
%{_datadir}/%{name}
