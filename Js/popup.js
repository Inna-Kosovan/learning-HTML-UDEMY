$(document).ready(function() {// popup page load event
	populateDevices();

	// grab the current URL and put into textbox
	setTimeout(function() {
		chrome.extension.sendMessage(
			{
				//instruct background.js to get the current tab URL
				getWindowUrl: true
			}, 
			function(response) {
				//alert(response);
			}
		);
	}, 100);
	
	// handle communications being sent from other scripts
	chrome.extension.onMessage.addListener(
		function(request, sender, sendResponse) {	
			if(request.test != undefined) {
				//get current tab url and put into textbox (sent from background.js)
				$('.url-txt').val(request.test);
				$('.url-txt').putCursorAtEnd();
			};
		}
	); 

	$('a').click(function() { // link clicked on popup.html		
		var popWidth = $(this).parent().attr('popWidth');
		var popHeight = $(this).parent().attr('popHeight');
		var selectedUserAgent = $(this).parent().attr('userAgent');
		var selectedDevice = $(this).parent().html().substring(1, $(this).parent().html().indexOf('('));
		var url = $('.url-txt').val();
		var isSwipe = true;
		
		if($(this).attr('class') == 'submit-a') {
			popWidth = $('#txtWidth').val();
			popHeight = $('#txtHeight').val();
			selectedUserAgent = $('#txtUserAgent').val();
			selectedDevice = 'Custom';
		}
		
		if(url == 'http://') {
			alert('Please enter a website URL');
		}
		else {
			if($(this).attr('class') == 'mobile-landscape-a') {
				// landscape mode
				var originalWidth = popWidth;
				
				popWidth = popHeight;
				popHeight = originalWidth;
			}
			
			if($('#chkSwipe').attr('checked') != 'checked') {
				isSwipe = false;
				
				// add 17 pixels to account for the scrollbar
				popWidth = parseInt(popWidth) + 17; 
			}
		
			// account for Chrome border, add 16px
			popWidth = parseInt(popWidth) + 16; 
			
			// account for Chrome border add 39px and an additional 30px in height to leave room for the mobile device label
			popHeight = parseInt(popHeight) + 69;
			
			// open new window with specified dimensions, go to the URL specified in the textbox
			//window.open(url, '','width=' + popWidth + ',height=' + popHeight);			
			
			// inform background script what the specified user agent is
			chrome.extension.sendMessage(
				{
					//selectedMobileDeviceInfo: selectedUserAgent + '|' + selectedMobileDevice
					selectedUserAgent: selectedUserAgent, 
					selectedDevice: selectedDevice,
					selectedUrl: url,
					selectedDeviceWidth: popWidth,
					selectedDeviceHeight: popHeight,
					swipe: isSwipe
				}, 
				function(response) {
					//alert(response.test);
				}
			);
		}
	});
	
	LoadRandomDonationCopy();
});

function populateDevices() {
	populateDevice(samsungphone(), 'samsungphone');
	populateDevice(huaweiphone(),'huaweiphone');
	populateDevice(xiaomiphone(),'xiaomiphone');
	populateDevice(iphone(),'iphone');
	populateDevice(androidtablets(),'androidtablets');
	populateDevice(misc(),'misc');
	populateDevice(ipad(),'ipad');
	
}

function populateDevice(devices, deviceClass) {
	var isLast;
	
	for(var i = 0; i < devices.length; i++) {
		if(i == devices.length -1) {
			isLast = true;
		}
		else {
			isLast = false;
		}
				
		$('.' + deviceClass).append(getDeviceTemplateHTML(devices[i].userAgent, devices[i].name, devices[i].width, devices[i].height, isLast));
	}
}

