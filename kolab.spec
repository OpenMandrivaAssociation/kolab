%define debug_package %{nil}

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


Summary:	Groupware Server
Name:		kolab
License:	GPL
Version:	2.2.4
Release:	5
Group:		System/Servers
URL:		http://www.kolab.org
Source0:	kolabd-%{version}.tar.gz
Source1:	README
Source2:	kolab.init
Patch1:		kolabsrv.diff
Patch2:		rc_config_template.patch
Patch3:		kolabd-slapd_template.diff
Patch4:		kolabd-amavisd_template_log.diff
Patch5:		mandriva.diff
Patch6:		Makefile.diff
Requires(post):	rpm-helper
Requires(preun):rpm-helper
Requires(pre):	rpm-helper
Requires(postun): rpm-helper
Requires(pre):	amavisd-new >= 2.6.4
Requires(pre):	apache-conf >= 2.2.14
Requires(pre):	apache-mod_php
Requires(pre):	apache-mpm-prefork >= 2.2.14
Requires(pre):	clamd >= 0.95.3
Requires(pre):	cyrus-imapd >= 2.3.15
Requires(pre):	openldap-servers >= 2.4.19
Requires(pre):	postfix >= 2.6.5
Requires:	amavisd-new >= 2.6.4
Requires:	apache-conf >= 2.2.14
Requires:	apache-mod_dav >= 2.2.14
Requires:	apache-mod_ldap >= 2.2.14
Requires:	apache-mod_php
Requires:	apache-mod_ssl >= 2.2.14
Requires:	apache-mpm-prefork >= 2.2.14
Requires:	clamd >= 0.95.0
Requires:	cyrus-imapd >= 2.2.15
Requires:	cyrus-imapd-utils >= 2.2.15
Requires:	cyrus-sasl
Requires:	horde-kolab-filter
Requires:	kolab-webadmin >= 2.2.4
Requires:	%{mklibname sasl 2}-plug-login
Requires:	%{mklibname sasl 2}-plug-plain
Requires:	openldap-clients
Requires:	openldap-servers
Requires:	openssl >= 0.9.8k
Requires:	perl-Convert-ASN1
Requires:	perl-Cyrus
Requires:	perl-kolab
Requires:	perl-ldap
Requires:	perl-Net-Netmask
Requires:	perl-Term-ReadKey
Requires:	php-cli >= 5.3.1
Requires:	php-imap >= 5.3.1
Requires:	php-ldap >= 5.3.1
Requires:	php-pear >= 1.9.0
Requires:	php-pear-Net_LMTP
Requires:	php-xml >= 5.3.1
Requires:	postfix >= 2.2.6
Requires:	postfix-ldap >= 2.2.6
Requires:	proftpd >= 1.3.0
Requires:	proftpd-mod_ldap >= 1.3.0
Requires:	spamassassin-spamc >= 3.2.5
Requires:	spamassassin-spamd >= 3.2.5
Provides:	kolab-server
Obsoletes:	kolab-server
Obsoletes: 	kolab-horde-framework
Obsoletes:	kolab-resource-handlers



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
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0

cp %{SOURCE2} kolab.init
cp %{SOURCE1} README


