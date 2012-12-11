%define bld	17

Summary:	Settlers II clone
Name:		widelands
Version:	b%{bld}
Release:	3
License:	GPLv2+
Group:		Games/Strategy
URL:		http://www.widelands.org/
Source0:	%{name}-build%{bld}-src.tar.bz2
Source1:	%{name}.desktop
Source10:	widelands.rpmlintrc
# fix "not find boost to build" issue
# patch from Open Build Service
Patch0:		%{name}-build%{bld}_boostfix.diff
# lower gcc optimization from -O3 to O2
Patch1:		widelands-0.17-cxxflags.patch
# fix build error
Patch2:		widelands-0.17-format-not-string-literal.patch

BuildRequires:	boost-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_net-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_gfx-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	optipng
BuildRequires:	pngrewrite
BuildRequires:	ctags
BuildRequires:	gettext-devel
BuildRequires:	cmake
BuildRequires:	ggz-client-libs-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	lua-devel
BuildRequires:	doxygen
BuildRequires: 	python-devel

Requires(post): ggz-client-libs
Requires(preun): ggz-client-libs

Requires:	%{name}-basic-data
Requires:	%{name}-maps
Requires:	%{name}-i18n
Requires:	%{name}-music

%description
Widelands is an open source real-time strategy game. It is built upon 
libSDL and other open source libraries and is still under heavy development.
If you know Settlers I & II™ (© Bluebyte), you might already have a rough 
idea what Widelands is about.

%files
%defattr(644,root,root,755)
%doc ChangeLog COPYING
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%defattr(755,root,root,755)
%{_gamesbindir}/%{name}

#------------------------------------------------

%package -n %{name}-i18n
Summary:	Translations for %{name}
Group:		Games/Strategy
Requires:	%{name} = %{version}

%description -n %{name}-i18n
Files to play %{name} in other languages than English.

%files -n %{name}-i18n
%defattr(644,root,root,755)
%{_gamesdatadir}/%{name}/locale

#------------------------------------------------

%package -n %{name}-basic-data
Summary:	Basic data set for %{name}
Group:		Games/Strategy
Requires:	%{name} = %{version}

%description -n %{name}-basic-data
Basic data set used by %{name}.
Without these files you will not be able to play.

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
Summary:	Maps for %{name}
Group:		Games/Strategy
Requires:	%{name} = %{version}

%description -n %{name}-maps
Maps for %{name}.

%files -n %{name}-maps
%defattr(644,root,root,755)
%{_gamesdatadir}/%{name}/maps

#------------------------------------------------

%package -n %{name}-music
Summary:	Music for %{name}
Group:		Games/Strategy
Requires:	%{name} = %{version}

%description -n %{name}-music
Music files for %{name}.
These are not needed, but may improve fun while playing.

%files -n %{name}-music
%defattr(644,root,root,755)
%{_gamesdatadir}/%{name}/music

#------------------------------------------------


%prep
%setup -q -n %{name}-build%{bld}-src
%patch0 -p1
%patch1 -p0
%patch2 -p1

%build
sed -i "1 i #include <unistd.h>" src/main.cc
%cmake  -DCMAKE_BUILD_TYPE="Release" \
	-DCMAKE_INSTALL_PREFIX=/usr \
	-DWL_BINDIR="games" \
	-DWL_INSTALL_PREFIX="/usr" \
	-DWL_INSTALL_DATADIR="share/games/%{name}" \
	-DWL_INSTALL_LOCALEDIR="share/games/%{name}/locale" \
	-DBoost_USE_STATIC_LIBS=OFF

%make

%install
%makeinstall_std -C build

#icons
install -d %{buildroot}{%{_miconsdir},%{_liconsdir}}
install -m644 pics/wl-ico-16.png -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 pics/wl-ico-32.png -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 pics/wl-ico-48.png -D %{buildroot}%{_liconsdir}/%{name}.png

# .desktop file
install -m644 %{SOURCE1} -D %{buildroot}/%{_datadir}/applications/%{name}.desktop
