%define snap 20050801
# no need to bzip2 patches, the macro below makes the .src.rpm use
# bzip2 compression instead of gzip (the default one)
%define _source_payload w9.bzdio

# the Management user/group name/id pair
%define l_musr kolab
%define l_mgrp kolab

# the Management numeric user/group name/id pair
%define l_muid 60001
%define l_mgid 60001

# the Rrestricted user/group name/id pair
%define l_rusr %{l_musr}
%define l_rgrp %{l_mgrp}

# the Non-privileged user/group name/id pair
%define l_nusr %{l_musr}
%define l_ngrp %{l_mgrp}

%define kolab_webroot /var/www/html/kolab

Summary:	Kolab Groupware Server
Name:		kolab
License:	GPL
Version:	1.9.5
Release:	%mkrel 0.%{snap}.5
Group:		System/Servers
URL:		http://www.kolab.org
Source0:	kolabd-%{version}-%{snap}.tar.bz2
Source1:	perl-kolab.tar.bz2
Source2:	kolab.init
Source3:	kolab_bootstrap.sh
Patch0:		kolab-2.0-namespace.diff
# XXX - andreas: use kolab's "macros" instead of hardcoded "ldap" user
Patch3:		kolab-2.0-ldapchown.patch
Patch4:		kolab-2.0-rc.conf.patch
Patch5:		kolabd-1.9.5-apache_template.diff
Patch6:		kolabd-1.9.4-cyradmpath.patch
Patch7:		kolabd-1.9.5-amavisd_template.diff
Patch8:		kolabd-1.9.4-clamav_template.diff
Patch9:		kolabd-1.9.4-postfix_template.diff
Patch10:	kolabd-1.9.5-initrddir.diff
Patch11:	kolabd-1.9.4-resmgr_template.diff
Patch12:	kolabd-1.9.4-fbview_template.diff
Patch13:	kolabd-1.9.4-phpini_template.diff
Patch14:	kolabd-1.9.4-rcconf_template.diff
Patch15:	kolabd-1.9.5-proftpd_template.diff
Patch16:	kolabd-1.9.5-imapd_template.diff
Patch17:	kolabd-1.9.5-main_template.diff
Patch18:	kolabd-1.9.5-smtpd_template.diff
Patch19:	kolabd-1.9.5-transport_template.diff
Patch20:	kolabd-1.9.5-virtual_template.diff
Patch21:	kolabd-1.9.5-slapd_template.diff
Patch22:	kolabd-1.9.5-ldapdistlist.patch
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires(pre):	rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.0.54 apache-mod_php apache-mpm-prefork >= 2.0.54
Requires(pre):	amavisd-new >= 2.2.1-4mdk clamd >= 0.86.2-1mdk cyrus-imapd >= 2.2.12-10mdk openldap-servers postfix >= 2.2.5-4mdk
#Requires(post):	kolab-resource-handlers >= 0.4.1 kolab-webadmin >= 0.4.9
Requires:	apache-conf >= 2.0.54 apache-mod_dav >= 2.0.54 apache-mod_mm_auth_ldap apache-mod_php
Requires:	apache-mod_ssl >= 2.0.54 apache-mpm-prefork >= 2.0.54
Requires:	amavisd-new >= 2.2.1-4mdk clamd >= 0.86.2-1mdk proftpd >= 1.2.10-9mdk cyrus-sasl
Requires:	cyrus-imapd >= 2.2.12-10mdk cyrus-imapd-utils >= 2.2.12-10mdk
Requires:	kolab-resource-handlers >= 0.4.1 kolab-webadmin >= 0.4.9
Requires:	openldap-clients openldap-servers openssl >= 0.9.7e
Requires:	perl-Convert-ASN1 perl-Cyrus perl-ldap perl-Net-Netmask perl-Term-ReadKey
Requires:	perl-Kolab >= 0.9.3 perl-Kolab-Conf >= 0.9.3 perl-Kolab-Cyrus >= 0.9.3 perl-Kolab-DirServ >= 0.9.3
Requires:	perl-Kolab-LDAP >= 0.9.3 perl-Kolab-LDAP-Backend >= 0.9.3 perl-Kolab-LDAP-Backend-dirservd >= 0.9.3
Requires:	perl-Kolab-LDAP-Backend-slurpd >= 0.9.3 perl-Kolab-Mailer >= 0.9.3 perl-Kolab-Util >= 0.9.3
Requires:	php-cli >= 5.0.4 php-imap >= 5.0.4-2mdk php-ldap >= 5.0.4 php-pear >= 5.0.4 php-pear-Net_LMTP php-xml >= 5.0.4
Requires:	postfix >= 2.2.5-4mdk postfix-ldap >= 2.2.5-4mdk
Requires:	spamassassin-spamc >= 2.60 spamassassin-spamd >= 2.60
Requires:       %{mklibname sasl 2}-plug-plain %{mklibname sasl 2}-plug-login
#Conflicts:	kolab-server
Provides:	kolab-server
Obsoletes:	kolab-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
Kolab is the KDE Groupware Server that provides full groupware features
to either KDE Kolab clients or Microsoft Outlook[tm] clients running on 
Windows[tm] using the Toltec Connector http://www.toltec.co.za. It can 
also use Aethera, from TheKompany.com, a multi-platform client that works on
Windows, Linux and Mac OS X.

