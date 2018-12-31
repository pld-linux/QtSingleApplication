#
# Conditional build:
%bcond_without	qt4		# build Qt4
%bcond_without	qt5		# build Qt5

# last commit to qtsingleapplication subdir in
# https://qt.gitorious.org/qt-solutions/qt-solutions/
%define	commit	ad9bc4600ce769a8b3ad10910803cd555811b70c
Summary:	Qt 4 library to start applications only once per user
Summary(pl.UTF-8):	Biblioteka Qt 4 do uruchamiania pojedynczej instancji aplikacji na użytkownika
Name:		QtSingleApplication
Version:	2.6.1
Release:	5
License:	GPL v3 or LGPL v2 with exceptions
Group:		Libraries
Source0:	https://github.com/qtproject/qt-solutions/archive/%{commit}/%{name}-%{commit}.tar.gz
# Source0-md5:	07f01898ad475c5cded2968d25bee85c
Source1:	qtsingleapplication.prf
Source2:	qtsinglecoreapplication.prf
Patch0:		qtsingleapplication-build.diff
Patch1:		qtlockedfile.patch
Patch2:		clementine.patch
Patch3:		version.patch
Patch4:		qtsingleapplication-install.patch
URL:		http://doc.qt.digia.com/solutions/4/qtsingleapplication/qtsingleapplication.html
BuildRequires:	glibc-misc
BuildRequires:	libstdc++-devel
%if %{with qt4}
BuildRequires:	QtGui-devel >= 4
BuildRequires:	QtLockedFile-devel
BuildRequires:	QtNetwork-devel >= 4
BuildRequires:	qt4-build >= 4
BuildRequires:	qt4-qmake >= 4
%endif
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5.4
BuildRequires:	Qt5Gui-devel >= 5.4
BuildRequires:	Qt5LockedFile-devel
BuildRequires:	Qt5Network-devel >= 5.4
BuildRequires:	Qt5Widgets-devel >= 5.4
BuildRequires:	qt5-build >= 5.4
BuildRequires:	qt5-qmake >= 5.4
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt4dir	%{_datadir}/qt4
%define		qt5dir	%{_libdir}/qt5

%description
For some applications it is useful or even critical that they are
started only once by any user. Future attempts to start the
application should activate any already running instance, and possibly
perform requested actions, e.g. loading a file, in that instance.

The QtSingleApplication class provides an interface to detect a
running instance, and to send command strings to that instance.

For console (non-GUI) applications, the QtSingleCoreApplication
variant is provided, which avoids dependency on QtGui.

%description -l pl.UTF-8
Dla niektórych aplikacji przydatne, lub nawet krytyczne, jest to, aby
uruchamiane były tylko w jednej instancji na użytkownika. Kolejne
próby uruchomienia powinny aktywować już działającą instancję i
ewentualnie wyjonywać żądane akcje, np. załadowanie pliku w tej
instancji.

Klasa QtSingleApplication udostępnia interfejs do wykrywania
działającej instancji i wysyłania do niej łańcuchów poleceń.

Dla aplikacji konsolowych (bez GUI) udostępniony jest wariant
QtSingleCoreApplication, który nie ma zależności od QtGui.

%package devel
Summary:	Development files for QtSingleApplication
Summary(pl.UTF-8):	Pliki programistyczne biblioteki QtSingleApplication
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	QtCore-devel >= 4

%description devel
This package contains header files for developing applications that
use QtSingleApplication.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących QtSingleApplication.

%package -n Qt5SingleApplication
Summary:	Qt 5 library to start applications only once per user
Summary(pl.UTF-8):	Biblioteka Qt 5 do uruchamiania pojedynczej instancji aplikacji na użytkownika
Group:		Libraries

%description -n Qt5SingleApplication
For some applications it is useful or even critical that they are
started only once by any user. Future attempts to start the
application should activate any already running instance, and possibly
perform requested actions, e.g. loading a file, in that instance.

The QtSingleApplication class provides an interface to detect a
running instance, and to send command strings to that instance.

For console (non-GUI) applications, the QtSingleCoreApplication
variant is provided, which avoids dependency on QtGui.

%description -n Qt5SingleApplication -l pl.UTF-8
Dla niektórych aplikacji przydatne, lub nawet krytyczne, jest to, aby
uruchamiane były tylko w jednej instancji na użytkownika. Kolejne
próby uruchomienia powinny aktywować już działającą instancję i
ewentualnie wyjonywać żądane akcje, np. załadowanie pliku w tej
instancji.

Klasa QtSingleApplication udostępnia interfejs do wykrywania
działającej instancji i wysyłania do niej łańcuchów poleceń.

Dla aplikacji konsolowych (bez GUI) udostępniony jest wariant
QtSingleCoreApplication, który nie ma zależności od QtGui.

%package -n Qt5SingleApplication-devel
Summary:	Development files for Qt5SingleApplication library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki Qt5SingleApplication
Group:		Development/Libraries
Requires:	Qt5SingleApplication = %{version}-%{release}
Requires:	Qt5Core-devel >= 5

