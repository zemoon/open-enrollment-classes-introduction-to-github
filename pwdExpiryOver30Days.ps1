<#
.SYNOPSIS
    Projects Password Expiry for the Next 30 Days
.DESCRIPTION
    Logs to the SQL Server on NDH-SQL-02 and is displayed on https://reports.us.tripadvisor.local
    
.EXAMPLE


#>     
[cmdletbinding()]
Param()

Begin{ 

    $date = (Get-Date).ToString('yyyy-MM-dd_H-mm')
    Start-Transcript -Path "E:\Scripts\Logs\SendPasswordExpiryDatestoDB\$date-expPassword.log"

    $users = $null
    $PwdMaxAge = 90
    $daysAhead = 30
    $kSQLSERVER = 'sql02.company.local'
    $OUs=@('ou=Users,dc=us,dc=company,dc=local','ou=Subsidiary,dc=us,dc=company,dc=local')
    $passwordExpiryDate = @()
    $kADTable = 'REPORTS.dbo.expPasswords'

    #Import-Module Graphite-PowerShell
    Write-Verbose "Checking password expiry for the next $daysAhead days"
    Write-Verbose "Assuming a 90 password expiry threshold"

}

Process{
    #region Retrieve AD Data
    foreach ($ou in $OUs){
        $users += Get-ADUser -Filter * -SearchBase $ou -Properties PasswordNeverExpires, PasswordLastSet, samaccountname, passwordExpired |
                    where {$_.Enabled -eq "True"} | 
                    where {$_.PasswordNeverExpires -eq $false } | 
                    where {$_.PasswordLastSet -ne $null} |
                    where {$_.PasswordExpired -eq $false}

                    Write-Verbose "Users found in $ou $($users.Count)"
 
        foreach ($user in $users){
            # Unix date used for Grafana. Grafana doesn't support future dates at present
            # $passwordExpiryDate += [Math]::Floor([decimal](Get-Date([datetime](Get-Date ($user.PasswordLastSet).AddDays(90) -Format d)).ToUniversalTime()-uformat "%s"))
        
            # Human readable date used for validation
            $passwordExpiryDate += (Get-Date ($user.PasswordLastSet).AddDays($PwdMaxAge) -Format d)
	    }
    }    
        # No Element as I don't what each individuals expiry date just a count of how many each day
        # Convert to a CustomObject because Group-Object has a property called count and I change this to Usercount
        # When checking $result.count a sum total of all records found is returned not the values in the NoteProperty
        $result = $passwordExpiryDate | Group-Object -Property $_.values -NoElement | foreach {[pscustomobject]@{Expires=[datetime]$_.Name;Usercount=$_.Count}} 
        $subResult = $result | Sort-Object -Property Expires | select -First $daysAhead


    Write-Verbose "Flushing $kADTable"
    Invoke-Sqlcmd -Query "delete from $kADTable" -ServerInstance $kSQLSERVER

    Write-Verbose "Inject new values"
    foreach($r in $subResult){
        Invoke-Sqlcmd -Query "INSERT INTO $kADTable VALUES ('$($r.usercount)', '$($r.expires)');" -ServerInstance $kSQLSERVER}
}

End{Stop-Transcript}

#foreach($r in $result){
#    Send-GraphiteMetric -CarbonServer 'grafana.company.com' -CarbonServerPort '2015' -UDP -MetricPath corpit.operations.mgmt.ad.user.pwdexpiring -MetricValue $($r.count) -UnixTime $($r.name)
#    #Write-Output "Send -MetricValue $($r.count) -UnixTime $($r.name)"
#    Start-Sleep -Seconds 3
#    }

