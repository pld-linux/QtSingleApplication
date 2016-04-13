#
# Conditional build:
%bcond_without	qt4		# build Qt4
%bcond_without	qt5		# build Qt5

# last commit to qtsingleapplication subdir in
# https://qt.gitorious.org/qt-solutions/qt-solutions/
%define	commit	ad9bc4600ce769a8b3ad10910803cd555811b70c
Summary:	Qt library to start applications only once per user
Name:		QtSingleApplication
Version:	2.6.1
Release:	3
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
URL:		http://doc.qt.digia.com/solutions/4/qtsingleapplication/qtsingleapplication.html
BuildRequires:	glibc-misc
BuildRequires:	libstdc++-devel
%if %{with qt4}
BuildRequires:	QtGui-devel
BuildRequires:	QtLockedFile-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
%endif
%if %{with qt5}
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5LockedFile-devel
BuildRequires:	Qt5Network-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	qt5-build
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

%package devel
Summary:	Development files for QtSingleApplication
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains libraries and header files for developing
applications that use QtSingleApplication.

%package -n Qt5SingleApplication
Summary:	Qt library to start applications only once per user
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

%package -n Qt5SingleApplication-devel
Summary:	Development files for Qt5SingleApplication library
Group:		Development/Libraries
Requires:	Qt5SingleApplication = %{version}-%{release}

%description -n Qt5SingleApplication-devel
This package contains libraries and header files for developing
applications that use Qt5SingleApplication.

%prep
%setup -qc
mv qt-solutions-* .qtsolutions
mv .qtsolutions/qtsingleapplication/* .
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p1

# We already disabled bundling this external library.
# But just to make sure:
rm src/{QtLocked,qtlocked}*

set -- *
install -d build-qt{4,5}
cp -al "$@" build-qt4
cp -al "$@" build-qt5

%build
%if %{with qt4}
cd build-qt4
# Does not use GNU configure
./configure -library
qmake-qt4
%{__make}

# ensure the it links to right version of LockedFile
for l in SingleApplication SingleCoreApplication; do
	f=libQtSolutions_$l-2.6.so
	ldd lib/$f | grep libQtSolutions_LockedFile
done
cd ..
%endif

%if %{with qt5}
cd build-qt5
./configure -library
# XXX fix QtLockedFile package?
qmake-qt5 INCLUDEPATH+=%{_includedir}/qt5/QtSolutions
%{__make}
# XXX: relink with proper version
%{__sed} -i -e 's/QtSolutions/Qt5Solutions/' buildlib/Makefile*
rm -r lib
%{__make}

# ensure the it links to right version of LockedFile
for l in SingleApplication SingleCoreApplication; do
	f=libQt5Solutions_$l-2.6.so
	ldd lib/$f | grep libQt5Solutions_LockedFile
done
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with qt4}
cd build-qt4
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/qt4/QtSolutions,%{qt4dir}/mkspecs/features}
cp -a lib/* $RPM_BUILD_ROOT%{_libdir}
rm $RPM_BUILD_ROOT%{_libdir}/lib*.so.1.0
cp -p src/qtsingle*application.h src/QtSingle*Application $RPM_BUILD_ROOT%{_includedir}/qt4/QtSolutions
cp -p %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{qt4dir}/mkspecs/features
cd ..
%endif

%if %{with qt5}
cd build-qt5
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/qt5/QtSolutions,%{qt5dir}/mkspecs/features}
cp -a lib/* $RPM_BUILD_ROOT%{_libdir}
rm $RPM_BUILD_ROOT%{_libdir}/lib*.so.1.0
cp -p src/qtsingle*application.h src/QtSingle*Application $RPM_BUILD_ROOT%{_includedir}/qt5/QtSolutions
cp -p %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{qt5dir}/mkspecs/features
cd ..

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
%{_libdir}/libQtSolutions_SingleApplication-2.6.so
%{_libdir}/libQtSolutions_SingleCoreApplication-2.6.so
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
%{_libdir}/libQt5Solutions_SingleApplication-2.6.so
%{_libdir}/libQt5Solutions_SingleCoreApplication-2.6.so
%{_includedir}/qt5/QtSolutions/QtSingleApplication
%{_includedir}/qt5/QtSolutions/QtSingleCoreApplication
%{_includedir}/qt5/QtSolutions/qtsingleapplication.h
%{_includedir}/qt5/QtSolutions/qtsinglecoreapplication.h
%{qt5dir}/mkspecs/features/qtsingleapplication.prf
%{qt5dir}/mkspecs/features/qtsinglecoreapplication.prf
%endif
