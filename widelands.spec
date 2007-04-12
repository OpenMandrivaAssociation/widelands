%define	name	widelands
%define	version	b10
#%define	svn	svn20070315
%define	release	%mkrel 1
%define	Summary	Settlers II clone

Epoch: 2

Name:		%{name}
Version:	%{version}
Release:	%{release}
URL:		http://widelands.sourceforge.net/
Source0:	%{name}.tar.bz2
Patch1:		widelands-localepath.patch
License:	GPL
Group:		Games/Strategy
Summary:	%{Summary}
BuildRequires:	SDL-devel SDL_image-devel SDL_net-devel SDL_ttf-devel SDL_mixer-devel gettext-devel scons
BuildRequires:  png-devel optipng pngrewrite ctags astyle
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
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
%patch1 -p0

%build
./build-widelands.sh \
	build="release" \
	install_prefix="%{_datadir}/games/%{name}" \
	bindir="%{_datadir}/games/%{name}" \
	datadir="%{_datadir}/games/%{name}"

#Build translations
cd locale
../utils/buildcat.py
%{__rm} -f *.po
%{__rm} -f *.pot
%{__rm} -f SConscript
cd ..

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__install} -m755 %{name} -D $RPM_BUILD_ROOT%{_gamesbindir}/%{name}.real
%{__cat} <<EOF > $RPM_BUILD_ROOT%{_gamesbindir}/%{name}

cd %{_gamesdatadir}/%{name}
#!/bin/sh
%{_gamesbindir}/%{name}.real \$@
EOF

#icons
%{__install} -d ${RPM_BUILD_ROOT}{%{_miconsdir},%{_liconsdir}}
%{__install} -m644 pics/wl-ico-16.png -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
%{__install} -m644 pics/wl-ico-32.png -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
%{__install} -m644 pics/wl-ico-48.png -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%{__install} -d $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}

%{__install} -d $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}
for i in campaigns game_server fonts maps music pics sound tribes txts worlds; do
	%{__mv} $i \
		$RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/$i
done

mv locale $RPM_BUILD_ROOT/usr/share/locale

%{__install} -d $RPM_BUILD_ROOT%{_menudir}
%{__cat} <<EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):command="%{_gamesbindir}/%{name}" \
		icon=strategy_section.png \
		needs="x11" \
		section="Amusement/Strategy" \
		title="Widelands"\
		longtitle="%{Summary}"\
		xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Widelands
Comment=%{Summary}
Exec=%{_gamesbindir}/%{name}.real
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;StrategyGame;X-MandrivaLinux-MoreApplications-Games-Strategy;
EOF

%find_lang %{name} --all-name

%post
%update_menus

%postun
%clean_menus

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(644,root,root,755)
%doc ChangeLog README.developers COPYING
%{_gamesdatadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%defattr(755,root,root,755)
%{_gamesbindir}/%{name}*


