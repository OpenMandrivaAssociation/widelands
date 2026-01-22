Summary:	Settlers II open source clone
Name:		widelands
Version:	1.3
Release:	2
License:	GPLv2+
Group:		Games/Strategy
Url:		https://www.widelands.org/
Source0:	https://github.com/widelands/widelands/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz
#Source0:	https://launchpad.net/widelands/build20/build20/+download/widelands-build21.tar.bz2
Source1:	%{name}.desktop
Source10:	widelands.rpmlintrc

BuildRequires:	ninja
BuildRequires:	cmake
BuildRequires:	ctags
BuildRequires:	doxygen
BuildRequires:	optipng
BuildRequires:	pngrewrite
BuildRequires:	atomic-devel
BuildRequires:	boost-devel
BuildRequires:  boost-static-devel
BuildRequires:  boost-regex-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk-update-icon-cache
BuildRequires:  optipng
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(asio)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glew)
BuildRequires:  icu-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(minizip)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(SDL2_gfx)
BuildRequires:	pkgconfig(SDL2_image)
BuildRequires:	pkgconfig(SDL2_mixer)
BuildRequires:	pkgconfig(SDL2_net)
BuildRequires:	pkgconfig(SDL2_ttf)
#BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(zlib-ng)

Requires:	%{name}-basic-data
Requires:	%{name}-maps
Obsoletes:	%{name}-i18n
Requires:	%{name}-music

%patchlist
#widelands-1.0-libstdc++-11-missing-include.patch
widelands-zlib-ng.patch

%description
Widelands is an open source real-time strategy game. It is built upon 
libSDL and other open source libraries and is still under heavy development.
If you know Settlers I & II™ (© Bluebyte), you might already have a rough 
idea what Widelands is about.

%files
%doc ChangeLog COPYING
%{_datadir}/applications/org.widelands.Widelands.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_iconsdir}/hicolor/*x*/apps/org.widelands.Widelands.png
%{_bindir}/widelands
%{_mandir}/man6/widelands.6.*
%{_datadir}/metainfo/org.widelands.Widelands.metainfo.xml

#------------------------------------------------

%package -n %{name}-basic-data
Summary:	Basic data set for %{name}
Group:		Games/Strategy
Requires:	%{name} = %{version}

%description -n %{name}-basic-data
Basic data set used by %{name}.
Without these files you will not be able to play.

%files -n %{name}-basic-data

%doc %{_datadir}/doc/%{name}/CREDITS
%doc %{_datadir}/doc/%{name}/VERSION
%{_datadir}/%{name}/ai/
%{_datadir}/%{name}/campaigns/
%{_datadir}/%{name}/i18n/
%{_datadir}/%{name}/images/
%{_datadir}/%{name}/scripting/
%{_datadir}/%{name}/sound/
%{_datadir}/%{name}/templates/
%{_datadir}/%{name}/tribes/
%{_datadir}/%{name}/txts/
%{_datadir}/%{name}/world/
%{_datadir}/%{name}/shaders/
%{_datadir}/%{name}/datadirversion


#------------------------------------------------

%package -n %{name}-maps
Summary:	Maps for %{name}
Group:		Games/Strategy
Requires:	%{name} = %{version}

%description -n %{name}-maps
Maps for %{name}.

%files -n %{name}-maps
%{_datadir}/%{name}/maps/

#------------------------------------------------

%package -n %{name}-music
Summary:	Music for %{name}
Group:		Games/Strategy
Requires:	%{name} = %{version}

%description -n %{name}-music
Music files for %{name}.
These are not needed, but may improve fun while playing.

%files -n %{name}-music
%{_datadir}/%{name}/music/

#------------------------------------------------

%prep
%autosetup -n %{name}-%{version} -p1

%build
export CC=gcc
export CXX=g++
export CXXFLAGS="%{optflags} -std=gnu++17"
%cmake -DCMAKE_BUILD_TYPE="Release" \
	-DBoost_NO_BOOST_CMAKE=ON \
	-DOPTION_BUILD_TESTS=OFF \
	-DOPTION_BUILD_WEBSITE_TOOLS=OFF \
	-DWL_INSTALL_BASEDIR="${EPREFIX}"/usr/share/doc/%{name}/ \
	-DWL_INSTALL_BINDIR="${EPREFIX}"/usr/bin/ \
	-DWL_INSTALL_DATADIR="${EPREFIX}"/usr/share/%{name}/ \
	-G Ninja

%ninja_build

%install
%ninja_install -C build

#icons
install -d %{buildroot}{%{_miconsdir},%{_liconsdir}}
install -m644 data/images/logos/wl-ico-16.png -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 data/images/logos/wl-ico-32.png -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 data/images/logos/wl-ico-48.png -D %{buildroot}%{_liconsdir}/%{name}.png

# from Fedora
# Scripting magic to add proper %%lang() markings to the locale files
find usr/share/widelands/i18n/translations/ -maxdepth 2 -type f -name \*_\*.po | sed -n 's#\(usr/share/widelands/i18n/translations/.*/\([^/]*\)_[^/]*\.po\)#%lang(\2) /\1#p' > %{_builddir}/%{?buildsubdir}/%{name}.files
find usr/share/widelands/i18n/translations/ -maxdepth 2 -type f -name \*.po -and ! -name "*_*.po" | sed -n -e 's#\(usr/share/widelands/i18n/translations/.*/\([^/]\+\)\.po\)#%lang(\2) /\1#p' >> %{_builddir}/%{?buildsubdir}/%{name}.files
find usr/share/widelands/ -mindepth 1 -maxdepth 1 -not -name i18n | sed -n 's#\(usr/share/widelands/*\)#/\1#p' >> %{_builddir}/%{?buildsubdir}/%{name}.files
#popd
	

# .desktop file
#install -m644 %{SOURCE1} -D %{buildroot}/%{_datadir}/applications/%{name}.desktop

# Symlink to PATH
#mkdir -p %{buildroot}%{_bindir}
#ln -s %{_prefix}/games/widelands/widelands %{buildroot}%{_bindir}/
