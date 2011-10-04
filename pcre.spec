#specfile originally created for Fedora, modified for MeeGo Linux
Name: pcre
Version: 8.11
Release: 1
Summary: Perl-compatible regular expression library
URL: http://www.pcre.org/
Source: ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{name}-%{version}.tar.bz2
Patch0: pcre-8.10-multilib.patch
License: BSD
Group: System/Libraries
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
# New libtool to get rid of rpath
BuildRequires: autoconf, automake, libtool

%description
Perl-compatible regular expression library.
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. The header file
for the POSIX-style functions is called pcreposix.h.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development files (Headers, libraries for dynamic linking, etc) for %{name}.

%prep
%setup -q
# Get rid of rpath
%patch0 -p1 -b .multilib
libtoolize --copy --force && autoreconf
# One contributor's name is non-UTF-8
for F in ChangeLog; do
    iconv -f latin1 -t utf8 "$F" >"${F}.utf8"
    touch --reference "$F" "${F}.utf8"
    mv "${F}.utf8" "$F"
done

%build
%configure --enable-utf8 --enable-unicode-properties

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install

mkdir -p $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libpcre.so.* $RPM_BUILD_ROOT/%{_lib}/
pushd $RPM_BUILD_ROOT%{_libdir}
ln -fs ../../%{_lib}/libpcre.so.0 libpcre.so
popd

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%docs_package

%files
%defattr(-,root,root,-)
/%{_lib}/*.so.*
%{_libdir}/*.so.*
%{_bindir}/pcregrep
%{_bindir}/pcretest

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_bindir}/pcre-config
%doc %{_docdir}/pcre
