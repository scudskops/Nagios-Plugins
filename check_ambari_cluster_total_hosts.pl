#!/usr/bin/perl -T
# nagios: -epn
#
#  Author: Hari Sekhon
#  Date: 2015-11-26 19:44:32 +0000 (Thu, 26 Nov 2015)
#
#  https://github.com/HariSekhon/Nagios-Plugins
#
#  License: see accompanying LICENSE file
#

$DESCRIPTION = "Nagios Plugin to check the total number of Ambari managed hosts in a Cluster via Ambari REST API

Optional thresholds may be applied to this number.

Tested on Ambari 2.1.0, 2.1.2, 2.2.1, 2.5.1 on Hortonworks HDP 2.2, 2.3, 2.4, 2.6";

$VERSION = "0.1";

use strict;
use warnings;
BEGIN {
    use File::Basename;
    use lib dirname(__FILE__) . "/lib";
}
use HariSekhonUtils;
use HariSekhon::Ambari;

$ua->agent("Hari Sekhon $progname version $main::VERSION");

%options = (
    %hostoptions,
    %useroptions,
    %ambari_options,
    %thresholdoptions,
);

get_options();

$host       = validate_host($host);
$port       = validate_port($port);
$user       = validate_user($user);
$password   = validate_password($password);
$cluster    = validate_ambari_cluster($cluster) if $cluster;

validate_tls();

validate_thresholds(undef, undef, { 'simple' => 'lower', 'integer' => 1, 'positive' => 1 } );

vlog2;
set_timeout();

$status = "OK";

$url_prefix = "$protocol://$host:$port$api";

list_ambari_components();
cluster_required();

$msg = "Ambari cluster '$cluster' total hosts = ";
$json = curl_ambari "$url_prefix/clusters/$cluster?fields=Clusters/total_hosts";
my $total_hosts = get_field_int("Clusters.total_hosts");
$msg .= $total_hosts;
check_thresholds($total_hosts);
$msg .= " | total_hosts=$total_hosts";
msg_perf_thresholds(undef, "lower");

vlog2;
quit $status, $msg;
