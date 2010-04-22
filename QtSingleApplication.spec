# TODO
# - rename as QtSingleApplication ?
# - subpackage for non-gui once any package appears needing so (QtSingleCoreApplication)
Summary:	Qt library to start applications only once per user
Name:		qtsingleapplication
Version:	2.6
Release:	1
License:	GPL v3 or LGPL v2 with exceptions
Group:		Libraries
URL:		http://qt.nokia.com/products/appdev/add-on-products/catalog/4/Utilities/qtsingleapplication
Source0:	http://get.qt.nokia.com/qt/solutions/lgpl/%{name}-%{version}_1-opensource.tar.gz
# Source0-md5:	902795eb13ecedbdc112f00d7ec22949
Patch0:		%{name}-build.diff
BuildRequires:	qt4-build
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	qt4-build

%description	devel
This package contains libraries and header files for developing
applications that use QtSingleCoreApplication.

%prep
%setup -q -n %{name}-%{version}_1-opensource
%patch0 -p1

%build
touch .licenseAccepted
# Does not use GNU configure
./configure -library
qmake-qt4
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

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LGPL_EXCEPTION.txt LICENSE.* README.TXT
%attr(755,root,root) %{_libdir}/libQtSolutions_SingleApplication-%{version}.so.1
%attr(755,root,root) %{_libdir}/libQtSolutions_SingleApplication-%{version}.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc doc examples
%{_libdir}/libQtSolutions_SingleApplication-%{version}.so
%{_includedir}/QtSolutions
