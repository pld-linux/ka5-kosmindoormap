#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	23.08.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kosmindoormap
Summary:	A library for rendering multi-level OSM indoor maps
Name:		ka5-%{kaname}
Version:	23.08.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	49f48bd805ab3112412c6694b90040a6
URL:		https://community.kde.org/
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Network-devel >= 5.15.2
BuildRequires:	Qt5Qml-devel >= 5.15.2
BuildRequires:	Qt5Quick-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	ka5-kopeninghours-devel >= %{kdeappsver}
BuildRequires:	ka5-kpublictransport-devel >= %{kdeappsver}
BuildRequires:	kf5-extra-cmake-modules >= 5.89
BuildRequires:	kf5-ki18n-devel
BuildRequires:	ninja
BuildRequires:	protobuf-devel
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library and QML component for rendering multi-level OSM indoor maps
of for example a (large) train station.

## Features

User facing:
- Floor-level separation of OSM data and inter-floor navigation using
  stairs, escalators or elevators.
- Information model for showing details about a selected amenity.
- Support for identifying railway platforms or airport gates in the
  map data.
- Integration with KPublicTransport line meta-data to show line icons
  for railway platforms.
- Integration with KPublicTransport rental vehicle data to show
  availability of rental bikes.
- Integration with KPublicTransport realtime equipment
  (elevators/escalators/etc) status information.

Technical:
- QPainter and QML integration interface.
- Declarative styling using MapCSS.
- Picking support for implementing interaction with map elements.
- Support for externally provided overlay elements.
- Based on OSM raw data tiles from maps.kde.org.
- Pre-loading and caching API for offline support in applications.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKOSM.so.1
%attr(755,root,root) %{_libdir}/libKOSM.so.*.*.*
%ghost %{_libdir}/libKOSMIndoorMap.so.1
%attr(755,root,root)%{_libdir}/libKOSMIndoorMap.so.*.*.*
%{_libdir}/qt5/qml/org/kde/kosmindoormap/IndoorMap.qml
%{_libdir}/qt5/qml/org/kde/kosmindoormap/IndoorMapAttributionLabel.qml
%{_libdir}/qt5/qml/org/kde/kosmindoormap/IndoorMapScale.qml
%dir %{_libdir}/qt5/qml/org/kde/kosmindoormap
%dir %{_libdir}/qt5/qml/org/kde/kosmindoormap/kpublictransport
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/kosmindoormap/kpublictransport/libkosmindoormap_kpublictransport_integration_plugin.so
%{_libdir}/qt5/qml/org/kde/kosmindoormap/kpublictransport/qmldir
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/kosmindoormap/libkosmindoormapquickplugin.so
%{_libdir}/qt5/qml/org/kde/kosmindoormap/qmldir
%{_datadir}/qlogging-categories5/org_kde_kosmindoormap.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KOSM
%{_includedir}/KOSMIndoorMap
%{_includedir}/kosm
%{_includedir}/kosmindoormap
%{_includedir}/kosmindoormap_version.h
%{_libdir}/cmake/KOSMIndoorMap
%{_libdir}/libKOSM.so
%{_libdir}/libKOSMIndoorMap.so
