%{?scl:%scl_package perl-DBD-MySQL}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}perl-DBD-MySQL
Version:        4.025
Release:        4%{?dist}
Summary:        A MySQL interface for Perl
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/DBD-mysql/
Source0:        http://www.cpan.org/authors/id/C/CA/CAPTTOFU/DBD-mysql-%{version}.tar.gz
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
BuildRequires:  mysql, mysql-devel
%else
BuildRequires:  mariadb, mariadb-devel
%endif
BuildRequires:  zlib-devel
BuildRequires:  %{?scl_prefix}perl
BuildRequires:  %{?scl_prefix}perl(Carp)
BuildRequires:  %{?scl_prefix}perl(Config)
BuildRequires:  %{?scl_prefix}perl(Data::Dumper)
BuildRequires:  %{?scl_prefix}perl(DBI) >= 1.08
BuildRequires:  %{?scl_prefix}perl(DBI::DBD)
BuildRequires:  %{?scl_prefix}perl(DynaLoader)
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker)
BuildRequires:  %{?scl_prefix}perl(File::Basename)
BuildRequires:  %{?scl_prefix}perl(File::Copy)
BuildRequires:  %{?scl_prefix}perl(File::Path)
BuildRequires:  %{?scl_prefix}perl(File::Spec)
BuildRequires:  %{?scl_prefix}perl(Getopt::Long)
BuildRequires:  %{?scl_prefix}perl(strict)
BuildRequires:  %{?scl_prefix}perl(warnings)
%{?scl:%global perl_version %(scl enable %{scl} 'eval "`perl -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`perl -V:version`"; echo $version)}
Requires:  %{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})
Provides:       %{?scl_prefix}perl-DBD-mysql = %{version}-%{release}

%{?perl_default_filter}

%description 
DBD::mysql is the Perl5 Database Interface driver for the MySQL database. In
other words: DBD::mysql is an interface between the Perl programming language
and the MySQL programming API that comes with the MySQL relational database
management system.

%prep
%setup -q -n DBD-mysql-%{version}
# Correct file permissions
find . -type f | xargs chmod -x

for file in lib/DBD/mysql.pm ChangeLog; do
  iconv -f iso-8859-1 -t utf-8 <$file >${file}_
  touch -r ${file}{,_}
  mv -f ${file}{_,}
done

%build
%{?scl:scl enable %{scl} '}
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" --ssl
%{?scl:'}
%{?scl:scl enable %{scl} "}
make %{?_smp_mflags}
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
%{?scl:"}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
# Full test coverage requires a live MySQL database
#make test

%files
%doc ChangeLog eg README.pod TODO
%{perl_vendorarch}/Bundle/
%{perl_vendorarch}/DBD/
%{perl_vendorarch}/auto/DBD/
%{_mandir}/man3/*.3*

%changelog
* Thu Feb 13 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.025-4
- Fix releases at changelog
- Resolves: rhbz#1064855

* Thu Feb 13 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.025-3
- Updated conditions to work properly for non-RHEL systems
- Resolves: rhbz#1064855

* Mon Jan 20 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.025-2
- Rebuilt against new libmysqlclient.so 
- Resolves: rhbz#1053653

* Tue Nov 19 2013 Jitka Plesnikova <jplesnik@redhat.com> - 4.025-1
- 4.025 bump

* Wed May 22 2013 Jitka Plesnikova <jplesnik@redhat.com> - 4.023-1
- 4.023 bump

* Fri Apr 05 2013 Jitka Plesnikova <jplesnik@redhat.com> - 4.022-1
- SCL package - initial import
