#
# TODO: What about this memleak(?) in 2.6? This game is not playable
#       on these kernels.
#
%define		snap	20040611
Summary:	Vegastrike - a free 3D space fight simulator
Summary(pl):	Vegastrike - trójwymiarowy symulator lotu
Name:		vegastrike
Version:	0.4.2_%{snap}
Release:	1
License:	GPL
Group:		X11/Applications/Games
Source0:	ftp://distfiles.pld-linux.org/src/%{name}-%{snap}-source.tgz
# Source0-md5:	41b3accf50382ef87c55a44985cfe94d
Source1:	ftp://distfiles.pld-linux.org/src/%{name}-%{snap}-data.tgz
# Source1-md5:	2b2104502586d357ef5b4e1b68213d32
Source2:	ftp://distfiles.pld-linux.org/src/%{name}-%{snap}-setup.tgz
# Source2-md5:	2269ca12013434b982538548bf4e49b6
Source3:	vsfinalize
Patch0:		%{name}-accountserver.patch
URL:		http://vegastrike.sourceforge.net
BuildRequires:	OpenGL-devel-base
BuildRequires:	SDL_mixer-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	glut-devel
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRequires:	OpenAL-devel
BuildRequires:	python-devel
BuildRequires:	perl-base
Requires:	OpenGL
Requires:	SDL_mixer
Requires:	glut
Requires:	libpng
Requires:	libjpeg
Requires:	python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1

%description
Vega Strike is an Interactive Flight Simulator/Real Time Strategy
being developed for Linux and Windows in 3D OpenGL... With stunning
Graphics reminiscent of Wing Commander, Vega Strike will be a hit for
all gamers!!! It's combination of old frontier/elite series and privateer.

%description -l pl
Vega Strike to interaktyny symulator lotu / strategia czasu
rzeczywistego korzystaj±ca z OpenGL, rozwijana pod Linuksa i Windows.
Ta gra to kombinacje starej serii elite/frontier i privateera.

%package tools
Summary:	Vegastrike tools
Summary(pl):	Narzêdzia dla Vegastrike
Group:		X11/Applications/Games
Requires:	%{name} = %{version}

%description tools
This provides tools for Vega Strike game. They are not needed to play the
game, so you will need them only if you know what they are doing.

%description tools -l pl
Ten pakiet zawiera narzêdzia do gry Vega Strike. Nie s± one konieczne by graæ,
wiêc bêdziesz ich potrzebowa³ tylko, kiedy wiesz do czego s³u¿±.

%prep
%setup -q -a1 -a2 -n %{name}
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-net-threads=posix \
	--enable-flags="%{rpmcflags}" \
	--with-data-dir="%{_datadir}/%{name}"
#	--enable-release
%{__make}
cd vssetup/src
perl ./build
cd ../../

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	bindir=%{_bindir} \
	pkgdatadir=%{_datadir}/%{name}/objconv \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_mandir}/man1,%{_bindir},%{_datadir}/%{name}}

# Makefiles not created - data must be installed manually
find data4.x -type d -name 'CVS' \
	-o -type d -name '.xvpics' \
	-o -type f -name 'Makefile*' \
	-o -type f -name '*~*' \
	-o -type f -name '*.nsi' \
	-o -type f -name '.#*' \
	-o -type f -name 'vsinstall' | sed -e "s/'/\\\'/g" | xargs rm -rf

cp -rf data4.x/* $RPM_BUILD_ROOT%{_datadir}/%{name}/
cp -rf data4.x/.vegastrike $RPM_BUILD_ROOT%{_datadir}/%{name}/

install vssetup/src/bin/setup $RPM_BUILD_ROOT%{_bindir}/vssetup
install %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/vsinstall
install src/networking/soundserver $RPM_BUILD_ROOT%{_datadir}/%{name}/
install data4.x/documentation/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%clean
rm -rf $RPM_BUILD_ROOT

%post
cat << EOF

Remember to run vsinstall
After configuration run Vega Strike with vslauncher
You can always run configuration tool with vssetup

EOF

%files
%defattr(644,root,root,755)
%doc README AUTHORS ChangeLog ToDo.txt
%attr(755,root,root) %{_bindir}/vegastrike
%attr(755,root,root) %{_bindir}/vsinstall
%attr(755,root,root) %{_bindir}/vssetup
%attr(755,root,root) %{_bindir}/vslauncher
%attr(755,root,root) %{_datadir}/%{name}/soundserver
%attr(755,root,root) %{_datadir}/%{name}/objconv/3ds2xml
%attr(755,root,root) %{_datadir}/%{name}/objconv/obj2xml
%attr(755,root,root) %{_datadir}/%{name}/objconv/wcp2xml
%{_datadir}/%{name}
%{_mandir}/*/*

%files tools
%defattr(644,root,root,755)
#%attr(755,root,root) %{_bindir}/accountserver
%attr(755,root,root) %{_bindir}/asteroidgen
%attr(755,root,root) %{_bindir}/replace
%attr(755,root,root) %{_bindir}/trisort
%attr(755,root,root) %{_bindir}/vegaserver
%attr(755,root,root) %{_bindir}/vsrextract
%attr(755,root,root) %{_bindir}/vsrmake