# cleanup
for i in `find . -type d -name CVS`  `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
#find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
#find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# fix perl_vendordir
# perl -pi -e "s|perl_vendorlib|%{perl_vendorlib}|g" dist_conf/mandriva

# force regeneration
# rm -f kolabcheckperm
# rm -f namespace/libexec/start
# rm -f namespace/libexec/stop


%build
#touch README
autoreconf -fi

aclocal; automake --add-missing --copy; autoconf


%configure2_5x \
    --with-dist=mandriva \
    --with-openpkg=no

%make


%install

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
install -d %{buildroot}%{_sysconfdir}/kolab/filter
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
install -d %{buildroot}%{_localstatedir}/www/html/kolab/freebusy

# create symlinks
SCRIPTS="kolab_ca.sh kolab_sslcert.sh"
for script in $SCRIPTS; do
  %__ln_s ../../%{_datadir}/kolab/scripts/$script %{buildroot}%{_sbindir}/${script%%.sh}
done

install -m0744 kolab.init %{buildroot}%{_initrddir}/kolab

# nuke templates for services we do not want to mess with because it is not nessesary
mv %{buildroot}%{_sysconfdir}/kolab/templates/httpd.local.template %{buildroot}%{_sysconfdir}/kolab/templates/httpd.local.template.not4mandriva
mv %{buildroot}%{_sysconfdir}/kolab/templates/php.ini.template %{buildroot}%{_sysconfdir}/kolab/templates/php.ini.template.not4mandriva
mv %{buildroot}%{_sysconfdir}/kolab/templates/clamd.conf.template %{buildroot}%{_sysconfdir}/kolab/templates/clamd.conf.template.not4mandriva
mv %{buildroot}%{_sysconfdir}/kolab/templates/freshclam.conf.template %{buildroot}%{_sysconfdir}/kolab/templates/freshclam.conf.template.not4mandriva


# cleanup
rm -f %{buildroot}%{_initrddir}/rc*
rm -rf %{buildroot}%{_datadir}/doc/kolab

# fix crontab entry for kolabquotawarn
cat > kolabquotawarn.cron << EOF
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

%files
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README.urpmi
%doc doc/README.amavisd doc/README.ldapdelete doc/README.outlook doc/README.sieve doc/README.webgui
#%attr(0755,root,root) %{_initrddir}/kolab
%dir %{_sysconfdir}/kolab
%dir %{_sysconfdir}/kolab/templates
%dir %{_sysconfdir}/kolab/filter
%dir %{_sysconfdir}/kolab/ca
%dir %{_sysconfdir}/kolab/backup
%dir %{_datadir}/kolab
%dir %{_localstatedir}/www/html/kolab/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/amavisd/templates/*/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/kolab/templates/*.template
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/kolab/templates/*.template.not4mandriva
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/kolab/kolab.globals
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/kolab/rootDSE.ldif
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/kolab
%attr(0644,root,root) %config(noreplace) %{_datadir}/openldap/schema/horde.schema
%attr(0644,root,root) %config(noreplace) %{_datadir}/openldap/schema/kolab2.schema
%attr(0644,root,root) %config(noreplace) %{_datadir}/openldap/schema/rfc2739.schema
%attr(0755,root,root) %{_sysconfdir}/cron.d/kolabquotawarn
%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/kolab
%attr(0744,root,root) %{_sbindir}/kolabsrv
%attr(0755,root,root) %{_sbindir}/kolab_ca
%attr(0755,root,root) %{_sbindir}/kolab_sslcert
%attr(0755,%{l_musr},%{l_mgrp}) %dir %{_var}/spool/kolab
%attr(0755,%{l_musr},%{l_mgrp}) %dir %{_var}/run/kolab
%attr(0755,amavis,amavis) %dir %{_var}/amavis
%attr(0755,amavis,amavis) %dir %{_var}/clamav
%attr(0775,amavis,amavis) %{_var}/log/kolab
%attr(0700,ldap,ldap) %dir %{_localstatedir}/lib/ldap-kolab
%attr(0750,%{l_musr},%{l_mgrp}) %dir %{_localstatedir}/lib/kolab
%attr(0750,%{l_musr},%{l_mgrp}) %dir %{_localstatedir}/www/html/kolab
%attr(0755,root,root) %{_libdir}/kolab/adduser
%attr(0755,root,root) %{_libdir}/kolab/deluser
%attr(0755,root,root) %{_libdir}/kolab/listusers
%attr(0755,root,root) %{_libdir}/kolab/newconfig
%attr(0755,root,root) %{_libdir}/kolab/services
%attr(0755,root,root) %{_libdir}/kolab/showlog
%attr(0755,root,root) %{_libdir}/kolab/showuser
%attr(0755,root,root) %{_libdir}/kolab/start
%attr(0755,root,root) %{_libdir}/kolab/stop
%dir %attr(0755,%{l_musr},%{l_mgrp}) %{_datadir}/kolab/scripts
%attr(0755,root,root) %{_datadir}/kolab/scripts/kolab_ca.sh
%attr(0755,root,root) %{_datadir}/kolab/scripts/kolab_sslcert.sh







%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.4-4mdv2011.0
+ Revision: 666033
- mass rebuild

* Mon Dec 20 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.2.4-3mdv2011.0
+ Revision: 623226
- Increased relase to 3
- Changed Clamav socket to same as amavis uses
-clamav_socket=${localstatedir}/clamav/clamd.sock
  +clamav_socket=${localstatedir}/lib/clamav/clamd.socket

* Thu Oct 21 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2.2.4-2mdv2011.0
+ Revision: 587173
- Do not add shebang in cron.d file
  CCBUG: 57855

* Wed Jul 14 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.2.4-1mdv2011.0
+ Revision: 553002
- Updated to upstream version 2.2.4

* Thu Apr 29 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.2.3-5mdv2010.1
+ Revision: 540736
- Updated the upgrade information and increased release version

* Tue Apr 20 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.2.3-4mdv2010.1
+ Revision: 536904
- changed location of sieve directory from /var/lib/sieve to /var/lib/imap/sieve
  Increase release verison to 4
- changed location of sieve directory from /var/lib/sieve to /var/lib/imap/sieve
  Increase release verison to 4

* Fri Apr 16 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.2.3-3mdv2010.1
+ Revision: 535315
- increased rel version to 3
- found another clamd >= 0.96.0 and changed it ti >=0.96

* Thu Apr 15 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.2.3-2mdv2010.1
+ Revision: 535003
- change require clamd version >=0.96.0 to 0.96

* Mon Apr 12 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.2.3-1mdv2010.1
+ Revision: 533613
- Updated to version 2.2.3
  Kolab-resource-handlers is not needed anymore.
  It is now provided by horde packages
- Updated to version 2.2.3
  Kolab-resource-handlers is not needed anymore.
  It is now provided by horde packages
- Updated to version 2.2.3
  Kolab-resource-handlers is not needed anymore.
  It is now provided by horde packages

* Tue Oct 06 2009 Thomas Spuhler <tspuhler@mandriva.org> 2.1.0-12mdv2010.0
+ Revision: 454441
- added mandriva to source
- bumped the release to 12
- cleaned up a commented line

* Mon Sep 21 2009 Thomas Spuhler <tspuhler@mandriva.org> 2.1.0-11mdv2010.0
+ Revision: 446153
-modified rel to 11
-modified mandriva.diff to correct the wrong paths for the sieve script, /var/lib/sieve to /var/lib/imap/sieve
-removed %%define _source_payload w9.bzdio
-removed %%define _default_patch_fuzz 0
-removed %%define _enable_debug_packages %%{nil}
-removed %%define debug_package          %%{nil}

* Sun Aug 23 2009 Thomas Spuhler <tspuhler@mandriva.org> 2.1.0-10mdv2010.0
+ Revision: 420182
- added the Makefile patch to delete double entry of namespace/libexec/newconfig to make it build on cooker
- bumped the version to 10 for cooker
- downgraded release to original and added subrel 1
- Fixed a whole lot of path and replaced slurpd with sincrepl. Kolabd stays alive
- lots of paths fixed and slurp replaced with syncrepl
- replaced slurpd with syncrepl because openldap doesn't suppot it anymore, corrected lotwrong paths
- replaced slurpd with syncrepl because openldap doesn't suppot it anymore, corrected lotwrong paths

* Fri Apr 10 2009 Funda Wang <fwang@mandriva.org> 2.1.0-9mdv2009.1
+ Revision: 365504
- rediff sysv patch

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 2.1.0-9mdv2009.0
+ Revision: 221868
- rebuild

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 2.1.0-8mdv2008.1
+ Revision: 150428
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Sep 26 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-7mdv2008.0
+ Revision: 93051
- drop P12 in an attempt to fix #33383 (Mail sending from outside the local network not possible)
- added some svn props

* Sat Sep 15 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-6mdv2008.0
+ Revision: 86791
- adjust for the latest changes in the apache-mod_ssl package,
  /etc/httpd/modules.d/41_mod_ssl.default-vhost.conf has ben moved to
  /etc/httpd/conf/vhosts.d/01_default_ssl_vhost.conf

* Mon Sep 10 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-5mdv2008.0
+ Revision: 84126
- fix #33325 (The template for imap.conf ist wrong for sieveshell)
- really fix build
- fix build
- fix deps

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-3mdv2008.0
+ Revision: 33610
- sync changes from the 1.9.x spec file
- sync patches from the 1.9.x package
- yet again, a lot of fixes...

* Thu May 31 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-2mdv2008.0
+ Revision: 33123
- fixed the cyrus-imapd template so that it won't spam the logfile with db errors
- updated the proftpd template for our proftpd package, added deps on proftpd-mod_ldap
- added debug mode in the kolab_bootstrap.sh script

* Sat May 26 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-1mdv2008.0
+ Revision: 31490
- 2.1.0
- fixed a lot of stuff, spec file hacks, patches etc.


* Wed Oct 11 2006 Oden Eriksson <oeriksson@mandriva.com>
+ 2006-10-10 09:54:51 (63288)
- rebuild

* Tue May 30 2006 Andreas Hasenack <andreas@mandriva.com>
+ 2006-05-29 08:36:37 (31646)
- renamed mdv to packages because mdv is too generic and it's hosting only packages anyway

* Sun Aug 28 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-27 09:36:39 (757)
- preparing release (1.9.5-0.20050801.4mdk)

* Sun Aug 28 2005 oeriksson
+ 2005-08-27 05:26:49 (756)
- fixed the syntax in the slapd.conf.template file so it passes slaptest
  without any errors.

* Sat Aug 27 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-26 16:10:34 (755)
- preparing release (1.9.5-0.20050801.3mdk)

* Sat Aug 27 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-26 15:45:03 (754)
- changed slapd_template patch to work with openldap-2.3.x
- did in that patch part of that was being done in the spec file
  with perl -pi
- merged the ldapmodules patch with slapd_template.diff

* Thu Aug 25 2005 oeriksson
+ 2005-08-24 09:39:19 (733)
- fix so that a possible kolab1 leftover configuration won't fool the initscript to start

* Sat Aug 20 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-19 14:42:43 (707)
- using gpasswd -a to add users to a group so that the
  previous group membership isn't overwritten
- using standard macro do add kolab user and give it an
  uid < 500

* Thu Aug 18 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-17 09:20:02 (681)
- postfix doesn't expand $mydestination in ldap maps

* Thu Aug 18 2005 oeriksson
+ 2005-08-17 05:19:57 (677)
- don't send exit code "1" from the kolab_bootstrap.sh script as
  it fools rpm thinking there was an error.

* Thu Aug 18 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-17 03:36:55 (676)
- added "LDAP_Persistent_G off" to apache's template file until
  we have a better fix for the mod_mm_auth_ldap problem

* Tue Aug 16 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-15 09:24:46 (648)
- fixed freebusy.conf file permissions (it has a password and thus
  can't be mode 0644)

* Tue Aug 16 2005 oeriksson
+ 2005-08-15 08:39:13 (647)
- added back some lib64 fixes
- make it provide and obsolete kolab-server (temporary fix)

* Tue Aug 16 2005 oeriksson
+ 2005-08-15 07:06:13 (646)
- make it conflict with kolab-server as there is no upgrade path

* Tue Aug 16 2005 oeriksson
+ 2005-08-15 07:00:14 (643)
- added one more kolab-server/kolab renaming in perl-kolab.tar.bz2

* Tue Aug 16 2005 oeriksson
+ 2005-08-15 06:51:57 (642)
- added one patch accidently deleted

* Tue Aug 16 2005 oeriksson
+ 2005-08-15 06:41:13 (641)
- fix references to kolab-server (kolab-server/kolab)

* Tue Aug 16 2005 oeriksson
+ 2005-08-15 06:12:20 (639)
- renamed to just "kolab" because there is no upgrade patch from kolab1 to kolab2

* Tue Aug 16 2005 oeriksson
+ 2005-08-15 05:26:40 (638)
- and requires line can only be so long it seems...

* Tue Aug 16 2005 oeriksson
+ 2005-08-15 03:47:35 (637)
- fix the php include path

* Tue Aug 16 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-15 03:24:31 (636)
- added two more rewrite rules to the apache config file to
  cope with http://bugs.kde.org/show_bug.cgi?id=110649
  (kontact is using /freebusy always instead of what was
  configured elsewhere which, in our case, would be
  /kolab/freebusy)

* Sun Aug 14 2005 oeriksson
+ 2005-08-13 09:58:11 (630)
- reworked the bootstrap script a little more

* Sun Aug 14 2005 oeriksson
+ 2005-08-13 08:30:56 (629)
- reworked the kolab_bootstrap bootscript after looking some at
  apr-config, it's now possible to "reset" the system after
  uninstalling kolab-server rendering a somewhat non polluted
  system...
- fixed one more init script invocation

* Sun Aug 14 2005 oeriksson
+ 2005-08-13 04:38:06 (627)
- fix smarter perl search and replace (works faster)
- drop P22 as andreas allready had fixed that
- fix deps

* Sat Aug 13 2005 oeriksson
+ 2005-08-12 07:08:17 (619)
- added a small cosmetic patch (P22)
- reworked the init script

* Sat Aug 13 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-12 02:50:05 (611)
- fixed admin url in the kolab_bootstrap script

* Sat Aug 13 2005 oeriksson
+ 2005-08-12 01:45:37 (609)
- fix deps
- also start/stop/reload spamd
- remove hardcoded path to /var/www/html/kolab

* Fri Aug 12 2005 oeriksson
+ 2005-08-11 09:35:15 (606)
- don't stop kolab-server in the kolab_bootstrap script
- make the stop services commant quiet

* Fri Aug 12 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-11 09:26:51 (605)
- fixed freebusy trigger url

* Fri Aug 12 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-11 09:17:40 (603)
- fixed rewrite rules in apache_template.diff

* Fri Aug 12 2005 oeriksson
+ 2005-08-11 08:37:59 (601)
- add the nobody user to the kolab group, seems needed to let kolab stop proftpd
- only start/stop/reload proftpd if it's needed

* Fri Aug 12 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-11 03:52:17 (599)
- adjust /var/log/kolab permissions so that it can be written to
  by other daemons/users in the kolab group

* Thu Aug 11 2005 oeriksson
+ 2005-08-10 22:54:56 (588)
- fix more loose permissions on the horde config files
- fix the /var/resmgr/*.log path
- own the %%{_sysconfdir}/kolab/resmgr directory since we make
  the config files from this package

* Wed Aug 10 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-09 06:11:31 (566)
- removed unused patches
- fixed permissions of the freebusy.conf.template file

* Tue Aug 09 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-08 07:54:46 (558)
- defined kolab_webroot macro

* Tue Aug 09 2005 oeriksson
+ 2005-08-08 03:42:25 (555)
- fix the replacements in the initscript

* Tue Aug 09 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-08 03:03:54 (553)
- fixed permissions on amavisd.conf, master.cf, resmgr.conf and virtual

* Tue Aug 09 2005 oeriksson
+ 2005-08-08 02:26:14 (552)
- add numeric uid/gid of 60001
- added P21 to fix schema locations
- added virtual kolab provides
- set permissions
- added cron entry and logrotate
- relocate the name space utils to %%{_datadir}/kolab/
- added some tools
- added better logic to add and remove the kolab user

* Sun Aug 07 2005 oeriksson
+ 2005-08-06 03:21:39 (544)
- commit test using a modem...

* Sat Aug 06 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-05 08:32:25 (542)
- added amavisd to the list of services to be stopped in /usr/sbin/kolab_bootstrap

* Sat Aug 06 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-05 08:29:32 (541)
- added amavisd to the kolab init script

* Sat Aug 06 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-05 06:07:53 (537)
- fixed patch7

* Sat Aug 06 2005 oeriksson
+ 2005-08-05 05:14:48 (536)
- fixed the amavisd template patch to use the amavis uid/gid

* Fri Aug 05 2005 oeriksson
+ 2005-08-04 05:54:52 (531)
- drop the lib64 fixes
- fix the init script patch
- move the usermod stuff back to the bootstrap script
- added the %%{_sysconfdir}/kolab/backup dir
- fix deps

* Fri Aug 05 2005 oeriksson
+ 2005-08-04 02:20:30 (530)
- added some %%mklibname lines to construct the deps
- fixed attributes for the imap config files
- corrected the path to rc.conf

* Thu Aug 04 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-03 10:13:00 (523)
- updated postfix main template patch to add the sasl dir
  configuration directive. Without it, contents of /etc/postfix/sasl
  are ignored.

* Thu Aug 04 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-03 09:38:31 (522)
- added requirements for the PLAIN and LOGIN SASL mechanisms
  (I included LOGIN because I know outlook uses it)

* Thu Aug 04 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-03 09:33:45 (521)
- added requirement for postfix-ldap (kolab-server needs the
  ldap map support)

* Wed Aug 03 2005 oeriksson
+ 2005-08-02 05:55:22 (508)
- fixed a stupid bug

* Wed Aug 03 2005 oeriksson
+ 2005-08-02 01:17:27 (504)
- the httpd.local.template file is not needed, nuke it

* Tue Aug 02 2005 oeriksson
+ 2005-08-01 19:26:07 (495)
- commit the files too

* Tue Aug 02 2005 oeriksson
+ 2005-08-01 19:25:03 (494)
- added things from the old kolab1 package (S2,S3), use only the kolab user
- fixed uid/gid plus permissions on the templates

* Tue Aug 02 2005 oeriksson
+ 2005-08-01 14:29:07 (491)
- fixed a silly typo (amavis-new/amavisd-new)

* Tue Aug 02 2005 oeriksson
+ 2005-08-01 13:46:30 (490)
- added the perl-kolab source to construct the /etc/kolab/config.h file
- broke out P1 (kolab-server-2.0-mdk.diff) into P15 -> P20
- rediffed P5
- fixed deps

* Tue Aug 02 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-01 08:03:19 (485)
- also chown to ldap the new slapd.access conf file

* Tue Aug 02 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-01 07:02:32 (484)
- started following CVS as of today
- redid mdk.diff patch for this version

* Fri Jul 29 2005 oeriksson
+ 2005-07-28 02:47:32 (456)
- broke out kolab-resource-handlers
- added one lib64 fix

* Wed Jul 27 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-07-26 09:23:33 (444)
- adjusted postfixtemplate patch so that the pipe transport
  in master.cf uses "null_sender=" instead of "flags=n" which
  is the way the kolab patch was integrated upstream in postfix
  2.3 and in my backported postfix kolab patch

* Wed Jul 27 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-07-26 08:19:56 (443)
- added php-pear-Net_LMTP to Requires

* Tue Jul 26 2005 oeriksson
+ 2005-07-25 05:59:38 (436)
- reverting my commit

* Tue Jul 26 2005 oeriksson
+ 2005-07-25 05:58:06 (435)
- testing commit

* Tue Jul 26 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-07-25 03:28:53 (433)
- commit test via svn+ssh

* Sat Jul 23 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-07-22 10:33:40 (426)
- fixed apache's mime.types path in the apachetemplate patch
- fixed php's extension_dir in phpinitemplate patch

* Sat Jul 23 2005 Helio Chissini de Castro <helio@mandriva.com>
+ 2005-07-22 08:06:02 (425)
- Commit test.

* Sat Jul 23 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-07-22 07:04:48 (424)
- added requirement for apache-mod_mm_auth_ldap (instead of apache-mod_ldap)
- prereq -> requires(foo)

* Sat Jul 23 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-07-22 06:20:34 (423)
- merged with Oden

* Fri Jul 22 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-07-21 12:06:03 (402)
- fixed postix default_privs user
- fixed apache ServerRoot
- loaded missing modules into apache and adjusted requires
- fixed apache user/group

* Fri Jul 22 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-07-21 09:57:05 (396)
- added more template patches
- added missing httpd_sessions directory with write permission
  for the apache group (php session files are stored there)

* Fri Jul 22 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-07-21 08:30:51 (393)
- fixed apachetemplate patch so that /usr/share/pear is also
  included in the php include_dir setting

* Fri Jul 22 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-07-21 08:25:16 (392)
- merged in Oden's changes:
  - added initrddir patch
  - fixed slapcat path
  - fixed tar path
  - added kolab/ca dir
  - not installing /etc/kolab/kolab anymore

* Tue Jul 19 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-07-18 11:10:40 (378)
- bunziped patches, this .src.rpm has a bzip2 payload already
- removed cyrus patch, already accomplished by another patch
- removed main.cf hunk from postfix patch, already done by another
  patch

* Tue Jul 19 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-07-18 10:58:48 (377)
- added lots of patches for the templates. There are more needed.

* Wed Jul 13 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-07-12 10:37:10 (365)
- renamed repository entry from kolab2 to kolab-server, which is
  the actual package name

* Wed Jul 13 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-07-12 08:24:22 (362)
- by Oden Eriksson <oeriksson@mandrakesoft.com>:
  - 2.0, first blood...
  - andreas:
    - added users kolab, kolab-n and kolab-r in %%pre
    - substituting @kolab_version@
    - fix slappasswd path
    - fix postfix sasl configuration file path
    - fix templates permissions
    - fix openldap paths and ownership
    - using rc.conf.template to install rc.conf
    - changed /etc/rc.conf to /etc/kolab/rc.conf
    - removed %%config tag from /etc/kolab/kolab_bootstrap
    - added /var/lib/kolab, changed kolabdcachetool accordingly
    - added more requirements
    - switched payload format to bzip2 and removed bzip2 from
      patches

