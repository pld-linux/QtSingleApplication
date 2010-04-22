Summary:	Qt library to start applications only once per user
Name:		QtSingleApplication
Version:	2.6
Release:	2
License:	GPL v3 or LGPL v2 with exceptions
Group:		Libraries
URL:		http://qt.nokia.com/products/appdev/add-on-products/catalog/4/Utilities/qtsingleapplication
Source0:	http://get.qt.nokia.com/qt/solutions/lgpl/qtsingleapplication-%{version}_1-opensource.tar.gz
# Source0-md5:	902795eb13ecedbdc112f00d7ec22949
Source1:	qtsingleapplication.prf
Patch0:		qtsingleapplication-build.diff
Patch1:		qtsingleapplication-dont-bundle-external-libs.patch
BuildRequires:	QtLockedFile-devel
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

%package	devel
Summary:	Development files for QtSingleApplication
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	qt4-build
Requires:	qt4-qmake

%description	devel
This package contains libraries and header files for developing
applications that use QtSingleApplication.

%prep
%setup -q -n qtsingleapplication-%{version}_1-opensource
%patch0 -p1
%patch1 -p1

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
install -d $RPM_BUILD_ROOT%{_includedir}/QtSolutions
cp -a \
    src/qtsingleapplication.h \
    src/QtSingleApplication \
    src/qtsinglecoreapplication.h \
    src/QtSingleCoreApplication \
    $RPM_BUILD_ROOT%{_includedir}/QtSolutions

install -d $RPM_BUILD_ROOT%{_qt4_datadir}/mkspecs/features
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_qt4_datadir}/mkspecs/features

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LGPL_EXCEPTION.txt LICENSE.* README.TXT
%attr(755,root,root) %{_libdir}/libQtSolutions_SingleApplication-%{version}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtSolutions_SingleApplication-%{version}.so.1

%files devel
%defattr(644,root,root,755)
%doc doc examples
%{_libdir}/libQtSolutions_SingleApplication-%{version}.so
# XXX dir shared dir with QtLockedFile.spec
%dir %{_includedir}/QtSolutions
%{_includedir}/QtSolutions/QtSingleApplication
%{_includedir}/QtSolutions/QtSingleCoreApplication
%{_includedir}/QtSolutions/qtsingleapplication.h
%{_includedir}/QtSolutions/qtsinglecoreapplication.h
%{_qt4_datadir}/mkspecs/features/qtsingleapplication.prf
