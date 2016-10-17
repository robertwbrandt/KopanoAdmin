<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" indent="yes" omit-xml-declaration="yes" />

<xsl:template match="/zarafaadmin/error">
  <table align="center">
    <caption style="color:red">An Error occurred, Please contact your System Administrator</caption>
    <tr>
      <td align="right" style="color:red">Error Number:</td>
      <td align="left"><xsl:value-of select="@code"/></td>
    </tr>
    <tr>
      <td align="right" style="color:red">Error Message:</td>
      <td align="left"><xsl:value-of select="@msg"/></td>
    </tr>
    <tr>
      <td align="right" style="color:red">Original Command:</td>
      <td align="left"><xsl:value-of select="@cmd"/></td>
    </tr>
  </table>
</xsl:template>

<xsl:template match="/zarafaadmin/system">
  <pre>
    <table id="zarafa-system">
      <tr class="hover"><td>Time when the server was started</td><td><xsl:value-of select="server_start_date/@date"/></td></tr>
      <tr class="hover"><td>Time when the cache was cleared</td><td><xsl:value-of select="cache_purge_date/@date"/></td></tr>
      <tr class="hover"><td>Time when the configuration file was reloaded / logrotation (SIGHUP)</td><td><xsl:value-of select="config_reload_date/@date"/></td></tr>
      <tr class="hover"><td><b>Number of allowed users</b></td><td><b><xsl:value-of select="@usercnt_licensed"/></b></td></tr>
      <tr class="hover"><td><b>Number of active users</b></td><td><b><xsl:value-of select="@usercnt_active"/></b></td></tr>
      <tr class="hover"><td><b>Number of total non-active objects</b></td><td><b><xsl:value-of select="@usercnt_nonactive"/></b></td></tr>
      <tr class="hover"><td>Number of non-active users</td><td><xsl:value-of select="@usercnt_na_user"/></td></tr>
      <tr class="hover"><td>Number of rooms</td><td><xsl:value-of select="@usercnt_room"/></td></tr>
      <tr class="hover"><td>Number of equipment</td><td><xsl:value-of select="@usercnt_equipment"/></td></tr>
      <tr class="hover"><td>Number of contacts</td><td><xsl:value-of select="@usercnt_contact"/></td></tr>      
      <tr class="hover"><td>Number of handled incoming connections</td><td><xsl:value-of select="@connections"/></td></tr>
      <tr class="hover"><td><b>Number of sessions</b></td><td><b><xsl:value-of select="@sessions"/></b></td></tr>
      <tr class="hover"><td>Memory usage of sessions</td><td><xsl:value-of select="@sessions_size"/></td></tr>
      <tr class="hover"><td>Number of session groups</td><td><xsl:value-of select="@sessiongroups"/></td></tr>
      <tr class="hover"><td>Memory usage of session groups</td><td><xsl:value-of select="@sessiongroups_size"/></td></tr>
      <tr class="hover"><td>Persistent connections</td><td><xsl:value-of select="@persist_conn"/></td></tr>
      <tr class="hover"><td>Memory usage of persistent connections</td><td><xsl:value-of select="@persist_conn_size"/></td></tr>
      <tr class="hover"><td>Persistent sessions</td><td><xsl:value-of select="@persist_sess"/></td></tr>
      <tr class="hover"><td>Memory usage of persistent sessions</td><td><xsl:value-of select="@persist_sess_size"/></td></tr>
      <tr class="hover"><td>Tables subscribed</td><td><xsl:value-of select="@tables_subscr"/></td></tr>
      <tr class="hover"><td>Memory usage of subscribed tables</td><td><xsl:value-of select="@tables_subscr_size"/></td></tr>
      <tr class="hover"><td>Objects subscribed</td><td><xsl:value-of select="@object_subscr"/></td></tr>
      <tr class="hover"><td>Memory usage of subscribed objects</td><td><xsl:value-of select="@object_subscr_size"/></td></tr>
      <tr class="hover"><td>Number of stores in use by search folders</td><td><xsl:value-of select="@searchfld_stores"/></td></tr>
      <tr class="hover"><td>Number of folders in use by search folders</td><td><xsl:value-of select="@searchfld_folders"/></td></tr>
      <tr class="hover"><td>Number of events waiting for searchfolder updates</td><td><xsl:value-of select="@searchfld_events"/></td></tr>
      <tr class="hover"><td>Memory usage of search folders</td><td><xsl:value-of select="@searchfld_size"/></td></tr>
      <tr class="hover"><td>Current queue length</td><td><xsl:value-of select="@queuelen"/></td></tr>
      <tr class="hover"><td>Age of the front queue item</td><td><xsl:value-of select="@queueage"/></td></tr>
      <tr class="hover"><td><b>Number of threads running to process items</b></td><td><b><xsl:value-of select="@threads"/></b></td></tr>
      <tr class="hover"><td>Number of idle threads</td><td><xsl:value-of select="@threads_idle"/></td></tr>
      <tr class="hover"><td>Current allocated memory by TCMalloc</td><td><xsl:value-of select="@tc_allocated"/></td></tr>
      <tr class="hover"><td>Bytes of system memory reserved by TCMalloc</td><td><xsl:value-of select="@tc_reserved"/></td></tr>
      <tr class="hover"><td>Number of bytes in free mapped pages in page heap</td><td><xsl:value-of select="@tc_page_map_free"/></td></tr>
      <tr class="hover"><td>Number of bytes in free unmapped pages in page heap (released to OS)</td><td><xsl:value-of select="@tc_page_unmap_free"/></td></tr>
      <tr class="hover"><td>A limit to how much memory TCMalloc dedicates for small objects</td><td><xsl:value-of select="@tc_threadcache_max"/></td></tr>
      <tr class="hover"><td>Current allocated memory in bytes for thread cache</td><td><xsl:value-of select="@tc_threadcache_cur"/></td></tr>      
      <tr class="hover"><td>Highest socket number used</td><td><xsl:value-of select="@max_socket"/></td></tr>
      <tr class="hover"><td>Number of redirected requests</td><td><xsl:value-of select="@redirections"/></td></tr>
      <tr class="hover"><td>Number of soap requests handled by server</td><td><xsl:value-of select="@soap_request"/></td></tr>
      <tr class="hover"><td>Response time of soap requests handled in milliseconds (includes time in queue)</td><td><xsl:value-of select="@response_time"/></td></tr>
      <tr class="hover"><td>Time taken to process soap requests in milliseconds (wallclock time)</td><td><xsl:value-of select="@processing_time"/></td></tr>
      <tr class="hover"><td>Total number of searchfolders</td><td><xsl:value-of select="@searchfld_loaded"/></td></tr>
      <tr class="hover"><td>Current number of running searchfolder threads</td><td><xsl:value-of select="@searchfld_threads"/></td></tr>
      <tr class="hover"><td>The number of times a search folder update was restarted</td><td><xsl:value-of select="@searchupd_retry"/></td></tr>
      <tr class="hover"><td>The number of failed search folder updates after retrying</td><td><xsl:value-of select="@searchupd_fail"/></td></tr>
      <tr class="hover"><td>Number of connections made to SQL server</td><td><xsl:value-of select="@sql_connect"/></td></tr>
      <tr class="hover"><td>Number of SQL Select commands executed</td><td><xsl:value-of select="@sql_select"/></td></tr>
      <tr class="hover"><td>Number of SQL Insert commands executed</td><td><xsl:value-of select="@sql_insert"/></td></tr>
      <tr class="hover"><td>Number of SQL Update commands executed</td><td><xsl:value-of select="@sql_update"/></td></tr>
      <tr class="hover"><td>Number of SQL Delete commands executed</td><td><xsl:value-of select="@sql_delete"/></td></tr>
      <tr class="hover"><td>Number of failed connections made to SQL server</td><td><xsl:value-of select="@sql_connect_fail"/></td></tr>
      <tr class="hover"><td>Number of failed SQL Select commands</td><td><xsl:value-of select="@sql_select_fail"/></td></tr>
      <tr class="hover"><td>Number of failed SQL Insert commands</td><td><xsl:value-of select="@sql_insert_fail"/></td></tr>
      <tr class="hover"><td>Number of failed SQL Update commands</td><td><xsl:value-of select="@sql_update_fail"/></td></tr>
      <tr class="hover"><td>Number of failed SQL Delete commands</td><td><xsl:value-of select="@sql_delete_fail"/></td></tr>
      <tr class="hover"><td>Timestamp of last failed SQL command</td><td><xsl:value-of select="sql_last_fail_time/@date"/></td></tr>
      <tr class="hover"><td>MAPI Write Operations</td><td><xsl:value-of select="@mwops"/></td></tr>
      <tr class="hover"><td>MAPI Read Operations</td><td><xsl:value-of select="@mrops"/></td></tr>
      <tr class="hover"><td>Number rows retrieved via deferred write table</td><td><xsl:value-of select="@deferred_fetches"/></td></tr>
      <tr class="hover"><td>Number of merges applied to the deferred write table</td><td><xsl:value-of select="@deferred_merges"/></td></tr>
      <tr class="hover"><td>Number records merged in the deferred write table</td><td><xsl:value-of select="@deferred_records"/></td></tr>
      <tr class="hover"><td>Number of table rows read in row order</td><td><xsl:value-of select="@row_reads"/></td></tr>
      <tr class="hover"><td>Number of time a counter resync was required</td><td><xsl:value-of select="@counter_resyncs"/></td></tr>
      <tr class="hover"><td>Number of logins through password authentication</td><td><xsl:value-of select="@login_password"/></td></tr>
      <tr class="hover"><td>Number of logins through SSL certificate authentication</td><td><xsl:value-of select="@login_ssl"/></td></tr>
      <tr class="hover"><td>Number of logins through Single Sign-on</td><td><xsl:value-of select="@login_sso"/></td></tr>
      <tr class="hover"><td>Number of logins through Unix socket</td><td><xsl:value-of select="@login_unix"/></td></tr>
      <tr class="hover"><td>Number of failed logins</td><td><xsl:value-of select="@login_failed"/></td></tr>
      <tr class="hover"><td>Number of created sessions</td><td><xsl:value-of select="@sessions_created"/></td></tr>
      <tr class="hover"><td>Number of deleted sessions</td><td><xsl:value-of select="@sessions_deleted"/></td></tr>
      <tr class="hover"><td>Number of timed-out sessions</td><td><xsl:value-of select="@sessions_timeout"/></td></tr>
      <tr class="hover"><td>Number of created internal sessions</td><td><xsl:value-of select="@sess_int_created"/></td></tr>
      <tr class="hover"><td>Number of deleted internal sessions</td><td><xsl:value-of select="@sess_int_deleted"/></td></tr>
      <tr class="hover"><td>Number of created sessiongroups</td><td><xsl:value-of select="@sess_grp_created"/></td></tr>
      <tr class="hover"><td>Number of deleted sessiongroups</td><td><xsl:value-of select="@sess_grp_deleted"/></td></tr>
      <tr class="hover"><td>Number of connections made to LDAP server</td><td><xsl:value-of select="@ldap_connect"/></td></tr>
      <tr class="hover"><td>Number of re-connections made to LDAP server</td><td><xsl:value-of select="@ldap_reconnect"/></td></tr>
      <tr class="hover"><td>Number of failed connections made to LDAP server</td><td><xsl:value-of select="@ldap_connect_fail"/></td></tr>
      <tr class="hover"><td>Total duration of connections made to LDAP server</td><td><xsl:value-of select="@ldap_connect_time"/></td></tr>
      <tr class="hover"><td>Longest connection time made to LDAP server</td><td><xsl:value-of select="@ldap_max_connect"/></td></tr>
      <tr class="hover"><td>Number of LDAP authentications</td><td><xsl:value-of select="@ldap_auth"/></td></tr>
      <tr class="hover"><td>Number of failed authentications</td><td><xsl:value-of select="@ldap_auth_fail"/></td></tr>
      <tr class="hover"><td>Total authentication time</td><td><xsl:value-of select="@ldap_auth_time"/></td></tr>
      <tr class="hover"><td>Longest duration of authentication made to LDAP server</td><td><xsl:value-of select="@ldap_max_auth"/></td></tr>
      <tr class="hover"><td>Average duration of authentication made to LDAP server</td><td><xsl:value-of select="@ldap_avg_auth"/></td></tr>
      <tr class="hover"><td>Number of searches made to LDAP server</td><td><xsl:value-of select="@ldap_search"/></td></tr>
      <tr class="hover"><td>Number of failed searches made to LDAP server</td><td><xsl:value-of select="@ldap_search_fail"/></td></tr>
      <tr class="hover"><td>Total duration of LDAP searches</td><td><xsl:value-of select="@ldap_search_time"/></td></tr>
      <tr class="hover"><td>Longest duration of LDAP search</td><td><xsl:value-of select="@ldap_max_search"/></td></tr>
      <tr class="hover"><td>Number of failed indexer queries</td><td><xsl:value-of select="@index_search_errors"/></td></tr>
      <tr class="hover"><td>Maximum duration of an indexed search query</td><td><xsl:value-of select="@index_search_max"/></td></tr>
      <tr class="hover"><td>Average duration of an indexed search query</td><td><xsl:value-of select="@index_search_avg"/></td></tr>
      <tr class="hover"><td>Number of indexed searches performed</td><td><xsl:value-of select="@search_indexed"/></td></tr>
      <tr class="hover"><td>Number of database searches performed</td><td><xsl:value-of select="@search_database"/></td></tr>
      <tr class="hover"><td>Cache obj items</td><td><xsl:value-of select="@cache_obj_items"/></td></tr>
      <tr class="hover"><td>Cache obj size</td><td><xsl:value-of select="@cache_obj_size"/></td></tr>
      <tr class="hover"><td>Cache obj maximum size</td><td><xsl:value-of select="@cache_obj_maxsz"/></td></tr>
      <tr class="hover"><td>Cache obj requests</td><td><xsl:value-of select="@cache_obj_req"/></td></tr>
      <tr class="hover"><td>Cache obj hits</td><td><xsl:value-of select="@cache_obj_hit"/></td></tr>
      <tr class="hover"><td>Cache store items</td><td><xsl:value-of select="@cache_store_items"/></td></tr>
      <tr class="hover"><td>Cache store size</td><td><xsl:value-of select="@cache_store_size"/></td></tr>
      <tr class="hover"><td>Cache store maximum size</td><td><xsl:value-of select="@cache_store_maxsz"/></td></tr>
      <tr class="hover"><td>Cache store requests</td><td><xsl:value-of select="@cache_store_req"/></td></tr>
      <tr class="hover"><td>Cache store hits</td><td><xsl:value-of select="@cache_store_hit"/></td></tr>
      <tr class="hover"><td>Cache acl items</td><td><xsl:value-of select="@cache_acl_items"/></td></tr>
      <tr class="hover"><td>Cache acl size</td><td><xsl:value-of select="@cache_acl_size"/></td></tr>
      <tr class="hover"><td>Cache acl maximum size</td><td><xsl:value-of select="@cache_acl_maxsz"/></td></tr>
      <tr class="hover"><td>Cache acl requests</td><td><xsl:value-of select="@cache_acl_req"/></td></tr>
      <tr class="hover"><td>Cache acl hits</td><td><xsl:value-of select="@cache_acl_hit"/></td></tr>
      <tr class="hover"><td>Cache quota items</td><td><xsl:value-of select="@cache_quota_items"/></td></tr>
      <tr class="hover"><td>Cache quota size</td><td><xsl:value-of select="@cache_quota_size"/></td></tr>
      <tr class="hover"><td>Cache quota maximum size</td><td><xsl:value-of select="@cache_quota_maxsz"/></td></tr>
      <tr class="hover"><td>Cache quota requests</td><td><xsl:value-of select="@cache_quota_req"/></td></tr>
      <tr class="hover"><td>Cache quota hits</td><td><xsl:value-of select="@cache_quota_hit"/></td></tr>
      <tr class="hover"><td>Cache uquota items</td><td><xsl:value-of select="@cache_uquota_items"/></td></tr>
      <tr class="hover"><td>Cache uquota size</td><td><xsl:value-of select="@cache_uquota_size"/></td></tr>
      <tr class="hover"><td>Cache uquota maximum size</td><td><xsl:value-of select="@cache_uquota_maxsz"/></td></tr>
      <tr class="hover"><td>Cache uquota requests</td><td><xsl:value-of select="@cache_uquota_req"/></td></tr>
      <tr class="hover"><td>Cache uquota hits</td><td><xsl:value-of select="@cache_uquota_hit"/></td></tr>
      <tr class="hover"><td>Cache extern items</td><td><xsl:value-of select="@cache_extern_items"/></td></tr>
      <tr class="hover"><td>Cache extern size</td><td><xsl:value-of select="@cache_extern_size"/></td></tr>
      <tr class="hover"><td>Cache extern maximum size</td><td><xsl:value-of select="@cache_extern_maxsz"/></td></tr>
      <tr class="hover"><td>Cache extern requests</td><td><xsl:value-of select="@cache_extern_req"/></td></tr>
      <tr class="hover"><td>Cache extern hits</td><td><xsl:value-of select="@cache_extern_hit"/></td></tr>
      <tr class="hover"><td>Cache userid items</td><td><xsl:value-of select="@cache_userid_items"/></td></tr>
      <tr class="hover"><td>Cache userid size</td><td><xsl:value-of select="@cache_userid_size"/></td></tr>
      <tr class="hover"><td>Cache userid maximum size</td><td><xsl:value-of select="@cache_userid_maxsz"/></td></tr>
      <tr class="hover"><td>Cache userid requests</td><td><xsl:value-of select="@cache_userid_req"/></td></tr>
      <tr class="hover"><td>Cache userid hits</td><td><xsl:value-of select="@cache_userid_hit"/></td></tr>
      <tr class="hover"><td>Cache abinfo items</td><td><xsl:value-of select="@cache_abinfo_items"/></td></tr>
      <tr class="hover"><td>Cache abinfo size</td><td><xsl:value-of select="@cache_abinfo_size"/></td></tr>
      <tr class="hover"><td>Cache abinfo maximum size</td><td><xsl:value-of select="@cache_abinfo_maxsz"/></td></tr>
      <tr class="hover"><td>Cache abinfo requests</td><td><xsl:value-of select="@cache_abinfo_req"/></td></tr>
      <tr class="hover"><td>Cache abinfo hits</td><td><xsl:value-of select="@cache_abinfo_hit"/></td></tr>
      <tr class="hover"><td>Cache server items</td><td><xsl:value-of select="@cache_server_items"/></td></tr>
      <tr class="hover"><td>Cache server size</td><td><xsl:value-of select="@cache_server_size"/></td></tr>
      <tr class="hover"><td>Cache server maximum size</td><td><xsl:value-of select="@cache_server_maxsz"/></td></tr>
      <tr class="hover"><td>Cache server requests</td><td><xsl:value-of select="@cache_server_req"/></td></tr>
      <tr class="hover"><td>Cache server hits</td><td><xsl:value-of select="@cache_server_hit"/></td></tr>
      <tr class="hover"><td>Cache cell items</td><td><xsl:value-of select="@cache_cell_items"/></td></tr>
      <tr class="hover"><td>Cache cell size</td><td><xsl:value-of select="@cache_cell_size"/></td></tr>
      <tr class="hover"><td>Cache cell maximum size</td><td><xsl:value-of select="@cache_cell_maxsz"/></td></tr>
      <tr class="hover"><td>Cache cell requests</td><td><xsl:value-of select="@cache_cell_req"/></td></tr>
      <tr class="hover"><td>Cache cell hits</td><td><xsl:value-of select="@cache_cell_hit"/></td></tr>
      <tr class="hover"><td>Cache index1 items</td><td><xsl:value-of select="@cache_index1_items"/></td></tr>
      <tr class="hover"><td>Cache index1 size</td><td><xsl:value-of select="@cache_index1_size"/></td></tr>
      <tr class="hover"><td>Cache index1 maximum size</td><td><xsl:value-of select="@cache_index1_maxsz"/></td></tr>
      <tr class="hover"><td>Cache index1 requests</td><td><xsl:value-of select="@cache_index1_req"/></td></tr>
      <tr class="hover"><td>Cache index1 hits</td><td><xsl:value-of select="@cache_index1_hit"/></td></tr>
      <tr class="hover"><td>Cache index2 items</td><td><xsl:value-of select="@cache_index2_items"/></td></tr>
      <tr class="hover"><td>Cache index2 size</td><td><xsl:value-of select="@cache_index2_size"/></td></tr>
      <tr class="hover"><td>Cache index2 maximum size</td><td><xsl:value-of select="@cache_index2_maxsz"/></td></tr>
      <tr class="hover"><td>Cache index2 requests</td><td><xsl:value-of select="@cache_index2_req"/></td></tr>
      <tr class="hover"><td>Cache index2 hits</td><td><xsl:value-of select="@cache_index2_hit"/></td></tr>
    </table>
  </pre>
</xsl:template>

</xsl:stylesheet>

