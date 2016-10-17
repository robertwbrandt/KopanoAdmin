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

<xsl:template match="/zarafaadmin/groups">
  <pre>
    <xsl:choose>
      <xsl:when test="count(group) = 1">
        <table id="zarafa-group">
          <tr><th colspan="4" class="center">Group Detail for <xsl:value-of select="group/@fullname"/></th></tr>
          <tr class="hover">
            <th colspan="2" align="right">Groupname:&#xA0;</th>
            <td colspan="2"><xsl:value-of select="group/@groupname"/></td>
          </tr>
          <tr class="hover">
            <th colspan="2" align="right">Fullname:&#xA0;</th>
            <td colspan="2"><xsl:value-of select="group/@fullname"/></td>
          </tr>
          <tr class="hover">
            <th colspan="2" align="right">Email:&#xA0;</th>
            <td colspan="2"><xsl:value-of select="group/@emailaddress"/></td>
          </tr>
          <tr class="hover">
            <th colspan="2" align="right">Visible:&#xA0;</th>
            <td colspan="2"><xsl:if test="group/@addressbook = 'Visible'">&#x2713;</xsl:if></td>
          </tr>
          <tr class="hover">
            <th colspan="4" align="center">Users (<xsl:value-of select="count(group/user)"/>)</th>
          </tr>

          <xsl:variable name="columns" select="4"/>
          <xsl:apply-templates select="group/user[(position() - 1) mod $columns = 0]" mode="first">
            <xsl:with-param name="columns" select="$columns"/>
            <xsl:sort select="translate(@username, 'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')" order="ascending" />            
          </xsl:apply-templates>

        </table>
      </xsl:when>

      <xsl:otherwise>
        <table id="zarafa-groups">
        <col width="50%"/>
        <col width="50%"/>          
        <tr class="hover">
          <th colspan="2" align="center">Group Name</th>
        </tr>

        <xsl:variable name="columns" select="2"/>
        <xsl:apply-templates select="group[(position() - 1) mod $columns = 0]" mode="first">
          <xsl:sort select="translate(@groupname, 'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')" order="ascending" />
          <xsl:with-param name="columns" select="$columns"/>
        </xsl:apply-templates>

        </table>
      </xsl:otherwise>
    </xsl:choose>
  </pre>
</xsl:template>



<xsl:template match="user" mode="first">
<xsl:param name="columns"/>  
  <tr>
     <xsl:apply-templates select=".|following-sibling::user[position() &lt; $columns]"/>
     <xsl:if test="count(following-sibling::user) &lt; ($columns - 1)">
        <xsl:call-template name="emptycell">
           <xsl:with-param name="columns" select="$columns"/>          
           <xsl:with-param name="cells" select="$columns - 1 - count(following-sibling::user)"/>
        </xsl:call-template>
     </xsl:if>
  </tr>
</xsl:template>

<xsl:template match="user">
  <td align="center" class="hover">
    <a href="./zarafa-users.php?user={@username}"><xsl:value-of select="@username"/></a>
  </td>
</xsl:template>

<xsl:template match="group" mode="first">
<xsl:param name="columns"/>  
  <tr>
     <xsl:apply-templates select=".|following-sibling::group[position() &lt; $columns]"/>
     <xsl:if test="count(following-sibling::group) &lt; ($columns - 1)">
        <xsl:call-template name="emptycell">
           <xsl:with-param name="columns" select="$columns"/>
           <xsl:with-param name="cells" select="$columns - 1 - count(following-sibling::group)"/>
        </xsl:call-template>
     </xsl:if>
  </tr>
</xsl:template>

<xsl:template match="group">
  <td align="center" class="hover">
    <a href="./zarafa-groups.php?group={@groupname}"><xsl:value-of select="@groupname"/></a>
  </td>
</xsl:template>

<xsl:template name="emptycell">
<xsl:param name="columns"/>  
  <xsl:param name="cells"/>
  <td>&#xA0;</td>
  <xsl:if test="$cells &gt; 1">
     <xsl:call-template name="emptycell">
        <xsl:with-param name="cells" select="$cells - 1"/>
     </xsl:call-template>
  </xsl:if>
</xsl:template>




</xsl:stylesheet>
