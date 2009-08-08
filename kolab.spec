%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

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

%define _default_patch_fuzz 0



Summary:	Kolab Groupware Server
Name:	kolab
License:	GPL
Version:	2.1.0
Release:	%mkrel 10
Group:		System/Servers
URL:		http://www.kolab.org
Source0:	kolabd-%{version}.tar.bz2
#Source1:	mandriva
Source2:	kolab.init
Source3:	kolab_bootstrap.sh
Patch0:		kolabd-kolabnamespacedir.diff
Patch1:		kolabd-bash_shellbang.diff
Patch2:		kolabd-apache_template.diff
Patch3:		kolabd-slapd.diff
Patch4:		kolabd-rc.conf.diff
Patch5:		kolabd-sysv.diff
Patch6:		kolabd-slapd_template.diff
Patch7:		kolabd-ldap_dir_chown.diff
Patch8:		kolabd-amavisd_template.diff
Patch9:		kolabd-cyrus-imapd_template.diff
Patch10:	kolabd-proftpd_template.diff
Patch11:	kolabd-postfix_template.diff
Patch13:	kolabd-smtpd_template.diff
Patch14:	kolabd-transport_template.diff
Patch15:	kolabd-virtual_template.diff
Patch16:	kolabd-imapd_template_loginfix.diff
Patch17:	kolabd-amavisd_template_log.diff
Patch18:	kolab.globals.diff
Patch19:	mandriva.diff
Patch20:	common.diff
Requires(post):	rpm-helper
Requires(preun):rpm-helper
Requires(pre):	rpm-helper
Requires(postun): rpm-helper
Requires(pre):	amavisd-new >= 2.4.5
Requires(pre):	apache-conf >= 2.2.6
Requires(pre):	apache-mod_php
Requires(pre):	apache-mpm-prefork >= 2.2.6
Requires(pre):	clamd >= 0.90.3
Requires(pre):	cyrus-imapd >= 2.2.12
Requires(pre):	openldap-servers
Requires(pre):	postfix >= 2.2.5
Requires:	amavisd-new >= 2.4.5
Requires:	apache-conf >= 2.2.6
Requires:	apache-mod_dav >= 2.2.6
Requires:	apache-mod_ldap >= 2.2.6
Requires:	apache-mod_php
Requires:	apache-mod_ssl >= 2.2.6
Requires:	apache-mpm-prefork >= 2.2.6
Requires:	clamd >= 0.90.3
Requires:	cyrus-imapd >= 2.2.12
Requires:	cyrus-imapd-utils >= 2.2.12
Requires:	cyrus-sasl
Requires:	kolab-resource-handlers >= 2.1.0
Requires:	kolab-webadmin >= 2.1.0
Requires:	%{mklibname sasl 2}-plug-login
Requires:	%{mklibname sasl 2}-plug-plain
Requires:	openldap-clients
Requires:	openldap-servers
Requires:	openssl >= 0.9.7e
Requires:	perl-Convert-ASN1
Requires:	perl-Cyrus
Requires:	perl-kolab
Requires:	perl-ldap
Requires:	perl-Net-Netmask
Requires:	perl-Term-ReadKey
Requires:	php-cli >= 5.2.2
Requires:	php-imap >= 5.2.2
Requires:	php-ldap >= 5.2.2
Requires:	php-pear >= 5.2.2
Requires:	php-pear-Net_LMTP
Requires:	php-xml >= 5.2.2
Requires:	postfix >= 2.2.5
Requires:	postfix-ldap >= 2.2.5
Requires:	proftpd >= 1.3.0
Requires:	proftpd-mod_ldap >= 1.3.0
Requires:	spamassassin-spamc >= 3.1.8
Requires:	spamassassin-spamd >= 3.1.8
Provides:	kolab-server
Obsoletes:	kolab-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
Kolab is the KDE Groupware Server that provides full groupware features to
either KDE Kolab clients or Microsoft Outlook[tm] clients running on
Windows[tm] using the Toltec Connector http://www.toltec.co.za. It can also use
Aethera, from TheKompany.com, a multi-platform client that works on Windows,
Linux and Mac OS X.

In addition it is a robust and flexible general imap mail server with LDAP
addressbook and nice web gui for administration.

%prep

%setup -q -n kolabd-%{version}
%patch0 -p0
%patch1 -p1
%patch2 -p0
%patch3 -p0
%patch4 -p1
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p0
%patch9 -p1
%patch10 -p0
%patch11 -p0
%patch13 -p0
%patch14 -p0
%patch15 -p0
%patch16 -p0
%patch17 -p0
%patch18 -p0
%patch19 -p0
%patch20 -p0

cp %{SOURCE2} kolab.init
cp %{SOURCE3} kolab_bootstrap.sh

