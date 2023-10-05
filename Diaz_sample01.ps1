using namespace System.Windows.Forms


class sample01 { <# Code element obfuscation technique i: many meaningless identifiers are sprinkled throughout the code #>
    [string]$prompt = "Want "+"a balloons"+" notification?"; <# Data Obfuscation technique i: we split the string #>
	$aIUf0 = "Surprised aren't you?";
    [string]$title = "CSC846 "+"-"+" sample01" <# Data Obfuscation technique i: we split the string #>
	$aZa2 = "This is Halloween, this is Halloween!";
    [string]$options = "Yes"+"No" <# Data Obfuscation technique i: we split the string #>
	$aFz2 = "I sense there's something in the wind.";

    [void]Start(){
		$aBCk8 = 3.141592;
        $top = new-Object System.Windows.Forms.Form
		$aZNy9 = 2.718281828;
        $top.TopMost = $True
		$aZf3 = 6.02214076;
        $input = [MessageBox]::Show($top,$this.prompt, $this.title, $this.options)
		$bHi3 = 6.626;
        if($input -eq "Yes"){
			<# Bogus Control Flows technique i: exception handling entered into code #>
			try {
				$x = $aBCk8 / 0;
			} catch { "ER-ROAR!" }
			$pFk4 = 1.618033;
            $this.bloons();
			$kLw2 = 186282;
            $this.moreBloons();
			$tYn7= 6.67300;
        }
        else{
			$hId7 = 1.380650;
			<# Data Obfuscation technique iii: we encode the string in base64 and then decode it when ran #>
			$DecodedText = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("RmluZS4="))
            [MessageBox]::Show("$DecodedText");
			<# Bogus Control Flows technique i: exception handling entered into code #>
			try {
				$x = $aZNy9 / 0;
			} catch { "ER-ROAR!" }
        }
    }
    
    [void]moreBloons(){
        $this.prompt = "Want "+"more balloons"+"?"; <# Data Obfuscation technique i: we split the string #>
        $this.Start();
     }   
    [void]bloons(){ <# Bogus Control Flows technique ii: we change the ordering of the forms and drawing commands based on the time #>
		$iMe7 = (Get-Date).ToString("mm")
        if ([int]($iMe7)%2 -eq 0) {
			[reflection.assembly]::loadwithpartialname('System.Windows.Forms')
        	[reflection.assembly]::loadwithpartialname('System.Drawing')
		} else {
        	[reflection.assembly]::loadwithpartialname('System.Drawing')
			[reflection.assembly]::loadwithpartialname('System.Windows.Forms')
		}

		$notify = new-object system.windows.forms.notifyicon
        $notify.icon = [System.Drawing.SystemIcons]::Information
		$notify.balloontipicon = [System.Windows.Forms.ToolTipIcon]::Info
		<# Data Obfuscation technique iii: we encode the string in base64 and then decode it when ran #>
		$DecodedText = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("SGF2ZSBzb21lIGJhbGxvb25zIQ=="))
		$notify.balloontiptext = "$DecodedText"
		$notify.balloontiptitle = "Balloon"+""<# Data Obfuscation technique i: we split the string #>
        $notify.visible = $true
		$notify.showballoontip(1000)
		
    }
	[void]jWh5Tv(){ <# Code element obfuscation techique iv: beginning of junk code #>
        $this.prompt = "One fish."
        $this.prompt = "Two fish."
        $this.prompt = "Red fish."
        $this.prompt = "Blue fish."
		<# Bogus Control Flows technique i: exception handling entered into code #>
		try {
			$x = 4 / 0;
		} catch { "ER-ROAR!" }
    }
	[void]vYd7Uo(){
        $this.prompt = "You're a wizard Harry"
        $this.prompt = "I'm a what?!"
        $this.prompt = "Harry was NOT a wizard."
        $this.prompt = "Hagrid was just crazy."
    } <# Code element obfuscation techique iv: ending of junk code #>
}

$sample = [sample01]::new()
$sample.Start()