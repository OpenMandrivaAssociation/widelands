%define	name	widelands
%define bld	16
%define	version	b%{bld}
%define	release	%mkrel 1
%define	Summary	Settlers II clone

Epoch: 2

Name:		%{name}
Version:	%{version}
Release:	%{release}
URL:		http://www.widelands.org/
Source0:	%{name}-build%{bld}-src.tar.bz2
License:	GPLv2+
Group:		Games/Strategy
Summary:	%{Summary}
BuildRequires:	boost-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_net-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:  png-devel
BuildRequires:  glew-devel
BuildRequires:  zlib-devel
BuildRequires:	optipng 
BuildRequires:	pngrewrite
BuildRequires:	ctags
BuildRequires:	gettext-devel
BuildRequires:	cmake
BuildRequires:	SDL_gfx-devel
BuildRequires:	ggz-client-libs-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtiff-devel
BuildRequires:	lua-devel
BuildRequires:	doxygen
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires(post): ggz-client-libs
Requires(preun): ggz-client-libs
Requires:       %{name}-basic-data
Requires:       %{name}-maps
Suggests:       %{name}-i18n
Suggests:       %{name}-music

%description
Widelands is an open source real-time strategy game. It is built upon 
libSDL and other open source libraries and is still under heavy development.
If you know Settlers I & II™ (© Bluebyte), you might already have a rough 
idea what Widelands is about.

%files
%defattr(644,root,root,755)
%doc ChangeLog COPYING
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%defattr(755,root,root,755)
%{_gamesbindir}/%{name}
%{_datadir}/ggz/%{name}.dsc

#------------------------------------------------

%package -n %{name}-i18n
Summary: Translations for %{name}
Group:   Games/Strategy
Requires: %{name}

%description -n %{name}-i18n
Files to play %{name} in other languages than English.

%files -n %{name}-i18n
%defattr(644,root,root,755)
%{_gamesdatadir}/%{name}/locale

#------------------------------------------------

%package -n %{name}-basic-data
Summary: Basic data set for %{name}
Group:   Games/Strategy
Requires: %{name}

%description -n %{name}-basic-data
Basic data set used by %{name}. Without these files you will not be able to play.

%files -n %{name}-basic-data
%defattr(644,root,root,755)
%{_gamesdatadir}/%{name}/COPYING
%{_gamesdatadir}/%{name}/CREDITS
%{_gamesdatadir}/%{name}/ChangeLog
%{_gamesdatadir}/%{name}/VERSION
%{_gamesdatadir}/%{name}/campaigns
%{_gamesdatadir}/%{name}/fonts
%{_gamesdatadir}/%{name}/global
%{_gamesdatadir}/%{name}/pics
%{_gamesdatadir}/%{name}/scripting
%{_gamesdatadir}/%{name}/sound
%{_gamesdatadir}/%{name}/tribes
%{_gamesdatadir}/%{name}/txts
%{_gamesdatadir}/%{name}/worlds

#------------------------------------------------

%package -n %{name}-maps
Summary: Maps for %{name}
Group:   Games/Strategy
Requires: %{name}

%description -n %{name}-maps
Maps for %{name}.

%files -n %{name}-maps
%defattr(644,root,root,755)
%{_gamesdatadir}/%{name}/maps

#------------------------------------------------

%package -n %{name}-music
Summary: Music for %{name}
Group:   Games/Strategy
Requires: %{name}

%description -n %{name}-music
Music files for %{name}. These are not needed, but may improve fun while playing.

%files -n %{name}-music
%defattr(644,root,root,755)
%{_gamesdatadir}/%{name}/music

#------------------------------------------------


%prep
%setup -q -n %{name}-build%{bld}-src

%build
%cmake -DCMAKE_BUILD_TYPE="Release" \
	-DWL_INSTALL_PREFIX="/usr" \
	-DWL_BINDIR="games" \
	-DWL_DATADIR="share/games/%{name}" \
	-DWL_LOCALEDIR="share/games/%{name}/locale"

%make

%install
%{__rm} -rf %{buildroot}
cd build
%makeinstall_std
cd ..

#icons
%{__install} -d %{buildroot}{%{_miconsdir},%{_liconsdir}}
%{__install} -m644 pics/wl-ico-16.png -D %{buildroot}%{_miconsdir}/%{name}.png
%{__install} -m644 pics/wl-ico-32.png -D %{buildroot}%{_iconsdir}/%{name}.png
%{__install} -m644 pics/wl-ico-48.png -D %{buildroot}%{_liconsdir}/%{name}.png

# include .dsc files
mkdir -p %{buildroot}%{_datadir}/ggz
install -p -D -m644 src/network/game_server/%{name}.dsc %{buildroot}%{_datadir}/ggz/%{name}.dsc

#menu entry
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

%post
%{_bindir}/ggz-config --install --force --modfile=%{_datadir}/ggz/%{name}.dsc || :

%preun
if [ $1 -eq 0 ]; then
   %{_bindir}/ggz-config --remove --modfile=%{_datadir}/ggz/%{name}.dsc || :
fi


