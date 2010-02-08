%define	name	widelands
%define	version	b14
%define svn	svn4498
%define	release	%mkrel 2
%define	Summary	Settlers II clone

Epoch: 2

Name:		%{name}
Version:	%{version}
Release:	%{release}
URL:		http://xoops.widelands.org/
Source0:	%{name}-build14.tar.xz
License:	GPLv2+
Group:		Games/Strategy
Summary:	%{Summary}
BuildRequires:	boost-devel 
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_net-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:  png-devel
BuildRequires:	optipng 
BuildRequires:	pngrewrite
BuildRequires:	ctags
BuildRequires:	gettext-devel
BuildRequires:	scons
BuildRequires:	SDL_gfx-devel
BuildRequires:	ggz-client-libs-devel 
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Widelands is inspired by Bluebyte's Settlers II and will someday be the
logical extension of this game although you do not need the original
game. Play it on Win/Linux against human & AI opponents.

%prep
%setup -q -n %{name}
sed -i 's#flagi#%{optflags}##' build/scons-tools/scons_configure.py

%build
scons	build=release \
	build_id=%{version}\
	install_prefix="%{_gamesdatadir}/%{name}"\
	bindir="%{_gamesbindir}/%{name}"\
	datadir="%{_gamesdatadir}/%{name}"\
	localedir="%{_datadir}/locale"
	
%install
%{__rm} -rf %{buildroot}
scons	datadir=%{buildroot}%{_gamesdatadir}/%{name}\
	bindir=%{buildroot}%{_gamesbindir}\
	localedir=%{buildroot}%{_datadir}/locale\
	build_id=%{version}\
	install


#icons
%{__install} -d ${RPM_BUILD_ROOT}{%{_miconsdir},%{_liconsdir}}
%{__install} -m644 pics/wl-ico-16.png -D %{buildroot}%{_miconsdir}/%{name}.png
%{__install} -m644 pics/wl-ico-32.png -D %{buildroot}%{_iconsdir}/%{name}.png
%{__install} -m644 pics/wl-ico-48.png -D %{buildroot}%{_liconsdir}/%{name}.png



mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Widelands
Comment=%{Summary}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;StrategyGame;
EOF

%find_lang %{name} --all-name

%pre
# preparing system before update
cat << EOF | while read name; do rm -rf "%{_gamesdatadir}/%{name}/maps/${name}.wmf"; done
Checkmate
Mystical Maze
Comet Island
Plateau
Crater
Rendez-Vous
Dry Riverbed
Riverlands
Elven Forests
SConscript
Enemy in sight
Swamp Island
Finlakes
The big lake
Firegames
The Far North
Four Castles
The long way
Four Mountains
The Oasis Triangle
Glacier Lake
The pass through the mountains
Golden Peninsula
The Thaw
Impact
Three Warriors
Islands at war
Two frontiers
Lake of tranquility
War of the Valleys
Last Bastion
Wisent Valley
EOF

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
%{__rm} -rf %{buildroot}

%files -f %name.lang
%defattr(644,root,root,755)
%doc ChangeLog COPYING
%{_gamesdatadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%defattr(755,root,root,755)
%{_gamesbindir}/%{name}


