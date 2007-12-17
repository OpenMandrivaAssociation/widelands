%define	name	widelands
%define	version	b11
#%define	svn	svn20070315
%define	release	%mkrel 3
%define	Summary	Settlers II clone

Epoch: 2

Name:		%{name}
Version:	%{version}
Release:	%{release}
URL:		http://widelands.sourceforge.net/
Source0:	%{name}-build-11-source.tar.bz2
Patch0:         widelands.flagfix.patch
License:	GPL
Group:		Games/Strategy
Summary:	%{Summary}
BuildRequires:	SDL-devel SDL_image-devel SDL_net-devel SDL_ttf-devel SDL_mixer-devel
BuildRequires:  png-devel optipng pngrewrite ctags gettext-devel scons
BuildRequires:	SDL_gfx-devel ggz-client-libs-devel
Provides: 	perl(Network::ClientHandler)
Provides: 	perl(Network::Server)
Provides:	perl(Protocol::ProtocolPacket)
Provides:	perl(Protocol::ProtocolPacket_ChatMessage)
Provides:	perl(Protocol::ProtocolPacket_Connect)
Provides:	perl(Protocol::ProtocolPacket_GetRoomInfo)
Provides:	perl(Protocol::ProtocolPacket_GetUserInfo)
Provides:	perl(Protocol::ProtocolPacket_Hello)
Provides:	perl(Protocol::ProtocolPacket_Ping)
Provides:	perl(Protocol::ProtocolPacket_UserEntered)

%description
Widelands is inspired by Bluebyte's Settlers II and will someday be the
logical extension of this game although you do not need the original
game. Play it on Win/Linux against human & AI opponents.

%prep
%setup -q -n %{name}
%patch0 -p0
sed -i 's#flagi#%{optflags}##' build/scons-tools/scons_configure.py

%build
scons	build=release \
	build_id=%{version}\
	install_prefix="%{_gamesdatadir}/%{name}"\
	bindir="%{_gamesbindir}/%{name}"\
	datadir="%{_gamesdatadir}/%{name}"\
	localedir=%{_datadir}/locale\
	enable_ggz=1
	
%install
%{__rm} -rf $RPM_BUILD_ROOT
scons	datadir=$RPM_BUILD_ROOT%{_gamesdatadir}/%{name}\
	bindir=$RPM_BUILD_ROOT%{_gamesbindir}\
	localedir=$RPM_BUILD_ROOT%{_datadir}\
	build_id=%{version}\
	install


#icons
%{__install} -d ${RPM_BUILD_ROOT}{%{_miconsdir},%{_liconsdir}}
%{__install} -m644 pics/wl-ico-16.png -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
%{__install} -m644 pics/wl-ico-32.png -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
%{__install} -m644 pics/wl-ico-48.png -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png



mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
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
Dry Riverbed
Elven Forests
Enemy in sight
Finlakes
Firegames
Four Castles
Glacier Lake
Golden Peninsula
Lake of tranquility
Plateau
Riverlands
The Oasis Triangle
The big lake
The long way
Two frontiers
War of the Valleys
EOF

%post
%update_menus

%postun
%clean_menus

%clean
%{__rm} -rf $RPM_BUILD_ROOT

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


