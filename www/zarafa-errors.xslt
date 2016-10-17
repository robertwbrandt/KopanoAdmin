<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" indent="yes" omit-xml-declaration="yes" />
<xsl:param name="log" select="'system'"/>
<xsl:param name="sort" select="'descending'"/>
<xsl:param name="filter"/>

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

<xsl:template match="/zarafaadmin/logs">
	<form method="get">
		<table valign="top" align="center">
			<tr>
				<td>
					<select name="log">
						<xsl:for-each select="log">
          		<xsl:sort select="@name" order="ascending"/>
							<option value="{@name}">
								<xsl:if test="$log = @name"><xsl:attribute name="selected"/></xsl:if>
								<xsl:value-of select="@display"/>
							</option>
						</xsl:for-each>
					</select>
				</td>
				<td> 
					<select name="sort">
					  <option value="ascending">
							<xsl:if test="$sort = 'ascending'"><xsl:attribute name="selected"/></xsl:if>
					  	Sort Ascending
					  </option>
					  <option value="descending">
							<xsl:if test="$sort = 'descending'"><xsl:attribute name="selected"/></xsl:if>
					  	Sort Descending
					  </option>					  
					</select>
				</td>			
				<td><input name="filter" type="text" value="{$filter}"/></td>
				<td><input name="submit" value="Filter Log" type="submit"/></td>
			</tr>	
		</table>
	</form>
</xsl:template>

<xsl:template match="/zarafaadmin/log">
  <pre>
	  <table id="zarafa-logs">
	  	<caption>
	  		<xsl:value-of select="@log"/> Log entries <xsl:if test="@filters != ''">using filter(s): <xsl:value-of select="@filters"/></xsl:if>
	  	</caption>
	    <xsl:apply-templates select="line"/>
	  </table>
	</pre>
</xsl:template>

<xsl:template match="line">
  <tr><td class="logdata"><xsl:value-of select="."/></td></tr>
</xsl:template>

</xsl:stylesheet>