%description -n Qt5SingleApplication-devel
This package contains header files for developing applications that
use Qt5SingleApplication.

%description -n Qt5SingleApplication-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących Qt5SingleApplication.

%prep
%setup -qc
%{__mv} qt-solutions-* .qtsolutions
%{__mv} .qtsolutions/qtsingleapplication/* .
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1

# We already disabled bundling this external library.
# But just to make sure:
%{__rm} src/{QtLocked,qtlocked}*

%build
# Does not use GNU configure
./configure -library

%if %{with qt4}
install -d build-qt4
cd build-qt4
qmake-qt4 ../qtsingleapplication.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}" \
	INSTALL_LIBDIR=%{_libdir}
%{__make}

# ensure the it links to right version of LockedFile
for l in SingleApplication SingleCoreApplication; do
	f=libQtSolutions_$l-2.6.so
	ldd ../lib/$f | grep libQtSolutions_LockedFile
done
cd ..
%endif

%if %{with qt5}
install -d build-qt5
cd build-qt5
qmake-qt5 ../qtsingleapplication.pro \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}" \
	INSTALL_LIBDIR=%{_libdir}
%{__make}

# ensure the it links to right version of LockedFile
for l in SingleApplication SingleCoreApplication; do
	f=libQt5Solutions_$l-2.6.so
	ldd ../lib/$f | grep libQt5Solutions_LockedFile
done
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with qt4}
%{__make} -C build-qt4 install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_includedir}/qt4/QtSolutions,%{qt4dir}/mkspecs/features}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.so.1.0
cp -p src/qtsingle*application.h src/QtSingle*Application $RPM_BUILD_ROOT%{_includedir}/qt4/QtSolutions
cp -p %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{qt4dir}/mkspecs/features
%endif

%if %{with qt5}
%{__make} -C build-qt5 install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_includedir}/qt5/QtSolutions,%{qt5dir}/mkspecs/features}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.so.1.0
cp -p src/qtsingle*application.h src/QtSingle*Application $RPM_BUILD_ROOT%{_includedir}/qt5/QtSolutions
%{__sed} -e 's/-lQtSolutions/-lQt5Solutions/g' %{SOURCE1} > $RPM_BUILD_ROOT%{qt5dir}/mkspecs/features/qtsingleapplication.prf
%{__sed} -e 's/-lQtSolutions/-lQt5Solutions/g' %{SOURCE2} > $RPM_BUILD_ROOT%{qt5dir}/mkspecs/features/qtsinglecoreapplication.prf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post	-n Qt5SingleApplication -p /sbin/ldconfig
%postun	-n Qt5SingleApplication -p /sbin/ldconfig

%if %{with qt4}
%files
%defattr(644,root,root,755)
%doc README.TXT
%attr(755,root,root) %{_libdir}/libQtSolutions_SingleApplication-2.6.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtSolutions_SingleApplication-2.6.so.1
%attr(755,root,root) %{_libdir}/libQtSolutions_SingleCoreApplication-2.6.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtSolutions_SingleCoreApplication-2.6.so.1

%files devel
%defattr(644,root,root,755)
%doc doc examples
%attr(755,root,root) %{_libdir}/libQtSolutions_SingleApplication-2.6.so
%attr(755,root,root) %{_libdir}/libQtSolutions_SingleCoreApplication-2.6.so
%{_includedir}/qt4/QtSolutions/QtSingleApplication
%{_includedir}/qt4/QtSolutions/QtSingleCoreApplication
%{_includedir}/qt4/QtSolutions/qtsingleapplication.h
%{_includedir}/qt4/QtSolutions/qtsinglecoreapplication.h
%{qt4dir}/mkspecs/features/qtsingleapplication.prf
%{qt4dir}/mkspecs/features/qtsinglecoreapplication.prf
%endif

%if %{with qt5}
%files -n Qt5SingleApplication
%defattr(644,root,root,755)
%doc README.TXT
%attr(755,root,root) %{_libdir}/libQt5Solutions_SingleApplication-2.6.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Solutions_SingleApplication-2.6.so.1
%attr(755,root,root) %{_libdir}/libQt5Solutions_SingleCoreApplication-2.6.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Solutions_SingleCoreApplication-2.6.so.1

%files -n Qt5SingleApplication-devel
%defattr(644,root,root,755)
%doc doc examples
%attr(755,root,root) %{_libdir}/libQt5Solutions_SingleApplication-2.6.so
%attr(755,root,root) %{_libdir}/libQt5Solutions_SingleCoreApplication-2.6.so
%{_includedir}/qt5/QtSolutions/QtSingleApplication
%{_includedir}/qt5/QtSolutions/QtSingleCoreApplication
%{_includedir}/qt5/QtSolutions/qtsingleapplication.h
%{_includedir}/qt5/QtSolutions/qtsinglecoreapplication.h
%{qt5dir}/mkspecs/features/qtsingleapplication.prf
%{qt5dir}/mkspecs/features/qtsinglecoreapplication.prf
%endif
