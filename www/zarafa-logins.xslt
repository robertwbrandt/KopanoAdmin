<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" indent="yes" omit-xml-declaration="yes" />
<xsl:param name="sort" select="'username'"/>

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

<xsl:template match="/zarafaadmin/log">
  <pre>
    <table id="zarafa-login-errors">
      <tr>
        <th><a href="./zarafa-logins.php?sort=username">Username</a></th>
        <th><a href="./zarafa-logins.php?sort=m1">1 Min</a></th>
        <th><a href="./zarafa-logins.php?sort=m5">5 Min</a></th>
        <th><a href="./zarafa-logins.php?sort=m15">15 Min</a></th>
        <th><a href="./zarafa-logins.php?sort=h1">1 Hour</a></th>
        <th><a href="./zarafa-logins.php?sort=h4">4 Hour</a></th>
        <th><a href="./zarafa-logins.php?sort=h8">8 Hour</a></th>
        <th><a href="./zarafa-logins.php?sort=d1">1 Day</a></th>
        <th><a href="./zarafa-logins.php?sort=d3">3 Day</a></th></tr>
 
        <xsl:choose>
        <xsl:when test="$sort = 'm1'">
            <xsl:apply-templates select="user"><xsl:sort select="@m1" order="descending" data-type="number"/></xsl:apply-templates>
        </xsl:when>
        <xsl:when test="$sort = 'm5'">
            <xsl:apply-templates select="user"><xsl:sort select="@m5" order="descending" data-type="number"/></xsl:apply-templates>
        </xsl:when>
        <xsl:when test="$sort = 'm15'">
            <xsl:apply-templates select="user"><xsl:sort select="@m15" order="descending" data-type="number"/></xsl:apply-templates>
        </xsl:when>
        <xsl:when test="$sort = 'h1'">
            <xsl:apply-templates select="user"><xsl:sort select="@h1" order="descending" data-type="number"/></xsl:apply-templates>
        </xsl:when>
        <xsl:when test="$sort = 'h4'">
            <xsl:apply-templates select="user"><xsl:sort select="@h4" order="descending" data-type="number"/></xsl:apply-templates>
        </xsl:when>
        <xsl:when test="$sort = 'h8'">
            <xsl:apply-templates select="user"><xsl:sort select="@h8" order="descending" data-type="number"/></xsl:apply-templates>
        </xsl:when>
        <xsl:when test="$sort = 'd1'">
            <xsl:apply-templates select="user"><xsl:sort select="@d1" order="descending" data-type="number"/></xsl:apply-templates>
        </xsl:when>
        <xsl:when test="$sort = 'd3'">
            <xsl:apply-templates select="user"><xsl:sort select="@d3" order="descending" data-type="number"/></xsl:apply-templates>
        </xsl:when>
        <xsl:otherwise>
            <xsl:apply-templates select="user"><xsl:sort select="translate(@user, 'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')" order="ascending" /></xsl:apply-templates>
        </xsl:otherwise>
        </xsl:choose>
    </table>
  </pre>
</xsl:template>

<xsl:template match="user">
  <tr class="hover" id="{@user}-basic">
    <td>
      <img id="{@user}-img" src="/images/toggle-expand.png" onclick="toggle('{@user}');"/>&#xA0;
      <a href="./zarafa-users.php?user={@user}"><xsl:value-of select="@user"/></a>
    </td>
    <td class="number"><xsl:value-of select="@m1"/></td>
    <td class="number"><xsl:value-of select="@m5"/></td>
    <td class="number"><xsl:value-of select="@m15"/></td>
    <td class="number"><xsl:value-of select="@h1"/></td>
    <td class="number"><xsl:value-of select="@h4"/></td>
    <td class="number"><xsl:value-of select="@h8"/></td>
    <td class="number"><xsl:value-of select="@d1"/></td>
    <td class="number"><xsl:value-of select="@d3"/></td>
    </tr>
    <tr class="hide" id="{@user}-details">
    <td colspan="9">
      <table>
        <tr><td align="right">Windows Name:&#xA0;</td><td align="left"><xsl:value-of select="@cn"/></td></tr>
        <tr><td align="right">Bad Password Count:&#xA0;</td><td align="left"><xsl:value-of select="@badpwdcount"/></td></tr>
        <tr><td align="right">Bad Password Time:&#xA0;</td><td align="left"><xsl:value-of select="@badpasswordtime"/></td></tr>
        <tr><td align="right">Last Logoff:&#xA0;</td><td align="left"><xsl:value-of select="@lastlogoff"/></td></tr>
        <tr><td align="right">Last Login:&#xA0;</td><td align="left"><xsl:value-of select="@lastlogon"/></td></tr>
        <tr><td align="right">Logon Hours:&#xA0;</td><td align="left"><xsl:value-of select="@logonhours"/></td></tr>
        <tr><td align="right">Password Last Set:&#xA0;</td><td align="left"><xsl:value-of select="@pwdlastset"/></td></tr>
        <tr><td align="right">Account Expires:&#xA0;</td><td align="left"><xsl:value-of select="@accountexpires"/></td></tr>
        <tr><td align="right">Logon Count:&#xA0;</td><td align="left"><xsl:value-of select="@logoncount"/></td></tr>
        <tr><td align="right">Last Login Time:&#xA0;</td><td align="left"><xsl:value-of select="@lastlogontimestamp"/></td></tr>
      </table>
    </td>
  </tr>
</xsl:template>

</xsl:stylesheet>
