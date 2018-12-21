Name:       pcre
%define keepstatic 1

Summary:    Perl-compatible regular expression library
Version:    8.31
Release:    5
Group:      System/Libraries
License:    BSD
URL:        http://www.pcre.org/
Source0:    ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{name}-%{version}.tar.bz2
# Fix unused memory usage on zero-repeat assertion condition.
# CVE-2014-8964, in upstream after 8.36
Patch0: pcre-8.33-Fix-zero-repeat-assertion-condition-bug.patch
#Fix compilation/tests with gcc4.9
Patch1: pcre-8.35-Fix-silly-quantifier-size-check.patch
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

%description
Perl-compatible regular expression library.
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. The header file
for the POSIX-style functions is called pcreposix.h.

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files (Headers, libraries for dynamic linking, etc) for %{name}.

%package static
Summary:    Static libraries files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description static
Static development files for %{name}.

%package doc
Summary:    Documentation for %{name}
Group:      Documentation
Requires:   %{name} = %{version}-%{release}

%description doc
Man pages and documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .zero_repeat_assertion
%patch1 -p1 -b .fix_silly_quantifier_size_check

%build
libtoolize --copy --force && autoreconf -vfi
# One contributor's name is non-UTF-8
for F in ChangeLog; do
iconv -f latin1 -t utf8 "$F" >"${F}.utf8"
touch --reference "$F" "${F}.utf8"
mv "${F}.utf8" "$F"
done

%configure  \
%ifnarch aarch64
    --enable-jit \
%endif
    --enable-utf \
    --enable-unicode-properties \
    --enable-pcre8 \
    --enable-pcre16

make %{_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_bindir}/pcregrep
%{_bindir}/pcretest

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_bindir}/pcre-config

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

%files doc
%defattr(-,root,root,-)
%{_mandir}/*/*.gz
%doc %{_docdir}/pcre
