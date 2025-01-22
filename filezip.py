import zipfile

def create_proxy_extension(proxy_host, proxy_port, proxy_user, proxy_pass):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = f"""
    var config = {{
            mode: "fixed_servers",
            rules: {{
              singleProxy: {{
                scheme: "http",
                host: "{proxy_host}",
                port: parseInt({proxy_port})
              }},
              bypassList: ["localhost"]
            }}
    }};

    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    chrome.webRequest.onAuthRequired.addListener(
        function(details) {{
            return {{authCredentials: {{username: "{proxy_user}", password: "{proxy_pass}"}}}};
        }},
        {{urls: ["<all_urls>"]}},
        ["blocking"]
    );
    """

    with zipfile.ZipFile("proxy_auth_plugin.zip", "w") as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

proxy_host = "in.proxymesh.com"
proxy_port = "31280"
proxy_user = "PGH"
proxy_pass = "prajwal2003@"

create_proxy_extension(proxy_host, proxy_port, proxy_user, proxy_pass)