In addition it is a robust and flexible general imap mail server with 
LDAP addressbook and nice web gui for administration.

%prep

%setup -q -c -n kolabd-%{version}-%{snap} -a1
%patch0 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p0
%patch6 -p1
%patch7 -p0
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p0
%patch16 -p0
%patch17 -p0
%patch18 -p0
%patch19 -p0
%patch20 -p0
%patch21 -p0
%patch22 -p1

cp %{SOURCE2} kolab.init
cp %{SOURCE3} kolab_bootstrap.sh

# fix attribs
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;
	
# cleanup
for i in `find . -type d -name CVS`  `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# major search and replace (aka openpkg anti borker)

# major search and replace (aka openpkg anti borker)
find . -type f|xargs perl -pi -e "s|/kolab/var/resmgr/resmgr\.log|/var/log/kolab/resmgr\.log|g; \
    s|/kolab/var/resmgr/freebusy\.log|/var/log/kolab/freebusy\.log|g; \
    s|/var/resmgr/resmgr\.log|/var/log/kolab/resmgr\.log|g; \
    s|/var/resmgr/freebusy\.log|/var/log/kolab/freebusy\.log|g; \
    s|\@l_prefix\@/bin/perl|%{_bindir}/perl|g; \
    s|\@l_prefix\@/lib/openpkg/bash|/bin/bash|g; \
    s|\@l_prefix\@||g; \
    s|/kolab/bin/|%{_bindir}/|g; \
    s|\\\${prefix}/etc|/etc|g; \
    s|\\\$PREFIX/etc|/etc|g; \
    s|\\\$PREFIX/bin|%{_bindir}|g; \
    s|\\\${prefix}/bin|%{_bindir}|g; \
    s|\\\${prefix}/sbin|%{_sbindir}|g; \
    s|\\\$prefix/var/kolab/kolab\.pid|/var/run/kolab/kolab\.pid|g; \
    s|\\\$kolab_prefix\.||g; \
    s|\\\$kolab_prefix/etc|/etc|g; \
    s|\\\$kolab_prefix/bin|%{_bindir}|g; \
    s|\\\$kolab_prefix/sbin|%{_sbindir}|g; \
    s|\\\$kolab_prefix/libexec/openldap/slapd|%{_sbindir}/slapd|g; \
    s|/kolab/etc/|/etc/|g; \
    s|/etc/resmgr/|/etc/kolab/resmgr/|g; \
    s|/etc/apache/php\.ini|/etc/php\.ini|g; \
    s|\\\${openpkg_prefix}/libexec|%{_datadir}|g; \
    s|\!/bin/php|\!%{_bindir}/php|g; \
    s|/usr/local/bin/php|%{_bindir}/php|g; \
    s|\"/sbin/slappasswd|\"/usr/sbin/slappasswd|g; \
    s|/sbin/slapcat|%{_sbindir}/slapcat|g; \
    s|/etc/sasl/apps/smtpd.conf|/etc/postfix/sasl/smtpd.conf|g; \
    s|/var/openldap/run|/var/run/ldap|g; \
    s|/var/openldap/openldap-data|%{_localstatedir}/ldap-kolab|g; \
    s|/var/openldap/replog|%{_localstatedir}/ldap-kolab/replog|g"

# beware of ordering: s|/var/openldap/stuff|bla|g *before* this one
find . -type f|xargs perl -pi -e "s|/var/openldap|%{_localstatedir}/ldap-kolab|g"
# XXX - andreas: better use a patch, this one is too risky
find . -type f|xargs perl -pi -e "s|openldap-data|ldap-kolab|g"
perl -pi -e "s|/kolab/var/kolab|%{_localstatedir}/kolab|g" kolabdcachetool

perl -pi -e "s|\\\$kolab_prefix/lib/openpkg/tar|/bin/tar|g" kolab_bootstrap

# fix cyrus imap paths
for i in deliver cyradm deliver uux ifmail bsmtp; do
    find . -type f|xargs perl -pi -e "s|%{_bindir}/${i}|%{_prefix}/lib/cyrus-imapd/${i}|g"
done

# fix uid and gid
# the Management user/group name/id pair
find . -type f|xargs perl -pi -e "s|\@l_musr\@|%{l_musr}|g;s|\@l_mgrp\@|%{l_mgrp}|g"

# the Restricted user/group name/id pair
find . -type f|xargs perl -pi -e "s|\@l_rgrp\@|%{l_rgrp}|g;s|\@l_rusr\@|%{l_rusr}|g"

# the Non-privileged user/group name/id pair
find . -type f|xargs perl -pi -e "s|\@l_nusr\@|%{l_nusr}|g;s|\@l_ngrp\@|%{l_ngrp}|g"

pushd templates
# fix ownership of the generated templates
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:ldap|g" DB_CONFIG.slapd.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:ldap|g" ldap.conf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:ldap|g" slapd.access.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:ldap|g" slapd.replicas.template
# amavisd complains if its config file is owned by other than root
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:amavis|g" amavisd.conf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=clamav:clamav|g" clamd.conf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=clamav:clamav|g" freshclam.conf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" cyrus.conf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" fbview.conf.template
# apache needs to read this file
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:%{l_musr}|g" freebusy.conf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" httpd.conf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" httpd.local.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" imapd.conf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" imapd.group.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" ldapdistlist.cf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" ldaptransport.cf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" ldapvirtual.cf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" main.cf.template
# master.cf has a password
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:postfix|g" master.cf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" php.ini.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" proftpd.conf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" rc.conf.template
# postfix and apache need access to this file
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:%{l_musr}|g" resmgr.conf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" saslauthd.conf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" session_vars.php.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" smtpd.conf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" transport.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" virtual.template
# fix locations
perl -pi -e "s|^TARGET.*|TARGET=%{_sysconfdir}/clamd\.conf|g" clamd.conf.template
perl -pi -e "s|^TARGET.*|TARGET=%{_sysconfdir}/freshclam\.conf|g" freshclam.conf.template
perl -pi -e "s|^TARGET.*|TARGET=%{_sysconfdir}/cyrus\.conf|g" cyrus.conf.template
perl -pi -e "s|^TARGET.*|TARGET=%{_sysconfdir}/imapd\.conf|g" imapd.conf.template
perl -pi -e "s|^TARGET.*|TARGET=%{_sysconfdir}/imapd\.group|g" imapd.group.template
perl -pi -e "s|^TARGET.*|TARGET=%{_sysconfdir}/kolab/rc\.conf|g" rc.conf.template
perl -pi -e "s|^TARGET.*|TARGET=%{_sysconfdir}/saslauthd\.conf|g" saslauthd.conf.template
perl -pi -e "s|^TARGET.*|TARGET=%{kolab_webroot}/admin/include/session_vars\.php|g" session_vars.php.template
perl -pi -e "s|^TARGET.*|TARGET=%{_sysconfdir}/postfix/sasl/smtpd\.conf|g" smtpd.conf.template
# fix file attributes
perl -pi -e "s|^PERMISSIONS.*|PERMISSIONS=0644|g" session_vars.php.template
perl -pi -e "s|^PERMISSIONS.*|PERMISSIONS=0644|g" imapd.conf.template
perl -pi -e "s|^PERMISSIONS.*|PERMISSIONS=0644|g" imapd.group.template
perl -pi -e "s|^PERMISSIONS.*|PERMISSIONS=0640|g" master.cf.template
perl -pi -e "s|^PERMISSIONS.*|PERMISSIONS=0640|g" amavisd.conf.template
# virtual has no password or any other secret that I can see, so let it be 0644
perl -pi -e "s|^PERMISSIONS.*|PERMISSIONS=0644|g" virtual.template
perl -pi -e "s|^PERMISSIONS.*|PERMISSIONS=0640|g" resmgr.conf.template
perl -pi -e "s|^PERMISSIONS.*|PERMISSIONS=0640|g" proftpd.conf.template
perl -pi -e "s|^PERMISSIONS.*|PERMISSIONS=0644|g" cyrus.conf.template
perl -pi -e "s|^PERMISSIONS.*|PERMISSIONS=0644|g" saslauthd.conf.template
perl -pi -e "s|^PERMISSIONS.*|PERMISSIONS=0644|g" fbview.conf.template
perl -pi -e "s|^PERMISSIONS.*|PERMISSIONS=0640|g" freebusy.conf.template
perl -pi -e "s|^PERMISSIONS.*|PERMISSIONS=0644|g" resmgr.conf.template
# lib64 fix
perl -pi -e "s|/usr/lib/postfix|%{_libdir}/postfix|g" main.cf.template
perl -pi -e "s|/usr/lib/sasl2|%{_libdir}/sasl2|g" main.cf.template
perl -pi -e "s|/usr/lib/php/extensions|%{_libdir}/php/extensions|g" php.ini.template
perl -pi -e "s|/usr/lib/openldap|%{_libdir}/openldap|g" slapd.conf.template
popd

# version
find . -type f|xargs perl -pi -e "s|\@kolab_version\@|%{version}|g"

%build

# construct the config.h file
pushd perl-kolab
chmod 755 configure
./configure \
    --program-prefix=%{?_program_prefix} \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --dist=Mandriva
popd

%install
rm -rf %{buildroot}

# make some directories
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/amavisd/templates
install -d %{buildroot}%{_sysconfdir}/kolab/templates
install -d %{buildroot}%{_sysconfdir}/kolab/ca
install -d %{buildroot}%{_sysconfdir}/kolab/backup
install -d %{buildroot}%{_sysconfdir}/cron.d
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_sysconfdir}/openldap/schema
install -d %{buildroot}%{_sysconfdir}/kolab/resmgr
install -d %{buildroot}%{_datadir}/kolab
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_var}/log/kolab
install -d %{buildroot}%{_var}/run/kolab
install -d %{buildroot}%{_var}/spool/kolab
install -d %{buildroot}%{_localstatedir}/ldap-kolab
install -d %{buildroot}%{_localstatedir}/kolab

# install the templates
install -m0644 templates/* %{buildroot}%{_sysconfdir}/kolab/templates/
cp -aRf amavisd/* %{buildroot}%{_sysconfdir}/amavisd/templates/

install -m0755 kolab_ca.sh %{buildroot}%{_sysconfdir}/kolab/
install -m0644 kolab.conf %{buildroot}%{_sysconfdir}/kolab/
install -m0644 kolab.globals %{buildroot}%{_sysconfdir}/kolab/
install -m0755 kolab_smtpdpolicy %{buildroot}%{_sysconfdir}/kolab/
install -m0755 kolab_sslcert.sh %{buildroot}%{_sysconfdir}/kolab/
install -m0644 quotawarning.txt %{buildroot}%{_sysconfdir}/kolab/
install -m0644 rootDSE.ldif %{buildroot}%{_sysconfdir}/kolab/
install -m0755 workaround.sh %{buildroot}%{_sysconfdir}/kolab/

install -m0744 namespace/kolab %{buildroot}%{_bindir}/
install -m0755 kolabpasswd %{buildroot}%{_bindir}/

# install the OpenLDAP schemas
install -m0644 kolab2.schema %{buildroot}%{_sysconfdir}/openldap/schema/
install -m0644 rfc2739.schema %{buildroot}%{_sysconfdir}/openldap/schema/

# install name space stuff
install -m0744 namespace/libexec/adduser %{buildroot}%{_datadir}/kolab/
install -m0744 namespace/libexec/deluser %{buildroot}%{_datadir}/kolab/
install -m0744 namespace/libexec/listusers %{buildroot}%{_datadir}/kolab/
install -m0744 namespace/libexec/newconfig %{buildroot}%{_datadir}/kolab/
install -m0744 namespace/libexec/services %{buildroot}%{_datadir}/kolab/
install -m0744 namespace/libexec/showlog %{buildroot}%{_datadir}/kolab/
install -m0744 namespace/libexec/showuser %{buildroot}%{_datadir}/kolab/
install -m0744 namespace/libexec/start %{buildroot}%{_datadir}/kolab/
install -m0744 namespace/libexec/stop %{buildroot}%{_datadir}/kolab/

install -m0744 kolabd %{buildroot}%{_sbindir}/
install -m0744 kolabconf %{buildroot}%{_sbindir}/
install -m0744 kolabcheckperm %{buildroot}%{_sbindir}/
install -m0755 dirservnotify %{buildroot}%{_sbindir}/
install -m0755 dirservupdate %{buildroot}%{_sbindir}/
install -m0755 kolabdcachetool %{buildroot}%{_sbindir}/
install -m0755 kolabquotawarn %{buildroot}%{_sbindir}/
install -m0755 kolabquotareport %{buildroot}%{_sbindir}/

install -m0744 kolab.init %{buildroot}%{_initrddir}/kolab
install -m0744 kolab_bootstrap %{buildroot}%{_sbindir}/kolab_bootstrap.real
install -m0744 kolab_bootstrap.sh %{buildroot}%{_sbindir}/kolab_bootstrap

# install the config.h file (required by the perl-Kolab modules)
install -m0644 perl-kolab/config.h %{buildroot}%{_sysconfdir}/kolab/config.h

# nuke templates for services we do not want to mess with because it is not nessesary
rm -f %{buildroot}%{_sysconfdir}/kolab/templates/clamd.conf.template
rm -f %{buildroot}%{_sysconfdir}/kolab/templates/freshclam.conf.template
rm -f %{buildroot}%{_sysconfdir}/kolab/templates/php.ini.template
rm -f %{buildroot}%{_sysconfdir}/kolab/templates/httpd.local.template

# fix crontab entry for kolabquotawarn
cat > kolabquotawarn.cron << EOF
#!/bin/sh
*/10 * * * * %{_sbindir}/kolabquotawarn
EOF
install -m0755 kolabquotawarn.cron %{buildroot}%{_sysconfdir}/cron.d/kolabquotawarn

# fix logrotate entries
cat > kolab.logrotate << EOF
/var/log/kolab/resmgr.log /var/log/kolab/freebusy.log {
    rotate 5
    monthly
    missingok
    notifempty
    nocompress
    prerotate
	%{_initrddir}/kolab reload
    endscript
    postrotate
	%{_initrddir}/kolab reload
    endscript
}
EOF
install -m0644 kolab.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/kolab

cat << EOF > README.urpmi
This is the first draft of the kolab (kolab2). The web interface should work,
namely adding/removing/modifying users, and the LDAP authentication should
work with Apache, PHP and cyrus-imap. There's still some work to do,
specially testing proftpd.

To test it, do the following:
1) /usr/sbin/kolab_bootstrap -b (note the manager password)
2) service kolab start
3) point your browser to https://localhost/kolab/admin and login as
   user "manager", with the password chosen in step 1.
4) create/modify/delete users
5) close all your browser windows, then return back to the web
administration site, but log in as a regular user you just created, to test
the forwarding and vacation functions, changing password, etc.
6) point your mail client smtp and imap servers to localhost, and try to
send yourself some mail, and read it.

To test the calendaring functions, you'll need the kroupware client, or
Microsoft Outlook with the Binary connector (proprietary).

For a fresh install please initialize Kolab by running '%{_sbindir}/kolab_bootstrap -b'. as user root.
If you upgraded from a previous version simply refresh Kolab by running run '%{_sbindir}/kolabconf' as user root.
In every case execute '%{_initrddir}/kolab restart' as user root.
EOF

%pre
#if getent group %{l_musr} >/dev/null 2>&1 ; then : ; else \
#    /usr/sbin/groupadd -g %{l_mgid} %{l_musr} > /dev/null 2>&1 || exit 1 ; fi
#if getent passwd %{l_musr} >/dev/null 2>&1 ; then : ; else \
#    /usr/sbin/useradd -u %{l_muid} -g %{l_mgid} -M -r -s /bin/bash -c "kolab system user" \
#    -d %{_localstatedir}/kolab %{l_musr} 2> /dev/null || exit 1 ; fi
%_pre_useradd %{l_musr} %{_localstatedir}/kolab /bin/false

# put some users in the kolab group
/usr/bin/gpasswd -a apache %{l_mgrp}
/usr/bin/gpasswd -a cyrus %{l_mgrp}
/usr/bin/gpasswd -a postfix %{l_mgrp}
/usr/bin/gpasswd -a ldap %{l_mgrp}
#/usr/sbin/usermod -G %{l_musr} apache
#/usr/sbin/usermod -G %{l_musr} cyrus
#/usr/sbin/usermod -G %{l_musr},postdrop postfix
#/usr/sbin/usermod -G %{l_musr},adm ldap

%post
%_post_service kolab

%preun
%_preun_service kolab
if [ $1 = 0 ]; then
    %{_sbindir}/kolab_bootstrap --restore
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README* doc/*
%attr(0755,root,root) %{_initrddir}/kolab
%dir %{_sysconfdir}/kolab
%dir %{_sysconfdir}/kolab/templates
%dir %{_sysconfdir}/kolab/ca
%dir %{_sysconfdir}/kolab/backup
%dir %{_sysconfdir}/kolab/resmgr
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/amavisd/templates/*/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/kolab/templates/*.template
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/kolab/kolab.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/kolab/kolab.globals
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/kolab/quotawarning.txt
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/kolab/rootDSE.ldif
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/kolab/config.h
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/kolab
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/schema/kolab2.schema
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/schema/rfc2739.schema
%attr(0755,root,root) %{_sysconfdir}/kolab/kolab_ca.sh
%attr(0755,root,root) %{_sysconfdir}/kolab/kolab_smtpdpolicy
%attr(0755,root,root) %{_sysconfdir}/kolab/kolab_sslcert.sh
%attr(0755,root,root) %{_sysconfdir}/kolab/workaround.sh
%attr(0755,root,root) %{_sysconfdir}/cron.d/kolabquotawarn
%attr(0744,root,root) %{_bindir}/kolab
%attr(0755,root,root) %{_bindir}/kolabpasswd
%attr(0744,root,root) %{_sbindir}/kolabcheckperm
%attr(0744,root,root) %{_sbindir}/kolabconf
%attr(0744,root,root) %{_sbindir}/kolabd
%attr(0755,root,root) %{_sbindir}/kolab_bootstrap.real
%attr(0755,root,root) %{_sbindir}/kolab_bootstrap
%attr(0755,root,root) %{_sbindir}/dirservnotify
%attr(0755,root,root) %{_sbindir}/dirservupdate
%attr(0755,root,root) %{_sbindir}/kolabdcachetool
%attr(0755,root,root) %{_sbindir}/kolabquotawarn
%attr(0755,root,root) %{_sbindir}/kolabquotareport
%attr(0755,%{l_musr},%{l_mgrp}) %dir %{_var}/spool/kolab
%attr(0755,%{l_musr},%{l_mgrp}) %dir %{_var}/run/kolab
%attr(0775,%{l_musr},%{l_mgrp}) %dir %{_var}/log/kolab
%attr(0700,ldap,ldap) %dir %{_localstatedir}/ldap-kolab
%attr(0750,%{l_musr},%{l_mgrp}) %dir %{_localstatedir}/kolab
%dir %{_datadir}/kolab
%attr(0755,root,root) %{_datadir}/kolab/adduser
%attr(0755,root,root) %{_datadir}/kolab/deluser
%attr(0755,root,root) %{_datadir}/kolab/listusers
%attr(0755,root,root) %{_datadir}/kolab/newconfig
%attr(0755,root,root) %{_datadir}/kolab/services
%attr(0755,root,root) %{_datadir}/kolab/showlog
%attr(0755,root,root) %{_datadir}/kolab/showuser
%attr(0755,root,root) %{_datadir}/kolab/start
%attr(0755,root,root) %{_datadir}/kolab/stop



