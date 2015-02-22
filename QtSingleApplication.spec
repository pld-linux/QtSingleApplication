# last commit to qtsingleapplication subdir in
# https://qt.gitorious.org/qt-solutions/qt-solutions/
%define	commit	841982ceec9d30a7ab7324979a0fd5c9c36fd121
Summary:	Qt library to start applications only once per user
Name:		QtSingleApplication
Version:	2.6.1
Release:	1
License:	GPL v3 or LGPL v2 with exceptions
Group:		Libraries
# git clone git@gitorious.org:qt-solutions/qt-solutions.git
# git checkout %{commit}
# tar -cjf QtSingleApplication-%{version}.tar.bz2 -C qt-solutions/qtsingleapplication .
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	2442ba5536b99b4b9144bd33ea23cb17
Source1:	qtsingleapplication.prf
Source2:	qtsinglecoreapplication.prf
Patch0:		qtsingleapplication-build.diff
Patch1:		qtlockedfile.patch
Patch2:		clementine.patch
URL:		http://doc.qt.digia.com/solutions/4/qtsingleapplication/qtsingleapplication.html
BuildRequires:	QtCore-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtLockedFile-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_qt4_datadir	%{_datadir}/qt4

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
Requires:	qt4-build
Requires:	qt4-qmake

%description devel
This package contains libraries and header files for developing
applications that use QtSingleApplication.

%prep
%setup -qc
%patch0 -p0
%patch1 -p0
%patch2 -p1

# We already disabled bundling this extrenal library.
# But just to make sure:
rm src/{QtLocked,qtlocked}*

%build
touch .licenseAccepted
# Does not use GNU configure
./configure \
	-library

# XXX fix QtLockedFile package
qmake-qt4 INCLUDEPATH+=%{_includedir}/QtSolutions
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

# libraries
install -d $RPM_BUILD_ROOT%{_libdir}
cp -a lib/* $RPM_BUILD_ROOT%{_libdir}
rm $RPM_BUILD_ROOT%{_libdir}/lib*.so.1.0

# headers
install -d $RPM_BUILD_ROOT%{_includedir}/qt4/QtSolutions
cp -a \
    src/qtsingleapplication.h \
    src/QtSingleApplication \
    src/qtsinglecoreapplication.h \
    src/QtSingleCoreApplication \
    $RPM_BUILD_ROOT%{_includedir}/qt4/QtSolutions

install -d $RPM_BUILD_ROOT%{_qt4_datadir}/mkspecs/features
cp -a %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_qt4_datadir}/mkspecs/features

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.TXT
#%doc LGPL_EXCEPTION.txt LICENSE.*
%attr(755,root,root) %{_libdir}/libQtSolutions_SingleApplication-2.6.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtSolutions_SingleApplication-2.6.so.1
%attr(755,root,root) %{_libdir}/libQtSolutions_SingleCoreApplication-2.6.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtSolutions_SingleCoreApplication-2.6.so.1

%files devel
%defattr(644,root,root,755)
%doc doc examples
%{_libdir}/libQtSolutions_SingleApplication-2.6.so
%{_libdir}/libQtSolutions_SingleCoreApplication-2.6.so
# XXX dir shared dir with QtLockedFile.spec
%dir %{_includedir}/qt4/QtSolutions
%{_includedir}/qt4/QtSolutions/QtSingleApplication
%{_includedir}/qt4/QtSolutions/QtSingleCoreApplication
%{_includedir}/qt4/QtSolutions/qtsingleapplication.h
%{_includedir}/qt4/QtSolutions/qtsinglecoreapplication.h
%{_qt4_datadir}/mkspecs/features/qtsingleapplication.prf
%{_qt4_datadir}/mkspecs/features/qtsinglecoreapplication.prf
