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

<xsl:template match="/zarafaadmin/emails">
  <pre>
    <table id="zarafa-emails">
      <caption>Information cached on <xsl:value-of select="@date"/></caption>
      <tr>
        <th colspan="5">
          <table align="center" id="zarafa-emails-totals" width="100%">
            <tr>
              <th align="right" width="25%">
                Total Emails:&#160;<br/>
                User Emails:&#160;<br/>
                Group Emails:&#160;<br/>
              </th>
              <th align="left" width="25%">
                <xsl:value-of select="count(email)"/><br/>
                <xsl:value-of select="count(email[@type = 'User'])"/><br/>
                <xsl:value-of select="count(email[@type = 'Group'])"/><br/>
              </th>
              <th align="right" width="25%">
                Zarafa Emails:&#160;<br/>
                Domino Emails:&#160;<br/>
                Zarafa-Only Emails:&#160;<br/>
                Domino-Only Emails:&#160;<br/>
              </th>
              <th align="left" width="25%">
                <xsl:value-of select="count(email[@zarafa = 'True'])"/><br/>
                <xsl:value-of select="count(email[@domino = 'True' and @forward = 'False'])"/><br/>
                <xsl:value-of select="count(email[@zarafa = 'True' and @domino = @forward])"/><br/>
                <xsl:value-of select="count(email[@domino = 'True' and @zarafa = 'False'])"/><br/>
              </th>
            </tr>
          </table>
        </th>
      </tr>          
      <tr>
        <th align="left"><a href="./zarafa-emails.php?sort=mail">Email Address</a></th>
        <th align="center"><a href="./zarafa-emails.php?sort=type">Account<br/>Type</a></th>
        <th align="center"><a href="./zarafa-emails.php?sort=zarafa">Zarafa<br/>Account</a></th>
        <th align="center"><a href="./zarafa-emails.php?sort=domino">Domino<br/>Account</a></th>
        <th align="center"><a href="./zarafa-emails.php?sort=forward">Forwarding</a></th>
      </tr>
      <xsl:choose>
      <xsl:when test="$sort = 'type'">
        <xsl:apply-templates select="email">
          <xsl:sort select="@type" order="ascending"/>
          <xsl:sort select="@mail" order="ascending"/>          
        </xsl:apply-templates>
      </xsl:when>
      <xsl:when test="$sort = 'zarafa'">
        <xsl:apply-templates select="email">
          <xsl:sort select="@zarafa" order="descending"/>
          <xsl:sort select="@domino" order="descending"/>
          <xsl:sort select="@forward" order="descending"/>
          <xsl:sort select="@mail" order="ascending"/>          
        </xsl:apply-templates>
      </xsl:when>
      <xsl:when test="$sort = 'domino'">
        <xsl:apply-templates select="email">
          <xsl:sort select="@domino" order="descending"/>
          <xsl:sort select="@forward" order="ascending"/>
          <xsl:sort select="@zarafa" order="descending"/>
          <xsl:sort select="@mail" order="ascending"/>
        </xsl:apply-templates>
      </xsl:when>
      <xsl:when test="$sort = 'forward'">
        <xsl:apply-templates select="email">
          <xsl:sort select="@forward" order="descending"/>
          <xsl:sort select="@domino" order="descending"/>
          <xsl:sort select="@zarafa" order="ascending"/>
          <xsl:sort select="@mail" order="ascending"/>
        </xsl:apply-templates>
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates select="email">
          <xsl:sort select="@mail" order="ascending"/>
        </xsl:apply-templates>
      </xsl:otherwise>
      </xsl:choose>
    </table>
  </pre>
</xsl:template>

<xsl:template match="email">
  <tr class="entry">
    <td align="left">
      <xsl:choose>
        <xsl:when test="@username = ''">
          <xsl:value-of select="@mail"/>
        </xsl:when>
        <xsl:otherwise>
          <a href="./zarafa-users.php?user={@username}"><xsl:value-of select="@mail"/></a>
        </xsl:otherwise>
      </xsl:choose>
    </td>
    <td align="center"><xsl:value-of select="@type"/></td>
    <td align="center">
      <xsl:attribute name="class">    
        <xsl:if test="@zarafa = 'True'">green</xsl:if>
        <xsl:if test="@zarafa = 'False'">red</xsl:if>
      </xsl:attribute>
      <xsl:value-of select="@zarafa"/>
    </td>
    <td align="center">
      <xsl:attribute name="class">    
        <xsl:if test="@domino = 'True'">green</xsl:if>
        <xsl:if test="@domino = 'False'">red</xsl:if>
      </xsl:attribute>
      <xsl:value-of select="@domino"/>
    </td>
    <td align="center">
      <xsl:attribute name="class">    
        <xsl:if test="@forward = 'True'">green</xsl:if>
        <xsl:if test="@forward = 'False'">red</xsl:if>
      </xsl:attribute>
      <xsl:value-of select="@forward"/>
    </td>
  </tr>
</xsl:template>

</xsl:stylesheet>