<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" indent="yes" omit-xml-declaration="yes" />
<xsl:param name="sort" select="'username'"/>
<xsl:param name="device"/>
<xsl:param name="user"/>

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

<xsl:template match="/zarafaadmin/devices">
  <pre>
    <xsl:choose>
      <xsl:when test="count(device) = 1">
        <table id="zarafa-device">
          <tr>
            <th colspan="3" align="center">Device Information</th>
            <th colspan="3" align="center">Wipe Information</th>
          </tr>
          <tr class="hover">
            <td>&#xA0;</td>
            <th align="right">User:&#xA0;</th>
            <td><a href="./zarafa-users.php?user={device/@synchronizedbyuser}"><xsl:value-of select="device/@synchronizedbyuser"/></a></td>
            <td>&#xA0;</td>
            <th align="right">Request On:&#xA0;</th>
            <td><xsl:value-of select="device/@wiperequeston"/></td>
          </tr>
          <tr class="hover">
            <td>&#xA0;</td>
            <th align="right">Device ID:&#xA0;</th>
            <td><a href="./zarafa-mdm.php?device={device/@deviceid}"><xsl:value-of select="device/@deviceid"/></a></td>
            <td>&#xA0;</td>
            <th align="right">Request By:&#xA0;</th>
            <td><xsl:value-of select="device/@wiperequestby"/></td>
          </tr>
          <tr class="hover">
            <td>&#xA0;</td>
            <th align="right">Device Type:&#xA0;</th>
            <td><xsl:value-of select="device/@devicetype"/></td>
            <td>&#xA0;</td>
            <th align="right">Wiped On:&#xA0;</th>
            <td><xsl:value-of select="device/@wipedon"/></td>
          </tr>
          <tr class="hover">
            <td>&#xA0;</td>
            <th align="right">User Agent:&#xA0;</th>
            <td><xsl:value-of select="device/@useragent"/></td>
            <td colspan="3">&#xA0;</td>
          </tr>
          <tr class="hover">
            <td>&#xA0;</td>
            <th align="right">Device Model:&#xA0;</th>
            <td><xsl:value-of select="device/@devicemodel"/></td>
            <th colspan="3" align="center">Folder Information</th>
          </tr>
          <tr class="hover">
            <td>&#xA0;</td>
            <th align="right">Device IMEI:&#xA0;</th>
            <td><xsl:value-of select="device/@deviceimei"/></td>
            <td>&#xA0;</td>
            <th align="right">First Sync:&#xA0;</th>
            <td><xsl:value-of select="device/firstsync/@date"/></td>
          </tr>
          <tr class="hover">
            <td>&#xA0;</td>
            <th align="right">Device Name:&#xA0;</th>
            <td><xsl:value-of select="device/@devicefriendlyname"/></td>
            <td>&#xA0;</td>
            <th align="right">Last Sync:&#xA0;</th>
            <td>
              <xsl:if test="device/lastsync/@lag &gt;= 30">
                <xsl:attribute name="class">red</xsl:attribute>
              </xsl:if>                     
              <xsl:value-of select="device/lastsync/@date"/>
            </td>            
          </tr>
          <tr class="hover">
            <td>&#xA0;</td>
            <th align="right">Device OS:&#xA0;</th>
            <td><xsl:value-of select="device/@deviceos"/></td>
            <td>&#xA0;</td>
            <th align="right">Total Folders:&#xA0;</th>
            <td><xsl:value-of select="device/@totalfolders"/></td>
          </tr>
          <tr class="hover">
            <td>&#xA0;</td>
            <th align="right">Device Language:&#xA0;</th>
            <td><xsl:value-of select="device/@deviceoslanguage"/></td>
            <td colspan="3">&#xA0;</td>
          </tr>
          <tr class="hover">
            <td>&#xA0;</td>
            <th align="right">Status:&#xA0;</th>
            <td><xsl:value-of select="device/@status"/></td>
            <td colspan="3">&#xA0;</td>
          </tr>
          <tr class="hover">
            <td>&#xA0;</td>
            <th align="right">Outbound SMS:&#xA0;</th>
            <td><xsl:value-of select="device/@deviceoutboundsms"/></td>
            <td colspan="3">&#xA0;</td>
          </tr>
          <tr class="hover">
            <td>&#xA0;</td>
            <th align="right">Device Operator:&#xA0;</th>
            <td><xsl:value-of select="device/@deviceoperator"/></td>
            <th colspan="3" align="center">Synced Folders (<xsl:value-of select="device/@synchronizedfolders"/>)</th>
          </tr>
          <tr class="hover">
            <td>&#xA0;</td>
            <th align="right">Version:&#xA0;</th>
            <td><xsl:value-of select="device/@activesyncversion"/></td>
            <td colspan="3" align="center"><xsl:value-of select="device/@synchronizeddata"/></td>
          </tr>
        </table>
        <table id="zarafa-device-errors">
          <tr class="hover">
            <td>&#xA0;</td>
            <th align="right">Errors:&#xA0;</th>
            <td><xsl:value-of select="device/@attentionneeded"/></td>
          </tr>          
          <xsl:for-each select="device/error">
            <tr><td colspan="3">&#xA0;</td></tr>
            <tr class="hover">
              <td>&#xA0;</td>
              <th align="right" nowrap="nowrap">Object:&#xA0;</th>
              <td><xsl:value-of select="@brokenobject"/></td>
            </tr>
            <tr class="hover">
              <td>&#xA0;</td>
              <th align="right" nowrap="nowrap">Information:&#xA0;</th>
              <td><xsl:value-of select="@information"/></td>
            </tr>
            <tr class="hover">
              <td>&#xA0;</td>
              <th align="right" nowrap="nowrap">Reason:&#xA0;</th>
              <td><xsl:value-of select="@reason"/></td>
            </tr>
            <tr class="hover">
              <td>&#xA0;</td>
              <th align="right" nowrap="nowrap">Item/Parent ID:&#xA0;</th>
              <td><xsl:value-of select="@itemparentid"/></td>
            </tr>
          </xsl:for-each>
        </table>
        <table id="zarafa-device-actions">
          <tr><th colspan="3" align="center"><br/>Actions</th></tr>
          <tr>
            <td align="right">
              <input type="button" value="Remove All State Data"/>
            </td>
            <td align="center">
              <input type="button" value="Remote Wipe All Data from Phone"/>
            </td>
            <td align="left">
              <input type="button" value="Clears All Loop Detection Data"/>
            </td>            
          </tr>
          <tr>
            <td align="right">
              <input type="button" value="Resynchronize"/>
            </td>
            <td align="left" colspan="2">
              <select>
                <option value="all" selected="">all folders for this device and user</option>
                <option value="email">folders of type 'email' for this device and user</option>
                <option value="calendar">folders of type 'calendar' for this device and user</option>
                <option value="contact">folders of type 'contact' for this device and user</option>
                <option value="task">folders of type 'task' for this device and user</option>
                <option value="note">folders of type 'note' for this device and user</option>
                <option value="hierarchy">Resynchronize the folder hierarchy for this device and user</option>
              </select>
            </td>
          </tr>
        </table>


      </xsl:when>

      <xsl:otherwise>
        <table id="zarafa-devices">
          <tr>
            <th align="left"><a href="./zarafa-mdm.php?user={$user}&amp;device={@device}&amp;sort=username">Username</a></th>
            <th align="left"><a href="./zarafa-mdm.php?user={$user}&amp;device={@device}&amp;sort=device">Device ID</a></th>
            <th align="left"><a href="./zarafa-mdm.php?user={$user}&amp;device={@device}&amp;sort=sync">Last Sync</a></th>
          </tr>
          <xsl:choose>
          <xsl:when test="$sort = 'device'">
            <xsl:apply-templates select="device">
              <xsl:sort select="translate(@deviceid, 'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')" order="ascending" />
              <xsl:sort select="translate(@username, 'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')" order="ascending" />              
            </xsl:apply-templates>
          </xsl:when>
          <xsl:when test="$sort = 'sync'">
            <xsl:apply-templates select="device">
              <xsl:sort select="lastsync/@lag" order="decending" data-type="number"/>
            </xsl:apply-templates>
          </xsl:when>
          <xsl:otherwise>
            <xsl:apply-templates select="device">
              <xsl:sort select="translate(@username, 'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')" order="ascending" />
              <xsl:sort select="lastsync/@lag" order="decending" data-type="number"/>              
            </xsl:apply-templates>
          </xsl:otherwise>
          </xsl:choose>
        </table>
      </xsl:otherwise>
    </xsl:choose>
  </pre>
</xsl:template>

<xsl:template match="device">
  <tr class="hover">
    <td><a href="./zarafa-users.php?user={@username}"><xsl:value-of select="@username"/></a></td>
    <td><a href="./zarafa-mdm.php?user={@username}&amp;device={@deviceid}"><xsl:value-of select="@deviceid"/></a></td>
    <td>       
      <a href="./zarafa-mdm.php?user={@username}&amp;device={@deviceid}">
        <xsl:if test="lastsync/@lag &gt;= 30">
          <xsl:attribute name="class">red</xsl:attribute>
        </xsl:if>          
        <xsl:value-of select="lastsync/@date"/>
      </a>
    </td>
  </tr>
</xsl:template>

</xsl:stylesheet>

