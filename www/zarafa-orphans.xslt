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

<xsl:template match="/zarafaadmin/orphans">
  <pre>
    <table id="zarafa-orphans">
    <tr>
      <th align="left"><a href="./zarafa-orphans.php?sort=guid">Store GUID</a></th>
      <th align="left"><a href="./zarafa-orphans.php?sort=user">Guessed Username</a></th>
      <th align="right"><a href="./zarafa-orphans.php?sort=size">Size (MB)</a></th>
      <th align="right"><a href="./zarafa-orphans.php?sort=type">Store Type</a></th>
      <th align="center"><a href="./zarafa-orphans.php?sort=logon">Last Logon</a></th>      
    </tr>
    <xsl:choose>
    <xsl:when test="$sort = 'guid'">
      <xsl:apply-templates select="orphan"><xsl:sort select="translate(@store, 'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')" order="ascending" /></xsl:apply-templates>
    </xsl:when>
    <xsl:when test="$sort = 'size'">
      <xsl:apply-templates select="orphan"><xsl:sort select="@size" order="descending" data-type="number"/></xsl:apply-templates>
    </xsl:when>
    <xsl:when test="$sort = 'type'">
      <xsl:apply-templates select="orphan"><xsl:sort select="@type" order="ascending"/></xsl:apply-templates>
    </xsl:when>
    <xsl:when test="$sort = 'logon'">
      <xsl:apply-templates select="orphan"><xsl:sort select="@lag" order="ascending" data-type="number"/></xsl:apply-templates>
    </xsl:when>
    <xsl:otherwise>
      <xsl:apply-templates select="orphan"><xsl:sort select="translate(@username, 'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')" order="ascending" /></xsl:apply-templates>
    </xsl:otherwise>
    </xsl:choose>
    </table>
  </pre>
</xsl:template>

<xsl:template match="orphan">
  <tr class="entry">
    <td><xsl:value-of select="@store"/></td>    
    <td><a href="./zarafa-users.php?user={@username}"><xsl:value-of select="@username"/></a></td>
    <td><xsl:value-of select="@size"/></td>
    <td><xsl:value-of select="@type"/></td>
    <td><xsl:value-of select="@logon"/></td>
  </tr>
</xsl:template>

</xsl:stylesheet>