function samsungphone(){ return [ 
getDevice('Galaxy S9 Plus', 846, 412 , 'Mozilla/5.0 (Linux; Android 9; SM-G965F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36 Viber/13.2.0.8'),getDevice('Galaxy S9', 740, 360 , 'Mozilla/5.0 (Linux; Android 9; SM-G965F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36 Viber/13.2.0.8'),getDevice('Galaxy Note 8', 740, 360 , 'Mozilla/5.0 (Linux; Android 4.4.2; GT-N5120 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Safari/537.36'),getDevice('Galaxy S8 Plus', 846, 412 , 'Mozilla/5.0 (Linux; Android 7.0;SAMSUNG SM-G955F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.2 Chrome/51.0.2704.106 Mobile Safari/537.36'),getDevice('Galaxy S8', 740, 360 , 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G950F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.2 Chrome/51.0.2704.106 Mobile Safari/537.36'),getDevice('Galaxy S7', 640, 360 , 'Mozilla/5.0 (Linux; Android 6.0; SAMSUNG SM-G930F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36'),getDevice('Galaxy S7 Edge', 640, 360 , 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G935F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36'),getDevice('Galaxy J3', 640, 360 , 'Mozilla/5.0 (Linux; Android 5.1; SM-J3119 Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.85 Mobile Safari/537.36'),getDevice('Galaxy J7', 640, 360 , 'Mozilla/5.0 (Linux; Android 5.1; SM-J700F Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.133 Mobile Safari/537.36'),getDevice('Galaxy S6', 640, 360 , 'Mozilla/5.0 (Linux; Android 6.0; SAMSUNG SM-G9287C Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36'), ]; }

function huaweiphone(){ return [ 
getDevice('Huawei P20', 748, 360 , 'Mozilla/5.0 (Linux; Android 8.0; ANE-LX1 Build/HUAWEIANE-LX1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.109 Mobile Safari/537.36'),getDevice('Huawei P10', 640, 360 , 'Mozilla/5.0 (Linux; Android 7.0; WAS-TL10 Build/HUAWEIWAS-TL10; xx-xx) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36'),getDevice('Huawei P9', 640, 360 , 'Mozilla/5.0 (Linux; Android 6.0; EVA-L09 Build/HUAWEIEVA-L09; xx-xx) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.106 Mobile Safari/537.36'),getDevice('Huawei P8 Lite', 640, 360 , 'Mozilla/5.0 (Linux; Android 5.0; ALE-L21 Build/HuaweiALE-L21) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36'), ]; }

function xiaomiphone(){ return [ 
getDevice('Redmi Note 5', 786, 393 , 'Mozilla/5.0 (Linux; U; Android 7.1; xx-xx; Redmi Note 5 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36'),getDevice('Redmi Note 4', 640, 360 , 'Mozilla/5.0 (Linux; Android 6.0; Redmi Note 4 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.85 Mobile Safari/537.36'),getDevice('Redmi Note 3', 640, 360 , 'Mozilla/5.0 (Linux; Android 5.0; Redmi Note 3 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'),getDevice('Redmi 4', 640, 360 , 'Mozilla/5.0 (Linux; Android 6.0; Redmi 4 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'), ]; }

function iphone(){ return [ 
getDevice('iPhone XR', 896, 414 , 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1'),getDevice('iPhone XS Max', 896, 414 , 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1'),getDevice('iPhone XS', 812, 375 , 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1'),getDevice('iPhone X', 812, 375 , 'Mozilla/5.0 (iPhone; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.25 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'),getDevice('iPhone 8 Plus', 736, 414 , 'Mozilla/5.0 (iPhone; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.25 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'),getDevice('iPhone 8', 667, 375 , 'Mozilla/5.0 (iPhone; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.25 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'),getDevice('iPhone 7 Plus', 736, 414 , 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1'),getDevice('iPhone 7', 667, 375 , 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1'),getDevice('iPhone 6S Plus', 736, 414 , 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'),getDevice('iPhone 6S', 667, 375 , 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'),getDevice('iPhone 6', 667, 375 , 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'), ]; }

function androidtablets(){ return [ 
getDevice('Nexus 10', 1280, 800 , 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 10 Build/LMY49F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Safari/537.36'),getDevice('Nexus 7', 960, 600 , 'Mozilla/5.0 (Linux; Android 4.2.1; Nexus 7 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19'),getDevice('Surface Pro 3', 1440, 960 , 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko'), ]; }

function misc(){ return [ 
getDevice('BlackBerry Z10', 640, 384 , 'Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.0.9.2372 Mobile Safari/537.10+'),getDevice('Kindle Fire', 1024, 600 , 'Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; Kindle Fire Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'), ]; }

function ipad(){ return [ 
getDevice('iPad', 1024, 768 , 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'),getDevice('iPad Pro', 2732, 2048 , 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'),getDevice('iPad Mini', 1024, 768 , 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A406 Safari/8536.25'),getDevice('iPad Mini 2-4', 2048, 1536 , 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4'), ]; }



function getDevice(deviceName, deviceWidth, deviceHeight, deviceUserAgent) {
	return {
		name : deviceName,
		width : deviceHeight,
		height : deviceWidth,
		userAgent : deviceUserAgent
	};
}

function getDeviceTemplateHTML(deviceUserAgent, deviceName, deviceWidth, deviceHeight, isLast){
	var html = '<div class="mobile-div';
	
	if(isLast) {
		html = html + ' mobile-last-div';
	}
	
	html = html + '" popWidth="' + deviceWidth + '" popHeight="' + deviceHeight + '" useragent="' + deviceUserAgent + '">\n';
	html = html + '<div>\n' + deviceName + ' (' + deviceWidth + ' x ' + deviceHeight + ')\n</div>\n<a href="javascript:void(0);" class="mobile-landscape-a"></a>\n<a href="javascript:void(0);" class="mobile-portrait-a"></a></div>';
	
	return html;						
}

function LoadRandomDonationCopy() {
	var copy = ['Is this extension helpful? I gladly accept donations!', 'Like this extension? Care to by me a beverage?', 'Would you like to contribue to the Human Fund?', 'Drinks on you right?... Maybe?', 'I have no money for lunch today...', 'Can I get a quarter? uh.. I need to make a phone call.', 'Just pretend this says whatever it needs to say to get you to donate.', 'Day Care is expensive, you know what I\'m saying?', 'If PBS pledge drives weren\'t bad enough, now you have to deal with this?', 'How about we go halfsies on lunch?', 'Remember that time I made that sweet Chrome extension? That was cool wasn\'t it?', 'In lieu of flowers, please send lunch.'];
	
	$('.donate-div p').html(copy[Math.floor(Math.random() * copy.length)]);
}