Summary:	Vegastrike - a free 3D space fight simulator
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
Requires:	OpenGL, glut, SDL, %{name}-data = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
Vega Strike is an Interactive Flight Simulator/Real Time Strategy
being developed for Linux and Windows in 3d OpenGL... With stunning
Graphics reminiscent of Wing Commander, Vega Strike will be a hit for
all gamers!!!

%package data
Summary:	Vegastrike data files
Version:	0.1.0
Release:	1
License:	GPL
Group:		X11/Applications/Games
Group(de):	X11/Applikationen/Spiele
Group(pl):	X11/Aplikacje/Gry
Requires:	%{name} = %{version}

%description data
This provides data files for Vega Strike game and simple 
configuration script.


%prep
rm -rf $RPM_BUILD_ROOT
%setup -q -a 1


%build
CC=%{__cc}
CFLAGS="%{rpmcflags} -I/usr/include -I%{_includedir}"
LDFLAGS="-L%{_libdir} -L/usr/lib"
export CC CFLAGS LDFLAGS

./configure --prefix=%{_prefix} --disable-sdltest --with-data-dir=%{_datadir}/%{name} \
	    --with-gl-inc=/usr/X11R6/include --with-glut-inc=/usr/X11R6/include
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} DESTDIR=$RPM_BUILD_ROOT install

# Zmieñ nazwê /usr/X11R6/games na /usr/X11R6/share 
# -- mo¿na ³atkê daæ zamiast tego
mv $RPM_BUILD_ROOT%{_prefix}/games $RPM_BUILD_ROOT/%{_prefix}/share

# Skopiuj pliki danych 
# Mo¿na spróbowaæ make install w tym katalogu >> TODO
cp -rf	$RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version}_data/* $RPM_BUILD_ROOT%{_datadir}/%{name}/

# Przenie¶ binarkê do /usr/X11R6/bin
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/bin
mv $RPM_BUILD_ROOT/%{_prefix}/share/%{name}/bin/* $RPM_BUILD_ROOT/%{_prefix}/bin/%{name}-%{version}

# Spakuj dokumentacjê
gzip -9nf README

# Instalacja skryptu konfiguracyjnego

%post data
echo "Remember to run /usr/X11R6/bin/vegastrike-config"
echo "After configuration run Vega Strike with: /usr/X11R6/bin/vegastrike"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,755)
%doc README.gz
%{_bindir}/*

%files data
%defattr(-,root,root,755)

%{_datadir}/%{name}/*