# cleanup
for i in `find . -type d -name CVS`  `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# fix perl_vendordir
perl -pi -e "s|perl_vendorlib|%{perl_vendorlib}|g" dist_conf/mandriva

# force regeneration
rm -f kolabcheckperm
rm -f namespace/libexec/start
rm -f namespace/libexec/stop

%build
aclocal; automake --add-missing --copy; autoconf

%configure2_5x \
    --with-dist=mandriva

%make

%install
rm -rf %{buildroot}

%makeinstall_std

# make some directories
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/amavisd/templates
install -d %{buildroot}%{_sysconfdir}/kolab/templates
install -d %{buildroot}%{_sysconfdir}/kolab/ca
install -d %{buildroot}%{_sysconfdir}/kolab/backup
install -d %{buildroot}%{_sysconfdir}/cron.d
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_datadir}/openldap/schema
install -d %{buildroot}%{_sysconfdir}/kolab/resmgr
install -d %{buildroot}%{_datadir}/kolab
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_var}/log/kolab
install -d %{buildroot}%{_var}/run/kolab
install -d %{buildroot}%{_var}/amavis
install -d %{buildroot}%{_var}/clamav
install -d %{buildroot}%{_var}/spool/kolab
install -d %{buildroot}%{_localstatedir}/lib/ldap-kolab
install -d %{buildroot}%{_localstatedir}/lib/kolab

install -m0744 kolab.init %{buildroot}%{_initrddir}/kolab
install -m0744 kolab_bootstrap.sh %{buildroot}%{_sbindir}/kolab_bootstrap

# nuke templates for services we do not want to mess with because it is not nessesary
rm -f %{buildroot}%{_sysconfdir}/kolab/templates/clamd.conf.template
rm -f %{buildroot}%{_sysconfdir}/kolab/templates/freshclam.conf.template
rm -f %{buildroot}%{_sysconfdir}/kolab/templates/php.ini.template
rm -f %{buildroot}%{_sysconfdir}/kolab/templates/httpd.local.template


# cleanup
rm -f %{buildroot}%{_initrddir}/rc*
rm -rf %{buildroot}%{_datadir}/doc/kolab

# fix crontab entry for kolabquotawarn
cat > kolabquotawarn.cron << EOF
#!/bin/sh
*/10 * * * * %{_datadir}/kolab/scripts/kolabquotawarn
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
This is an updated version that works with the current ldap server. Please test it and report problems.
The calendering function may not be working

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



pushd %{buildroot}%{_sysconfdir}/kolab/templates
# fix ownership of the generated templates
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:ldap|g" DB_CONFIG.slapd.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:ldap|g" ldap.conf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:ldap|g" slapd.conf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:ldap|g" slapd.access.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:ldap|g" slapd.replicas.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" ldapdistlist.cf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" ldaptransport.cf.template
perl -pi -e "s|^OWNERSHIP.*|OWNERSHIP=root:root|g" ldapvirtual.cf.template
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
popd

%pre
#if getent group %{l_musr} >/dev/null 2>&1 ; then : ; else \
#    /usr/sbin/groupadd -g %{l_mgid} %{l_musr} > /dev/null 2>&1 || exit 1 ; fi
#if getent passwd %{l_musr} >/dev/null 2>&1 ; then : ; else \
#    /usr/sbin/useradd -u %{l_muid} -g %{l_mgid} -M -r -s /bin/bash -c "kolab system user" \
#    -d %{_localstatedir}/lib/kolab %{l_musr} 2> /dev/null || exit 1 ; fi
%_pre_useradd %{l_musr} %{_localstatedir}/lib/kolab /bin/false

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
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README.urpmi
%doc doc/README.amavisd doc/README.ldapdelete doc/README.outlook doc/README.sieve doc/README.webgui
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
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/kolab
%attr(0644,root,root) %config(noreplace) %{_datadir}/openldap/schema/horde.schema
%attr(0644,root,root) %config(noreplace) %{_datadir}/openldap/schema/kolab2.schema
%attr(0644,root,root) %config(noreplace) %{_datadir}/openldap/schema/rfc2739.schema
%attr(0755,root,root) %{_sysconfdir}/cron.d/kolabquotawarn
%attr(0744,root,root) %{_bindir}/kolab
%attr(0755,root,root) %{_bindir}/kolabpasswd
%attr(0744,root,root) %{_sbindir}/kolabcheckperm
%attr(0744,root,root) %{_sbindir}/kolabconf
%attr(0744,root,root) %{_sbindir}/kolabd
%attr(0755,root,root) %{_sbindir}/kolab_bootstrap
%attr(0755,%{l_musr},%{l_mgrp}) %dir %{_var}/spool/kolab
%attr(0755,%{l_musr},%{l_mgrp}) %dir %{_var}/run/kolab
%attr(0755,amavis,amavis) %dir %{_var}/amavis
%attr(0755,amavis,amavis) %dir %{_var}/clamav
%attr(0775,amavis,amavis) %{_var}/log/kolab
%attr(0700,ldap,ldap) %dir %{_localstatedir}/lib/ldap-kolab
%attr(0750,%{l_musr},%{l_mgrp}) %dir %{_localstatedir}/lib/kolab
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
%dir %attr(0755,%{l_musr},%{l_mgrp}) %{_datadir}/kolab/scripts
%attr(0755,root,root) %{_datadir}/kolab/scripts/kolab
%attr(0755,root,root) %{_datadir}/kolab/scripts/kolab_bootstrap
%attr(0755,root,root) %{_datadir}/kolab/scripts/kolab_ca.sh
%attr(0755,root,root) %{_datadir}/kolab/scripts/kolabquotawarn
%attr(0755,root,root) %{_datadir}/kolab/scripts/kolab_smtpdpolicy
%attr(0755,root,root) %{_datadir}/kolab/scripts/kolab_sslcert.sh
%attr(0755,root,root) %{_datadir}/kolab/scripts/kolab_upgrade
%attr(0755,root,root) %{_datadir}/kolab/scripts/workaround.sh


